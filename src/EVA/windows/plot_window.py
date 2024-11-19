from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QGridLayout,
    QWidget,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QComboBox
)

from EVA.windows.backends import FindPeaks, getmatch, Plot_Spectra, SortMatch
from EVA.classes.app import get_app, get_config
import time

from EVA.classes.plot_widget import PlotWidget

class PlotWindow(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
    """

    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.scn_res = int(get_config()["display"]["screen_resolution"])

        # the size of this widget is currently set to maximised from MainWindow
        """
        if self.scn_res == 1:
            self.resize(1800, 900)
            self.setMinimumSize(1600, 700)
        elif self.scn_res == 2:
            self.resize(1600, 900)
            self.setMinimumSize(1400, 700)
        else:
            self.resize(2800, 900)
            self.setMinimumSize(1800, 700)
        """

        # Set up window
        self.setWindowTitle("Plot Window ")
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # set up clickpeaks window and find peaks window
        self.tabs = QTabWidget()
        self.clickpeaks = self.setup_clickpeaks_widget()
        self.findpeaks = self.setup_peakfind_widget()

        self.tabs.addTab(self.clickpeaks, "Peak Identification")
        self.tabs.addTab(self.findpeaks, "Element Search")

        # set up plot window and navigator
        self.plot = self.plot_spectra()
        plt.connect('button_press_event', self.on_click)

        # Add everything to main window layout (gridlayout)
        self.layout.addWidget(self.tabs, 0, 0, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.plot, 1, 1)
        #self.layout.addWidget(self.findpeaks, 2, 1)

        self.numoflines = 0
        self.linenum = []
        self.lines = []
        self.elementline = []

    def setup_clickpeaks_widget(self):
        # temporary size fix
        MIN_WIDTH1 = 650
        MIN_WIDTH2 = 450

        MIN_HEIGHT1 = 600
        MIN_HEIGHT2 = 400

        NCOLS_MUON = 3
        NCOLS_GAMMA = 5

        COLWIDTH_MUON = (MIN_WIDTH2-50)//NCOLS_MUON
        COLWIDTH_GAMMA = (MIN_WIDTH2-50)//NCOLS_GAMMA

        clickpeaks = QWidget()
        clickpeaks_layout = QVBoxLayout()
        clickpeaks.setLayout(clickpeaks_layout)

        clickpeaks.desc_muon = QLabel("Possible Muonic X-ray Transition:",clickpeaks)
        clickpeaks.tab_muon = QTabWidget(clickpeaks)

        # wrapper container to hold muon tab page and title
        clickpeaks.muon_container = QWidget()
        clickpeaks.muon_container_layout = QVBoxLayout()
        clickpeaks.muon_container_layout.addWidget(clickpeaks.desc_muon)
        clickpeaks.muon_container_layout.addWidget(clickpeaks.tab_muon)
        clickpeaks.muon_container.setLayout(clickpeaks.muon_container_layout)

        clickpeaks_layout.addWidget(clickpeaks.muon_container)

        clickpeaks.tab1 = QWidget()
        clickpeaks.tab2 = QWidget()
        clickpeaks.tab3 = QWidget()
        clickpeaks.tab4 = QWidget()

        if self.scn_res == 1:
            clickpeaks.tab_muon.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)
        elif self.scn_res == 2:
            clickpeaks.tab_muon.setMinimumSize(MIN_WIDTH2, MIN_HEIGHT2)
        else:
            clickpeaks.tab_muon.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)

        clickpeaks.tab_muon.addTab(clickpeaks.tab1, "All Peaks")
        clickpeaks.tab_muon.addTab(clickpeaks.tab2, "Primary")
        clickpeaks.tab_muon.addTab(clickpeaks.tab3, "Secondary")
        clickpeaks.tab_muon.addTab(clickpeaks.tab4, "Remove Plot lines")

        clickpeaks.table_plotted_lines = QTableWidget(clickpeaks.tab4)
        clickpeaks.table_plotted_lines.setShowGrid(True)
        clickpeaks.table_plotted_lines.setColumnCount(2)
        clickpeaks.table_plotted_lines.setRowCount(10)

        if self.scn_res == 1:
            clickpeaks.table_plotted_lines.setMinimumSize(600, MIN_HEIGHT1)
        elif self.scn_res == 2:
            clickpeaks.table_plotted_lines.setMinimumSize(MIN_WIDTH2,  MIN_HEIGHT2)
        else:
            clickpeaks.table_plotted_lines.setMinimumSize(600, MIN_HEIGHT1)

        clickpeaks.table_plotted_lines.verticalScrollBar()
        clickpeaks.table_plotted_lines.setHorizontalHeaderLabels(['Muonic X-ray', 'Gamma'])
        clickpeaks.table_plotted_lines.setColumnWidth(0, (MIN_WIDTH2-50)//2)
        clickpeaks.table_plotted_lines.setColumnWidth(1, (MIN_WIDTH2-50)//2)
        clickpeaks.table_plotted_lines.cellClicked.connect(self.remove_line)

        # table for all peaks
        clickpeaks.table_muon = QTableWidget(clickpeaks.tab1)
        clickpeaks.table_muon.setShowGrid(True)
        clickpeaks.table_muon.setColumnCount(3)
        clickpeaks.table_muon.setRowCount(9)
        clickpeaks.table_muon.setColumnWidth(0, COLWIDTH_MUON)
        clickpeaks.table_muon.setColumnWidth(1, COLWIDTH_MUON)
        clickpeaks.table_muon.setColumnWidth(2, COLWIDTH_MUON)


        if self.scn_res == 1:
            clickpeaks.table_muon.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)
        elif self.scn_res == 2:
            clickpeaks.table_muon.setMinimumSize(MIN_WIDTH2, MIN_HEIGHT2)
        else:
            clickpeaks.table_muon.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)

        clickpeaks.table_muon.verticalScrollBar()
        clickpeaks.table_muon.setHorizontalHeaderLabels(['Element', 'Transition', 'Error'])
        clickpeaks.table_muon.cellClicked.connect(self.clickpeaks_table_clickpeaks)

        # table for primary peaks
        clickpeaks.table_muon_prim = QTableWidget(clickpeaks.tab2)
        clickpeaks.table_muon_prim.setShowGrid(True)
        clickpeaks.table_muon_prim.setColumnCount(3)
        clickpeaks.table_muon_prim.setRowCount(9)
        clickpeaks.table_muon_prim.setColumnWidth(0, COLWIDTH_MUON)
        clickpeaks.table_muon_prim.setColumnWidth(1, COLWIDTH_MUON)
        clickpeaks.table_muon_prim.setColumnWidth(2, COLWIDTH_MUON)

        if self.scn_res == 1:
            clickpeaks.table_muon_prim.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)
        elif self.scn_res == 2:
            clickpeaks.table_muon_prim.setMinimumSize(MIN_WIDTH2, MIN_HEIGHT2)
        else:
            clickpeaks.table_muon_prim.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)

        clickpeaks.table_muon_prim.verticalScrollBar()
        clickpeaks.table_muon_prim.setHorizontalHeaderLabels(['Element', 'Transition', 'Error'])
        clickpeaks.table_muon_prim.cellClicked.connect(self.clickpeaks_table_clickpeaks_prim)

        # table for secondary peaks
        clickpeaks.table_muon_sec = QTableWidget(clickpeaks.tab3)
        clickpeaks.table_muon_sec.setShowGrid(True)
        clickpeaks.table_muon_sec.setColumnCount(3)
        clickpeaks.table_muon_sec.setRowCount(9)
        clickpeaks.table_muon_sec.setColumnWidth(0, COLWIDTH_MUON)
        clickpeaks.table_muon_sec.setColumnWidth(1, COLWIDTH_MUON)
        clickpeaks.table_muon_sec.setColumnWidth(2, COLWIDTH_MUON)

        if self.scn_res == 1:
            clickpeaks.table_muon_sec.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)
        elif self.scn_res == 2:
            clickpeaks.table_muon_sec.setMinimumSize(MIN_WIDTH2, MIN_HEIGHT2)
        else:
            clickpeaks.table_muon_sec.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)

        clickpeaks.table_muon_sec.verticalScrollBar()
        clickpeaks.table_muon_sec.setHorizontalHeaderLabels(['Element', 'Transition', 'Error'])
        clickpeaks.table_muon_sec.cellClicked.connect(self.clickpeaks_table_clickpeaks_sec)

        # Gamma table
        clickpeaks.desc_gamma = QLabel("Possible Gamma Transition:", clickpeaks)
        clickpeaks.table_gamma = QTableWidget(clickpeaks)

        # wrapper container to hold gamma tab page and title
        clickpeaks.gamma_container = QWidget()
        clickpeaks.gamma_container_layout = QVBoxLayout()
        clickpeaks.gamma_container_layout.addWidget(clickpeaks.desc_gamma)
        clickpeaks.gamma_container_layout.addWidget(clickpeaks.table_gamma)
        clickpeaks.gamma_container.setLayout(clickpeaks.gamma_container_layout)

        clickpeaks_layout.addWidget(clickpeaks.gamma_container)
        clickpeaks.table_gamma.setShowGrid(True)
        clickpeaks.table_gamma.setSortingEnabled(True)

        clickpeaks.table_gamma.setColumnCount(5)
        clickpeaks.table_gamma.setRowCount(9)
        clickpeaks.table_gamma.setColumnWidth(0, COLWIDTH_GAMMA)
        clickpeaks.table_gamma.setColumnWidth(1, COLWIDTH_GAMMA)
        clickpeaks.table_gamma.setColumnWidth(2, COLWIDTH_GAMMA)
        clickpeaks.table_gamma.setColumnWidth(3, COLWIDTH_GAMMA)
        clickpeaks.table_gamma.setColumnWidth(4, COLWIDTH_GAMMA)

        if self.scn_res == 1:
            clickpeaks.table_gamma.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)
        elif self.scn_res == 2:
            clickpeaks.table_gamma.setMinimumSize(MIN_WIDTH2, MIN_HEIGHT2)
        else:
            clickpeaks.table_gamma.setMinimumSize(MIN_WIDTH1, MIN_HEIGHT1)

        clickpeaks.table_gamma.setHorizontalHeaderLabels(['Element', 'Energy', 'Error', 'Intensity', 'Lifetime'])
        clickpeaks.table_gamma.cellClicked.connect(self.clickpeaks_table_clickpeaks_gamma)

        return clickpeaks

    def setup_peakfind_widget(self):
        findpeaks = QWidget()
        findpeaks_layout = QVBoxLayout()
        findpeaks.setLayout(findpeaks_layout)

        # Set up settings menu as form widget
        findpeaks.settings_form_layout = QFormLayout()
        findpeaks.settings_form = QWidget()
        findpeaks.settings_form.setLayout(findpeaks.settings_form_layout)

        findpeaks.desc_peaks = QLabel("Peak detection", findpeaks)

        findpeaks.find_peaks_button = QPushButton("Find Peaks", findpeaks)

        findpeaks.find_peaks_button.clicked.connect(
            lambda: self.find_peaks_automatically())

        findpeaks.useDef_checkbox = QCheckBox(findpeaks)

        findpeaks.useDef_checkbox.setChecked(True)
        findpeaks.useDef_checkbox.toggled.connect(self.useDef_onClicked)

        findpeaks.peakfindroutine = QComboBox(findpeaks)
        findpeaks.peakfindroutine.addItem('scipy.FindPeak')
        #findpeaks.peakfindroutine.addItem('scipy.Find_Peak_Cwt')
        findpeaks.peakfindroutine.addItem('find peaks (dev)')

        findpeaks.label_FindPeak_Height = QLabel("Height", findpeaks)
        findpeaks.label_FindPeak_Height.hide()

        findpeaks.lineedit_FindPeak_Height = QLineEdit("10", findpeaks)
        findpeaks.lineedit_FindPeak_Height.hide()
        findpeaks.lineedit_FindPeak_Height.setFixedWidth(100)

        findpeaks.label_FindPeak_Thres = QLabel("Threshold", findpeaks)
        findpeaks.label_FindPeak_Thres.hide()

        findpeaks.lineedit_FindPeak_Thres = QLineEdit("15", findpeaks)
        findpeaks.lineedit_FindPeak_Thres.setFixedWidth(100)
        findpeaks.lineedit_FindPeak_Thres.hide()

        findpeaks.label_FindPeak_Dist = QLabel("Distance", findpeaks)
        findpeaks.label_FindPeak_Dist.hide()

        findpeaks.lineedit_FindPeak_Dist = QLineEdit("1", findpeaks)
        findpeaks.lineedit_FindPeak_Dist.setFixedWidth(100)
        findpeaks.lineedit_FindPeak_Dist.hide()

        # add all widgets to layout
        findpeaks.settings_form_layout.addRow(findpeaks.desc_peaks, findpeaks.find_peaks_button)
        findpeaks.settings_form_layout.addRow(QLabel("Peak finding routine"), findpeaks.peakfindroutine)
        findpeaks.settings_form_layout.addRow(QLabel("Use default settings?"), findpeaks.useDef_checkbox)

        findpeaks.settings_form.setMaximumWidth(400)


        findpeaks.settings_form_layout.addRow(findpeaks.label_FindPeak_Height, findpeaks.lineedit_FindPeak_Height)
        findpeaks.settings_form_layout.addRow(findpeaks.label_FindPeak_Thres, findpeaks.lineedit_FindPeak_Thres)
        findpeaks.settings_form_layout.addRow(findpeaks.label_FindPeak_Dist, findpeaks.lineedit_FindPeak_Dist)

        # Set up peak find result table and tab view
        findpeaks.tabs = QTabWidget(findpeaks)
        findpeaks.clickpeaks = QWidget()
        findpeaks.tab2 = QWidget()
        # self.tab2.tab3 = QWidget()

        findpeaks.tabs.addTab(findpeaks.clickpeaks, "Most Probable")
        findpeaks.tabs.addTab(findpeaks.tab2, "Transitions")
        # self.tab2.tabs.addTab(self.tab2.tab3, "Secondary")

        findpeaks.table_peaks = QTableWidget(findpeaks.clickpeaks)
        findpeaks.table_peaks.setShowGrid(True)
        findpeaks.table_peaks.setColumnCount(2)
        findpeaks.table_peaks.setRowCount(4)
        findpeaks.table_peaks.setColumnWidth(1, 420)
        findpeaks.table_peaks.setMinimumSize(650, 200)
        findpeaks.table_peaks.setHorizontalHeaderLabels(['Detector', 'Probable Elements'])
        findpeaks.table_peaks.verticalScrollBar()
        findpeaks.table_peaks.horizontalScrollBar()

        #findpeaks_layout.addWidget(findpeaks.settings)
        findpeaks_layout.addWidget(findpeaks.settings_form)
        findpeaks_layout.addWidget(findpeaks.tabs)

        return findpeaks

    def update_legend(self):
        for i in range(len(self.plot.canvas.axs)):
            # get all unique labels for the legend to avoid duplicates when plotting multiple lines with same name
            h, l = self.plot.canvas.axs[i].get_legend_handles_labels()
            by_label = dict(zip(l, h))

            # remove legend if there are no labels left
            if len(by_label) == 0 and self.plot.canvas.axs[i].get_legend() is not None:
                self.plot.canvas.axs[i].get_legend().remove()
            else:
                self.plot.canvas.axs[i].legend(by_label.values(), by_label.keys(), loc="upper right")


    def remove_line(self, row: int, col: int):
        cell_contents = self.clickpeaks.table_plotted_lines.item(row, col)

        if cell_contents is None:
            return

        element = cell_contents.text()

        # loop through all lines in all detectors and delete the line if the label is equal to element
        for i in range(len(self.plot.canvas.axs)):

            # search for all lines with label == element
            lines_to_remove = [line for line in self.plot.canvas.axs[i].lines if line.get_label() == element]
            num = len(lines_to_remove)

            for j in range(num):
                lines_to_remove[j].remove()


        self.update_legend()
        self.plot.canvas.draw() # update figure

        self.clickpeaks.table_plotted_lines.removeRow(row)
        #self.clickpeaks.table_plotted_lines.setRowCount(10)
        self.numoflines -= 1

    def clickpeaks_table_clickpeaks_gamma(self, row, col):
        table = self.clickpeaks.table_gamma
        if table.item(row, col) is None:
            return

        Ele = table.item(row, 0).text()
        En = table.item(row, 1).text()

        if col == 0:  # plot all the lines from an element
            res = getmatch.getmatchesgammas_clicked(Ele)
            next_color = self.plot.canvas.axs[0]._get_lines.get_next_color()
            for match in res:
                rowres = [match['Element'], match['Energy'], match['Intensity'], match['lifetime']]
                for i in range(len(self.plot.canvas.axs)):
                    self.plot.canvas.axs[i].axvline(
                        float(rowres[1]), color=next_color, linestyle='--', label=str(Ele))


        if col == 1:  # plots just one transition
            res = getmatch.getmatchesgammastrans_clicked(Ele, En)
            for match in res:
                rowres = [match['Element'], match['Energy'], match['Intensity'], match['lifetime']]
                for i in range(len(self.plot.canvas.axs)):
                    self.plot.canvas.axs[i].axvline(
                        float(rowres[1]), color=self.plot.canvas.axs[i]._get_lines.get_next_color(), linestyle='--', label=Ele)


        # update figure
        self.update_legend()
        self.plot.canvas.draw()

        # increment number of lines in table
        self.numoflines += 1

        # update table
        self.clickpeaks.table_plotted_lines.setRowCount(self.numoflines)
        self.clickpeaks.table_plotted_lines.setItem(self.numoflines-1, 1, QTableWidgetItem(Ele))


    def clickpeaks_table_clickpeaks_sec(self, row, col):
        table = self.clickpeaks.table_muon_sec

        if table.item(row, col) is None:
            return

        Ele = table.item(row, 0).text()
        Trans = table.item(row, 1).text()

        if col == 0:  # plot all the lines from an element
            res = getmatch.get_matches_Element(Ele)
            next_color = self.plot.canvas.axs[0]._get_lines.get_next_color()
            for match in res:
                rowres = [match['element'], match['energy'], match['transition']]
                for i in range(len(self.plot.canvas.axs)):
                    self.plot.canvas.axs[i].axvline(
                        float(rowres[1]), color=next_color, linestyle='--', label=str(Ele))

        if col == 1:  # plots just one transition
            res = getmatch.get_matches_Trans(Ele, Trans)
            for match in res:
                rowres = [match['element'], match['energy'], match['transition']]
                for i in range(len(self.plot.canvas.axs)):
                    self.plot.canvas.axs[i].axvline(
                        float(rowres[1]), color=self.plot.canvas.axs[i]._get_lines.get_next_color(), linestyle='--', label=Ele)

        # update figure
        self.update_legend()
        self.plot.canvas.draw()

        # increment number of lines in table
        self.numoflines += 1

        # update table
        self.clickpeaks.table_plotted_lines.setRowCount(self.numoflines)
        self.clickpeaks.table_plotted_lines.setItem(self.numoflines - 1, 0, QTableWidgetItem(Ele))


    def clickpeaks_table_clickpeaks_prim(self, row, col):
        table = self.clickpeaks.table_muon_prim

        if table.item(row, col) is None:
            return

        Ele = table.item(row, 0).text()
        Trans = table.item(row, 1).text()

        if col == 0:  # plot all the lines from an element
            res = getmatch.get_matches_Element(Ele)
            next_color = self.plot.canvas.axs[0]._get_lines.get_next_color()
            for match in res:
                rowres = [match['element'], match['energy'], match['transition']]
                for i in range(len(self.plot.canvas.axs)):
                    self.plot.canvas.axs[i].axvline(
                        float(rowres[1]), color=next_color, linestyle='--', label=str(Ele))

        if col == 1:  # plots just one transition
            res = getmatch.get_matches_Trans(Ele, Trans)
            for match in res:
                rowres = [match['element'], match['energy'], match['transition']]
                for i in range(len(self.plot.canvas.axs)):
                    self.plot.canvas.axs[i].axvline(
                        float(rowres[1]), color=self.plot.canvas.axs[i]._get_lines.get_next_color(), linestyle='--', label=Ele)

        # update figure
        self.update_legend()
        self.plot.canvas.draw()

        # increment number of lines in table
        self.numoflines += 1

        # update table
        self.clickpeaks.table_plotted_lines.setRowCount(self.numoflines)
        self.clickpeaks.table_plotted_lines.setItem(self.numoflines - 1, 0, QTableWidgetItem(Ele))


    def clickpeaks_table_clickpeaks(self, row, col):
        table = self.clickpeaks.table_muon

        if table.item(row, col) is None:
            return

        Ele = table.item(row, 0).text()
        Trans = table.item(row, 1).text()

        if col == 0:  # plot all the lines from an element
            res = getmatch.get_matches_Element(Ele)
            next_color = self.plot.canvas.axs[0]._get_lines.get_next_color()
            for match in res:
                rowres = [match['element'], match['energy'], match['transition']]
                for i in range(len(self.plot.canvas.axs)):
                    self.plot.canvas.axs[i].axvline(
                        float(rowres[1]), color=next_color, linestyle='--', label=str(Ele))

        if col == 1:  # plots just one transition
            res = getmatch.get_matches_Trans(Ele, Trans)
            for match in res:
                rowres = [match['element'], match['energy'], match['transition']]
                for i in range(len(self.plot.canvas.axs)):
                    self.plot.canvas.axs[i].axvline(
                        float(rowres[1]), color=self.plot.canvas.axs[i]._get_lines.get_next_color(), linestyle='--', label=str(Ele))
        # update figure
        self.update_legend()
        self.plot.canvas.draw()

        # increment number of lines in table
        self.numoflines += 1

        # update table
        self.clickpeaks.table_plotted_lines.setRowCount(self.numoflines)
        self.clickpeaks.table_plotted_lines.setItem(self.numoflines - 1, 0, QTableWidgetItem(Ele))

    def useDef_onClicked(self):
        if self.findpeaks.useDef_checkbox.isChecked():
            print('checked')
            self.findpeaks.lineedit_FindPeak_Height.hide()
            self.findpeaks.lineedit_FindPeak_Thres.hide()
            self.findpeaks.lineedit_FindPeak_Dist.hide()
            self.findpeaks.label_FindPeak_Height.hide()
            self.findpeaks.label_FindPeak_Thres.hide()
            self.findpeaks.label_FindPeak_Dist.hide()

        else:
            print('not checked')
            self.findpeaks.lineedit_FindPeak_Height.show()
            self.findpeaks.lineedit_FindPeak_Thres.show()
            self.findpeaks.lineedit_FindPeak_Dist.show()
            self.findpeaks.label_FindPeak_Height.show()
            self.findpeaks.label_FindPeak_Thres.show()
            self.findpeaks.label_FindPeak_Dist.show()


    def find_peaks_automatically(self):
        app = get_app()
        data = app.loaded_run.data
        config = app.config

        if self.findpeaks.useDef_checkbox.isChecked():
            h=10
            t=15
            d=1
        else:
            h = float(self.findpeaks.lineedit_FindPeak_Height.text())
            t = float(self.findpeaks.lineedit_FindPeak_Thres.text())
            d = float(self.findpeaks.lineedit_FindPeak_Dist.text())
            #print(h,t,d)

        print(self.findpeaks.peakfindroutine.currentText())
        i = 0

        if self.findpeaks.peakfindroutine.currentText() == "find peaks (dev)":
            for dataset in data:
                if config.parser.getboolean(dataset.detector, "show_plot"):
                    peaks, peaks_pos = FindPeaks.Findpeak_with_bck_removed(dataset.x, dataset.y)
                    default_peaks = peaks[0]

                    default_sigma = [2.0] * len(default_peaks)
                    input_data = list(zip(default_peaks, default_sigma))
                    match_GE1, res_PM, res_SM = getmatch.get_matches(input_data)

                    Plot_Spectra.Plot_Peak_Location(self.plot.canvas.axs, peaks, dataset.x, i)
                    out = SortMatch.SortMatch(match_GE1)
                    self.findpeaks.table_peaks.setItem(i, 0, QTableWidgetItem(dataset.detector))
                    self.findpeaks.table_peaks.setItem(i, 1, QTableWidgetItem(str(dict(list(out.items())))))
                    # print('after table_peaks')
                    i += 1
                    self.plot.canvas.draw()

            """              
            if globals.plot_GE1:
                peaks_GE1, peak_pos_GE1 = FindPeaks.Findpeak_with_bck_removed(globals.x_GE1, globals.y_GE1)
                default_peaks = peaks_GE1[0]
                #print('dp', default_peaks)
                # default_peaks = peaks_GE1
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE1, res_PM, res_SM = getmatch.get_matches(input_data)

                Plot_Spectra.Plot_Peak_Location(self.plot.canvas.axs, peaks_GE1, globals.x_GE1, i)
                # Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, peak_pos_GE1, i)

                out = SortMatch.SortMatch(match_GE1)
                self.findpeaks.table_peaks.setItem(i, 0, QTableWidgetItem("Detector 1"))
                self.findpeaks.table_peaks.setItem(i, 1, QTableWidgetItem(str(dict(list(out.items())))))
                #print('after table_peaks')
                i += 1
                self.plot.canvas.draw()
        """
        if self.findpeaks.peakfindroutine.currentText() == "scipy.FindPeak":
            for dataset in data:
                if data is not None and config.parser.getboolean(dataset.detector, "show_plot"):
                    peaks, peaks_pos = FindPeaks.FindPeaks(dataset.x, dataset.y, h, t, d)
                    default_peaks = peaks[0]
                    # print('dp',default_peaks)
                    default_sigma = [2.0] * len(default_peaks)
                    input_data = list(zip(default_peaks, default_sigma))
                    match_GE1, res_PM, res_SM = getmatch.get_matches(input_data)

                    Plot_Spectra.Plot_Peak_Location(self.plot.canvas.axs, peaks, dataset.x, i)
                    # Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, globals.x_GE1,i)
                    # Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, peak_pos_GE1, i)

                    out = SortMatch.SortMatch(match_GE1)
                    self.findpeaks.table_peaks.setItem(i, 0, QTableWidgetItem(dataset.detector))
                    self.findpeaks.table_peaks.setItem(i, 1, QTableWidgetItem(str(dict(list(out.items())))))
                    # print('after table_peaks')
                    i += 1
            self.plot.canvas.draw()

        """
        if self.findpeaks.peakfindroutine.currentText() == "scipy.Find_Peak_Cwt":
            # Not working at the moment
            if globals.plot_GE1:
                peaks_GE1, peak_pos_GE1 = FindPeaks.FindPeaksCwt(globals.x_GE1, globals.y_GE1, h, t, d)

                default_peaks = peaks_GE1[0]

                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE1, res_PM, res_SM = getmatch.get_matches(input_data)

                Plot_Spectra.Plot_Peak_Location(self.plot.canvas.axs, peaks_GE1, globals.x_GE1, i)

                out = SortMatch.SortMatch(match_GE1)
                print('after out')
                self.findpeaks.table_peaks.setItem(i, 0, QTableWidgetItem("Detector 1"))
                self.findpeaks.table_peaks.setItem(i, 1, QTableWidgetItem(str(dict(list(out.items())))))
                print('after table_peaks')
                i += 1

            if globals.plot_GE2:
                peaks_GE2, peak_pos_GE2 = FindPeaks.FindPeaksCwt(globals.x_GE2, globals.y_GE2, h, t, d)
                default_peaks = peaks_GE2[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE2, res_PM, res_SM = getmatch.get_matches(input_data)
                Plot_Spectra.Plot_Peak_Location(self.plot.canvas.axs, peaks_GE2, globals.x_GE2, i)
                i+=1


            if globals.plot_GE3:
                peaks_GE3, peak_pos_GE3 = FindPeaks.FindPeaksCwt(globals.x_GE3, globals.y_GE3, h, t, d)
                default_peaks = peaks_GE3[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE3, res_PM, res_SM = getmatch.get_matches(input_data)
                Plot_Spectra.Plot_Peak_Location(self.plot.canvas.axs, peaks_GE3, globals.x_GE3, i)
                i += 1

            if globals.plot_GE4:
                peaks_GE4, peak_pos_GE4 = FindPeaks.FindPeaksCwt(globals.x_GE4, globals.y_GE4, h, t, d)
                default_peaks = peaks_GE4[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE4, res_PM, res_SM = getmatch.get_matches(input_data)
                Plot_Spectra.Plot_Peak_Location(self.plot.canvas.axs, peaks_GE4, globals.x_GE4, i)
                i+=1
    
            self.plot.canvas.draw()
        """


    def plot_spectra(self):
        run = get_app().loaded_run
        fig, axs = Plot_Spectra.plot_run(run)
        return PlotWidget(fig, axs)


    def on_click(self, event):
        print("here")
        if event.button is MouseButton.RIGHT:
            #Find possible gamma peaks
            x, y = event.xdata, event.ydata
            if event.inaxes:
                ax = event.inaxes  # the axes instance
                default_peaks = [event.xdata]
                print('disconnecting callback')
                #plt.disconnect(binding_id)
                print('start peak find', time.time())


                #default_peaks = [20.500]
                default_peaks = [event.xdata]

                # default_peaks = peaks_GE1
                default_sigma = [2.0] * len(default_peaks)

                self.clickpeaks.desc_gamma.setText('Possible Gamma transitions at '
                                                + "{:.1f}".format(default_peaks[0]) + ' +/- '
                                                + str(default_sigma[0]))

                input_data = list(zip(default_peaks, default_sigma))

                res = getmatch.getmatchesgammas(input_data)
                print('end peak find', time.time())
                if res == []:
                    self.clickpeaks.table_gamma.setItem(0, 0, QTableWidgetItem('No match'))
                else:
                    i = 0
                    for match in res:
                        row = [match['Element'], match['Energy'], match['diff'],
                               match['Intensity'], match['lifetime']]



                        self.clickpeaks.table_gamma.setItem(i, 0, QTableWidgetItem(row[0].strip()))
                        self.clickpeaks.table_gamma.setItem(i, 1, QTableWidgetItem(
                            str("{:.2f}".format(row[1])).strip()))

                        self.clickpeaks.table_gamma.setItem(i, 2, QTableWidgetItem(
                            str("{:.2f}".format(row[2])).strip()))
                        self.clickpeaks.table_gamma.setItem(i, 3, QTableWidgetItem(
                            "{:.2f}".format(100.0*float(row[3]))))
                        self.clickpeaks.table_gamma.setItem(i, 4, QTableWidgetItem(row[4]))

                        i += 1

                    self.clickpeaks.table_gamma.setRowCount(i)


        if event.button is MouseButton.LEFT:
            #find possible muonic X-ray peaks
            x, y = event.xdata, event.ydata
            if event.inaxes:
                ax = event.inaxes  # the axes instance
                default_peaks=[event.xdata]
                default_sigma = [0.5]*len(default_peaks)
                "{:.1f}".format(45.34531)
                self.clickpeaks.desc_muon.setText('Possible Muonic X-ray transitions at '
                                           + "{:.1f}".format(default_peaks[0]) +' +/- '
                                           + str(default_sigma[0]))
                input_data = list(zip(default_peaks, default_sigma))
                res, res_PM, res_SM = getmatch.get_matches(input_data)
                """
                print('res',res)
                print('res_PM',res_PM)
                print('res_SM',res_SM)
                """

                temp = res[0]
                i = 0
                self.clickpeaks.table_muon.setRowCount(len(res[0]))
                for match in temp:

                    row = [match['peak_centre'], match['energy'], match['element'],
                           match['transition'], match['error'], match['diff']]

                    self.clickpeaks.table_muon.setItem(i, 0, QTableWidgetItem(row[2]))
                    self.clickpeaks.table_muon.setItem(i, 1, QTableWidgetItem(row[3]))
                    self.clickpeaks.table_muon.setItem(i, 2, QTableWidgetItem("{:.2f}".format(row[5])))

                    i += 1

                self.clickpeaks.table_muon.setRowCount(i)

                temp = res_PM
                i = 0
                #print('res_PM',res_PM)
                if len(res_PM) != 0:
                    self.clickpeaks.table_muon_prim.setRowCount(len(res_PM))
                    for match in temp:

                        row_PM = [match['peak_centre'], match['energy'], match['element'],
                                  match['transition'], match['error'], match['diff']]

                        self.clickpeaks.table_muon_prim.setItem(i, 0, QTableWidgetItem(row_PM[2]))
                        self.clickpeaks.table_muon_prim.setItem(i, 1, QTableWidgetItem(row_PM[3]))
                        self.clickpeaks.table_muon_prim.setItem(i, 2, QTableWidgetItem("{:.2f}".format(row_PM[5])))

                        i += 1

                    self.clickpeaks.table_muon_prim.setRowCount(i)
                else:
                    self.clickpeaks.table_muon_prim.setRowCount(0)

                self.show()

                temp = res_SM
                i = 0
                if len(res_PM) != 0:

                    self.clickpeaks.table_muon_sec.setRowCount(len(res_SM))
                    for match in temp:

                        row = [match['peak_centre'], match['energy'], match['element'],
                               match['transition'], match['error'], match['diff']]


                        self.clickpeaks.table_muon_sec.setItem(i, 0, QTableWidgetItem(row[2]))
                        self.clickpeaks.table_muon_sec.setItem(i, 1, QTableWidgetItem(row[3]))
                        self.clickpeaks.table_muon_sec.setItem(i, 2, QTableWidgetItem("{:.2f}".format(row[5])))

                        i += 1

                    self.clickpeaks.table_muon_sec.setRowCount(i)
                    self.show()
                else:
                    self.clickpeaks.table_muon_sec.setRowCount(0)
                    self.show()

                    #self.show()
