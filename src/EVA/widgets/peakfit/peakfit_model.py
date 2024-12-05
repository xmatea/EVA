import json
import time
import numpy as np
import uncertainties as uc
from PyQt6.QtCore import pyqtSignal, QObject
from EVA.core.fitting import FitData
from EVA.util.Trimdata import Trimdata

from EVA.core.app import get_app, get_config
from EVA.core.plot import plotting

from EVA.core.data_structures.detector import DetectorIndices

class PeakFitModel(QObject):
    def __init__(self, presenter, detector):
        super().__init__()
        self.presenter = presenter

        # Get loaded spectrum from app
        app = get_app()
        self.run = app.loaded_run
        self.spectrum = self.run.data[DetectorIndices[detector].value]
        self.detector = detector

        # Set up containers to store initial and fitted parameters
        self.initial_params = {
            "background": {
                "a": {
                    "value": 0,
                    "vary": True
                },
                "b": {
                    "value": 1,
                    "vary": True
                },
                "c": {
                    "value": 1,
                    "vary": True
                }
            }
        }

        self.fitted_params = {}
        self.fit_result = None
        self.x_range = None
        self.y_range = None

    def fit_peaks(self):
        self.fitted_params = {} # clear fit parameters in between fits
        x_data, y_data = Trimdata(self.spectrum.x, self.spectrum.y, self.x_range[0], self.x_range[1])

        self.fit_result = FitData.fit_gaussian_lmfit(x_data, y_data, self.initial_params)

        # store new fit parameters in model
        for param_name, param in self.fit_result.params.items():
            prefix, var_name = param_name.split("_")

            if var_name == "fwhm" or var_name == "height": # ignore these
                continue

            # if error is not available, set error to 0
            stderr = param.stderr if param.stderr is not None else 0

            # re-structure fit result to match the structure of initial parameters
            if prefix in self.fitted_params.keys():
                self.fitted_params[prefix][var_name] = {
                    "value": param.value,
                    "stderr": stderr,
                    "vary": self.initial_params[prefix][var_name]["vary"]
                }
            else:
                self.fitted_params[prefix] = {
                    var_name: {
                        "value": param.value,
                        "stderr": stderr,
                        "vary": self.initial_params[prefix][var_name]["vary"]
                    }
                }

            # save the rest of the constraints if present
            x_min = self.initial_params[prefix][var_name].get("min", None)
            x_max = self.initial_params[prefix][var_name].get("max", None)
            expr = self.initial_params[prefix][var_name].get("expr", None)

            if x_min is not None:
                self.fitted_params[prefix][var_name]["min"] = x_min

            if x_max is not None:
                self.fitted_params[prefix][var_name]["max"] = x_max

            if expr is not None:
                self.fitted_params[prefix][var_name]["expr"] = expr

        return x_data

    def add_initial_peak_params(self, line, x, name):
        # find height of curve at specified x to give as initial peak height guess
        ix = np.argmin(abs(line.get_xdata() - x))
        height = line.get_ydata()[ix]

        center = x
        sigma = 0.7 # estimated sigma based on measurements
        area = height * sigma * np.sqrt(np.pi*2) # calculating area from height and sigma

        self.initial_params[name] = {
            "center": {
                "value": center,
                "vary": True,
                "min": 0
            },
            "sigma": {
                "value": sigma,
                "vary": True,
                "min": 0
            },
            "amplitude": {
                "value": area,
                "vary": True,
                "min": 0
            }
        }

    def calculate_x_range(self):
        # extract peak centres and sigmas from all loaded parameters
        params = list(zip(*[[self.initial_params[name]["center"]["value"], self.initial_params[name]["sigma"]["value"]]
                 for name in self.initial_params.keys() if name != "background"]))

        center = np.array(params[0])
        sigma = np.array(params[1])

        start_peak = np.min(center)
        start_sigma = sigma[center == start_peak][0]

        stop_peak = np.max(center)
        stop_sigma = sigma[center == stop_peak][0]

        e_start = start_peak - 8*start_sigma
        if e_start < 0:
            e_start = 0

        e_stop = stop_peak + 8*stop_sigma

        self.x_range = (e_start, e_stop)

    # y range for plotting (to make plot look nice)
    def calculate_y_range(self, ydata):
        y_range = (-np.max(ydata) * 0.05, np.max(ydata) * 1.3)
        self.y_range = y_range

    def save_params(self, path):
        with open(path, "w") as file:
            json.dump(self.fitted_params, file, indent=4)

        file.close()

    def load_params(self, path):
        with open(path, "r") as file:
            self.initial_params = json.load(file)

        file.close()

    def save_fit_report(self, path):
        with open(path, "w") as file:
            file.write(self.fit_result.fit_report())

        file.close()



