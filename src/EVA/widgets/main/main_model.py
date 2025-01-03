import logging
from PyQt6.QtCore import QObject

from EVA.core.app import get_config, get_app
from EVA.core.data_loading import loaddata
logger = logging.getLogger(__name__)

class MainModel(QObject):
    def __init__(self):
        super().__init__()
        self.run = None

    def load_run(self, run_num):
        config = get_config()

        run, flags = loaddata.load_run(run_num, config)
        all_detectors = config["general"]["all_detectors"].split(" ")

        if flags["no_files_found"]:  # no data was loaded - return now
            logging.error("No files were found in %s for run %s", config["general"]["working_directory"],
                          run_num)

        else:  # update run number field in gui and in config
            self.run = run
            config["general"]["run_num"] = str(run_num)

            logging.info("Found spectra for run number %s.", run_num)
            missing_detectors = [det for det in all_detectors if det not in self.run.loaded_detectors]

            if missing_detectors:
                logging.warning("No files were found for detectors %s.", ", ".join(missing_detectors))

            # Update run number in config
            config["general"]["run_num"] = str(run_num)

        if flags["comment_not_found"]:  # Comment file was not found
            logging.error("No comment file found for run %s", run_num)

        else:  # write comment info to GUI
            logging.info("Found metadata from comment file for run %s", run_num)

        if flags["norm_by_spills_error"]:
            self.set_run_normalisation("none")  # normalisation by spills failed
            logging.error(
                "Failed to apply normalisation by spills due to missing comment file. Normalisation set to None.")

        return flags

    def set_run_normalisation(self, normalisation):
        # Apply new normalisation to data (if data is already loaded)
        try:
            if self.run is not None:
                self.run.set_normalisation(normalisation)

            logger.info("Normalisation type set to '%s'.", normalisation)
            get_config()["general"]["normalisation"] = normalisation

        except (KeyError, ValueError, AttributeError) as e:
            logger.error("Normalisation type '%s' failed! Normalisation reverted to 'none'.", normalisation)
            get_config()["general"]["normalisation"] = "none"
            raise e

    def read_comment_data(self):
        mapping = dict.fromkeys(range(32))
        start = self.run.start_time.translate(mapping)[21:]
        end = self.run.end_time.translate(mapping)[21:]
        events = self.run.events_str.translate(mapping)[20:]
        comment = self.run.comment.translate(mapping)[11:]

        return comment, start, end, events

    @staticmethod
    def set_default_directory(new_dir):
        config = get_config()
        if new_dir:
            config["general"]["working_directory"] = new_dir
            logger.info("Working directory set to %s.", new_dir)

    @staticmethod
    def toggle_plot_detector(value, detector):
        config = get_config()
        if value:
            config[detector]["show_plot"] = "yes"
            logger.debug("Enabled %s for plotting.", detector)
        else:
            config[detector]["show_plot"] = "no"
            logger.debug("Disabled %s for plotting.", detector)