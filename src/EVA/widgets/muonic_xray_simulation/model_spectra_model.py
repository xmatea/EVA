import json
import numpy as np
from matplotlib import pyplot as plt

from EVA.core.data_structures.detector import DetectorIndices
from EVA.util.path_handler import get_path


class ModelSpectraModel(object):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

    def get_element_names(self):
        path = get_path("src/EVA/databases/muonic_xrays/mudirac_data_default_isotopes_readable.json")
        with open(path) as file:
            data = json.load(file)
            file.close()
        return data.keys()

    def gaussian(self, x, mean, sigma):
        return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (x - mean) ** 2 / sigma ** 2)

    def line(self, x, x0, x1):
        return x0 + x1 * x

    def quadratic(self, x, x0, x1, x2):
        return x0 + x1 * x + x2 * x ** 2

    def get_closest_x(self, x, y, target_x):
        diff = abs(x - target_x)
        index = diff.argmin()
        return y[index]

    def get_model(self, elements, proportions, detectors, e_range=None,
                  notation="spectroscopic", dx=0.1, show_components=False, e_res_model="linear",
                  show_primary=True, show_secondary=False):

        # Load energy vs FWHM curves for the detectors
        if e_res_model == "linear":
            energy_res = np.loadtxt(get_path("./src/EVA/databases/detectors/energy_resolution_linear.txt"),
                                    delimiter=",", skiprows=1)
        elif e_res_model == "quadratic":
            energy_res = np.loadtxt(get_path("./src/EVA/databases/detectors/energy_resolution_qudratic.txt"),
                                    delimiter=",", skiprows=1)
        else:
            raise ValueError("Invalid energy resolution model")

        # TODO: Make this the default database to use for mudirac
        with open(get_path("./src/EVA/databases/muonic_xrays/mudirac_data_default_isotopes_readable.json")) as file:
            all_energies = json.load(file)

        mu_capture_z, mu_capture_ratios = np.loadtxt(
            get_path("./src/EVA/databases/muonic_xrays/capture_probabilites_interpolated.txt"), delimiter=",", unpack=True)

        fig, axs = plt.subplots(len(detectors))
        fig.supxlabel("Energy / keV")
        fig.supylabel("Intensity / arb")

        for j, det in enumerate(detectors):
            ax = axs[j] if len(detectors) != 1 else axs

            all_transitions = []
            for i, element in enumerate(elements):

                element_data = all_energies[element]
                prim_trans = element_data["Primary"]
                sec_trans = element_data["Secondary"]
                Z = element_data["Z"]

                proportion = proportions[i]
                muonic_capture_ratio = mu_capture_ratios[mu_capture_z == Z]
                weights = proportion * muonic_capture_ratio

                detector_energy_res = energy_res[DetectorIndices[det].value]

                """
                print(
                    f"Detector: {detector_energy_res[0]} \nc = {detector_energy_res[1]} \nm = {detector_energy_res[2]}")
                """

                # Calculate Gaussians for each transition and add both secondary and primary transitions all_trans

                if show_primary:
                    for trans in prim_trans:
                        mean = np.array(prim_trans[trans]["E"])

                        # Calculate FWHM from energy resolution curves and convert to standard deviations
                        if e_res_model == "linear":
                            sigma = self.line(mean, detector_energy_res[1], detector_energy_res[2]) / (
                                        2 * np.sqrt(2 * np.log(2)))
                        elif e_res_model == "quadratic":
                            sigma = self.quadratic(mean, detector_energy_res[1], detector_energy_res[2],
                                              detector_energy_res[3]) / (2 * np.sqrt(2 * np.log(2)))
                        else:
                            raise ValueError("Invalid energy resolution model")

                        all_transitions.append(
                            {"name": trans, "E": mean, "sigma": sigma, "weights": weights, "type": "primary",
                             "element": element})

                if show_secondary:
                    for trans in sec_trans:
                        mean = np.array(sec_trans[trans]["E"])

                        # Calculate FWHM from energy resolution curves and convert to standard deviations
                        if e_res_model == "linear":
                            sigma = self.line(mean, detector_energy_res[1], detector_energy_res[2]) / (
                                        2 * np.sqrt(2 * np.log(2)))
                        elif e_res_model == "quadratic":
                            sigma = self.quadratic(mean, detector_energy_res[1], detector_energy_res[2],
                                              detector_energy_res[3]) / (2 * np.sqrt(2 * np.log(2)))
                        else:
                            raise ValueError("Invalid energy resolution model")

                        all_transitions.append(
                            {"name": trans, "E": mean, "sigma": sigma, "weights": weights, "type": "secondary",
                             "element": element})

            # sort list of all transitions by ascending energy
            all_transitions = sorted(all_transitions, key=lambda d: d["E"])

            if e_range is not None:
                xdata = np.arange(e_range[0], e_range[1], dx)
            else:
                max_e = np.max([trans["E"] for trans in all_transitions]) * 1.1
                xdata = np.arange(0, max_e, dx)

            total = np.zeros_like(xdata)

            for trans in all_transitions:
                trans["curve"] = self.gaussian(xdata, mean=trans["E"], sigma=trans["sigma"]) * trans["weights"]
                total += trans["curve"]

            ax.plot(xdata, total, label="Total spectrum")
            ax.set_title(det)
            ax.set_ylim((0, np.max(total) * 1.1))

            if show_components:
                ax = self.add_components(ax, xdata, all_transitions, total, notation)

        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.45, wspace=0.23)
        return fig, axs

    def add_components(self, ax, xdata, all_trans, total, notation="siegbahn"):
        # load notation dict
        with open(get_path("src/EVA/databases/names/transition_notations.json")) as file:
            notations = json.load(file)

        for i, trans in enumerate(all_trans):
            if np.sum(trans["curve"]) > 0.1:  # Check if the peak is within the viewing range of the plot
                color = ax._get_lines.get_next_color()

                ax.plot(xdata, trans["curve"], label=trans["name"], color=color)

                peak_height = trans["weights"] / (trans["sigma"] * np.sqrt(2 * np.pi))

                spec_name = trans["name"]
                element = trans["element"]

                font = {
                    "size": 7,
                    "family": "sans-serif",
                    "color": color
                }

                if notation == "siegbahn":
                    siegbahn_name = notations[spec_name][1]
                    if siegbahn_name:
                        # Raise the text label for every odd peak (to improve plot readability)
                        font["size"] = 8
                        max_height = np.max(total)
                        y_offset = (peak_height * 0.03) if i % 2 else (peak_height * 0.2)
                        ax.text(x=trans["E"], y=peak_height + y_offset, s=rf"{element} ${siegbahn_name}$",
                                fontdict=font, horizontalalignment="center")

                elif notation == "spectroscopic":
                    # Raise the text label for every odd peak (to improve plot readability)
                    max_height = np.max(total)
                    y_offset = (peak_height * 0.03) if i % 2 else (peak_height * 0.2)

                    ax.text(x=trans["E"], y=peak_height + y_offset, s=f"{element} {spec_name}", fontdict=font,
                            horizontalalignment="center")

                elif notation == "iupac":
                    # Raise the text label for every odd peak (to improve plot readability)
                    max_height = np.max(total)
                    y_offset = peak_height * 0.03 if i % 2 else peak_height * 0.2
                    iupac_name = notations[spec_name][0]
                    ax.text(x=trans["E"], y=peak_height + y_offset, s=f"{element} {iupac_name}", fontdict=font,
                            horizontalalignment="center")
        return ax