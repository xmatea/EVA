from PyQt6.QtWidgets import (
    QCheckBox,
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QGridLayout,
)

from EVA import globals

class Correction_E(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
        """

    def __init__(self, parent = None):
        super(Correction_E,self).__init__(parent)
        #label = QLabel("Energy Correction ", self)

        self.setMaximumSize(850, 500)
        self.setWindowTitle("Energy Correction ")

        # setting up buttons
        self.save_GE1_Esettings = QPushButton("Save Detector 1")
        self.save_GE1_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('GE1', LE_GE1_off.text(), LE_GE1_grad.text()))
        self.save_GE2_Esettings = QPushButton("Save Detector 2")
        self.save_GE2_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('GE2', LE_GE2_off.text(), LE_GE2_grad.text()))
        self.save_GE3_Esettings = QPushButton("Save Detector 3")
        self.save_GE3_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('GE3', LE_GE3_off.text(), LE_GE3_grad.text()))
        self.save_GE4_Esettings = QPushButton("Save Detector 4")
        self.save_GE4_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('GE4', LE_GE4_off.text(), LE_GE4_grad.text()))
        self.save_All_Esettings = QPushButton("Save Detector 4")
        self.save_All_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('All'))

        # Setting up Checkboxes
        GE1_apply = QCheckBox()
        GE1_apply.setChecked(globals.E_Corr_GE1_apply)
        #GE1_apply.text('GE1')
        GE1_apply.stateChanged.connect(lambda: self.set_E_corr_apply('GE1', GE1_apply))
        GE2_apply = QCheckBox()
        GE2_apply.setChecked(globals.E_Corr_GE2_apply)
        GE2_apply.stateChanged.connect(lambda: self.set_E_corr_apply('GE2', GE2_apply))
        GE3_apply = QCheckBox()
        GE3_apply.setChecked(globals.E_Corr_GE3_apply)
        GE3_apply.stateChanged.connect(lambda: self.set_E_corr_apply('GE3', GE3_apply))
        GE4_apply = QCheckBox()
        GE4_apply.setChecked(globals.E_Corr_GE4_apply)
        GE4_apply.stateChanged.connect(lambda: self.set_E_corr_apply('GE4', GE4_apply))

        # Setting up Line edits
        LE_GE1_off = QLineEdit(str(globals.E_Corr_GE1_offset))
        LE_GE1_grad = QLineEdit(str(globals.E_Corr_GE1_gradient))
        LE_GE2_off = QLineEdit(str(globals.E_Corr_GE2_offset))
        LE_GE2_grad = QLineEdit(str(globals.E_Corr_GE2_gradient))
        LE_GE3_off = QLineEdit(str(globals.E_Corr_GE3_offset))
        LE_GE3_grad = QLineEdit(str(globals.E_Corr_GE3_gradient))
        LE_GE4_off = QLineEdit(str(globals.E_Corr_GE4_offset))
        LE_GE4_grad = QLineEdit(str(globals.E_Corr_GE4_gradient))

        self.layout = QGridLayout()
        self.layout.addWidget(QLabel('Detector 1'), 1, 0)
        self.layout.addWidget(QLabel('Detector 2'), 2, 0)
        self.layout.addWidget(QLabel('Detector 3'), 3, 0)
        self.layout.addWidget(QLabel('Detector 4'), 4, 0)
        self.layout.addWidget(QLabel("Offset"), 0, 1)
        self.layout.addWidget(QLabel("Gradient"), 0, 2)
        self.layout.addWidget(LE_GE1_off, 1, 1)
        self.layout.addWidget(LE_GE1_grad, 1, 2)
        self.layout.addWidget(LE_GE2_off, 2, 1)
        self.layout.addWidget(LE_GE2_grad, 2, 2)
        self.layout.addWidget(LE_GE3_off, 3, 1)
        self.layout.addWidget(LE_GE3_grad, 3, 2)
        self.layout.addWidget(LE_GE4_off, 4, 1)
        self.layout.addWidget(LE_GE4_grad, 4, 2)
        self.layout.addWidget(GE1_apply, 1, 3)
        self.layout.addWidget(GE2_apply, 2, 3)
        self.layout.addWidget(GE3_apply, 3, 3)
        self.layout.addWidget(GE4_apply, 4, 3)

        self.layout.addWidget(self.save_GE1_Esettings, 1, 4)
        self.layout.addWidget(self.save_GE2_Esettings, 2, 4)
        self.layout.addWidget(self.save_GE3_Esettings, 3, 4)
        self.layout.addWidget(self.save_GE4_Esettings, 4, 4)

        self.setLayout(self.layout)
        self.show()

    def save_GE_E_settings(self, det, off, grad):

        if det == 'GE1':
            globals.E_Corr_GE1_offset = off
            globals.E_Corr_GE1_gradient = grad
        if det == 'GE2':
            globals.E_Corr_GE2_offset = off
            globals.E_Corr_GE2_gradient = grad
        if det == 'GE3':
            globals.E_Corr_GE3_offset = off
            globals.E_Corr_GE3_gradient = grad
        if det == 'GE4':
            globals.E_Corr_GE4_offset = off
            globals.E_Corr_GE4_gradient = grad

    def closeEvent(self, event):
        #close window cleanly
        globals.we = None
        return None

    def set_E_corr_apply(self, det,checkbox):

        if det == 'GE1':
            globals.E_Corr_GE1_apply = checkbox.isChecked()
        if det == 'GE2':
            globals.E_Corr_GE2_apply = checkbox.isChecked()
        if det == 'GE3':
            globals.E_Corr_GE3_apply = checkbox.isChecked()
        if det == 'GE4':
            globals.E_Corr_GE4_apply = checkbox.isChecked()
