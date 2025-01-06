import logging
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QGridLayout,
    QSizePolicy
)

from EVA.core.app import get_app, get_config
logger = logging.getLogger(__name__)

class MainView(QWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        config = get_config()

        # Set up action bar items
        self.bar = self.parent.menuBar() # since parent is the QMainWindow instance
        self.file_menu = self.bar.addMenu('File')
        self.file_load_default = self.file_menu.addAction('Load Default Setting')
        self.file_browse_dir = self.file_menu.addAction('Browse to Data Directory')
        self.file_exit = self.file_menu.addAction('Exit')

        self.plot_menu = self.bar.addMenu('Plot')
        self.plot_settings = self.plot_menu.addAction('Plot Settings')
        self.plot_multiplot = self.plot_menu.addAction('Multi-Run Plot')
        self.plot_detectors_menu = self.plot_menu.addMenu('Select detectors')

        self.plot_which_det_GE1 = self.plot_detectors_menu.addAction('GE1')
        self.plot_which_det_GE1.setCheckable(True)
        self.plot_which_det_GE1.setChecked(config.parser.getboolean("GE1", "show_plot"))
        self.plot_which_det_GE1.setShortcut("Alt+1")

        self.plot_which_det_GE2 = self.plot_detectors_menu.addAction('GE2')
        self.plot_which_det_GE2.setCheckable(True)
        self.plot_which_det_GE2.setChecked(config.parser.getboolean("GE2", "show_plot"))
        self.plot_which_det_GE2.setShortcut("Alt+2")

        self.plot_which_det_GE3 = self.plot_detectors_menu.addAction('GE3')
        self.plot_which_det_GE3.setCheckable(True)
        self.plot_which_det_GE3.setChecked(True)
        self.plot_which_det_GE3.setChecked(config.parser.getboolean("GE3", "show_plot"))
        self.plot_which_det_GE3.setShortcut("Alt+3")

        self.plot_which_det_GE4 = self.plot_detectors_menu.addAction('GE4')
        self.plot_which_det_GE4.setCheckable(True)
        self.plot_which_det_GE4.setChecked(config.parser.getboolean("GE4", "show_plot"))
        self.plot_which_det_GE4.setShortcut("Alt+4")

        self.normalisation_menu = self.bar.addMenu('Normalisation')
        self.norm_none = self.normalisation_menu.addAction('Use Raw Data')
        self.norm_none.setCheckable(True)
        self.norm_none.setShortcut("Alt+D")

        self.norm_counts = self.normalisation_menu.addAction('Normalise by total Counts')
        self.norm_counts.setCheckable(True)
        self.norm_counts.setShortcut("Alt+C")

        self.norm_events = self.normalisation_menu.addAction('Normalise by Events')
        self.norm_events.setCheckable(True)
        self.norm_events.setShortcut("Alt+S")

        self.corrections_menu = self.bar.addMenu('Corrections')
        self.efficiency_corrections = self.corrections_menu.addAction('Efficiency Corrections')
        self.energy_corrections = self.corrections_menu.addAction('Energy Corrections')

        self.analysis_menu = self.bar.addMenu('Analysis')
        self.peakfit_menu = self.analysis_menu.addMenu('Peak Fitting')
        self.peakfit_menu.setDisabled(True)

        self.peakfit_GE1 = self.peakfit_menu.addAction('GE1')
        self.peakfit_GE2 = self.peakfit_menu.addAction('GE2')
        self.peakfit_GE3 = self.peakfit_menu.addAction('GE3')
        self.peakfit_GE4 = self.peakfit_menu.addAction('GE4')

        self.tools_menu = self.bar.addMenu('Tools')
        self.trim_simulation = self.tools_menu.addAction('SRIM/TRIM Simulation')
        self.trim_simulation_test = self.tools_menu.addAction('SRIM/TRIM Simulation test')

        self.model_muon_spectrum = self.tools_menu.addAction("Simulate Muonic X-ray Spectra")

        self.help_menu = self.bar.addMenu('Help')
        self.help_manual = self.help_menu.addAction("Manual")

        # Set up window components
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.run_number_label = QLabel(self)
        self.run_number_label.setText("Run Number")
        self.run_number_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.comment_label = QLabel(self)
        self.comment_label.setText("Comment")
        self.comment_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.events_label = QLabel(self)
        self.events_label.setText("Events")
        self.events_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.start_label = QLabel(self)
        self.start_label.setText("Start Time")
        self.start_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.end_label = QLabel(self)
        self.end_label.setText("End Time")
        self.end_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        # setting up the buttons and run number
        self.run_number_line_edit = QLineEdit(self)
        self.run_number_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.run_number_line_edit.setMinimumWidth(200)
        self.run_number_line_edit.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.run_number_line_edit.setText(config["general"]["run_num"])

        self.get_next_run_button = QPushButton(self)
        self.get_next_run_button.setText('+1')
        self.get_next_run_button.setMinimumWidth(200)
        self.get_next_run_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.load_next_run_button = QPushButton(self)
        self.load_next_run_button.setText('Load +1')
        self.load_next_run_button.setMinimumWidth(200)
        self.load_next_run_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.get_prev_run_button = QPushButton(self)
        self.get_prev_run_button.setText('-1')
        self.get_prev_run_button.setMinimumWidth(200)
        self.get_prev_run_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.load_prev_run_button = QPushButton(self)
        self.load_prev_run_button.setText('Load -1')
        self.load_prev_run_button.setMinimumWidth(200)
        self.load_prev_run_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.load_button = QPushButton(self)
        self.load_button.setText('Load')
        self.load_button.setMinimumWidth(200)
        self.load_button.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.layout.addWidget(self.run_number_label, 0, 0, 1, 3)
        self.layout.addWidget(self.comment_label, 1, 0, 1, 3)
        self.layout.addWidget(self.events_label, 2, 0, 1, 3)
        self.layout.addWidget(self.start_label, 3, 0, 1, 3)
        self.layout.addWidget(self.end_label, 4, 0, 1, 3)

        self.layout.addWidget(self.run_number_line_edit, 5, 1)
        self.layout.addWidget(self.get_next_run_button, 5, 2)
        self.layout.addWidget(self.load_next_run_button, 6, 2)
        self.layout.addWidget(self.get_prev_run_button, 5, 0)
        self.layout.addWidget(self.load_prev_run_button, 6, 0)
        self.layout.addWidget(self.load_button, 6, 1)

        # Store references to all windows in the view
        self.main_window = None
        self.plot_window = None
        self.multiplot_window = None
        self.peakfit_window = None
        self.trim_window = None
        self.efficiency_correction_window = None
        self.energy_correction_window = None
        self.manual_window = None
        self.muon_spectrum_window = None


    def set_run_num_line_edit(self, num):
        self.run_number_line_edit.setText(num)

    def get_run_num_line_edit(self):
        run_num = self.run_number_line_edit.text()
        print(run_num)
        return self.run_number_line_edit.text()

    def set_run_num_label(self, run_num):
        self.run_number_label.setText(f"Run Number\t{run_num}")

    def set_comment_labels(self, comment, start, end, events):
        self.comment_label.setText(f"Comment\t{comment} ")
        self.events_label.setText(f"Events\t\t{events} ")
        self.start_label.setText(f"Start Time\t{start} ")
        self.end_label.setText(f"End Time\t{end} ")

    def update_normalisation_menu(self, norm):
        self.norm_counts.setChecked(norm == "counts")
        self.norm_none.setChecked(norm == "none")
        self.norm_events.setChecked(norm == "events")

    def get_dir(self):
        return QFileDialog.getExistingDirectory(self, "Choose Directory", "C:\\")

    def show_info_box(self, msg):
        _ = QMessageBox.information(parent=self, title="Information", text=msg, buttons=QMessageBox.StandardButton.Ok)

    def show_error_box(self, msg, title="Error"):
        # this will block the program until user presses "ok"
        _ = QMessageBox.critical(self, title, msg,
                                 buttons=QMessageBox.StandardButton.Ok,
                                 defaultButton=QMessageBox.StandardButton.Ok)

    def show_message_box(self, msg, title="Message"):
        # this will block the program until user presses "ok"
        _ = QMessageBox.information(self, title, msg,
                                 buttons=QMessageBox.StandardButton.Ok,
                                 defaultButton=QMessageBox.StandardButton.Ok)

