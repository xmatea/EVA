# imports
import re
import json
from PyQt6.QtWidgets import QMainWindow, QTreeWidgetItem, QTableWidgetItem, QMessageBox
from functools import partial

from EVA.core.data_searching.get_match import search_muxrays
from EVA.windows.periodic_table.periodic_table import Ui_MainWindow
from EVA.util.path_handler import get_path
from EVA.util.transition_utils import to_iupac

# lists
elements = ["H", "He", 
            "Li", "Be", "B", "C", "N", "O", "F", "Ne", 
            "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", 
            "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
            "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
            "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
            "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
            ]

elements_disable = ["H", "Kr", "Xe", "Tc", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", 
                    "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og", "Pm", "Pa", "U", "Np", "Pu", "Am",
                    "Cm", "Bk", "Cf", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"] 

# class definitions
class PeriodicTableWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # disable buttons for some of the elements for which no muonic X-ray data exist
        for element in elements_disable:
            button = getattr(self, f"{element}_button", None)
            button.setEnabled(False)
            button.setStyleSheet("QPushButton {background-color: transparent}")

        # signal when a button in the periodic table is pressed
        for element in elements:
            button = getattr(self, f"{element}_button", None)
            button.pressed.connect(partial(self.open_element, element))

        # signal when the print button in the "Muonix X-ray search" group box is pressed
        self.print_button.pressed.connect(self.energy_search)

        # the first tab, for muonic X-rays, is set to active when the GUI opens
        self.tabWidget.setCurrentIndex(0)

    def open_element(self, name):
        with open(get_path('src/EVA/databases/muonic_xrays/mudirac_data_readable.json'), 'r') as jsonfile1:
            mudirac_data_from_file = json.load(jsonfile1)
        with open(get_path('src/EVA/databases/gammas/gammas.json'), 'r') as jsonfile2:
            gamma_data_from_file = json.load(jsonfile2)
        with open(get_path('src/EVA/databases/electronic_xrays/xray_booklet_data.json'), 'r') as jsonfile3:
            electronic_data_from_file = json.load(jsonfile3)

        for k1, v1 in mudirac_data_from_file.items():
            if k1 == name:
                for k2, v2 in v1.items():
                    if k2 == "Info":
                        text = f"{v2}"
                    elif k2 == "Isotopes":
                        data = v2
        self.element_info_text.setPlainText(text)
        self.element_info_text.setReadOnly(True)

        items = []
        self.element_info_muonic_xray_tree.clear()
        for k3, v3 in data.items():
            item = QTreeWidgetItem([k3])
            for k4, v4 in v3.items():
                match k4:
                    case "Abundancy":
                        info = QTreeWidgetItem([k4, v4])
                        item.addChild(info)
                    case "Primary" | "Secondary":
                        d1 = re.sub('[^A-Za-z0-9-./ ]+', '', str(v4)).split()
                        d2 = [d for d in d1 if (d != "E" and d != "I")]
                        d3 = "\n"
                        for i in range(0, len(v4)):
                            d3 = d3 + f"{d2[3*i]}\t{float(d2[3*i+1]):.3f}\t\t{d2[3*i+2]}\n"
                        info = QTreeWidgetItem([k4, d3])
                        item.addChild(info) 
            items.append(item)
        self.element_info_muonic_xray_tree.insertTopLevelItems(0, items)

        for kg1, vg1 in gamma_data_from_file.items():
            if kg1 == name:
                for kg2, vg2 in vg1.items():
                    if kg2 == "Isotopes":
                        datag = vg2

        itemsg = []
        self.treeWidget_2.clear()
        for kg3, vg3 in datag.items():
            itemg = QTreeWidgetItem([kg3])
            for i in vg3:
                for j in i.items():
                    d1g = re.sub('[^A-Za-z0-9-./ ]+', '', str(i)).split()
                    d2g = [dg for dg in d1g if (dg != "E" and dg != "T1/2")]
                    d3g = ""
                    for k in range(0, 1):
                        d3g = d3g + f"{d2g[3*k]}\t{float(d2g[3*k+1]):.4f}"
                    info = QTreeWidgetItem(["", str(d3g)])
                itemg.addChild(info)
            itemsg.append(itemg)
        self.treeWidget_2.insertTopLevelItems(0, itemsg)

        for ke1, ve1 in electronic_data_from_file.items():
            if ke1 == name:
                for i, (ke2, ve2) in enumerate(ve1.items()):
                    self.element_info_electronic_xray_table.setRowCount(len(ve1))
                    item_transition = QTableWidgetItem(ke2)
                    item_energy = QTableWidgetItem(ve2)
                    self.element_info_electronic_xray_table.setItem(i, 0, item_transition)
                    self.element_info_electronic_xray_table.setItem(i, 1, item_energy)

    def energy_search(self):
        self.x_ray_search.setPlainText("")
        try:
            energy = float(self.energy_input.text())
            error = float(self.uncertainty_input.text())
        except (AttributeError, ValueError):
            msg = QMessageBox.critical(self, "Search error", "Invalid input in energy search.",
                                       QMessageBox.StandardButton.Ok)
            return

        res, _, _ = search_muxrays([[energy, error]])

        for r in res:
            if r["error"] == error: # Only get results that are within the search width (get_match will get matches within
                # 1x error, 2x error and 3x error)
                line = f"{r["energy"]:.4f}\t{r["transition"]}\t{to_iupac(r["transition"])}\t{r["element"]}\n"
                self.x_ray_search.insertPlainText(line)

        """ Previous method using the .dat files and custom search
        
        energy_min = int(self.energy_input.text()) - int(self.uncertainty_input.text())
        energy_max = int(self.energy_input.text()) + int(self.uncertainty_input.text())
        self.x_ray_search.insertPlainText(f"Searching for all values in between the energies {energy_min} and {energy_max} keV:\n")
        
        energy_list = range(energy_min, energy_max)
        separator = "\\.|"
        energy_pattern = separator.join(str(x) for x in energy_list)+"\\."
        filelist = glob.glob("elements/*.dat")
        for i in filelist:
            with open(i, "r", encoding = "utf8") as fp:
                for line in fp:
                    if re.match(energy_pattern, line):
                        self.x_ray_search.insertPlainText(line)
        """

