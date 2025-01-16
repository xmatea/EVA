import json
import time
import logging

import numpy as np
from matplotlib import pyplot as plt

from EVA.core.data_structures.detector import DetectorIndices
from EVA.core.app import get_app
from EVA.core.data_structures.spectrum import Spectrum

logger = logging.getLogger(__name__)
from EVA.util.path_handler import get_path

def gaussian(x, mean, sigma, A):
    return (A / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / sigma)**2)

def line(x, x0, x1):
    return x0 + x1 * x

def quadratic(x, x0, x1, x2):
    return x0 + x1 * x + x2 * x * x

class ModelSpectraModel(object):
    def __init__(self):
        super().__init__()
        app = get_app()

        self.element_names = app.mudirac_muon_database["Atomic numbers"].keys()
        self.mu_capture_ratios = app.mudirac_muon_database["Capture ratios"]
        self.energies = app.mudirac_muon_database

        self.all_spectra = []
        self.all_transitions = []

        with open(get_path("src/EVA/databases/names/transition_notations.json"), encoding="utf-8") as file:
            self.notations = json.load(file)
            file.close()

        self.linear_e_res = np.loadtxt(get_path("./src/EVA/databases/detectors/energy_resolution_linear.txt"),
                                    delimiter=",", skiprows=1)
        self.quadratic_e_res = np.loadtxt(get_path("./src/EVA/databases/detectors/energy_resolution_quadratic.txt"),
                                    delimiter=",", skiprows=1)


    def calculate_sigma(self, e_res_model, mean, detector_name):
        # Calculate FWHM from energy resolution curves and convert to standard deviations
        if e_res_model == "linear":
            detector_energy_res = self.linear_e_res[DetectorIndices[detector_name].value]
            sigma = line(mean, detector_energy_res[1], detector_energy_res[2]) / (
                    2 * np.sqrt(2 * np.log(2)))

        elif e_res_model == "quadratic":
            detector_energy_res = self.quadratic_e_res[DetectorIndices[detector_name].value]
            sigma = quadratic(mean, detector_energy_res[1], detector_energy_res[2],
                              detector_energy_res[3]) / (2 * np.sqrt(2 * np.log(2)))
        else:
            raise ValueError("Invalid energy resolution model")

        return sigma


    def model_spectrum(self, elements, proportions, detectors, e_range=None, dx=1, e_res_model="linear",
                 notation=0, show_components=False, show_primary=True, show_secondary=False):
        logger.info("Modelling spectrum for %s.", elements)
        logger.debug("Settings: elements = %s, proportions = %s, dx = %s, show_primary = %s, "
                     "show_secondary = %s, show_components = %s, detectors = %s, "
                     "energy_resolution_model = %s, notation = %s.", elements, proportions, dx, show_primary,
                     show_secondary, show_components, detectors, e_res_model, notation)

        t0 = time.time_ns()

        self.all_spectra = []
        self.all_transitions = []

        fig, axs = plt.subplots(len(detectors))
        fig.supxlabel("Energy / keV")
        fig.supylabel("Intensity / arb")

        for j, det in enumerate(detectors):
            ax = axs[j] if len(detectors) != 1 else axs

            # select energy resolution model for current detector
            if e_res_model == "linear":
                sigma_params = self.linear_e_res[DetectorIndices[det].value][1:]
                sigma_model = line
            else:
                sigma_params = self.quadratic_e_res[DetectorIndices[det].value][1:]
                sigma_model = quadratic

            # Get transition energies for each element
            transitions = []
            for i, element in enumerate(elements):
                prim_trans = self.energies["Primary energies"][element]
                sec_trans = self.energies["Secondary energies"][element]

                proportion = proportions[i]
                muonic_capture_ratio = self.mu_capture_ratios[element]["Value"]
                weights = proportion * muonic_capture_ratio

                if show_primary:
                    for trans in prim_trans:
                        mean = np.array(prim_trans[trans]["E"])
                        intensity = np.array(prim_trans[trans]["I"])

                        sigma = sigma_model(mean, *sigma_params)

                        # Store all transition info in dictionary
                        transitions.append(
                            {"name": trans, "E": mean, "sigma": sigma, "weights": weights, "type": "primary",
                             "element": element, "intensity": intensity})

                if show_secondary:
                    for trans in sec_trans:
                        mean = np.array(sec_trans[trans]["E"])
                        intensity = np.array(sec_trans[trans]["I"])

                        sigma = sigma_model(mean, *sigma_params)

                        transitions.append(
                            {"name": trans, "E": mean, "sigma": sigma, "weights": weights, "type": "secondary",
                             "element": element, "intensity": intensity})

            # sort list of all transitions by ascending energy
            transitions = sorted(transitions, key=lambda d: d["E"])

            # calculate energy range
            if e_range is not None:
                xdata = np.arange(e_range[0], e_range[1], dx)
            else:
                max_e = np.max([trans["E"] for trans in transitions]) * 1.1
                xdata = np.arange(0, max_e, dx)

            total = np.zeros_like(xdata)

            # calculate gaussian for each curve and sum all curves to obtain total curve
            g_time_start = time.time_ns()
            for trans in transitions:

                trans["curve"] = (gaussian(xdata, mean=trans["E"], sigma=trans["sigma"], A=trans["intensity"])
                                  * trans["weights"])
                total += trans["curve"]

            g_time_end = time.time_ns()

            # store x and y data as Spectrum object
            spectrum = Spectrum(x=xdata, y=total, detector=det, run_number="")

            self.all_transitions.append(transitions)
            self.all_spectra.append(spectrum)

            # Plot results to axis
            ax.plot(spectrum.x, spectrum.y, label="Total spectrum")
            ax.set_title(spectrum.detector)
            ax.set_ylim((0, np.max(spectrum.y) * 1.25))

            if show_components:
                self.plot_components(ax, spectrum=spectrum, transitions=transitions, notation_index=notation)

            plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.45, wspace=0.23)

        t1 = time.time_ns()
        logger.info("Spectrum modelled in %ss.", round((t1-t0)/1e9, 4))
        return fig, axs

    def plot_components(self, ax, spectrum, transitions, notation_index=0):
        for i, trans in enumerate(transitions):
            if np.sum(trans["curve"]) > 0.1:  # Check if the peak is within the viewing range of the plot
                color = ax._get_lines.get_next_color()

                ax.plot(spectrum.x, trans["curve"], label=trans["name"], color=color)

                # Calculate peak height
                peak_height = (trans["intensity"] * trans["weights"]) / (trans["sigma"] * np.sqrt(2 * np.pi))

                spec_name = trans["name"]
                element = trans["element"]

                font = {
                    "size": 7,
                    "family": "sans-serif",
                    "color": color
                }

                if notation_index == 0: # siegbahn notation
                    name = self.notations[spec_name][1]
                    if not name:
                        continue # skip if peak does not have siegbahn name

                    font["size"] = 9

                elif notation_index == 1: # spectroscopic notation
                    name = spec_name

                elif notation_index == 2: # iupac notation
                    name = self.notations[spec_name][0]
                else:
                    raise ValueError("Invalid notation index!")

                y_offset = (peak_height * 0.03) if i % 2 else (peak_height * 0.2)
                ax.text(x=trans["E"], y=peak_height + y_offset, s=f"{element} {name}",
                        fontdict=font, horizontalalignment="center")

    def reset(self):
        self.all_spectra = []
        self.all_transitions = []