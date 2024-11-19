from PyQt6.QtWidgets import QApplication

from EVA.classes import config
from EVA.classes.loaders import LoadDatabaseFile, loadgamma, loaddata


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

        # store config in app
        self.config = config.Config()
        self.config.load()

        # store the loaded run in the app
        self.loaded_run = None

        # load and store databases in app
        self.gamma_database = loadgamma.load_gamma_data()
        self.mudirac_muon_database = LoadDatabaseFile.load_mudirac_data()
        self.legacy_muon_database = LoadDatabaseFile.load_legacy_data()

        # Check config and set default "muon database" accordingly
        if self.config["database"]["mu_xray_db"] == "legacy":
            self.muon_database = self.legacy_muon_database
        elif self.config["database"]["mu_xray_db"] == "mudirac":
            self.muon_database = self.mudirac_muon_database
        else:
            raise KeyError # Invalid muon database in config

        # Store references to all windows in the app
        self.main_window = None
        self.plot_window = None
        self.multiplot_window = None
        self.peakfit_window = None
        self.trim_window = None
        self.efficiency_correction_window = None
        self.energy_correction_window = None
        self.manual_window = None

    # Handy setter functions to switch database and update config
    def use_mudirac_muon_db(self):
        self.muon_database = self.mudirac_muon_database
        self.config["database"]["mu_xray_db"] = "mudirac"

    def use_legacy_muon_db(self):
        self.muon_database = self.legacy_muon_database
        self.config["database"]["mu_xray_db"] = "legacy"

    # Load run and update config
    def set_loaded_run(self, run_num):
        run, flags = loaddata.load_run(run_num, self.config)

        if flags["no_files_found"]:
            self.loaded_run = None
        else:
            self.loaded_run = run
            self.config["general"]["run_num"] = str(run_num)

        return flags

