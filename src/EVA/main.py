import sys
import logging
from pathlib import Path

from EVA.widgets.main.main_window import MainWindow
from EVA.core.app import App

logger = logging.getLogger(__name__)
logging.basicConfig(filename='EVA.log', encoding='utf-8', level=logging.DEBUG, filemode="w",
                    format='%(asctime)s %(levelname)s: %(message)s')

logging.getLogger("matplotlib.font_manager").disabled = True

handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parent.parent.parent
    #os.chdir(ROOT)

    logging.info("Starting EVA...")

    logger.debug("Root directory: %s", ROOT)
    app = App(sys.argv)
    app.setStyle("")

    logger.debug("Initialising main window.")
    app.main_window = MainWindow()
    logger.info("Launching main window.")
    app.main_window.show()
    sys.exit(app.exec())
