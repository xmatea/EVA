import sys
import os
import logging
from pathlib import Path
from EVA.widgets.main.main_window import MainWindow
from EVA.core.app import App

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='EVA.log', encoding='utf-8', level=logging.DEBUG, filemode="w",
                        format='%(asctime)s %(levelname)s: %(message)s')
    logging.getLogger("matplotlib.font_manager").disabled = True

    ROOT = Path(__file__).resolve().parent.parent.parent
    os.chdir(ROOT)

    logging.info("Starting EVA...")

    logger.debug("Root directory: %s", ROOT)
    app = App(sys.argv)
    app.setStyleSheet("QLabel{font-size: 8pt;}"
                      "QLineEdit{font-size: 8pt;}"
                      "QPushButton{font-size: 8pt;}")

    logger.debug("Initialising main window.")
    app.main_window = MainWindow()
    logger.info("Launching main window.")
    app.main_window.show()
    sys.exit(app.exec())
