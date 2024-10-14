from PyQt6.QtWidgets import QApplication

from EVA import config


def get_app():
    return QApplication.instance()


def get_config():
    return get_app().config


class App(QApplication):
    """
    The app class contains all settings, parameters, etc. of the app. It has a single instance (created in main.py)
    which can be accessed anywhere using QApplication.instance(). The instance can easily be returned using the
    get_app() method defined above.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # store config in app
        self.config = config.Config()
        self.config.load()

        # store the loaded run in the app
        self.loaded_run = None

        # store databases in app
        self.gamma_database = None
        self.muon_database = None

    """
    # Convenience function to load run, set the currently loaded run and update config
    def set_loaded_run(self, run_num):
        flags, run = loaddata.load_run(run_num)
        self.config["general"]["run_num"] = run_num
        self.loaded_run = run
    """