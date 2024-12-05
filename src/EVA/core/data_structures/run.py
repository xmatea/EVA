from copy import deepcopy

from EVA.core.data_structures.spectrum import Spectrum
from EVA.core.physics.normalisation import normalise_events, normalise_counts
from EVA.core.physics.energy_correction import lincorr

class Run:
    """
    The 'Run' class holds lists of 'Spectra' from all the detectors from a single run, as well as the run number,
    normalisation status and the comment from a single run.

    'detectors' is a list of names of the detectors in the Spectrum lists. ex: ["GE1", "GE3"].

    'raw' contains a list of Spectra, one Spectrum for each detector, with no energy calibration or normalisation
    applied - read from the .dat files as-is. The order of the Spectra in the list corresponds to the order specified
    in 'detectors'.

    'raw_e_corr' is a copy of raw but with the energy calibration applied as specified by config.ini. If no energy
    calibration is specified for any detectors in the config, it is just a copy of 'raw'.

    'data' contains a list of Spectra with the energy calibration and normalisation as specified in config.ini.
    This is the main data to be used for plotting and such.
    """
    def __init__(self, raw : list[Spectrum], loaded_detectors : list[str], run_num: str, start_time: str, end_time: str,
                 events_str: str, comment: str):

        # Main data containers
        self.raw = raw # raw, unprocessed data as read from file - is NOT to be changed
        self.data = deepcopy(raw) # deepcopy ensures that raw and data do not point to the same memory address and thus
        # any changes to data will not change raw

        # Basic run info
        self.loaded_detectors = loaded_detectors
        self.run_num = run_num

        # Normalisation and energy correction info (initial read from default.ini)
        self.normalisation = None
        self.normalise_which = []
        self.e_corr_params = None
        self.e_corr_which = []

        # Metadata from comment file (may not be available)
        self.start_time = start_time
        self.end_time = end_time
        self.events_str = events_str
        self.comment = comment


    def set_normalisation(self, normalisation, normalise_which=None):
        if normalise_which is None:
            normalise_which = self.normalise_which

        if normalisation == "counts":
            for i, spectrum in enumerate(self.raw):

                # Apply normalisation to specified spectra
                if spectrum.detector in normalise_which:
                    self.data[i].y = normalise_counts(spectrum.y)
                else:
                    self.data[i].y = self.raw[i].y

            # Update the normalisation status
            self.normalisation = normalisation
            self.normalise_which = normalise_which
            return 0

        if normalisation == "events":
            try:
                spills = int(self.events_str[19:])
                for i, spectrum in enumerate(self.raw):

                    # Apply normalisation to specified spectra
                    if spectrum.detector in normalise_which:
                        self.data[i].y = normalise_events(spectrum.y, spills)
                    else:
                        self.data[i].y = self.raw[i].y

                # Update the normalisation status
                self.normalisation = normalisation
                self.normalise_which = normalise_which
                return 0

            except ValueError:
                # If spills data is not available, revert normalisation to none
                for i, spectrum in enumerate(self.raw):
                    self.data[i].y = self.raw[i].y

                # set normalisation status to "none"
                self.normalisation = "none"
                self.normalise_which = self.loaded_detectors
                return 1

        elif normalisation == "none":
            for i, spectrum in enumerate(self.raw):
                self.data[i].y = self.raw[i].y

            self.normalisation = normalisation
            self.normalise_which = self.loaded_detectors
            return 0

        else:
            raise KeyError # normalisation type specified in config doesn't exist

    def set_energy_correction(self, e_corr_params, e_corr_which=None):
        if e_corr_which is None:
            e_corr_which = self.e_corr_which

        # Iterate through each Spectrum in the run and apply energy correction if the detector is in e_corr_which
        for i, spectrum in enumerate(self.raw):
            detector = spectrum.detector

            if detector in e_corr_which:
                gradient = e_corr_params[i][0]
                offset = e_corr_params[i][1]

                self.data[i].x = self.raw[i].x * gradient + offset # store energy correction in data

        self.e_corr_which = e_corr_which
        self.e_corr_params = e_corr_params

    def is_empty(self) -> bool:
        # Returns a boolean indicating whether any data was loaded or not
        return all([spectrum.x.size == 0 for spectrum in self.raw])

    def get_nonzero_data(self) -> list[Spectrum]:
        # Returns only the loaded spectra (without empty arrays for missing detectors)
        return [spectrum for spectrum in self.data if spectrum.x.size != 0]