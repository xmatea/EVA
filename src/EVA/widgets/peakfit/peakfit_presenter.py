from EVA.widgets.peakfit.peakfit_model import PeakFitModel
from EVA.widgets.peakfit.constraints_window import ConstraintsWindow


class PeakFitPresenter(object):
    def __init__(self, view):
        self.view = view
        self.model = PeakFitModel(self, view.detector)

        # connect all signals from the view to slots
        self.view.fit_button_clicked_s.connect(self.start_peakfit)
        self.view.remove_peak_button_clicked_s.connect(self.remove_peak)
        self.view.peak_selected_s.connect(self.add_peak_selection)
        self.view.peak_table_cell_changed_s.connect(self.modify_peak_parameter)
        self.view.bckg_table_cell_changed_s.connect(self.modify_background_parameter)
        self.view.constraints_button_clicked_s.connect(self.launch_constraints_menu)
        self.view.save_params_s.connect(self.on_save_params)
        self.view.load_params_s.connect(self.on_load_params)
        self.view.save_fit_report_s.connect(self.save_fit_report)

    def launch_constraints_menu(self):
        # Launches dialog to select constraints and bounds
        constraints_dialog = ConstraintsWindow(self.view, self.model.initial_params)
        constraints_dialog.param_settings_saved_s.connect(self.get_constraint_settings)
        constraints_dialog.show()

    def get_constraint_settings(self, params):
        # Updates the initial parameters in the model when signal is received from the constraint dialogue
        self.model.initial_params = params

    def update_peaks_table(self, params):
        # Filters out only peak parameters and updates the table in view
        peak_params = {k:v for k, v in params.items() if k != "background"}
        for i, param in enumerate(peak_params.items()):
            peak_id = param[0]
            vars = param[1]
            self.view.update_table_row(self.view.peak_selection_table, row=i, vars=vars,
                                       order=("center", "sigma", "amplitude"), param_id=peak_id)

    def update_background_table(self, params):
        # Retrieves background parameters and updates the table in view
        bckg_params = params["background"]
        self.view.update_table_row(self.view.background_function_table, row=0, vars=bckg_params,
                                   order=("a", "b", "c"))

    def modify_background_parameter(self, ix):
        # Updates the current initial background parameters in background table when table is updated
        row, col = ix

        headers = ["a", "b", "c"]
        var_name = headers[col]

        table = self.view.background_function_table
        old_val = self.model.initial_params["background"][var_name] # store previous value

        try:
            field = table.item(row, col).text()
            value = float(field.split("+/-")[0]) # get rid of error part if present (not needed for intial params)

            self.model.initial_params["background"][var_name]["value"] = value

        except ValueError: # if casting to float failed
            self.view.show_error_dialogue("Invalid parameter in peak table.")
            self.view.update_table_cell(table, row, col, old_val)

        except AttributeError: # if parameter is left blank (None)
            self.view.show_error_dialogue("Parameter cannot be empty.")
            self.view.update_table_cell(table, row, col, old_val)


    def modify_peak_parameter(self, ix):
        # Updates the current initial peak parameters in background table when table is updated
        row, col = ix
        headers = ["id", "center", "sigma", "amplitude"]

        table = self.view.peak_selection_table

        peak_params = {k:v for k, v in self.model.initial_params.items() if k != "background"}

        var_name = headers[col]
        peak_id = list(peak_params)[row]

        # ignore if ID is edited
        if col == 0:
            return

        old_val = self.model.initial_params[peak_id][var_name]["value"]

        try:
            field = table.item(row, col).text()
            value = float(field.split("+/-")[0]) # get rid of error part if present
            self.model.initial_params[peak_id][var_name]["value"] = value

        except ValueError: # if casting to float failed
            self.view.show_error_dialogue("Invalid parameter in peak table.")
            self.view.update_table_cell(table, row, col, old_val, peak_id)

        except AttributeError: # if field is left blank (None)
            self.view.show_error_dialogue("Parameter cannot be empty.")
            self.view.update_table_cell(table, row, col, old_val, peak_id)

    def get_e_range(self):
        e_min = float(self.view.e_range_lower_edit.text())
        e_max = float(self.view.e_range_upper_edit.text())
        return e_min, e_max

    def start_peakfit(self):
        # starts peak fitting in the model

        if len(self.model.initial_params) <= 1:
            self.view.show_error_dialogue("Please add at least one peak to fit.")
            return

        if self.view.e_range_auto_check.isChecked():
            self.model.calculate_x_range()
            self.view.update_e_range_form(self.model.x_range)
        else:
            try:
                self.model.x_range = self.get_e_range()
            except ValueError:
                self.view.show_error_dialogue("Please specify a valid energy range.")
                return
        try:
            self.model.fit_peaks()
            xdata = self.model.fit_result.userkws["x"] # get the xdata used in the fit to plot

        except TypeError as e:
            if e.args[0] == "Not enough points":
                self.view.show_error_dialogue("Selected fitting range too narrow to fit curve. (Not enough data points in range.)\n"
                                              "Either specify a wider energy range or increase initial peak width of peaks.")
                #raise e
                return
            else:
                self.view.show_error_dialogue(
                    f"An unexpected error occurred. Please ensure your initial parameters are good enough, and"
                    f" that any constraints / bounds are valid, if specified.\n"
                    f"Error message from lmfit: {e.args[0]}")
                #raise e
                return

        except ValueError as e:
            self.view.show_error_dialogue(f"An unexpected error occurred. Please ensure your initial parameters "
                                          f"are good enough.\nError message from lmfit: {e.args[0]}")
            return
            #raise e

        except RecursionError:
            self.view.show_error_dialogue("A recursion error occurred. If parameter constraints have been set, "
                                          "ensure they are not recursive.")
            return

        # Display fit report in text window
        self.view.results_text.setText(self.model.fit_result.fit_report())

        # Update plot
        self.model.calculate_y_range(self.model.fit_result.best_fit)

        # Print new results in the tables
        self.update_peaks_table(self.model.fitted_params)
        self.update_background_table(self.model.fitted_params)

        self.view.plot_fit(xdata, self.model.fit_result.best_fit, self.model.fit_result.residual,
                           x_range=self.model.x_range, y_range=self.model.y_range)

        # If errors could not be estimated, notify user
        if not self.model.fit_result.errorbars:
            self.view.show_error_dialogue("Could not estimate fit errors. Please adjust your initial parameters "
                                         "and constraints / bounds if specified.")

    def remove_peak(self):
        params = self.model.initial_params

        # remove background parameters
        peak_params = {k:v for k, v in params.items() if k != "background"}

        # get id of last peak in peak_params
        peak_id = list(peak_params)[-1]

        self.model.initial_params.pop(peak_id)

    def add_peak_selection(self, params):
        x = params["x"]
        ax = params["axes"]
        name = f"p{self.view.peak_selection_table.rowCount()}"

        # Get spectrum data by label (_child1 because plotted data does not have an assigned label)
        line = [l for l in ax.get_lines() if l.get_label() == "_child1"][0]

        # Send the data to the model to add the initial parameters
        self.model.add_initial_peak_params(line, x, name=name)

        # Add the new peak to the table
        self.update_peaks_table(self.model.initial_params)
        self.view.quit_add_peak_mode(peak_added=True)

    def on_save_params(self, path):
        self.model.save_params(path)

    def on_load_params(self, path):
        self.model.load_params(path)
        self.update_peaks_table(self.model.initial_params)
        self.update_background_table(self.model.initial_params)

    def save_fit_report(self, path):
        self.model.save_fit_report(path)
