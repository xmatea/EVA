from copy import deepcopy

from EVA.core.data_structures.spectrum import Spectrum
from EVA.core.physics.normalisation import normalise_events, normalise_counts

class Run:
    """
    The Run class specifies the experiment data and context for all detectors during a single measurement run.

   Args:
       raw: List of Spectrum objects, one Spectrum for each detector. The list may
       contain empty Spectrum objects if no data was found for a detector.
       loaded_detectors: Names of all detectors for which data was successfully loaded.
       run_num: Run number.
       start_time: Time run was started.
       end_time: Time run was ended.
       events_str: Number of events registered.
       comment: All metadata available for the run.
       """
    def __init__(self, raw : list[Spectrum], loaded_detectors : list[str], run_num: str, start_time: str, end_time: str,
                 events_str: str, comment: str):

        # Main data containers
        self._raw = raw # raw, unprocessed data as read from file - is NOT to be changed
        self.data = deepcopy(raw) # copy of raw which can be modified and accessed outside the class

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

    # dispatcher method to set normalisation from string
    def set_normalisation(self, normalisation: str, normalise_which: bool=None):
        """
        Sets normalisation to ``data``.

        Args:
            normalisation: name of desired normalisation method. Valid options: "none", "counts", "spills".
            normalise_which: Which detectors to set normalisation for. If normalisation type is set to "none", all
            detectors will be affected.

        Raises:
            TypeError: when invalid normalisation type is specified.
        """
        if normalise_which is None:
            normalise_which = self.normalise_which

        if normalisation == "counts":
            self.set_normalisation_counts(normalise_which)

        elif normalisation == "events":
            self.set_normalisation_events(normalise_which)

        elif normalisation == "none":
            self.set_normalisation_none()

        else:
            raise TypeError(f"Normalisation type '{normalisation}' is not valid.")

    def set_normalisation_none(self):
        """
        Resets all normalisation applied for each detector.
        """
        for i, spectrum in enumerate(self._raw):
            self.data[i].y = self._raw[i].y

        self.normalisation = "none"
        self.normalise_which = self.loaded_detectors

    def set_normalisation_counts(self, normalise_which: list[str]):
        """
        Sets normalisation by counts for each detector specified.

        Args:
            normalise_which: Names of which detectors to apply normalisation by counts for.
        """
        for i, spectrum in enumerate(self._raw):
            # Apply normalisation to specified spectra
            if spectrum.detector in normalise_which:
                self.data[i].y = normalise_counts(spectrum.y)
            else:
                self.data[i].y = self._raw[i].y

        # Update the normalisation status
        self.normalisation = "counts"
        self.normalise_which = normalise_which

    def set_normalisation_events(self, normalise_which: list[str]):
        """
        Sets normalisation by events for each detector specified.

        Args:
            normalise_which: Names of which detectors to apply normalisation by events for.
        """
        try:
            spills = int(self.events_str[19:])
            for i, spectrum in enumerate(self._raw):
                # Apply normalisation to specified spectra
                if spectrum.detector in self.normalise_which:
                    self.data[i].y = normalise_events(spectrum.y, spills)
                else:
                    self.data[i].y = self._raw[i].y

            # Update the normalisation status
            self.normalisation = "events"
            self.normalise_which = normalise_which

        except ValueError:
            # If spills data is not available, revert normalisation to none
            for i, spectrum in enumerate(self._raw):
                self.data[i].y = self._raw[i].y

            # set normalisation status to "none"
            self.normalisation = "none"
            self.normalise_which = self.loaded_detectors
            raise ValueError

    def set_energy_correction(self, e_corr_params: list[tuple[float]], e_corr_which=list[str]):
        """
        Sets current energy correction.

        Args:
            e_corr_params: List of tuples containing energy correction (gradient, offset) for each detector.
            e_corr_which: Names of which detectors to apply energy correction to.
        """

        if e_corr_which is None:
            e_corr_which = self.e_corr_which

        # Iterate through each Spectrum in the run and apply energy correction if the detector is in e_corr_which
        for i, spectrum in enumerate(self._raw):
            detector = spectrum.detector

            if detector in e_corr_which:
                gradient = e_corr_params[i][0]
                offset = e_corr_params[i][1]

                self.data[i].x = self._raw[i].x * gradient + offset # store energy correction in data

        self.e_corr_which = e_corr_which
        self.e_corr_params = e_corr_params

    def is_empty(self) -> bool:
        """
        Returns: Boolean indicating whether any data was loaded or not.
        """
        return all([spectrum.x.size == 0 for spectrum in self._raw])

    def get_nonzero_data(self) -> list[Spectrum]:
        """
        Returns: Copy of ``data`` without empty Spectrum objects for missing detectors.
        """
        return [spectrum for spectrum in self.data if spectrum.x.size != 0]

    def get_raw(self) -> list[Spectrum]:
        """
        Returns: Copy of ``raw``.
        """
        return deepcopy(self._raw)