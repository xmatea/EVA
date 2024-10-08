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

        # A reference to all windows will be stored within the app class
        self.main_window = None
        self.multiplot_window = None
        self.manual_window = None
        self.peakfit_window = None
        self.plot_window = None
        self.srim_window = None

        # store config in app
        self.config = config.Config()
        self.config.load()

        # store the loaded run in the app
        self.loaded_run = None



