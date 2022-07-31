import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from PyQt5.QtWidgets import (
    QCheckBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QComboBox,
)
import getmatch
import Plot_Spectra
import FindPeaks
import SortMatch
import time
import globals


class PlotWindow(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
        """

    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        # label = QLabel("Plot Window ", self)

        self.resize(1200, 1100)
        self.setMinimumSize(1200,1100)
        self.setWindowTitle("Plot Window ")

        self.layout = QVBoxLayout(self)
        self.temp = QLabel(self)



        # Initialize tab screen
        print('initialising tabs')
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(200, 500)
        self.tabs.move(500,500)

        # Add tabs
        self.tabs.addTab(self.tab1, "Peak Identification")
        self.tabs.addTab(self.tab2, "Element Search")

        # Create first tab

        self.tab1.label_Element = QLabel("Possible Muonic X-ray Transition:                                            "
                                         , self.tab1)
        self.tab1.label_Element.move(30, 10)
        self.tab1.label_Element.show()

        self.tab1.tab_clicked_elements = QTabWidget(self.tab1)
        self.tab1.tab1 = QWidget()
        self.tab1.tab2 = QWidget()
        self.tab1.tab3 = QWidget()
        self.tab1.tab4 = QWidget()
        self.tab1.tab_clicked_elements.move(50,50)
        self.tab1.tab_clicked_elements.setMinimumSize(1000,450)

        self.tab1.tab_clicked_elements.addTab(self.tab1.tab1, "All Peaks")
        self.tab1.tab_clicked_elements.addTab(self.tab1.tab2, "Primary")
        self.tab1.tab_clicked_elements.addTab(self.tab1.tab3, "Secondary")
        self.tab1.tab_clicked_elements.addTab(self.tab1.tab4, "Remove Plot lines")

        self.tab1.table_plotted_lines = QTableWidget(self.tab1.tab4)
        self.tab1.table_plotted_lines.setShowGrid(True)
        self.tab1.table_plotted_lines.setColumnCount(2)
        self.tab1.table_plotted_lines.setRowCount(10)
        self.tab1.table_plotted_lines.move(10,10)
        self.tab1.table_plotted_lines.setMinimumSize(1000, 350)
        self.tab1.table_plotted_lines.verticalScrollBar()
        #self.tab1.table_clickpeaks.
        self.tab1.table_plotted_lines.setHorizontalHeaderLabels(['Muonic X-ray', 'Gamma'])
        self.tab1.table_plotted_lines.setColumnWidth(0, 250)
        self.tab1.table_plotted_lines.setColumnWidth(1, 205)
        self.tab1.table_plotted_lines.cellClicked.connect(self.remove_line)


        self.tab1.table_plotted_lines.show()

        # table for all peaks

        self.tab1.table_clickpeaks = QTableWidget(self.tab1.tab1)
        self.tab1.table_clickpeaks.setShowGrid(True)
        self.tab1.table_clickpeaks.setColumnCount(3)
        self.tab1.table_clickpeaks.setRowCount(10)
        self.tab1.table_clickpeaks.move(10,10)
        self.tab1.table_clickpeaks.setMinimumSize(1000,350)
        self.tab1.table_clickpeaks.verticalScrollBar()
        #self.tab1.table_clickpeaks.
        self.tab1.table_clickpeaks.setHorizontalHeaderLabels(['Element', 'Transition', 'Error'])
        self.tab1.table_clickpeaks.setColumnWidth(0, 175)
        self.tab1.table_clickpeaks.setColumnWidth(1, 205)
        self.tab1.table_clickpeaks.setColumnWidth(2, 175)
        self.tab1.table_clickpeaks.cellClicked.connect(self.tab1_table_clickpeaks)



        self.tab1.table_clickpeaks.show()

        # table for primary peaks

        self.tab1.table_clickpeaks_prim = QTableWidget(self.tab1.tab2)
        self.tab1.table_clickpeaks_prim.setShowGrid(True)
        self.tab1.table_clickpeaks_prim.setColumnCount(3)
        self.tab1.table_clickpeaks_prim.setRowCount(10)
        self.tab1.table_clickpeaks_prim.move(10,10)
        self.tab1.table_clickpeaks_prim.setMinimumSize(1000,350)
        self.tab1.table_clickpeaks_prim.verticalScrollBar()
        #self.tab1.table_clickpeaks.
        self.tab1.table_clickpeaks_prim.setHorizontalHeaderLabels(['Element', 'Transition', 'Error'])
        self.tab1.table_clickpeaks_prim.setColumnWidth(0, 175)
        self.tab1.table_clickpeaks_prim.setColumnWidth(1, 205)
        self.tab1.table_clickpeaks_prim.setColumnWidth(2, 175)
        self.tab1.table_clickpeaks_prim.cellClicked.connect(self.tab1_table_clickpeaks_prim)

        self.tab1.table_clickpeaks_prim.show()

        # table for secondary peaks

        self.tab1.table_clickpeaks_sec = QTableWidget(self.tab1.tab3)
        self.tab1.table_clickpeaks_sec.setShowGrid(True)
        self.tab1.table_clickpeaks_sec.setColumnCount(3)
        self.tab1.table_clickpeaks_sec.setRowCount(10)
        self.tab1.table_clickpeaks_sec.move(10,10)
        self.tab1.table_clickpeaks_sec.setMinimumSize(1000,350)
        self.tab1.table_clickpeaks_sec.verticalScrollBar()
        #self.tab1.table_clickpeaks.
        self.tab1.table_clickpeaks_sec.setHorizontalHeaderLabels(['Element', 'Transition', 'Error'])
        self.tab1.table_clickpeaks_sec.setColumnWidth(0, 175)
        self.tab1.table_clickpeaks_sec.setColumnWidth(1, 205)
        self.tab1.table_clickpeaks_sec.setColumnWidth(2, 175)
        self.tab1.table_clickpeaks_sec.cellClicked.connect(self.tab1_table_clickpeaks_sec)


        self.tab1.table_clickpeaks_sec.show()





        self.tab1.label_Element2 = QLabel("Possible Gamma Transition:                                            "
                                         , self.tab1)
        self.tab1.label_Element2.move(30, 500)
        self.tab1.label_Element2.show()

        self.tab1.table_clickpeaks2 = QTableWidget(self.tab1)
        self.tab1.table_clickpeaks2.setShowGrid(True)
        self.tab1.table_clickpeaks2.setColumnCount(5)
        self.tab1.table_clickpeaks2.setRowCount(10)
        self.tab1.table_clickpeaks2.move(50, 570)
        self.tab1.table_clickpeaks2.setMinimumSize(1000, 350)
        # self.tab1.table_clickpeaks.
        self.tab1.table_clickpeaks2.setHorizontalHeaderLabels(['Element', 'Energy','Error', 'Intensity', 'Lifetime'])
        self.tab1.table_clickpeaks2.setColumnWidth(0, 175)
        self.tab1.table_clickpeaks2.setColumnWidth(1, 175)
        self.tab1.table_clickpeaks2.setColumnWidth(2, 175)
        self.tab1.table_clickpeaks2.setColumnWidth(3, 175)
        self.tab1.table_clickpeaks2.setColumnWidth(4, 175)
        self.tab1.table_clickpeaks2.cellClicked.connect(self.tab1_table_clickpeaks_gamma)

        #self.tab1.table_clickpeaks2.setFixedWidth(700)
        self.tab1.table_clickpeaks2.show()

        #self.tab1.setLayout(self.tab1.layout)

        print('setting up tab2')



        self.tab2.label_Element2 = QLabel("hello", self.tab2)
        self.tab2.label_Element2.move(70, 20)

        self.tab2.label_Element2.show()

        self.tab2.find_peaks_button = QPushButton("Find Peaks", self.tab2)
        self.tab2.find_peaks_button.move(70,70)
        self.tab2.find_peaks_button.show()
        self.tab2.find_peaks_button.clicked.connect(
            lambda: self.find_peaks_automatically())

        self.tab2.useDef_checkbox = QCheckBox("Use defaults",self.tab2)
        self.tab2.useDef_checkbox.move(70,160)
        self.tab2.useDef_checkbox.setChecked(True)
        self.tab2.useDef_checkbox.show()
        self.tab2.useDef_checkbox.toggled.connect(self.useDef_onClicked)

        self.tab2.peakfindroutine = QComboBox(self.tab2)
        self.tab2.peakfindroutine.move(330,70)
        self.tab2.peakfindroutine.addItem('scipy.FindPeak')
        self.tab2.peakfindroutine.addItem('scipy.Find_Peak_Cwt')
        self.tab2.peakfindroutine.addItem('find peaks (dev)')
        self.tab2.peakfindroutine.show()

        self.tab2.label_FindPeak_Height = QLabel("Height", self.tab2)
        self.tab2.label_FindPeak_Height.move(730, 70)
        self.tab2.label_FindPeak_Height.hide()

        self.tab2.lineedit_FindPeak_Height = QLineEdit("10", self.tab2)
        self.tab2.lineedit_FindPeak_Height.move(900, 70)
        self.tab2.lineedit_FindPeak_Height.hide()
        self.tab2.lineedit_FindPeak_Height.setFixedWidth(100)

        self.tab2.label_FindPeak_Thres = QLabel("Threshold", self.tab2)
        self.tab2.label_FindPeak_Thres.move(730, 120)
        self.tab2.label_FindPeak_Thres.hide()

        self.tab2.lineedit_FindPeak_Thres = QLineEdit("15", self.tab2)
        self.tab2.lineedit_FindPeak_Thres.move(900, 120)
        self.tab2.lineedit_FindPeak_Thres.setFixedWidth(100)
        self.tab2.lineedit_FindPeak_Thres.hide()

        self.tab2.label_FindPeak_Dist = QLabel("Distance", self.tab2)
        self.tab2.label_FindPeak_Dist.move(730, 170)
        self.tab2.label_FindPeak_Dist.hide()

        self.tab2.lineedit_FindPeak_Dist = QLineEdit("1", self.tab2)
        self.tab2.lineedit_FindPeak_Dist.move(900, 170)
        self.tab2.lineedit_FindPeak_Dist.setFixedWidth(100)
        self.tab2.lineedit_FindPeak_Dist.hide()

        self.tab2.tabs = QTabWidget(self.tab2)
        self.tab2.tab1 = QWidget()
        self.tab2.tab2 = QWidget()
        self.tab2.tab3 = QWidget()


        self.tab2.tabs.addTab(self.tab2.tab1, "Most Probable")

        self.tab2.table_peaks = QTableWidget(self.tab2.tab1)
        self.tab2.table_peaks.setShowGrid(True)
        self.tab2.table_peaks.setColumnCount(2)
        self.tab2.table_peaks.setRowCount(4)
        self.tab2.table_peaks.move(20,50)
        self.tab2.table_peaks.setMinimumSize(650,400)
        self.tab2.table_peaks.setHorizontalHeaderLabels(['Detector', 'Probable Elements'])
        self.tab2.table_peaks.setColumnWidth(1,420)
        self.tab2.table_peaks.verticalScrollBar()
        self.tab2.table_peaks.horizontalScrollBar()
        self.tab2.table_peaks.show()

        self.tab2.tabs.addTab(self.tab2.tab2, "Transitions")
        #self.tab2.tabs.addTab(self.tab2.tab3, "Secondary")

        self.tab2.tabs.move(50,220)
        self.tab2.tabs.resize(700,600)

        # Add tabs to widget

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.show()

        self.PlotSpectra()

        self.numoflines = 0
        self.linenum = []
        self.lines= []
        self.elementline = []

    def tab1_table_clickpeaks_gamma(self, row, col):

        try:
            print('in clickpeaks')
            print(row, col)
            # get Element
            Ele = self.tab1.table_clickpeaks2.item(row, 0).text()
            En = self.tab1.table_clickpeaks2.item(row, 1).text()

            print('Ele', Ele)

            if col == 0:  # plot all the lines from an element
                print('ere')
                # find all peaks for this element and plt vertical lines
                res = getmatch.getmatchesgammas_clicked(Ele)
                next_color = self.axs[0]._get_lines.get_next_color()
                print('res', res)
                for match in res:
                    print('match', match)
                    rowres = [match['Element'], match['Energy'], match['Intensity'],match['lifetime']]
                    print('rowres',rowres)
                    # print(len(self.axs))
                    for i in range(len(self.axs)):
                        # print(i)
                        self.axs[i].axvline(
                            float(rowres[1]), color=next_color, linestyle='--', label=str(Ele))

                self.tab1.table_plotted_lines.setItem(self.numoflines, 0, QTableWidgetItem(Ele))
                self.numoflines += 1
                print('self.numoflines', self.numoflines)

            if col == 1:  # plots just one transition
                res = getmatch.getmatchesgammastrans_clicked(Ele,En)
                #print('res',res)
                for match in res:
                    #print('match', match)
                    rowres = [match['Element'], match['Energy'], match['Intensity'],match['lifetime']]
                    #print('rowres', rowres)
                    #print('rowres[1]', rowres[1])
                    for i in range(len(self.axs)):
                        #print(i)
                        self.axs[i].axvline(
                            float(rowres[1]), color=self.axs[i]._get_lines.get_next_color(), linestyle='--', label=Ele)
                self.tab1.table_plotted_lines.setItem(self.numoflines, 0, QTableWidgetItem(Ele))
                self.numoflines += 1

            # add search for peaks in col 0
            # plot of one peak if col 1

            print()
            self.fig.canvas.draw()
        except:
            temp=1

        return

    def tab1_table_clickpeaks_sec(self, row, col):

        try:
            print('hello')
            print(row,col)
            # get Element
            Ele = self.tab1.table_clickpeaks_sec.item(row,0).text()
            Trans = self.tab1.table_clickpeaks_sec.item(row, 1).text()

            print('Ele', Ele)
            if col == 0: # plot all the lines from an element
                print('ere')
                # find all peaks for this element and plt vertical lines
                res = getmatch.get_matches_Element_PrimorSec(Ele,'Secondary')
                print('res',res)
                next_color = self.axs[0]._get_lines.get_next_color()
                for match in res:
                    print('match', match)
                    rowres = [match['element'], match['energy'], match['transition']]
                    #print('rowres[1]',rowres[1])
                    #print(len(self.axs))
                    for i in range(len(self.axs)):
                        #print(i)
                        self.axs[i].axvline(
                                float(rowres[1]), color=next_color, linestyle='--', label=Ele)


                self.tab1.table_plotted_lines.setItem(self.numoflines, 0, QTableWidgetItem(Ele))
                self.numoflines += 1
                print('self.numoflines', self.numoflines)


            if col == 1: # plots just one transition
                res = getmatch.get_matches_Trans(Ele,Trans)
                print(res)
                for match in res:
                    print('match', match)
                    rowres = [match['element'], match['energy'], match['transition']]
                    print('rowres[1]',rowres[1])
                    for i in range(len(self.axs)):
                        print(i)
                        self.axs[i].axvline(
                            float(rowres[1]), color=self.axs[i]._get_lines.get_next_color(), linestyle='--', label = Ele)
                self.tab1.table_plotted_lines.setItem(self.numoflines, 0, QTableWidgetItem(Ele))
                self.numoflines += 1

            # add search for peaks in col 0
            # plot of one peak if col 1

            print()
            self.fig.canvas.draw()
        except:
            temp = 1
        return



    def tab1_table_clickpeaks_prim(self, row, col):
        try:

            print('hello')
            print(row,col)
            # get Element
            Ele = self.tab1.table_clickpeaks_prim.item(row,0).text()
            Trans = self.tab1.table_clickpeaks_prim.item(row, 1).text()

            print('Ele', Ele)
            if col == 0: # plot all the lines from an element
                print('ere')
                # find all peaks for this element and plt vertical lines
                res = getmatch.get_matches_Element_PrimorSec(Ele,'Primary')
                print('res',res)
                for match in res:
                    print('match', match)
                    rowres = [match['element'], match['energy'], match['transition']]
                    next_color = self.axs[0]._get_lines.get_next_color()
                    #print('rowres[1]',rowres[1])
                    #print(len(self.axs))
                    for i in range(len(self.axs)):
                        #print(i)
                        self.axs[i].axvline(
                                float(rowres[1]), color=next_color, linestyle='--', label=Ele)


                self.tab1.table_plotted_lines.setItem(self.numoflines, 0, QTableWidgetItem(Ele))
                self.numoflines += 1
                print('self.numoflines', self.numoflines)


            if col == 1: # plots just one transition
                res = getmatch.get_matches_Trans(Ele,Trans)
                print(res)
                for match in res:
                    print('match', match)
                    rowres = [match['element'], match['energy'], match['transition']]
                    print('rowres[1]',rowres[1])
                    for i in range(len(self.axs)):
                        print(i)
                        self.axs[i].axvline(
                            float(rowres[1]), color=self.axs[i]._get_lines.get_next_color(), linestyle='--', label= Ele)
                self.tab1.table_plotted_lines.setItem(self.numoflines, 0, QTableWidgetItem(Ele))
                self.numoflines += 1

            # add search for peaks in col 0
            # plot of one peak if col 1

            print()
            self.fig.canvas.draw()
        except:
            temp = 1
        return



    def remove_line(self, row, col):
        try:
            print('row col', row, col)

            Ele = self.tab1.table_plotted_lines.item(row,col).text()
            print('Ele', Ele)
            print('0',len(self.axs[0].lines))
            print('1',len(self.axs[1].lines))

            for i in range(len(self.axs)):
                #print(i)
                line = [line for line in self.axs[i].lines if line.get_label() == Ele]

                #print(line)
                for j in range(len(line)):
                    self.axs[i].lines.remove(line[j])
                self.fig.canvas.draw()
            print('0',len(self.axs[0].lines))
            print('1',len(self.axs[1].lines))
        except:
            temp=1
        return


    def tab1_table_clickpeaks(self, row, col):
        try:
            print('hello')
            print(row,col)
            # get Element
            Ele = self.tab1.table_clickpeaks.item(row,0).text()
            Trans = self.tab1.table_clickpeaks.item(row, 1).text()

            print('Ele', Ele)
            if col == 0: # plot all the lines from an element
                # find all peaks for this element and plt vertical lines
                res = getmatch.get_matches_Element(Ele)
                #print('res',res)
                next_color = self.axs[0]._get_lines.get_next_color()
                for match in res:
                    #print('match', match)
                    rowres = [match['element'], match['energy'], match['transition']]
                    #print('rowres[1]',rowres[1])
                    #print(len(self.axs))
                    for i in range(len(self.axs)):
                        #print(i)
                        self.axs[i].axvline(
                                float(rowres[1]), color=next_color, linestyle='--', label=Ele)


                self.tab1.table_plotted_lines.setItem(self.numoflines, 0, QTableWidgetItem(Ele))
                self.numoflines += 1
                print('self.numoflines', self.numoflines)
                self.plt.legend()

            if col == 1: # plots just one transition
                res = getmatch.get_matches_Trans(Ele,Trans)
                print(res)
                for match in res:
                    print('match', match)
                    rowres = [match['element'], match['energy'], match['transition']]
                    print('rowres[1]',rowres[1])
                    for i in range(len(self.axs)):
                        print(i)
                        self.axs[i].axvline(
                            float(rowres[1]), color=self.axs[i]._get_lines.get_next_color(), linestyle='--', label=Ele)
                self.tab1.table_plotted_lines.setItem(self.numoflines, 0, QTableWidgetItem(Ele))
                self.numoflines += 1

            # add search for peaks in col 0
            # plot of one peak if col 1

            print()
            self.fig.canvas.draw()
        except:
            temp = 1
        return


    def useDef_onClicked(self):
        print('hello ')
        if self.tab2.useDef_checkbox.isChecked():
            print('checked')
            self.tab2.lineedit_FindPeak_Height.hide()
            self.tab2.lineedit_FindPeak_Thres.hide()
            self.tab2.lineedit_FindPeak_Dist.hide()
            self.tab2.label_FindPeak_Height.hide()
            self.tab2.label_FindPeak_Thres.hide()
            self.tab2.label_FindPeak_Dist.hide()

        else:
            print('not checked')
            self.tab2.lineedit_FindPeak_Height.show()
            self.tab2.lineedit_FindPeak_Thres.show()
            self.tab2.lineedit_FindPeak_Dist.show()
            self.tab2.label_FindPeak_Height.show()
            self.tab2.label_FindPeak_Thres.show()
            self.tab2.label_FindPeak_Dist.show()


    def closeEvent(self, event):
        event.ignore()

    def find_peaks_automatically(self):
        whichpeakfindroute = self.tab2.peakfindroutine.currentText()
        figpeak, axspeak, pltpeak = Plot_Spectra.Plot_Spectra3(globals.x_GE1, globals.y_GE1,
                                                   globals.x_GE2, globals.y_GE2,
                                                   globals.x_GE3, globals.y_GE3,
                                                   globals.x_GE4, globals.y_GE4, "Automatic peak finding")
        i = 0

        if self.tab2.useDef_checkbox.isChecked():
            h=10
            t=15
            d=1
        else:
            h = float(self.tab2.lineedit_FindPeak_Height.text())
            t = float(self.tab2.lineedit_FindPeak_Thres.text())
            d = float(self.tab2.lineedit_FindPeak_Dist.text())
            #print(h,t,d)

        print(self.tab2.peakfindroutine.currentText())

        if self.tab2.peakfindroutine.currentText() == "find peaks (dev)":
            if globals.plot_GE1:
                peaks_GE1, peak_pos_GE1 = FindPeaks.Findpeak_with_bck_removed(globals.x_GE1,globals.y_GE1)
                default_peaks = peaks_GE1[0]
                print('dp', default_peaks)
                # default_peaks = peaks_GE1
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE1, res_PM, res_SM = getmatch.get_matches(input_data)

                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, globals.x_GE1, i)
                # Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, peak_pos_GE1, i)

                out = SortMatch.SortMatch(match_GE1)
                self.tab2.table_peaks.setItem(i, 0, QTableWidgetItem("Detector 1"))
                self.tab2.table_peaks.setItem(i, 1, QTableWidgetItem(str(dict(list(out.items())))))
                #print('after table_peaks')
                i += 1

        if self.tab2.peakfindroutine.currentText() == "scipy.FindPeak":

            if globals.plot_GE1:
                peaks_GE1, peak_pos_GE1 = FindPeaks.FindPeaks(globals.x_GE1,globals.y_GE1,h,t,d)

                default_peaks = peaks_GE1[0]
                print('dp',default_peaks)
                #default_peaks = peaks_GE1
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE1, res_PM, res_SM = getmatch.get_matches(input_data)


                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, globals.x_GE1,i)
                #Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, peak_pos_GE1, i)

                out = SortMatch.SortMatch(match_GE1)
                self.tab2.table_peaks.setItem(i, 0, QTableWidgetItem("Detector 1"))
                self.tab2.table_peaks.setItem(i, 1, QTableWidgetItem(str(dict(list(out.items())))))
                #print('after table_peaks')
                i += 1

            if globals.plot_GE2:
                peaks_GE2, peak_pos_GE2 = FindPeaks.FindPeaks(globals.x_GE2,globals.y_GE2,h,t,d)
                default_peaks = peaks_GE2[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE2, res_PM, res_SM = getmatch.get_matches(input_data)
                print('match_GE2', match_GE2)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE2, globals.x_GE2,i)
                i += 1


            if globals.plot_GE3:
                peaks_GE3, peak_pos_GE3 = FindPeaks.FindPeaks(globals.x_GE3,globals.y_GE3,h,t,d)
                default_peaks = peaks_GE3[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE3, res_PM, res_SM = getmatch.get_matches(input_data)
                print('match_GE3',match_GE3)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE3, globals.x_GE3,i)
                i += 1

            if globals.plot_GE4:
                peaks_GE4, peak_pos_GE4 = FindPeaks.FindPeaks(globals.x_GE4,globals.y_GE4,h,t,d)
                default_peaks = peaks_GE4[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE4, res_PM, res_SM = getmatch.get_matches(input_data)
                print('match_GE4',match_GE4)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE4, globals.x_GE4,i)
                i += 1

            pltpeak.show()

        if self.tab2.peakfindroutine.currentText() == "scipy.Find_Peak_Cwt":
            if globals.plot_GE1:
                peaks_GE1, peak_pos_GE1 = FindPeaks.FindPeaksCwt(globals.x_GE1,globals.y_GE1,h,t,d)

                default_peaks = peaks_GE1[0]
                #print('dpcwt',default_peaks)
                #default_peaks = peaks_GE1
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE1, res_PM, res_SM = getmatch.get_matches(input_data)

                #print('after match')


                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, globals.x_GE1,i)
                #Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, peak_pos_GE1, i)
                #print('here')

                out = SortMatch.SortMatch(match_GE1)
                print('after out')
                self.tab2.table_peaks.setItem(i, 0, QTableWidgetItem("Detector 1"))
                self.tab2.table_peaks.setItem(i, 1, QTableWidgetItem(str(dict(list(out.items())))))
                print('after table_peaks')
                i += 1

            if globals.plot_GE2:
                peaks_GE2, peak_pos_GE2 = FindPeaks.FindPeaksCwt(globals.x_GE2,globals.y_GE2,h,t,d)
                default_peaks = peaks_GE2[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE2, res_PM, res_SM = getmatch.get_matches(input_data)
                print('match_GE2', match_GE2)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE2, globals.x_GE2,i)
                i+=1


            if globals.plot_GE3:
                peaks_GE3, peak_pos_GE3 = FindPeaks.FindPeaksCwt(globals.x_GE3,globals.y_GE3,h,t,d)
                default_peaks = peaks_GE3[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE3, res_PM, res_SM = getmatch.get_matches(input_data)
                print('match_GE3',match_GE3)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE3, globals.x_GE3,i)
                i += 1

            if globals.plot_GE4:
                peaks_GE4, peak_pos_GE4 = FindPeaks.FindPeaksCwt(globals.x_GE4,globals.y_GE4,h,t,d)
                default_peaks = peaks_GE4[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE4, res_PM, res_SM = getmatch.get_matches(input_data)
                print('match_GE4',match_GE4)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE4, globals.x_GE4,i)
                i+=1

            pltpeak.show()


    def PlotSpectra(self):


        if globals.Normalise_do_not:
            self.fig,self.axs,self.plt = Plot_Spectra.Plot_Spectra3(globals.x_GE1, globals.y_GE1,
                                       globals.x_GE2, globals.y_GE2,
                                       globals.x_GE3, globals.y_GE3,
                                       globals.x_GE4, globals.y_GE4,
                                                     "Plot of Data: "+str(globals.RunNum))
            plt.show()
        elif globals.Normalise_counts:
            self.fig,self.axs,self.plt = Plot_Spectra.Plot_Spectra3(globals.x_GE1_Ncounts, globals.y_GE1_Ncounts,
                                       globals.x_GE2_Ncounts, globals.y_GE2_Ncounts,
                                       globals.x_GE3_Ncounts, globals.y_GE3_Ncounts,
                                       globals.x_GE4_Ncounts, globals.y_GE4_Ncounts,
                                                     "Plot of Data: "+str(globals.RunNum))
            plt.show()
        elif globals.Normalise_spill:
            self.fig,self.axs,self.plt = Plot_Spectra.Plot_Spectra3(globals.x_GE1_NEvents, globals.y_GE1_NEvents,
                                       globals.x_GE2_NEvents, globals.y_GE2_NEvents,
                                       globals.x_GE3_NEvents, globals.y_GE3_NEvents,
                                       globals.x_GE4_NEvents, globals.y_GE4_NEvents,
                                                     "Plot of Data: "+ str(globals.RunNum))
            plt.show()
        print('axs', len(self.axs))

        def on_click(event):

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

                    self.tab1.label_Element2.setText('Possible transitions at '
                                                    + "{:.1f}".format(default_peaks[0]) + ' +/- '
                                                    + str(default_sigma[0]))

                    input_data = list(zip(default_peaks, default_sigma))

                    res = getmatch.getmatchesgammas(input_data)
                    print('end peak find', time.time())
                    print(res)
                    if res == []:
                        self.tab1.table_clickpeaks2.setItem(0, 0, QTableWidgetItem('No match'))
                    else:
                        i = 0
                        for match in res:
                            row = [match['Element'], match['Energy'], match['diff'],
                                   match['Intensity'], match['lifetime']]



                            self.tab1.table_clickpeaks2.setItem(i, 0, QTableWidgetItem(row[0].strip()))
                            self.tab1.table_clickpeaks2.setItem(i, 1, QTableWidgetItem(
                                str("{:.2f}".format(row[1])).strip()))

                            self.tab1.table_clickpeaks2.setItem(i, 2, QTableWidgetItem(
                                str("{:.2f}".format(row[2])).strip()))
                            self.tab1.table_clickpeaks2.setItem(i, 3, QTableWidgetItem(
                                "{:.2f}".format(100.0*float(row[3]))))
                            self.tab1.table_clickpeaks2.setItem(i, 4, QTableWidgetItem(row[4]))

                            i += 1

                        self.tab1.table_clickpeaks2.setRowCount(i)


            if event.button is MouseButton.LEFT:
                #find possible muonic X-ray peaks
                x, y = event.xdata, event.ydata
                if event.inaxes:
                    ax = event.inaxes  # the axes instance
                    default_peaks=[event.xdata]
                    default_sigma = [0.5]*len(default_peaks)
                    "{:.1f}".format(45.34531)
                    self.tab1.label_Element.setText('Possible transitions at '
                                               + "{:.1f}".format(default_peaks[0]) +' +/- '
                                               + str(default_sigma[0]))
                    input_data = list(zip(default_peaks, default_sigma))
                    res, res_PM, res_SM = getmatch.get_matches(input_data)
                    print('res',res)
                    print('res_PM',res_PM)
                    print('res_SM',res_SM)

                    temp = res[0]
                    i = 0
                    self.tab1.table_clickpeaks.setRowCount(len(res[0]))
                    for match in temp:

                        row = [match['peak_centre'], match['energy'], match['element'],
                               match['transition'], match['error'], match['diff']]

                        self.tab1.table_clickpeaks.setItem(i, 0, QTableWidgetItem(row[2]))
                        self.tab1.table_clickpeaks.setItem(i, 1, QTableWidgetItem(row[3]))
                        self.tab1.table_clickpeaks.setItem(i, 2, QTableWidgetItem("{:.2f}".format(row[5])))

                        i += 1

                    self.tab1.table_clickpeaks.setRowCount(i)

                    temp = res_PM
                    i = 0
                    print('res_PM',res_PM)
                    if len(res_PM) != 0:
                        self.tab1.table_clickpeaks_prim.setRowCount(len(res_PM))

                        print('temp prim', temp)

                        for match in temp:

                            row_PM = [match['peak_centre'], match['energy'], match['element'],
                                      match['transition'], match['error'], match['diff']]

                            self.tab1.table_clickpeaks_prim.setItem(i, 0, QTableWidgetItem(row_PM[2]))
                            self.tab1.table_clickpeaks_prim.setItem(i, 1, QTableWidgetItem(row_PM[3]))
                            self.tab1.table_clickpeaks_prim.setItem(i, 2, QTableWidgetItem("{:.2f}".format(row_PM[5])))

                            i += 1

                        self.tab1.table_clickpeaks_prim.setRowCount(i)
                    else:
                        self.tab1.table_clickpeaks_prim.setRowCount(0)

                    self.show()

                    temp = res_SM
                    i = 0
                    print(len(res_SM))
                    if len(res_PM) != 0:

                        self.tab1.table_clickpeaks_sec.setRowCount(len(res_SM))
                        for match in temp:

                            row = [match['peak_centre'], match['energy'], match['element'],
                                   match['transition'], match['error'], match['diff']]


                            self.tab1.table_clickpeaks_sec.setItem(i, 0, QTableWidgetItem(row[2]))
                            self.tab1.table_clickpeaks_sec.setItem(i, 1, QTableWidgetItem(row[3]))
                            self.tab1.table_clickpeaks_sec.setItem(i, 2, QTableWidgetItem("{:.2f}".format(row[5])))

                            i += 1

                        self.tab1.table_clickpeaks_sec.setRowCount(i)
                        self.show()
                    else:
                        self.tab1.table_clickpeaks_sec.setRowCount(0)
                        self.show()

                    self.show()

        plt.connect('button_press_event', on_click)
