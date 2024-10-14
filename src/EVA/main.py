import sys
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow
from EVA import config, loadgamma, LoadDatabaseFile
from EVA.app import App

if __name__ == "__main__":
    app = App(sys.argv)
    app.setStyleSheet("QLabel{font-size: 8pt;}"
                      "QLineEdit{font-size: 8pt;}"
                      "QPushButton{font-size: 8pt;}")

    # load energy databases
    app.gamma_database = loadgamma.load_gamma_data()

    # set muon database as specified in config
    if app.config["database"]["mu_xray_db"] == "legacy":
        app.muon_database = LoadDatabaseFile.load_legacy_data()

    elif app.config["database"]["mu_xray_db"] == "mudirac":
        app.muon_database = LoadDatabaseFile.load_mudirac_data()
    else:
        raise ValueError()
    
    app.main_window = MainWindow()
    app.main_window.show()
    sys.exit(app.exec())
