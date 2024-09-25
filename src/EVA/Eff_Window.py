from PyQt6.QtWidgets import (
    QCheckBox,
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QGridLayout,
)
from EVA import globals

class Correction_Eff(QWidget):

    def __init__(self, parent = None):
        super(Correction_Eff,self).__init__(parent)

        self.setMaximumSize(1200, 500)
        self.setWindowTitle("Efficiency Correction ")

        # setting up buttons
        self.save_GE1_Effsettings = QPushButton("Save Detector 1")
        self.save_GE1_Effsettings.clicked.connect(
            lambda: self.save_GE_Eff_settings('GE1', LE_GE1_P0.text(), LE_GE1_P1.text(),
                                              LE_GE1_P2.text(), LE_GE1_P3.text(), LE_GE1_P4.text()))
        self.save_GE2_Effsettings = QPushButton("Save Detector 2")
        self.save_GE2_Effsettings.clicked.connect(
            lambda: self.save_GE_Eff_settings('GE2', LE_GE2_P0.text(), LE_GE2_P1.text(),
                                              LE_GE2_P2.text(), LE_GE2_P3.text(), LE_GE2_P4.text()))
        self.save_GE3_Effsettings = QPushButton("Save Detector 3")
        self.save_GE3_Effsettings.clicked.connect(
            lambda: self.save_GE_Eff_settings('GE3', LE_GE3_P0.text(), LE_GE3_P1.text(),
                                              LE_GE3_P2.text(), LE_GE3_P3.text(), LE_GE3_P4.text()))
        self.save_GE4_Effsettings = QPushButton("Save Detector 4")
        self.save_GE4_Effsettings.clicked.connect(
            lambda: self.save_GE_Eff_settings('GE4', LE_GE4_P0.text(), LE_GE4_P1.text(),
                                              LE_GE4_P2.text(), LE_GE4_P3.text(), LE_GE4_P4.text()))
        self.save_All_Effsettings = QPushButton("Save Detector 4")
        self.save_All_Effsettings.clicked.connect(
            lambda: self.save_GE_Eff_settings('All'))

        # Setting up Checkboxes
        GE1_apply = QCheckBox()
        GE1_apply.setChecked(globals.Eff_Corr_GE1_apply)
        # GE1_apply.text('GE1')
        GE1_apply.stateChanged.connect(lambda: self.set_Eff_corr_apply('GE1', GE1_apply))
        GE2_apply = QCheckBox()
        GE2_apply.setChecked(globals.Eff_Corr_GE2_apply)
        GE2_apply.stateChanged.connect(lambda: self.set_Eff_corr_apply('GE2', GE2_apply))
        GE3_apply = QCheckBox()
        GE3_apply.setChecked(globals.Eff_Corr_GE3_apply)
        GE3_apply.stateChanged.connect(lambda: self.set_Eff_corr_apply('GE3', GE3_apply))
        GE4_apply = QCheckBox()
        GE4_apply.setChecked(globals.Eff_Corr_GE4_apply)
        GE4_apply.stateChanged.connect(lambda: self.set_Eff_corr_apply('GE4', GE4_apply))

        # Setting up Line edits
        LE_GE1_P0 = QLineEdit(str(globals.Eff_Corr_GE1_P0))
        LE_GE1_P1 = QLineEdit(str(globals.Eff_Corr_GE1_P1))
        LE_GE1_P2 = QLineEdit(str(globals.Eff_Corr_GE1_P2))
        LE_GE1_P3 = QLineEdit(str(globals.Eff_Corr_GE1_P3))
        LE_GE1_P4 = QLineEdit(str(globals.Eff_Corr_GE1_P4))

        LE_GE2_P0 = QLineEdit(str(globals.Eff_Corr_GE2_P0))
        LE_GE2_P1 = QLineEdit(str(globals.Eff_Corr_GE2_P1))
        LE_GE2_P2 = QLineEdit(str(globals.Eff_Corr_GE2_P2))
        LE_GE2_P3 = QLineEdit(str(globals.Eff_Corr_GE2_P3))
        LE_GE2_P4 = QLineEdit(str(globals.Eff_Corr_GE2_P4))

        LE_GE3_P0 = QLineEdit(str(globals.Eff_Corr_GE3_P0))
        LE_GE3_P1 = QLineEdit(str(globals.Eff_Corr_GE3_P1))
        LE_GE3_P2 = QLineEdit(str(globals.Eff_Corr_GE3_P2))
        LE_GE3_P3 = QLineEdit(str(globals.Eff_Corr_GE3_P3))
        LE_GE3_P4 = QLineEdit(str(globals.Eff_Corr_GE3_P4))

        LE_GE4_P0 = QLineEdit(str(globals.Eff_Corr_GE4_P0))
        LE_GE4_P1 = QLineEdit(str(globals.Eff_Corr_GE4_P1))
        LE_GE4_P2 = QLineEdit(str(globals.Eff_Corr_GE4_P2))
        LE_GE4_P3 = QLineEdit(str(globals.Eff_Corr_GE4_P3))
        LE_GE4_P4 = QLineEdit(str(globals.Eff_Corr_GE4_P4))

        self.layout = QGridLayout()
        self.layout.addWidget(QLabel('Detector 1'), 1, 0)
        self.layout.addWidget(QLabel('Detector 2'), 2, 0)
        self.layout.addWidget(QLabel('Detector 3'), 3, 0)
        self.layout.addWidget(QLabel('Detector 4'), 4, 0)
        self.layout.addWidget(QLabel("P0"), 0, 1)
        self.layout.addWidget(QLabel("P1"), 0, 2)
        self.layout.addWidget(QLabel("P2"), 0, 3)
        self.layout.addWidget(QLabel("P3"), 0, 4)
        self.layout.addWidget(QLabel("P4"), 0, 5)

        self.layout.addWidget(QLabel("Apply"), 0, 6)

        self.layout.addWidget(LE_GE1_P0, 1, 1)
        self.layout.addWidget(LE_GE1_P1, 1, 2)
        self.layout.addWidget(LE_GE1_P2, 1, 3)
        self.layout.addWidget(LE_GE1_P3, 1, 4)
        self.layout.addWidget(LE_GE1_P4, 1, 5)

        self.layout.addWidget(LE_GE2_P0, 2, 1)
        self.layout.addWidget(LE_GE2_P1, 2, 2)
        self.layout.addWidget(LE_GE2_P2, 2, 3)
        self.layout.addWidget(LE_GE2_P3, 2, 4)
        self.layout.addWidget(LE_GE2_P4, 2, 5)

        self.layout.addWidget(LE_GE3_P0, 3, 1)
        self.layout.addWidget(LE_GE3_P1, 3, 2)
        self.layout.addWidget(LE_GE3_P2, 3, 3)
        self.layout.addWidget(LE_GE3_P3, 3, 4)
        self.layout.addWidget(LE_GE3_P4, 3, 5)

        self.layout.addWidget(LE_GE4_P0, 4, 1)
        self.layout.addWidget(LE_GE4_P1, 4, 2)
        self.layout.addWidget(LE_GE4_P2, 4, 3)
        self.layout.addWidget(LE_GE4_P3, 4, 4)
        self.layout.addWidget(LE_GE4_P4, 4, 5)

        self.layout.addWidget(GE1_apply, 1, 6)
        self.layout.addWidget(GE2_apply, 2, 6)
        self.layout.addWidget(GE3_apply, 3, 6)
        self.layout.addWidget(GE4_apply, 4, 6)

        self.layout.addWidget(self.save_GE1_Effsettings, 1, 7)
        self.layout.addWidget(self.save_GE2_Effsettings, 2, 7)
        self.layout.addWidget(self.save_GE3_Effsettings, 3, 7)
        self.layout.addWidget(self.save_GE4_Effsettings, 4, 7)

        self.setLayout(self.layout)
        self.show()

    def save_GE_Eff_settings(self, det, P0, P1, P2, P3, P4):

        if det == 'GE1':
            globals.Eff_Corr_GE1_P0 = P0
            globals.Eff_Corr_GE1_P1 = P1
            globals.Eff_Corr_GE1_P2 = P2
            globals.Eff_Corr_GE1_P3 = P3
            globals.Eff_Corr_GE1_P4 = P4

        if det == 'GE2':
            globals.Eff_Corr_GE2_P0 = P0
            globals.Eff_Corr_GE2_P1 = P1
            globals.Eff_Corr_GE2_P2 = P2
            globals.Eff_Corr_GE2_P3 = P3
            globals.Eff_Corr_GE2_P4 = P4
        if det == 'GE3':
            globals.Eff_Corr_GE3_P0 = P0
            globals.Eff_Corr_GE3_P1 = P1
            globals.Eff_Corr_GE3_P2 = P2
            globals.Eff_Corr_GE3_P3 = P3
            globals.Eff_Corr_GE3_P4 = P4

        if det == 'GE4':
            globals.Eff_Corr_GE4_P0 = P0
            globals.Eff_Corr_GE4_P1 = P1
            globals.Eff_Corr_GE4_P2 = P2
            globals.Eff_Corr_GE4_P3 = P3
            globals.Eff_Corr_GE4_P4 = P4

    def closeEvent(self, event):
        # close window cleanly
        #print(event)
        globals.weff = None
        return None

    def set_Eff_corr_apply(self, det, checkbox):

        if det == 'GE1':
            globals.Eff_Corr_GE1_apply = checkbox.isChecked()
        if det == 'GE2':
            globals.Eff_Corr_GE2_apply = checkbox.isChecked()
        if det == 'GE3':
            globals.Eff_Corr_GE3_apply = checkbox.isChecked()
        if det == 'GE4':
            globals.Eff_Corr_GE4_apply = checkbox.isChecked()
