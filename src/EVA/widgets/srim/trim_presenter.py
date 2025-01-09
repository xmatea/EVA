import time
from copy import copy
from PyQt6.QtWidgets import QWidget

from EVA.core.app import get_config


class TrimPresenter(QWidget):
    def __init__(self, view, model, parent=None):
        super().__init__(parent)
        self.view = view
        self.model = model

        self.view.run_sim_button.clicked.connect(self.start_sim)
        self.view.plot_comp_s.connect(self.on_show_plot_comp)
        self.view.plot_whole_s.connect(self.on_show_plot_whole)
        self.view.save_s.connect(self.on_save)

        """
        
        self.view.file_save.triggered.connect(lambda: self.file_save(SampleName, SimType, Momentum,
                                                                     MomentumSpread, ScanType, MinMomentum,
                                                                     MaxMomentum, StepMomentum, SRIMdir,
                                                                     TRIMOutDir, Stats))

        self.view.file_load.triggered.connect(lambda: self.file_load(SampleName, SimType, Momentum,
                                                                     MomentumSpread, ScanType, MinMomentum,
                                                                     MaxMomentum, StepMomentum, SRIMdir,
                                                                     TRIMOutDir, Stats))
        """
    def connect_results_table(self):
        # connects buttons in result table to methods from the model
        table = self.view.tab2.table_PlotRes
        for row in range(table.rowCount()):
            momentum = table.item(row, 0).text()
            self.view.plot_comp_buttons[row].clicked.connect(lambda _, r=row, m=momentum: self.on_show_plot_comp(r, m))
            self.view.plot_whole_buttons[row].clicked.connect(lambda _, r=row, m=momentum: self.on_show_plot_whole(r, m))
            self.view.save_buttons[row].clicked.connect(lambda _, r=row: self.on_save(r))

    def start_sim(self):
        # get form data
        try:
            form_data = self.view.get_form_data()
        except (ValueError, AttributeError) as e:
            self.view.show_error_box("Invalid form input!")
            # raise e
            return

        # get table data
        try:
            layers = self.view.get_table_data()
        except (ValueError, AttributeError) as e:
            self.view.show_error_box("You must specify a valid sample name and thickness for all layers.")
            # raise e
            return

        # send data to model and simulate
        try:
            self.model.trim_simulation(**form_data, layers=layers)
        except KeyError:
            self.view.show_error_box(title="Form error", msg="All element layers must have a specified density.")
            return

        self.view.setup_results_table(self.model.momentum, self.model.components) # display results in table
       # self.connect_results_table() # connect results table buttons after successful simulation

    def on_show_plot_comp(self, row, momentum):
        t0 = time.time_ns()
        # Generate figure to display in view
        fig, ax = self.model.plot_components(row, momentum)
        self.view.plot.update_plot(fig, ax)
        t1 = time.time_ns()
        print("time taken: ", (t1-t0)/1e9)

    def on_show_plot_whole(self, row, momentum):
        # Generate figure to display in view
        fig, ax = self.model.plot_whole(row, momentum)
        self.view.plot.update_plot(fig, ax)

    def on_save(self, row):
        self.model.save_sim(row)

