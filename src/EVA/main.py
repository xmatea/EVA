import sys
import os
from pathlib import Path
from EVA.widgets.main.main_window import MainWindow
from EVA.core.app import App

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parent.parent.parent
    os.chdir(ROOT)

    app = App(sys.argv)
    app.setStyleSheet("QLabel{font-size: 8pt;}"
                      "QLineEdit{font-size: 8pt;}"
                      "QPushButton{font-size: 8pt;}")
    
    app.main_window = MainWindow()
    app.main_window.show()
    sys.exit(app.exec())
