import time
from copy import copy
from PyQt6.QtWidgets import QWidget

from EVA.core.app import get_config


class TrimPresenter(QWidget):
    def __init__(self, view, model, parent=None):
        super().__init__(parent)
        self.view = view
        self.model = model

        self.view.file_load.triggered.connect(self.load_settings)
        self.view.file_save.triggered.connect(self.save_settings)

        self.view.run_sim_button.clicked.connect(self.start_sim)
        self.view.plot_comp_s.connect(self.on_show_plot_comp)
        self.view.plot_whole_s.connect(self.on_show_plot_whole)
        self.view.save_s.connect(self.on_save)

        self.view.tab1.table_TRIMsetup.cellClicked.connect(self.on_cell_clicked)

    """
    # NOT USED AT THE MOMEMENT
    def connect_results_table(self):
        # connects buttons in result table to methods from the model
        table = self.view.tab2.table_PlotRes
        for row in range(table.rowCount()):
            momentum = table.item(row, 0).text()
            self.view.plot_comp_buttons[row].clicked.connect(lambda _, r=row, m=momentum: self.on_show_plot_comp(r, m))
            self.view.plot_whole_buttons[row].clicked.connect(lambda _, r=row, m=momentum: self.on_show_plot_whole(r, m))
            self.view.save_buttons[row].clicked.connect(lambda _, r=row: self.on_save(r))
    """

    def start_sim(self):
        # get form data
        try:
            form_data = self.view.get_form_data()
        except (ValueError, AttributeError) as e:
            self.view.show_error_box("Invalid form input!")
            return

        # get table data
        try:
            layers = self.view.get_table_data()
        except (ValueError, AttributeError) as e:
            self.view.show_error_box("You must specify a valid sample name and thickness for all layers.")
            return
        except KeyError:
            self.view.show_error_box("All element layers must have a specified density.")
            return

        # check if path is valid
        srimdir_valid = self.model.is_valid_path(form_data["srim_dir"])
        outputdir_valid = self.model.is_valid_path(form_data["output_dir"])

        if not srimdir_valid or not outputdir_valid:
            self.view.show_error_box("Could not find SRIM.exe at specified location. "
                                     "Please ensure you have SRIM2013 installed.")
            return

        # if everything is ok, send data to model and simulate
        try:
            self.model.trim_simulation(**form_data, layers=layers)
        except Exception as e:
            self.view.show_error_box(f"An unexpected error has occurred! \n{e.args}")
            return

        self.view.setup_results_table(self.model.momentum, self.model.components) # display results in table

    def on_show_plot_comp(self, row, momentum):
        t0 = time.time_ns()
        # Generate figure to display in view
        fig, ax = self.model.plot_components(row, momentum)
        self.view.plot.update_plot(fig, ax)
        t1 = time.time_ns()
        print("time taken: ", (t1-t0)/1e9)

    def on_cell_clicked(self, row, col):
        table = self.view.tab1.table_TRIMsetup
        if row == table.rowCount() - 1: # if cell on last row is edited
            self.view.add_trimsetup_row()

    def on_show_plot_whole(self, row, momentum):
        # Generate figure to display in view
        fig, ax = self.model.plot_whole(row, momentum)
        self.view.plot.update_plot(fig, ax)

    def on_save(self, row):
        self.model.save_sim(row)


    def save_settings(self):
        try:
            form_data = self.view.get_form_data()
            layers = self.view.get_table_data()
        except (AttributeError, ValueError) as e:
            self.view.show_error_box("Cannot save settings. Invalid data in form or layers table.")
            #raise e
            return

        path = self.view.request_save_file()
        if path != "":
            self.model.save_settings(**form_data, layers=layers, target_dir=path)

    def load_settings(self):
        path = self.view.request_load_file()
        if path != "":
            form_data, table_data = self.model.load_settings(path)
            self.view.set_form_data(form_data)
            self.view.set_table_data(table_data)

