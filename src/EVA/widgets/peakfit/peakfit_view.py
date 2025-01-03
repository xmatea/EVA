from PyQt6.QtCore import pyqtSignal, Qt
from matplotlib.backend_bases import MouseButton

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QTextEdit,
    QCheckBox,
    QFileDialog
)

from EVA.widgets.plot import plot_widget
from EVA.core.app import get_app, get_config

class PeakFitView(QWidget):
    fit_button_clicked_s = pyqtSignal()
    add_peak_button_clicked_s = pyqtSignal()
    remove_peak_button_clicked_s = pyqtSignal()
    peak_selected_s = pyqtSignal(dict)
    peak_table_cell_changed_s = pyqtSignal(tuple)
    bckg_table_cell_changed_s = pyqtSignal(tuple)
    constraints_button_clicked_s = pyqtSignal()
    save_params_s = pyqtSignal(str)
    load_params_s = pyqtSignal(str)
    save_fit_report_s = pyqtSignal(str)

    def __init__(self, detector, parent=None):
        super().__init__(parent)
        conf = get_config()
        self.run_num = conf["general"]["run_num"]
        self.detector = detector
        self.add_peak_mode = False
        self.init_gui()

    def init_gui(self):
        self.setMinimumSize(1000, 700)
        self.setWindowTitle("Peak Fitting Window: Run Number " + self.run_num + " Det: " + self.detector)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # FIT SETTINGS FORM
        self.fit_settings_w = QWidget()
        self.fit_settings_w.setContentsMargins(0,0,0,0)
        self.fit_settings_layout = QGridLayout()
        self.fit_settings_w.setLayout(self.fit_settings_layout)
        self.fit_settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.e_ranges_label = QLabel("Set energy range")
        self.e_range_auto_check = QCheckBox("Auto")
        self.e_range_auto_check.setChecked(True)
        #self.e_range_upper_label = QLabel("Start")
        #self.e_range_lower_label = QLabel("Stop")
        self.e_range_upper_edit = QLineEdit()
        self.e_range_lower_edit = QLineEdit()

        # automatically uncheck auto range if text is edited
        self.e_range_lower_edit.textEdited.connect(lambda: self.e_range_auto_check.setChecked(False))
        self.e_range_upper_edit.textEdited.connect(lambda: self.e_range_auto_check.setChecked(False))

        self.fit_settings_layout.addWidget(self.e_ranges_label, 2, 0)
        self.fit_settings_layout.addWidget(self.e_range_auto_check, 2, 1)
        self.fit_settings_layout.addWidget(self.e_range_lower_edit, 2, 2)
        self.fit_settings_layout.addWidget(self.e_range_upper_edit, 2, 3)

        # PEAK SELECTION
        self.peak_selection_w = QWidget()
        self.peak_selection_w.setContentsMargins(0,0,0,0)
        self.peak_selection_layout = QGridLayout()
        self.peak_selection_w.setLayout(self.peak_selection_layout)
        self.peak_selection_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.add_peak_button = QPushButton("Add peak")
        self.cancel_add_peak_button = QPushButton("Cancel add peak")
        self.remove_peak_button = QPushButton("Remove last peak")
        self.add_constraints_button = QPushButton("Set constraints or bounds")
        self.add_peak_label = QLabel("Right-click on a peak in the spectrum to select.")
        self.add_peak_label.hide()

        # hard coded table width
        table_width = 490
        self.peak_selection_table_label = QLabel("Peak parameters")
        self.peak_selection_table = QTableWidget()
        self.peak_selection_table.setShowGrid(True)
        self.peak_selection_table.setColumnCount(4)
        self.peak_selection_table.setContentsMargins(0,0,0,0)
        self.peak_selection_table.setColumnWidth(0, int(table_width*(1/8)))
        self.peak_selection_table.setColumnWidth(1, int(table_width*(3/8)))
        self.peak_selection_table.setColumnWidth(2, int(table_width*(2/8)))
        self.peak_selection_table.setColumnWidth(3, int(table_width*(2/8)))

        self.peak_selection_table.setHorizontalHeaderLabels(["ID", "Peak Position (keV)", "Width (keV)", "Area"])
        self.peak_selection_table.cellChanged.connect(self.on_peak_table_cell_changed)

        self.add_peak_button.clicked.connect(self.start_add_peak_mode)
        self.cancel_add_peak_button.clicked.connect(lambda: self.quit_add_peak_mode(peak_added=False))
        self.cancel_add_peak_button.hide()

        self.remove_peak_button.clicked.connect(self.remove_peak_from_table)
        self.add_constraints_button.clicked.connect(self.show_constraints_dialog)

        self.fit_peaks_button = QPushButton("Fit Peaks")
        self.fit_peaks_button.clicked.connect(self.on_fit_button_click)

        # BACKGROUND PARAMETERS TABLE
        self.background_function_table_label = QLabel("Polynomial background parameters")
        self.background_function_table = QTableWidget()
        self.background_function_table.setColumnCount(3)
        self.background_function_table.setRowCount(1)
        self.background_function_table.setHorizontalHeaderLabels(["a", "b", "c"])
        self.background_function_table.setItem(0, 0, QTableWidgetItem("0"))
        self.background_function_table.setItem(0, 1, QTableWidgetItem("1"))
        self.background_function_table.setItem(0, 2, QTableWidgetItem("1"))
        self.background_function_table.setColumnWidth(0, int(table_width/3))
        self.background_function_table.setColumnWidth(1, int(table_width/3))
        self.background_function_table.setColumnWidth(2, int(table_width/3))
        self.background_function_table.setFixedHeight(75)

        self.background_function_table.cellChanged.connect(self.on_bckg_table_cell_changed)

        self.peak_selection_layout.addWidget(self.peak_selection_table_label, 0, 0, 1, -1)
        self.peak_selection_layout.addWidget(self.add_peak_label, 1, 0, 1, -1)
        self.peak_selection_layout.addWidget(self.add_peak_button, 2, 0)
        self.peak_selection_layout.addWidget(self.cancel_add_peak_button, 2, 0)
        self.peak_selection_layout.addWidget(self.remove_peak_button, 2, 1)
        self.peak_selection_layout.addWidget(self.add_constraints_button, 2, 2)
        self.peak_selection_layout.addWidget(self.peak_selection_table, 3, 0, 1, -1)
        self.peak_selection_layout.addWidget(self.background_function_table_label, 4, 0, 1, -1)
        self.peak_selection_layout.addWidget(self.background_function_table, 5, 0, 1, -1)
        self.peak_selection_layout.addWidget(self.fit_peaks_button, 6, 0, 1, -1)

        # RESULTS WIDGET
        self.results_w = QWidget()
        self.results_w.setContentsMargins(0,0,0,0)
        self.results_layout = QVBoxLayout()
        self.results_w.setLayout(self.results_layout)

        self.results_label = QLabel("Fit report")
        self.results_text = QTextEdit()

        self.results_layout.addWidget(self.results_label)
        self.results_layout.addWidget(self.results_text)

        # Assemble widgets into side panel
        self.side_panel_w = QWidget()
        self.side_panel_w.setMinimumWidth(550)
        self.side_panel_layout = QVBoxLayout()
        self.side_panel_w.setLayout(self.side_panel_layout)

        self.side_panel_layout.addWidget(self.fit_settings_w)
        self.side_panel_layout.addWidget(self.peak_selection_w)
        self.side_panel_layout.addWidget(self.results_w)

        # SAVE BUTTONS
        self.save_fit_button = QPushButton("Save fitted parameters")
        self.load_fit_button = QPushButton("Load fitted parameters")
        self.save_fit_report_button = QPushButton("Save fit report")

        self.save_fit_button.clicked.connect(self.save_params)
        self.load_fit_button.clicked.connect(self.load_params)
        self.save_fit_report_button.clicked.connect(self.save_fit_report)

        # set up plot widget
        self.plot_title = "Analysis of RunNum: " + self.run_num + "Det: " + self.detector

        self.plot = plot_widget.PlotWidget()

        self.plot.canvas.mpl_connect('button_press_event', self.on_plot_click)

        self.layout.addWidget(self.side_panel_w, 0, 0, 1, 3)
        self.layout.addWidget(self.save_fit_report_button, 1, 0)
        self.layout.addWidget(self.save_fit_button, 1, 1)
        self.layout.addWidget(self.load_fit_button, 1, 2)
        self.layout.addWidget(self.plot, 0, 3, -1, 1)

    def update_plot(self, fig, ax):
        self.plot.update_plot(fig, ax)

    def on_peak_table_cell_changed(self, row, col):
        """
            Runs every time a cell is updated in the peak parameter table. This will inevitably also run when a
            new peak is added to the table (initial peaks will be added from add_initial_peak() in presenter,
            then immediately re-added via this signal), so keep that in mind when debugging.
        """
        self.peak_table_cell_changed_s.emit((row, col))

    def on_bckg_table_cell_changed(self, row, col):
        self.bckg_table_cell_changed_s.emit((row, col))

    def remove_peak_from_table(self):
        # Removes last set of peak parameters from the table, and sends a signal to remove the initial parameters
        # for that peak
        rows = self.peak_selection_table.rowCount()
        if rows > 0:
            self.peak_selection_table.setRowCount(rows-1)
            self.remove_peak_button_clicked_s.emit()

    def update_e_range_form(self, e_range):
        # Writes new energy range to energy range form
        self.e_range_lower_edit.setText(f"{e_range[0]:.2f}")
        self.e_range_upper_edit.setText(f"{e_range[1]:.2f}")

    def update_table_row(self, table, row, vars, order, param_id=None):
        # update entire table row
        if row >= table.rowCount():
            table.setRowCount(row+1)

        # if id is specified, set id in first column to id
        if param_id is not None:
            table.setItem(row, 0, QTableWidgetItem(param_id))

            for col, var_name in enumerate(order):
                self.update_table_cell(table, row, col+1, vars[var_name])
        else:
            for col, var_name in enumerate(order):
                self.update_table_cell(table, row, col, vars[var_name])

    def update_table_cell(self, table, row, col, var):
        # Determines the format to display values with
        if var.get("stderr", None) is not None:
            item = QTableWidgetItem(f"{var["value"]:.3f} +/- {var["stderr"]:.3f}")
        else:
            item = QTableWidgetItem(f"{var["value"]:.3f}")

        table.setItem(row, col, item)


    def show_constraints_dialog(self):
        self.constraints_button_clicked_s.emit()

    def on_fit_button_click(self):
        self.fit_button_clicked_s.emit()

    def show_error_dialogue(self, message):
        _ = QMessageBox.critical(self, "Error!", message)

    def plot_fit(self, x, fit, residuals, x_range, y_range, overwrite_old=True):
        # removes previous fit from figure is prompted
        if overwrite_old:
            for line in self.plot.canvas.axs[0].lines:
                if line.get_label() == "Best fit" or line.get_label() == "Residuals":
                    line.remove()

        self.plot.canvas.axs[0].plot(x, fit, label="Best fit")

        # Because for some reason this is not always the case... The residuals could be calculated manually
        # to avoid this, but it seems to only happen when the fit is really bad, so ignoring for now.
        if len(x) == len(residuals):
            self.plot.canvas.axs[0].plot(x, residuals, label="Residuals")

        self.plot.canvas.axs[0].set_xlim(x_range)
        self.plot.canvas.axs[0].set_ylim(y_range)
        self.plot.canvas.axs[0].legend()
        self.plot.canvas.draw()

    def load_params(self):
        config = get_config()
        file = QFileDialog.getOpenFileName(self, 'Save File', directory=config["general"]["working_directory"])
        if file[0]:
            self.load_params_s.emit(file[0])

    def save_params(self):
        config = get_config()
        file = QFileDialog.getSaveFileName(self, 'Save File', directory=config["general"]["working_directory"])

        if file[0]:
            self.save_params_s.emit(file[0])

    def save_fit_report(self):
        config = get_config()
        file = QFileDialog.getSaveFileName(self, 'Save File', directory=config["general"]["working_directory"])

        if file[0]:
            self.save_fit_report_s.emit(file[0])

    def start_add_peak_mode(self):
        # Shows "right click to add peak" label, replaces the add button with a cancel button and enables add peak mode
        self.add_peak_button.hide()
        self.cancel_add_peak_button.show()
        self.add_peak_label.show()
        self.add_peak_mode = True

    def quit_add_peak_mode(self, peak_added):
        # Resets to the initial view
        self.add_peak_button.show()
        self.cancel_add_peak_button.hide()
        self.add_peak_label.hide()
        self.add_peak_mode = False

    def on_plot_click(self, event):
        # Ensures that plot was clicked correctly while in add peak mode
        if self.add_peak_mode and event.button is MouseButton.RIGHT and event.inaxes:
            # Release any zoom rubber band or pan if user right-clicked while using navigation tools
            self.plot.release_navigation(event)

            reply = QMessageBox.question(self, 'Add peak', f"Do you wish to add a peak at {event.xdata:.1f} keV?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.peak_selected_s.emit({"x": event.xdata, "axes": event.inaxes})

