from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFormLayout, QComboBox, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QCheckBox,
    QCompleter
)

from EVA.plot_widget import PlotWidget
from EVA import model_spectra

class ModelSpectraWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.settings = QWidget()
        self.settings_layout = QVBoxLayout()
        self.settings.setLayout(self.settings_layout)

        self.element_list = model_spectra.get_element_names()
        print(self.element_list)

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
        self.element_select_form_layout.setContentsMargins(0,0,0,0)

        self.element_count = 0
        self.add_element_select_box()

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
        self.plot_settings_layout.setContentsMargins(0,0,0,0)

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

        print(len(self.element_list))

    def on_auto_e_range_click(self):
        check = self.e_range_auto.isChecked()
        self.e_min.setDisabled(check)
        self.e_max.setDisabled(check)

    def on_show_components(self):
        check = self.show_components_box.isChecked()
        self.select_notation.setVisible(check)

    def get_element_select_box(self):
        box = QComboBox()
        for element in self.element_list:
            box.addItem(element)
        completer = QCompleter(self.element_list)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        box.setCompleter(completer)
        box.setMinimumWidth(50)

        return box

    def add_element_select_box(self):
        if self.element_count >= 6:
            #QMessageBox.critical("no")
            return

        new_box = self.get_element_select_box()
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
        elements = [element.currentText() for element in self.element_selects]
        proportions = [float(proportion.text()) for proportion in self.proportion_selects]
        show_components = self.show_components_box.isChecked()
        show_detectors = [button.isChecked() for button in self.detectors]
        detectors = ["GE1", "GE2", "GE3", "GE4"]

        if show_components:
            selected_notation_index =  self.select_notation.currentIndex()
            notations = ["spectroscopic", "iupac", "siegbahn"]
            notation = notations[selected_notation_index]
        else:
            notation = "iupac"

        detectors = [detector for i, detector in enumerate(detectors) if show_detectors[i]]

        if self.e_range_auto.isChecked():
            e_range = None
        else:
            e_range = [float(self.e_min.text()), float(self.e_max.text())]

        fig, ax = model_spectra.get_model(elements, proportions, detectors, e_range, notation=notation, dx=0.1,
                                          show_components=show_components , e_res_model="linear",
                                          show_primary=self.show_primary.isChecked(),
                                          show_secondary=self.show_secondary.isChecked())

        self.plot.update_plot(fig, ax)