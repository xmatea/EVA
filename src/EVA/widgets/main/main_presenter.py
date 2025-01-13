import logging

from PyQt6.QtCore import QObject

from EVA.core.app import get_config, get_app
from EVA.widgets.multiplot.multi_plot_window import MultiPlotWindow
from EVA.widgets.muonic_xray_simulation.model_spectra_widget import ModelSpectraWidget
from EVA.widgets.srim import trim_window
from EVA.widgets.plot_analysis import plot_window
from EVA.widgets.settings import energy_correction_window, efficiency_correction_window
from EVA.widgets.manual import manual_window
from EVA.widgets.peakfit import peakfit_widget

logger = logging.getLogger(__name__)

class MainPresenter(object):
    def __init__(self, view, model):
        config = get_config()
        self.view = view
        self.model = model

        # Set up action bar connections
        self.view.file_exit.triggered.connect(self.view.closeEvent)
        self.view.file_browse_dir.triggered.connect(self.set_default_directory)
        self.view.file_load_default.triggered.connect(self.load_default_config)

        self.view.plot_which_det_GE1.triggered.connect(lambda: self.model.toggle_plot_detector(
            self.view.plot_which_det_GE1.isChecked(), "GE1"))
        self.view.plot_which_det_GE2.triggered.connect(lambda: self.model.toggle_plot_detector(
            self.view.plot_which_det_GE2.isChecked(), "GE2"))
        self.view.plot_which_det_GE3.triggered.connect(lambda: self.model.toggle_plot_detector(
            self.view.plot_which_det_GE3.isChecked(), "GE3"))
        self.view.plot_which_det_GE4.triggered.connect(lambda: self.model.toggle_plot_detector(
            self.view.plot_which_det_GE4.isChecked(), "GE4"))

        self.view.plot_multiplot.triggered.connect(self.open_multiplot)

        self.view.update_normalisation_menu(config["general"]["normalisation"])
        self.view.norm_none.triggered.connect(lambda: self.set_norm_none(self.view.norm_none.isChecked()))
        self.view.norm_counts.triggered.connect(lambda: self.set_norm_counts(self.view.norm_counts.isChecked()))
        self.view.norm_events.triggered.connect(lambda: self.set_norm_events(self.view.norm_events.isChecked()))

        self.view.energy_corrections.triggered.connect(self.open_energy_corrections)
        self.view.efficiency_corrections.triggered.connect(self.open_efficiency_corrections)

        self.view.peakfit_GE1.triggered.connect(lambda: self.open_peakfit("GE1"))
        self.view.peakfit_GE2.triggered.connect(lambda: self.open_peakfit("GE2"))
        self.view.peakfit_GE3.triggered.connect(lambda: self.open_peakfit("GE3"))
        self.view.peakfit_GE4.triggered.connect(lambda: self.open_peakfit("GE4"))

        self.view.trim_simulation.triggered.connect(self.open_trim)
        #self.view.trim_simulation_test.triggered.connect(self.RunTrimExample)
        self.view.model_muon_spectrum.triggered.connect(self.open_model_muon_spectrum)

        self.view.help_manual.triggered.connect(self.open_manual)

        self.view.get_next_run_button.clicked.connect(self.increment_run_num)
        self.view.load_next_run_button.clicked.connect(lambda: self.increment_run_num(load=True))
        self.view.get_prev_run_button.clicked.connect(self.decrement_run_num)
        self.view.load_prev_run_button.clicked.connect(lambda: self.decrement_run_num(load=True))
        self.view.load_button.clicked.connect(self.load_run_num)

    def set_norm_none(self, checked):
        if checked:
            self.model.set_run_normalisation("none")
            self.view.update_normalisation_menu("none")
            self.view.show_message_box("Normalisation mode has been set to none.", title="Normalisation")
        else:
            self.view.norm_none.setChecked(True)

    def set_norm_counts(self, checked):
        if checked:
            self.model.set_run_normalisation("counts")
            self.view.update_normalisation_menu("counts")
            self.view.show_message_box("Normalisation mode has been set to counts.", title="Normalisation")
        else:
            self.view.norm_counts.setChecked(True)

    def set_norm_events(self, checked):
        if not checked:
            self.view.norm_events.setChecked(True)
        try:
            self.model.set_run_normalisation("events")
            self.view.update_normalisation_menu("events")
            self.view.show_message_box("Normalisation mode has been set to events.", title="Normalisation")
        except ValueError:
            err_str = "Cannot use normalisation by events when comment file has not been loaded."
            self.view.update_normalisation_menu("none")
            logger.error(err_str)
            self.view.show_error_box(err_str)

    def set_default_directory(self):
        new_dir = self.view.get_dir()
        self.model.set_directory(new_dir)

    def load_default_config(self):
        get_config().restore_defaults()
        self.view.show_message_box("Configurations have been restored to defaults.")

    def increment_run_num(self, load=False):
        try:
            run_num = int(self.view.get_run_num_line_edit()) + 1
            self.view.set_run_num_line_edit(str(run_num))

            if load:
                self.load_run_num()

        except (ValueError, AttributeError):
            self.view.show_error_box("Invalid run number!")
            return

    def decrement_run_num(self, load=False):
        try:
            run_num = int(self.view.get_run_num_line_edit()) - 1
            self.view.set_run_num_line_edit(str(run_num))

            if load:
                self.load_run_num()

        except (ValueError, AttributeError):
            self.view.show_error_box("Invalid run number!")
            return

    def load_run_num(self):
        try:
            run_num = int(self.view.get_run_num_line_edit())
        except (ValueError, AttributeError):
            self.view.show_error_box("Invalid run number!")
            return

        flags = self.model.load_run(run_num)

        if flags["no_files_found"]: #  no data was loaded - return now
            # Update GUI
            self.view.set_run_num_label("File load failed")
            self.view.set_comment_labels("Comment file not found.", "N/A", "N/A", "N/A")
            return

        self.view.set_run_num_label(str(run_num))

        if flags["comment_not_found"]: # Comment file was not found
            self.view.set_comment_labels(comment="Comment file not found.", start="N/A", end="N/A", events="N/A")

        else: # write comment info to GUI
            comment, start, end, events = self.model.read_comment_data()
            self.view.set_comment_labels(comment, start, end, events)

        if flags["norm_by_spills_error"]:  # normalisation by spills failed
            self.view.update_normalisation_menu("none")

            # display error message to let user know what happened
            err_str = ("Cannot use normalisation by spills when comment file has not been loaded. Normalisation has been "
                       "set to none.")

            self.view.show_error_box(err_str, title="Normalisation error")

        self.open_plot_window()
        self.view.peakfit_menu.setDisabled(False)

    def open_multiplot(self):
        logger.info("Launching multiplot window.")
        self.view.multiplot_window = MultiPlotWindow()
        self.view.multiplot_window.show()

    def open_energy_corrections(self):
        logger.info("Launching energy correction window.")

        if self.view.energy_correction_window is None:
            self.view.energy_correction_window = energy_correction_window.Correction_E()
            self.view.energy_correction_window.show()
        else:
            self.view.energy_correction_window.show()

        self.view.energy_correction_window.energycorr_window_closed_s.connect(self.close_energy_corrections)

    def close_energy_corrections(self, event):
        event.accept()
        self.view.energy_correction_window = None
        logger.info("Closing energy correction window.")

    def open_efficiency_corrections(self):
        logger.info("Launching efficiency correction window.")

        if self.view.efficiency_correction_window is None:
            self.view.efficiency_correction_window = efficiency_correction_window.Correction_Eff()
            self.view.efficiency_correction_window.show()
        else:
            self.view.efficiency_correction_window.show()

        self.view.efficiency_correction_window.effcorr_window_closed_s.connect(self.close_efficiency_corrections)

    def close_efficiency_corrections(self, event):
        event.accept()
        self.view.efficiency_correction_window = None
        logger.info("Closed efficiency corrections window.")

    def open_peakfit(self, detector):
        logger.info("Launching peak fitting window for %s.", detector)
        self.view.peak_fit_window = peakfit_widget.PeakFitWidget(self.model.run, detector)
        self.view.peak_fit_window.showMaximized()

    def open_trim(self):
        logger.info("Launching TRIM window.")
        self.view.TRIM_window = trim_window.RunSimTRIMSRIM()
        self.view.TRIM_window.showMaximized()

    def open_model_muon_spectrum(self):
        logger.info("Launching muonic x-ray modelling window.")
        self.view.muon_spectrum_window = ModelSpectraWidget()
        self.view.muon_spectrum_window.showMaximized()

    def open_manual(self):
        logger.info("Launching manual window.")
        if self.view.manual_window is None:
            self.view.manual_window = manual_window.ManualWindow()
            self.view.manual_window.show()
        else:
            self.view.manual_window.show()

    def open_plot_window(self):
        config = get_config()

        logger.info("Launching plot window.")
        if self.view.plot_window is None:
            self.view.plot_window = plot_window.PlotWindow(run=self.model.run)
            self.view.plot_window.setWindowTitle("Plot Window: " + config["general"]["run_num"])
            self.view.plot_window.showMaximized()

        else:
            self.view.plot_window = plot_window.PlotWindow(run=self.model.run)
            self.view.plot_window.setWindowTitle("Plot Window" + config["general"]["run_num"])
            self.view.plot_window.showMaximized()

