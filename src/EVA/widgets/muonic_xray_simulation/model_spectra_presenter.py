from EVA.widgets.muonic_xray_simulation.model_spectra_model import ModelSpectraModel

class ModelSpectraPresenter(object):
    def __init__(self, view):
        self.view = view
        self.model = ModelSpectraModel(self)
        self.view.on_simulation_start_s.connect(self.start_simulation)
        self.populate_gui()

    def start_simulation(self):
        elements = [element.currentText() for element in self.view.element_selects]
        proportions = [float(proportion.text()) for proportion in self.view.proportion_selects]
        show_components = self.view.show_components_box.isChecked()
        show_detectors = [button.isChecked() for button in self.view.detectors]
        detectors = ["GE1", "GE2", "GE3", "GE4"]

        if self.view.show_components_box.isChecked():
            notations = ["spectroscopic", "iupac", "siegbahn"]
            notation = notations[self.view.select_notation.currentIndex()]
        else:
            notation = "iupac"

        detectors = [detector for i, detector in enumerate(detectors) if show_detectors[i]]

        if self.view.e_range_auto.isChecked():
            e_range = None
        else:
            e_range = [float(self.view.e_min.text()), float(self.view.e_max.text())]

        fig, ax = self.model.get_model(elements, proportions, detectors,
                                       e_range, notation=notation, dx=0.1,
                                          show_components=show_components, e_res_model="linear",
                                          show_primary=self.view.show_primary.isChecked(),
                                          show_secondary=self.view.show_secondary.isChecked())

        self.view.plot.update_plot(fig, ax)

    def populate_gui(self):
        print("populating...")
        element_list = self.model.get_element_names()
        self.view.populate_gui(element_list)


