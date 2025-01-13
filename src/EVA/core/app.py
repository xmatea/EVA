import logging
import time
import os
import sys

from PyQt6.QtWidgets import QApplication
from EVA.core.settings.config import Config
from EVA.core.data_loading import LoadDatabaseFile, loadgamma, loaddata

logger = logging.getLogger(__name__)


def get_app():
    return QApplication.instance()


def get_config():
    return get_app().config


class App(QApplication):
    """
    The app class contains all settings, parameters, etc. of the app. It has a single instance (created in main.py)
    which can be accessed anywhere using QApplication.instance(). The instance can easily be returned using the
    shorthand function get_app() defined above.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = None

        # store config in app
        self.config = Config()
        self.config.load()

        # load and store databases in app
        t0 = time.time_ns()
        self.gamma_database = loadgamma.load_gamma_data()
        self.mudirac_muon_database = LoadDatabaseFile.load_mudirac_data()
        self.legacy_muon_database = LoadDatabaseFile.load_legacy_data()
        logger.debug("Loaded all databases in %ss.", (time.time_ns()-t0)/1e9)

        # Check config and set default "muon database" accordingly
        if self.config["database"]["mu_xray_db"] == "legacy":
            self.muon_database = self.legacy_muon_database
            logger.info("Using legacy muon database.")
        elif self.config["database"]["mu_xray_db"] == "mudirac":
            logger.info("Using mudirac muon database.")
            self.muon_database = self.mudirac_muon_database
        else:
            raise KeyError # Invalid muon database in config

    # Handy setter functions to switch database and update config
    def use_mudirac_muon_db(self):
        self.muon_database = self.mudirac_muon_database
        self.config["database"]["mu_xray_db"] = "mudirac"
        logger.info("Muon database has been set to mudirac.")

    def use_legacy_muon_db(self):
        self.muon_database = self.legacy_muon_database
        self.config["database"]["mu_xray_db"] = "legacy"
        logger.info("Muon database has been set to legacy.")