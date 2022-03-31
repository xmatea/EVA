import time

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QMenuBar,
    QMenu,
    QHBoxLayout,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QComboBox,
    QGridLayout,
)
from PyQt5.QtGui import QPalette, QColor, QCloseEvent
import sys
import loaddata
import loadcomment
import globals
import getmatch
import loadsettings as ls
import Plot_Spectra
import FindPeaks
import SortMatch

import LoadDatabaseFile as ldf
import loadgamma as lg


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class Correction_E(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
        """

    def __init__(self, parent = None):
        super(Correction_E,self).__init__(parent)
        #label = QLabel("Energy Correction ", self)

        self.resize(800, 500)
        self.setMinimumSize(800, 500)
        self.setWindowTitle("Energy Correction ")

        # setting up buttons
        self.save_GE1_Esettings = QPushButton("Save Detector 1")
        self.save_GE1_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('GE1', LE_GE1_off.text(), LE_GE1_grad.text()))
        self.save_GE2_Esettings = QPushButton("Save Detector 2")
        self.save_GE2_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('GE2', LE_GE2_off.text(), LE_GE2_grad.text()))
        self.save_GE3_Esettings = QPushButton("Save Detector 3")
        self.save_GE3_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('GE3', LE_GE3_off.text(), LE_GE3_grad.text()))
        self.save_GE4_Esettings = QPushButton("Save Detector 4")
        self.save_GE4_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('GE4', LE_GE4_off.text(), LE_GE4_grad.text()))
        self.save_All_Esettings = QPushButton("Save Detector 4")
        self.save_All_Esettings.clicked.connect(
            lambda: self.save_GE_E_settings('All'))

        # Setting up Checkboxes
        GE1_apply = QCheckBox()
        GE1_apply.setChecked(globals.E_Corr_GE1_apply)
        #GE1_apply.text('GE1')
        GE1_apply.stateChanged.connect(lambda: self.set_E_corr_apply('GE1', GE1_apply))
        GE2_apply = QCheckBox()
        GE2_apply.setChecked(globals.E_Corr_GE2_apply)
        GE2_apply.stateChanged.connect(lambda: self.set_E_corr_apply('GE2', GE2_apply))
        GE3_apply = QCheckBox()
        GE3_apply.setChecked(globals.E_Corr_GE3_apply)
        GE3_apply.stateChanged.connect(lambda: self.set_E_corr_apply('GE3', GE3_apply))
        GE4_apply = QCheckBox()
        GE4_apply.setChecked(globals.E_Corr_GE4_apply)
        GE4_apply.stateChanged.connect(lambda: self.set_E_corr_apply('GE4', GE4_apply))

        # Setting up Line edits
        LE_GE1_off = QLineEdit(str(globals.E_Corr_GE1_offset))
        LE_GE1_grad = QLineEdit(str(globals.E_Corr_GE1_gradient))
        LE_GE2_off = QLineEdit(str(globals.E_Corr_GE2_offset))
        LE_GE2_grad = QLineEdit(str(globals.E_Corr_GE2_gradient))
        LE_GE3_off = QLineEdit(str(globals.E_Corr_GE3_offset))
        LE_GE3_grad = QLineEdit(str(globals.E_Corr_GE3_gradient))
        LE_GE4_off = QLineEdit(str(globals.E_Corr_GE4_offset))
        LE_GE4_grad = QLineEdit(str(globals.E_Corr_GE4_gradient))



        self.layout = QGridLayout()
        self.layout.addWidget(QLabel('Detector 1'), 1, 0)
        self.layout.addWidget(QLabel('Detector 2'), 2, 0)
        self.layout.addWidget(QLabel('Detector 3'), 3, 0)
        self.layout.addWidget(QLabel('Detector 4'), 4, 0)
        self.layout.addWidget(QLabel("Offset"), 0, 1)
        self.layout.addWidget(QLabel("Gradient"), 0, 2)
        self.layout.addWidget(LE_GE1_off, 1, 1)
        self.layout.addWidget(LE_GE1_grad, 1, 2)
        self.layout.addWidget(LE_GE2_off, 2, 1)
        self.layout.addWidget(LE_GE2_grad, 2, 2)
        self.layout.addWidget(LE_GE3_off, 3, 1)
        self.layout.addWidget(LE_GE3_grad, 3, 2)
        self.layout.addWidget(LE_GE4_off, 4, 1)
        self.layout.addWidget(LE_GE4_grad, 4, 2)
        self.layout.addWidget(GE1_apply, 1, 3)
        self.layout.addWidget(GE2_apply, 2, 3)
        self.layout.addWidget(GE3_apply, 3, 3)
        self.layout.addWidget(GE4_apply, 4, 3)

        self.layout.addWidget(self.save_GE1_Esettings, 1, 4)
        self.layout.addWidget(self.save_GE2_Esettings, 2, 4)
        self.layout.addWidget(self.save_GE3_Esettings, 3, 4)
        self.layout.addWidget(self.save_GE4_Esettings, 4, 4)

        self.setLayout(self.layout)
        self.show()

    def save_GE_E_settings(self, det, off, grad):

        if det == 'GE1':
            globals.E_Corr_GE1_offset = off
            globals.E_Corr_GE1_gradient = grad
        if det == 'GE2':
            globals.E_Corr_GE2_offset = off
            globals.E_Corr_GE2_gradient = grad
        if det == 'GE3':
            globals.E_Corr_GE3_offset = off
            globals.E_Corr_GE3_gradient = grad
        if det == 'GE4':
            globals.E_Corr_GE4_offset = off
            globals.E_Corr_GE4_gradient = grad

    def closeEvent(self, event):
        #close window cleanly
        globals.we = None
        return None

    def set_E_corr_apply(self, det,checkbox):

        if det == 'GE1':
            globals.E_Corr_GE1_apply = checkbox.isChecked()
        if det == 'GE2':
            globals.E_Corr_GE2_apply = checkbox.isChecked()
        if det == 'GE3':
            globals.E_Corr_GE3_apply = checkbox.isChecked()
        if det == 'GE4':
            globals.E_Corr_GE4_apply = checkbox.isChecked()


class PlotWindow(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
        """

    def __init__(self, parent = None):
        super(PlotWindow,self).__init__(parent)
        #label = QLabel("Plot Window ", self)

        self.resize(500, 1100)
        self.setMinimumSize(500,1100)
        self.setWindowTitle("Plot Window ")

        self.layout = QVBoxLayout(self)
        self.temp = QLabel(self)



        # Initialize tab screen
        print('initialising tabs')
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(200, 300)
        self.tabs.move(500,500)

        # Add tabs
        self.tabs.addTab(self.tab1, "Peak Identification")
        self.tabs.addTab(self.tab2, "Element Search")

        # Create first tab

        self.tab1.label_Element = QLabel("Possible Muonic X-ray Transition:                                            "
                                         , self.tab1)
        self.tab1.label_Element.move(30, 50)
        self.tab1.label_Element.show()

        self.tab1.table_clickpeaks = QTableWidget(self.tab1)
        self.tab1.table_clickpeaks.setShowGrid(True)
        self.tab1.table_clickpeaks.setColumnCount(3)
        self.tab1.table_clickpeaks.setRowCount(10)
        self.tab1.table_clickpeaks.move(50,120)
        self.tab1.table_clickpeaks.setMinimumSize(700,350)
        #self.tab1.table_clickpeaks.
        self.tab1.table_clickpeaks.setHorizontalHeaderLabels(['Element', 'Transition', 'Error'])
        self.tab1.table_clickpeaks.setColumnWidth(0, 150)
        self.tab1.table_clickpeaks.setColumnWidth(1, 150)
        self.tab1.table_clickpeaks.setColumnWidth(2, 150)

        #self.tab1.table_clickpeaks.setFixedWidth(700)
        self.tab1.table_clickpeaks.show()

        self.tab1.label_Element2 = QLabel("Possible Gamma Transition:                                            "
                                         , self.tab1)
        self.tab1.label_Element2.move(30, 500)
        self.tab1.label_Element2.show()

        self.tab1.table_clickpeaks2 = QTableWidget(self.tab1)
        self.tab1.table_clickpeaks2.setShowGrid(True)
        self.tab1.table_clickpeaks2.setColumnCount(4)
        self.tab1.table_clickpeaks2.setRowCount(10)
        self.tab1.table_clickpeaks2.move(50, 570)
        self.tab1.table_clickpeaks2.setMinimumSize(700, 350)
        # self.tab1.table_clickpeaks.
        self.tab1.table_clickpeaks2.setHorizontalHeaderLabels(['Element', 'Error', 'Intensity', 'Lifetime'])
        self.tab1.table_clickpeaks2.setColumnWidth(0, 150)
        self.tab1.table_clickpeaks2.setColumnWidth(1, 150)
        self.tab1.table_clickpeaks2.setColumnWidth(2, 150)

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

        '''self.tab2.id_peaks_button = QPushButton("Find Peaks", self.tab2)
        self.tab2.id_peaks_button.move(70,70)
        self.tab2.id_peaks_button.show()
        self.tab2.id_peaks_button.clicked.connect(lambda: self.id_peaks())'''



        self.tab2.useDef_checkbox = QCheckBox("Use defaults",self.tab2)
        self.tab2.useDef_checkbox.move(70,160)
        self.tab2.useDef_checkbox.setChecked(True)
        self.tab2.useDef_checkbox.show()
        self.tab2.useDef_checkbox.toggled.connect(self.useDef_onClicked)


        self.tab2.peakfindroutine = QComboBox(self.tab2)
        self.tab2.peakfindroutine.move(330,70)
        self.tab2.peakfindroutine.addItem('scipy.FindPeak')
        self.tab2.peakfindroutine.addItem('scipy.Find_Peak_Cwt')
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
        #self.tab2.table_peaks.setFixedWidth(700)
        self.tab2.table_peaks.verticalScrollBar()
        self.tab2.table_peaks.horizontalScrollBar()
        self.tab2.table_peaks.show()

        self.tab2.tabs.addTab(self.tab2.tab2, "Transitions")
        #self.tab2.tabs.addTab(self.tab2.tab3, "Secondary")

        self.tab2.tabs.move(50,220)
        self.tab2.tabs.resize(700,600)



        # Add tabs to widget
        #self.layout.addWidget(self.temp)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


        self.show()

        self.PlotSpectra()

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
                                                   globals.x_GE4, globals.y_GE4)
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

        if self.tab2.peakfindroutine.currentText() == "scipy.FindPeak":

            if globals.plot_GE1:
                peaks_GE1, peak_pos_GE1 = FindPeaks.FindPeaks(globals.x_GE1,globals.y_GE1,h,t,d)

                default_peaks = peaks_GE1[0]
                print('dp',default_peaks)
                #default_peaks = peaks_GE1
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE1 = getmatch.get_matches(input_data)


                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, globals.x_GE1,i)
                #Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, peak_pos_GE1, i)

                out = SortMatch.SortMatch(match_GE1)
                self.tab2.table_peaks.setItem(i, 0, QTableWidgetItem("Detector 1"))
                self.tab2.table_peaks.setItem(i, 1, QTableWidgetItem(str(dict(list(out.items())))))
                print('after table_peaks')
                i += 1

            if globals.plot_GE2:
                peaks_GE2, peak_pos_GE2 = FindPeaks.FindPeaks(globals.x_GE2,globals.y_GE2,h,t,d)
                default_peaks = peaks_GE2[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE2 = getmatch.get_matches(input_data)
                print('match_GE2', match_GE2)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE2, globals.x_GE2,i)
                i+=1


            if globals.plot_GE3:
                peaks_GE3, peak_pos_GE3 = FindPeaks.FindPeaks(globals.x_GE3,globals.y_GE3,h,t,d)
                default_peaks = peaks_GE3[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE3 = getmatch.get_matches(input_data)
                print('match_GE3',match_GE3)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE3, globals.x_GE3,i)
                i+=1

            if globals.plot_GE4:
                peaks_GE4, peak_pos_GE4 = FindPeaks.FindPeaks(globals.x_GE4,globals.y_GE4,h,t,d)
                default_peaks = peaks_GE4[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE4 = getmatch.get_matches(input_data)
                print('match_GE4',match_GE4)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE4, globals.x_GE4,i)
                i+=1

            pltpeak.show()

        if self.tab2.peakfindroutine.currentText() == "scipy.Find_Peak_Cwt":
            if globals.plot_GE1:
                peaks_GE1, peak_pos_GE1 = FindPeaks.FindPeaksCwt(globals.x_GE1,globals.y_GE1,h,t,d)

                default_peaks = peaks_GE1[0]
                print('dpcwt',default_peaks)
                #default_peaks = peaks_GE1
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE1 = getmatch.get_matches(input_data)

                print('after match')


                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, globals.x_GE1,i)
                #Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE1, peak_pos_GE1, i)
                print('here')

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
                match_GE2 = getmatch.get_matches(input_data)
                print('match_GE2', match_GE2)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE2, globals.x_GE2,i)
                i+=1


            if globals.plot_GE3:
                peaks_GE3, peak_pos_GE3 = FindPeaks.FindPeaksCwt(globals.x_GE3,globals.y_GE3,h,t,d)
                default_peaks = peaks_GE3[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE3 = getmatch.get_matches(input_data)
                print('match_GE3',match_GE3)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE3, globals.x_GE3,i)
                i+=1

            if globals.plot_GE4:
                peaks_GE4, peak_pos_GE4 = FindPeaks.FindPeaksCwt(globals.x_GE4,globals.y_GE4,h,t,d)
                default_peaks = peaks_GE4[0]
                default_sigma = [2.0] * len(default_peaks)
                input_data = list(zip(default_peaks, default_sigma))
                match_GE4 = getmatch.get_matches(input_data)
                print('match_GE4',match_GE4)
                Plot_Spectra.Plot_Peak_Location(figpeak, axspeak, pltpeak, peaks_GE4, globals.x_GE4,i)
                i+=1

            pltpeak.show()


    def PlotSpectra(self):


        if globals.Normalise_do_not:
            fig,axs,plt = Plot_Spectra.Plot_Spectra3(globals.x_GE1, globals.y_GE1,
                                       globals.x_GE2, globals.y_GE2,
                                       globals.x_GE3, globals.y_GE3,
                                       globals.x_GE4, globals.y_GE4)
            plt.show()
        elif globals.Normalise_counts:
            fig,axs,plt = Plot_Spectra.Plot_Spectra3(globals.x_GE1_Ncounts, globals.y_GE1_Ncounts,
                                       globals.x_GE2_Ncounts, globals.y_GE2_Ncounts,
                                       globals.x_GE3_Ncounts, globals.y_GE3_Ncounts,
                                       globals.x_GE4_Ncounts, globals.y_GE4_Ncounts)
            plt.show()
        elif globals.Normalise_spill:
            fig,axs,plt = Plot_Spectra.Plot_Spectra3(globals.x_GE1_NEvents, globals.y_GE1_NEvents,
                                       globals.x_GE2_NEvents, globals.y_GE2_NEvents,
                                       globals.x_GE3_NEvents, globals.y_GE3_NEvents,
                                       globals.x_GE4_NEvents, globals.y_GE4_NEvents)
            plt.show()





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
                                str("{:.2f}".format(row[2])).strip()))
                            self.tab1.table_clickpeaks2.setItem(i, 2, QTableWidgetItem(
                                "{:.2f}".format(100.0*float(row[3]))))
                            self.tab1.table_clickpeaks2.setItem(i, 3, QTableWidgetItem(row[4]))

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
                    res = getmatch.get_matches(input_data)

                    temp = res[0]
                    i = 0
                    print(len(res[0]))
                    self.tab1.table_clickpeaks.setRowCount(len(res[0]))
                    for match in temp:

                        row = [match['peak_centre'], match['energy'], match['element'],
                               match['transition'], match['error'], match['diff']]

                        self.tab1.table_clickpeaks.setItem(i, 0, QTableWidgetItem(row[2]))
                        self.tab1.table_clickpeaks.setItem(i, 1, QTableWidgetItem(row[3]))
                        print(row[4])
                        print(row[5])
                        self.tab1.table_clickpeaks.setItem(i, 2, QTableWidgetItem("{:.2f}".format(row[5])))

                        i += 1

                    self.tab1.table_clickpeaks.setRowCount(i)

                    self.show()

        plt.connect('button_press_event', on_click)



class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)
        self.wp = None
        globals.we = None


        self.resize(600, 500)
        self.setWindowTitle("Elemental Analysis")

        # setting up the menu bar'''

        bar = QMenuBar(self)
        file = bar.addMenu('File')
        file_loaddef = file.addAction('Load Default Setting')
        file_browse_dir = file.addAction('Browse to Data Directory')
        file_exit = file.addAction('Exit')
        plot = bar.addMenu('Plot')
        plot_set = plot.addAction('Plot Settings')
        plot_det = plot.addMenu('Select detectors')

        plot_which_det_GE1 = plot_det.addAction('GE1')
        plot_which_det_GE1.setCheckable(True)
        print('plot_ge1', globals.plot_GE1)
        plot_which_det_GE1.setChecked(globals.plot_GE1)
        plot_which_det_GE1.setShortcut("Alt+1")

        plot_which_det_GE2 = plot_det.addAction('GE2')
        plot_which_det_GE2.setCheckable(True)
        plot_which_det_GE2.setChecked(globals.plot_GE2)
        plot_which_det_GE2.setShortcut("Alt+2")

        plot_which_det_GE3 = plot_det.addAction('GE3')
        plot_which_det_GE3.setCheckable(True)
        plot_which_det_GE3.setChecked(True)
        plot_which_det_GE3.setChecked(globals.plot_GE3)
        plot_which_det_GE3.setShortcut("Alt+3")

        plot_which_det_GE4 = plot_det.addAction('GE4')
        plot_which_det_GE4.setCheckable(True)
        plot_which_det_GE4.setChecked(globals.plot_GE4)
        plot_which_det_GE4.setShortcut("Alt+4")

        Normalise = bar.addMenu('Normalisation')
        Normalise_do_not = Normalise.addAction('Use Raw Data')
        Normalise_do_not.setCheckable(True)
        Normalise_do_not.setShortcut("Alt+D")
        Normalise_do_not.setChecked(False)
        Normalise_do_not.triggered.connect(lambda: self.N_do_not(Normalise_do_not.isChecked(),
                                                                  Normalise_total_counts, Normalise_total_spills
                                                                 ,Normalise_do_not))

        Normalise_total_counts = Normalise.addAction('Normalise by total Counts')
        Normalise_total_counts.setCheckable(True)
        Normalise_total_counts.setShortcut("Alt+C")
        Normalise_total_counts.setChecked(True)
        Normalise_total_counts.triggered.connect(lambda: self.NTC(Normalise_total_counts.isChecked(),
                                                                  Normalise_total_counts, Normalise_total_spills
                                                                  ,Normalise_do_not))

        Normalise_total_spills = Normalise.addAction('Normalise by spills')
        Normalise_total_spills.setCheckable(True)
        Normalise_total_spills.setShortcut("Alt+S")
        Normalise_total_spills.setChecked(False)
        Normalise_total_spills.triggered.connect(lambda: self.NTS(Normalise_total_spills.isChecked(),
                                                                  Normalise_total_counts, Normalise_total_spills
                                                                  ,Normalise_do_not))

        Corr = bar.addMenu('Corrections')
        Corr_eff = Corr.addAction('Efficiency Corrections')

        Corr_E = Corr.addAction('Energy Corrections')
        #Corr_E.setCheckable(True)
        #Corr_E.setChecked(False)
        Corr_E.triggered.connect(lambda: self.Corr_Energy())

        #Corr_Abs = plot.addAction('Absorption Correction')


        TRIM = bar.addMenu('SRIM/TRIM')
        Trim_sim = TRIM.addAction('SRIM/TRIM Simulation')

        # setting up the actions

        file_exit.triggered.connect(lambda: self.closeit(app))
        file_browse_dir.triggered.connect(lambda: self.Browse_dir())
        plot_which_det_GE1.triggered.connect(lambda: self.setplotGE1(plot_which_det_GE1.isChecked()))
        plot_which_det_GE2.triggered.connect(lambda: self.setplotGE2(plot_which_det_GE2.isChecked()))
        plot_which_det_GE3.triggered.connect(lambda: self.setplotGE3(plot_which_det_GE3.isChecked()))
        plot_which_det_GE4.triggered.connect(lambda: self.setplotGE4(plot_which_det_GE4.isChecked()))

        # setting up the layout

        self.label_RN = QLabel(self)
        self.label_RN.setText("Run Number                                            ")
        self.label_RN.move(50, 80)
        self.label_RN.show()

        self.label_Com = QLabel(self)
        self.label_Com.setText("Comment " +
             "                                                                                                  ")
        self.label_Com.move(50, 130)
        self.label_Com.show()

        self.label_Events = QLabel(self)
        self.label_Events.setText("Events                                            ")
        self.label_Events.move(50, 180)
        self.label_Events.show()

        self.label_Start = QLabel(self)
        self.label_Start.setText("Start Time                                            ")
        self.label_Start.move(50, 230)
        self.label_Start.show()

        self.label_End = QLabel(self)
        self.label_End.setText("End Time                                             ")
        self.label_End.move(50, 280)
        self.label_End.show()

        # setting up the buttons and run number

        RunNum_Text = QLineEdit(self)
        RunNum_Text.setAlignment(Qt.AlignCenter)
        RunNum_Text.setText('2630')
        RunNum_Text.move(200, 350)


        button_plus = QPushButton(self)
        button_plus.setText('+1')
        button_plus.move(410, 350)
        button_plus.clicked.connect(lambda: self.Incr_RunNum(RunNum_Text))

        button_plusandload = QPushButton(self)
        button_plusandload.setText('Load +1')
        button_plusandload.move(410, 420)
        button_plusandload.clicked.connect(lambda: self.Incr_RunNumandload(RunNum_Text.text(),RunNum_Text))

        button_minus = QPushButton(self)
        button_minus.setText('-1')
        button_minus.move(50, 350)
        button_minus.clicked.connect(lambda: self.Decr_RunNum(RunNum_Text))

        button_minusandload = QPushButton(self)
        button_minusandload.setText('Load -1')
        button_minusandload.move(50, 420)
        button_minusandload.clicked.connect(lambda: self.Decr_RunNumandload(RunNum_Text.text(),RunNum_Text))


        button_load = QPushButton(self)
        button_load.setText('Load')
        button_load.move(230, 420)
        button_load.clicked.connect(lambda: self.loadrunandcom(
            RunNum_Text.text()))


    def Corr_Energy(self):
        print('in Corr_Energy')
        #self.show(Correction_Energy())
        if globals.we is None:
            globals.we = Correction_E()
            print('self,wp = none')
            #self.we.resize(1200, 600)
            #self.we.setWindowTitle("Plot Window: "+globals.RunNum)
            globals.we.show()

        else:
            print('window exists')




    def N_do_not(self,checked,Norm_Counts,Norm_Spills,Normalise_do_not):
        print(checked)
        if checked:
            Norm_Spills.setChecked(False)
            Norm_Counts.setChecked(False)
            Normalise_do_not.setChecked(True)
            globals.Normalise_do_not = True

        else:
            Norm_Spills.setChecked(globals.Normalise_spill)
            Norm_Counts.setChecked(globals.Normalise_counts)
            Normalise_do_not.setChecked(False)
            globals.Normalise_do_not = False




    def NTC(self,checked,Norm_Counts,Norm_Spills,Normalise_do_not):
        print(checked)
        if checked:
            Norm_Spills.setChecked(False)
            Normalise_do_not.setChecked(False)
            globals.Normalise_counts = True
            globals.Normalise_spill = False
            globals.Normalise_do_not = False
        else:
            Norm_Spills.setChecked(True)
            globals.Normalise_counts = False
            globals.Normalise_spill = True
            Normalise_do_not.setChecked(False)


    def NTS(self,checked,Norm_Counts,Norm_Spills,Normalise_do_not):
        if checked:
            Norm_Counts.setChecked(False)
            Normalise_do_not.setChecked(False)
            globals.Normalise_counts = False
            globals.Normalise_spill = True
            globals.Normalise_do_not = False
        else:
            Norm_Counts.setChecked(True)
            globals.Normalise_counts = True
            globals.Normalise_spill = False
            Normalise_do_not.setChecked(False)


    def closeEvent(self, event):
        #close window cleanly

        widgetList = QApplication.topLevelWidgets()
        numWindows = len(widgetList)
        if numWindows > 0:
            event.accept()
            QApplication.quit()
        else:
            event.ignore()

    def closeit(self, app):
        print('here')
        quit_msg = "Are you sure you want to quit?"
        reply = QMessageBox.question(self, 'Message', quit_msg,
                                               QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()
            return

    def setplotGE1(self,value):
        print('in here self.plot_which_det_GE1',value)
        globals.plot_GE1 = value

    def setplotGE2(self,value):
        print('in here self.plot_which_det_GE2',value)
        globals.plot_GE2 = value

    def setplotGE3(self,value):
        print('in here self.plot_which_det_GE3',value)
        globals.plot_GE3 = value

    def setplotGE4(self,value):
        print('in here self.plot_which_det_GE4',value)
        globals.plot_GE4 = value


    def Decr_RunNumandload(self, RunNum, RunNum_text):
        print('in decr')
        NewRunNum = int(RunNum) - 1
        self.loadcom(str(NewRunNum))
        print('back')
        RunNum_text.setText(str(NewRunNum))

    def Incr_RunNumandload(self, RunNum, RunNum_text):
        NewRunNum = int(RunNum) + 1
        self.loadcom(str(NewRunNum))
        RunNum_text.setText(str(NewRunNum))


    def loadrunandcom(self, RunNum):
        print('hello')
        self.loadcom(RunNum)
        print('Im back')

    def loadcom(self, RunNum):
        print('load data and comment')
        globals.RunNum = RunNum
        flag, rtn_str = loadcomment.loadcomment(RunNum)
        print(flag, rtn_str)
        if flag == 1:
            mapping = dict.fromkeys(range(32))

            pr_str = rtn_str[0].translate(mapping)
            self.label_Start.setText("Start Time:    " + pr_str[20:] + "")

            pr_str = rtn_str[1].translate(mapping)
            self.label_End.setText("End Time:      " + pr_str[20:])

            pr_str = rtn_str[2].translate(mapping)
            self.label_Events.setText("Events:          " + pr_str[19:])

            pr_str = rtn_str[3].translate(mapping)
            self.label_Com.setText("Comment:      " + pr_str[10:])
        else:
            self.label_Com.setText("Comment:      Comment file not found")
            self.label_Start.setText("Start Time:    ")
            self.label_End.setText("End Time:       ")
            self.label_Events.setText("Events:")

        flag = loaddata.loaddata(RunNum)
        if (globals.flag_d_GE1 == 0 or globals.flag_d_GE2 == 0 or globals.flag_d_GE3 == 0 or globals.flag_d_GE4 == 0):
            print('oh no')
            self.label_RN.setText("Run Number:   File load failed")
        else:
            print ('yeah!')
            self.label_RN.setText("Run Number:   " + str(RunNum))

            self.Show_Plot_Window()



    def Show_Plot_Window(self):

        print('in Show_plot_window')
        print(self.wp)

        if self.wp is None:
            self.wp = PlotWindow()
            print('self,wp = none')
            self.wp.resize(850, 550)
            self.wp.setWindowTitle("Plot Window: "+globals.RunNum)
            self.wp.show()

        else:
            print('window exists')
            self.wp = PlotWindow()
            print('self,wp = none')
            self.wp.resize(850, 550)
            self.wp.setWindowTitle("Plot Window"+globals.RunNum)
            self.wp.show()




    def Incr_RunNum(self, RunNum_text):
        print('plus 1')
        RunNum_text.setText(str(int(RunNum_text.text()) + 1))

    def Decr_RunNum(self, RunNum_text):
        print('minus 1e')
        RunNum_text.setText(str(int(RunNum_text.text()) - 1))

    def Browse_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Choose Directory", "C:\\")
        print(dir_path)
        globals.workingdirectory = dir_path

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    # load settings file
    ls.loadsettings()
    print(ls.settings_info)

    # load database file
    ldf.loadDatabaseFile()

    print('loading gamma start',time.time())

    lg.loadgamma()
    print('loading gamma end',time.time())


app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())
