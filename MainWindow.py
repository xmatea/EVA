import time

import matplotlib.pyplot as plt
#from ui_EfficiencyUI import Ui_EfficienyCorrection
from matplotlib.backend_bases import MouseButton
from PyQt5.QtCore import QSize, Qt
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
from PyQt5.QtGui import QPalette, QColor, QCloseEvent, QFont
import sys

import TRIM_Window
import loaddata
import loadcomment
import globals
import loadsettings as ls

import Eff_Window
import ECorr_Window
import Plot_Window
import MultiPlotWindow
import LoadDatabaseFile as ldf
import loadgamma as lg
import RunTrimExample
import TRIM_Window

'''if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
'''


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)







class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)
        self.wp = None
        globals.we = None


        self.resize(1000, 500)
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
        plot_multi = plot.addAction('Multi-Run Plot')

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

        plot_multi.triggered.connect(lambda: self.multiplot())

        Normalise = bar.addMenu('Normalisation')
        Normalise_do_not = Normalise.addAction('Use Raw Data')
        Normalise_do_not.setCheckable(True)
        Normalise_do_not.setShortcut("Alt+D")
        Normalise_do_not.setChecked(False)
        Normalise_do_not.triggered.connect(lambda: self.N_do_not(Normalise_do_not.isChecked(),
                                                                  Normalise_total_counts, Normalise_total_spills
                                                                 , Normalise_do_not))

        Normalise_total_counts = Normalise.addAction('Normalise by total Counts')
        Normalise_total_counts.setCheckable(True)
        Normalise_total_counts.setShortcut("Alt+C")
        Normalise_total_counts.setChecked(True)
        Normalise_total_counts.triggered.connect(lambda: self.NTC(Normalise_total_counts.isChecked(),
                                                                  Normalise_total_counts, Normalise_total_spills
                                                                  , Normalise_do_not))

        Normalise_total_spills = Normalise.addAction('Normalise by spills')
        Normalise_total_spills.setCheckable(True)
        Normalise_total_spills.setShortcut("Alt+S")
        Normalise_total_spills.setChecked(False)
        Normalise_total_spills.triggered.connect(lambda: self.NTS(Normalise_total_spills.isChecked(),
                                                                  Normalise_total_counts, Normalise_total_spills
                                                                  , Normalise_do_not))

        Corr = bar.addMenu('Corrections')
        Corr_eff = Corr.addAction('Efficiency Corrections')

        Corr_E = Corr.addAction('Energy Corrections')
        #Corr_E.setCheckable(True)
        #Corr_E.setChecked(False)
        Corr_E.triggered.connect(lambda: self.Corr_Energy())
        Corr_eff.triggered.connect(lambda: self.Corr_Eff())

        #Corr_Abs = plot.addAction('Absorption Correction')


        TRIM = bar.addMenu('SRIM/TRIM')
        Trim_sim = TRIM.addAction('SRIM/TRIM Simulation')
        Trim_sim.triggered.connect(lambda: self.RunTrim())
        Trim_sim_test = TRIM.addAction('SRIM/TRIM Simulation test')
        Trim_sim_test.triggered.connect(lambda: self.RunTrimExample())

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
        RunNum_Text.resize(220,70)
        font = QFont()
        font.setPointSize(12)
        RunNum_Text.setFont(font)
        RunNum_Text.setText('2630')
        RunNum_Text.move(350, 350)


        button_plus = QPushButton(self)
        button_plus.setText('+1')
        button_plus.move(650, 350)
        button_plus.clicked.connect(lambda: self.Incr_RunNum(RunNum_Text))

        button_plusandload = QPushButton(self)
        button_plusandload.setText('Load +1')
        button_plusandload.move(650, 420)
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
        button_load.move(350, 420)
        button_load.clicked.connect(lambda: self.loadrunandcom(
            RunNum_Text.text()))

    def multiplot(self):
        print('hello in multiplot')
        MultiPlotWindow.MultiPlotWindow()

    def RunTrimExample(self):

        print('In TRIM')
        print('going to TRIM')
        RunTrimExample.RunTRIM_Start()

    def RunTrim(self):
        ''' Launch TRIM Window'''
        print('in TRIM')
        # self.show(Correction_Energy())
        if globals.wTrim is None:
            globals.wTrim = TRIM_Window.RunSimTRIMSRIM()
            print('self,wp = none')
            # self.we.resize(1200, 600)
            # self.we.setWindowTitle("Plot Window: "+globals.RunNum)
            globals.wTrim.show()

        else:
            print('window exists')

    def Corr_Eff(self):
        print('in Corr_Eff')
        #self.show(Correction_Energy())
        if globals.weff is None:
            globals.weff = Eff_Window.Correction_Eff()
            print('self,wp = none')
            #self.we.resize(1200, 600)
            #self.we.setWindowTitle("Plot Window: "+globals.RunNum)
            globals.weff.show()

        else:
            print('window exists')

    def Corr_Energy(self):
        print('in Corr_Energy')
        #self.show(Correction_Energy())
        if globals.we is None:
            globals.we = ECorr_Window.Correction_E()
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
            self.wp = Plot_Window.PlotWindow()
            print('self,wp = none')
            self.wp.resize(850, 550)
            self.wp.setWindowTitle("Plot Window: "+globals.RunNum)
            self.wp.show()

        else:
            print('window exists')
            self.wp = Plot_Window.PlotWindow()
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
