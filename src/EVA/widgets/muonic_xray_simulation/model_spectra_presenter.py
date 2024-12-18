
class ModelSpectraPresenter(object):
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.on_simulation_start_s.connect(self.start_simulation)
        self.populate_gui()

    def start_simulation(self):
        parameters = self.view.get_form_data()
        if not parameters:
            return

        fig, axs = self.model.model_spectrum(**parameters)
        self.view.plot.update_plot(fig, axs)

    def populate_gui(self):
        element_list = self.model.element_names
        self.view.populate_gui(element_list)
