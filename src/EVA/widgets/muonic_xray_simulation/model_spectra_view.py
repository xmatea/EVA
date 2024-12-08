from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFormLayout, QComboBox, QLineEdit, QHBoxLayout, QCheckBox,
    QCompleter, QMessageBox
)

from EVA.widgets.plot.plot_widget import PlotWidget

class ModelSpectraView(QWidget):
    on_simulation_start_s = pyqtSignal()
    on_gui_initialised_s = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Model Muonic X-ray Spectra")
        self.init_gui()

    def init_gui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.settings = QWidget()
        self.settings_layout = QVBoxLayout()
        self.settings.setLayout(self.settings_layout)

        self.element_list = []


        # Energy range form
        self.e_range_form_layout = QFormLayout()
        self.e_range_form = QWidget()
        self.e_range_form.setLayout(self.e_range_form_layout)

        self.e_min = QLineEdit("0")
        self.e_max = QLineEdit("2000")
        self.e_range_auto = QCheckBox("Auto")

        self.e_range_auto.clicked.connect(self.on_auto_e_range_click)

        self.e_range_form_layout.addRow(QLabel("Start"), self.e_min)
        self.e_range_form_layout.addRow(QLabel("Stop"), self.e_max)
        self.e_range_form_layout.addWidget(self.e_range_auto)

        # Element selection form
        self.element_select_form_layout = QGridLayout()
        self.element_select_form = QWidget()
        self.element_select_form.setLayout(self.element_select_form_layout)

        # Set up combo box for selecting elements to simulate for
        self.element_selects = []
        self.proportion_selects = []

        self.element_label = QLabel("Element")
        self.proportion_label = QLabel("Ratio")
        self.element_select_form_layout.addWidget(self.element_label, 0, 0)
        self.element_select_form_layout.addWidget(self.proportion_label, 0, 1)
        self.element_select_form_layout.setContentsMargins(0, 0, 0, 0)

        self.element_count = 0

        self.add_element_button = QPushButton("Add element")
        self.add_element_button.clicked.connect(self.add_element_select_box)

        self.remove_element_button = QPushButton("Remove last element")
        self.remove_element_button.clicked.connect(self.remove_element_select_box)

        self.start_button = QPushButton("Simulate Spectrum")
        self.start_button.clicked.connect(self.simulate)

        # Plot settings
        self.plot_settings_layout = QGridLayout()
        self.plot_settings = QWidget()
        self.plot_settings.setLayout(self.plot_settings_layout)
        self.plot_settings_layout.setContentsMargins(0, 0, 0, 0)

        self.show_components_box = QCheckBox("Show components")
        self.show_components_box.clicked.connect(self.on_show_components)
        self.show_primary = QCheckBox("Show primary transitions")
        self.show_primary.setChecked(True)
        self.show_secondary = QCheckBox("Show secondary transitions")

        self.select_notation = QComboBox()
        self.select_notation.addItems(["Spectroscopic", "IUPAC", "Siegbahn (only major lines)"])
        self.select_notation.hide()

        self.plot_settings_layout.addWidget(self.show_components_box, 0, 0, 1, -1)
        self.plot_settings_layout.addWidget(self.show_primary, 1, 0, 1, -1)
        self.plot_settings_layout.addWidget(self.show_secondary, 2, 0, 1, -1)

        self.plot_settings_layout.addWidget(self.select_notation, 3, 0, 1, -1)
        self.detectors = [QCheckBox("Ge1"), QCheckBox("Ge2"), QCheckBox("Ge3"), QCheckBox("Ge4")]
        self.plot_settings_layout.addWidget(QLabel("Select detectors"), 4, 0, 1, -1)
        self.detectors[0].setChecked(True)

        for i, detector in enumerate(self.detectors):
            self.plot_settings_layout.addWidget(detector, 5, i)

        self.settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.settings_layout.addWidget(QLabel("Select elements"))
        self.settings_layout.addWidget(self.element_select_form)
        self.settings_layout.addWidget(self.add_element_button)
        self.settings_layout.addWidget(self.remove_element_button)
        self.settings_layout.addSpacing(50)

        self.settings_layout.addWidget(QLabel("Select energy range"))
        self.settings_layout.addWidget(self.e_range_form)
        self.settings_layout.addSpacing(50)

        self.settings_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignBottom)

        self.settings_layout.addWidget(QLabel("Plot settings"))
        self.settings_layout.addWidget(self.plot_settings)

        self.plot = PlotWidget()
        self.settings.setMaximumWidth(300)

        self.layout.addWidget(self.settings)
        self.layout.addWidget(self.plot)

    def populate_gui(self, element_list):
        # TODO move more of the gui data into here
        self.element_list = element_list
        self.add_element_select_box()

    def on_auto_e_range_click(self):
        check = self.e_range_auto.isChecked()
        self.e_min.setDisabled(check)
        self.e_max.setDisabled(check)

    def on_show_components(self):
        check = self.show_components_box.isChecked()
        self.select_notation.setVisible(check)

    def create_element_select_box(self):
        box = QComboBox()
        for element in self.element_list:
            box.addItem(element)
        completer = QCompleter(self.element_list)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        box.setCompleter(completer)
        box.setMinimumWidth(50)

        return box

    def add_element_select_box(self):
        if self.element_count >= 20:
            #QMessageBox.critical("no")
            return

        new_box = self.create_element_select_box()
        ratio_line_edit = QLineEdit("1")
        ratio_line_edit.setMaximumWidth(50)

        self.element_selects.append(new_box)
        self.proportion_selects.append(ratio_line_edit)
        self.element_count = self.element_count + 1

        self.element_select_form_layout.addWidget(self.element_selects[-1], self.element_count+1, 0)
        self.element_select_form_layout.addWidget(self.proportion_selects[-1], self.element_count+1, 1)

    def remove_element_select_box(self):
        print(self.element_count)
        if self.element_count > 1:
            self.element_select_form_layout.removeWidget(self.element_selects[-1])
            self.element_select_form_layout.removeWidget(self.proportion_selects[-1])

            self.element_selects.pop()
            self.proportion_selects.pop()

            self.element_count = self.element_count - 1

    def simulate(self):
        if not self.show_primary.isChecked() and not self.show_secondary.isChecked():
            _ = QMessageBox.critical(self, "Error", "No transitions selected. Please select at least one transition type "
                                                    "to simulate.")
            return

        self.on_simulation_start_s.emit()