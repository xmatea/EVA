import sys
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow
from EVA import config

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 8pt;}"
                      "QLineEdit{font-size: 8pt;}"
                      "QPushButton{font-size: 8pt;}")
    config.init()
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
