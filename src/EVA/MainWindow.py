import time

#from ui_EfficiencyUI import Ui_EfficienyCorrection
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtGui import QPalette, QColor
import sys

from EVA import (
    PeakFit,
    loaddata,
    loadcomment,
    globals,
    loadsettings as ls,
    Eff_Window,
    ECorr_Window,
    Plot_Window,
    MultiPlotWindow,
    LoadDatabaseFile as ldf,
    loadgamma as lg,
    RunTrimExample,
    TRIM_Window,
    manual_window
)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)







class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)
        self.wp = None
        globals.we = None

        #if globals.scn_res == 1:
        #    self.resize(1000, 500)
        #elif globals.scn_res == 2:
        #    self.resize(700, 300)
        #else:
        #    self.resize(1000,500)


        self.setWindowTitle("Elemental Analysis")
        self.setMinimumSize(QSize(650, 300))

        # setting up the menu bar'''
        
        #bar = QMenuBar(self)
        bar = self.menuBar()
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

        self.Analysis = bar.addMenu('Analysis')
        self.PeakFit_menu = self.Analysis.addMenu('Peak Fitting')
        #self.PeakFit_menu.triggered.connect(lambda: self.PeakFit())
        self.PeakFit_menu.setDisabled(True)

        self.Ana_GE1 = self.PeakFit_menu.addAction('GE1')
        self.Ana_GE1.triggered.connect(lambda: self.PeakFit_GE1())

        self.Ana_GE2 = self.PeakFit_menu.addAction('GE2')
        self.Ana_GE2.triggered.connect(lambda: self.PeakFit_GE2())

        self.Ana_GE3 = self.PeakFit_menu.addAction('GE3')
        self.Ana_GE3.triggered.connect(lambda: self.PeakFit_GE3())

        self.Ana_GE4 = self.PeakFit_menu.addAction('GE4')
        self.Ana_GE4.triggered.connect(lambda: self.PeakFit_GE4())

        TRIM = bar.addMenu('SRIM/TRIM')
        Trim_sim = TRIM.addAction('SRIM/TRIM Simulation')
        Trim_sim.triggered.connect(lambda: self.RunTrim())
        Trim_sim_test = TRIM.addAction('SRIM/TRIM Simulation test')
        Trim_sim_test.triggered.connect(lambda: self.RunTrimExample())

        # Manual tab
        help = bar.addMenu('Help')
        help_manual = help.addAction("Manual")
        help_manual.triggered.connect(lambda: self.show_manual())

        # setting up the actions

        file_exit.triggered.connect(lambda: self.closeit(app))
        file_browse_dir.triggered.connect(lambda: self.Browse_dir())
        plot_which_det_GE1.triggered.connect(lambda: self.setplotGE1(plot_which_det_GE1.isChecked()))
        plot_which_det_GE2.triggered.connect(lambda: self.setplotGE2(plot_which_det_GE2.isChecked()))
        plot_which_det_GE3.triggered.connect(lambda: self.setplotGE3(plot_which_det_GE3.isChecked()))
        plot_which_det_GE4.triggered.connect(lambda: self.setplotGE4(plot_which_det_GE4.isChecked()))

        # setting up the layout

        layout = QGridLayout()

        self.label_RN = QLabel(self)
        self.label_RN.setText("Run Number")
        self.label_RN.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #if globals.scn_res == 1:
        #    self.label_RN.move(50, 80)
        #elif globals.scn_res == 2:
        #    self.label_RN.move(20, 50)
        #else:
        #    self.label_RN.move(50, 80)

        #self.label_RN.show()
        layout.addWidget(self.label_RN, 0, 0, 1, 3)

        self.label_Com = QLabel(self)
        self.label_Com.setText("Comment")
        self.label_Com.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)                                                                                                 
        #if globals.scn_res == 1:
        #    self.label_Com.move(50, 130)
        #elif globals.scn_res == 2:
        #    self.label_Com.move(20, 75)
        #else:
        #    self.label_Com.move(50, 130)
        #self.label_Com.show()
        layout.addWidget(self.label_Com, 1, 0, 1, 3)

        self.label_Events = QLabel(self)
        self.label_Events.setText("Events")
        self.label_Events.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #if globals.scn_res == 1:
        #    self.label_Events.move(50, 180)
        #elif globals.scn_res == 2:
        #    self.label_Events.move(20, 100)
        #else:
        #    self.label_Events.move(50, 180)

        #self.label_Events.show()
        layout.addWidget(self.label_Events, 2, 0, 1, 3)

        self.label_Start = QLabel(self)
        self.label_Start.setText("Start Time")
        self.label_Start.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #if globals.scn_res == 1:
        #    self.label_Start.move(50, 230)
        #elif globals.scn_res == 2:
        #    self.label_Start.move(20, 125)
        #else:
        #    self.label_Start.move(50, 230)

        #self.label_Start.show()
        layout.addWidget(self.label_Start, 3, 0, 1, 3)

        self.label_End = QLabel(self)
        self.label_End.setText("End Time")
        self.label_End.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #if globals.scn_res == 1:
        #    self.label_End.move(50, 280)
        #elif globals.scn_res == 2:
        #    self.label_End.move(20, 150)
        #else:
        #    self.label_End.move(50, 280)

        #self.label_End.show()
        layout.addWidget(self.label_End, 4, 0, 1, 3)

        # setting up the buttons and run number

        RunNum_Text = QLineEdit(self)
        RunNum_Text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        RunNum_Text.setMinimumWidth(200)
        RunNum_Text.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #font = QFont()
        #font.setPointSize(8)
        #RunNum_Text.setFont(font)
        RunNum_Text.setText('2630')
        #if globals.scn_res == 1:
        #    RunNum_Text.resize(220, 70)
        #    RunNum_Text.move(350, 350)
        #elif globals.scn_res == 2:
        #    RunNum_Text.resize(120, 35)
        #    RunNum_Text.move(200, 200)
        #else:
        #    RunNum_Text.resize(220, 70)
        #    RunNum_Text.move(350, 350)
        layout.addWidget(RunNum_Text, 5, 1)



        button_plus = QPushButton(self)
        button_plus.setText('+1')
        button_plus.setMinimumWidth(200)
        button_plus.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #button_plus.move(650, 350)
        #if globals.scn_res == 1:
        #    button_plus.move(650, 350)
        #elif globals.scn_res == 2:
        #    button_plus.move(350, 200)
        #else:
        #    button_plus.move(650, 350)
        layout.addWidget(button_plus, 5, 2)

        button_plus.clicked.connect(lambda: self.Incr_RunNum(RunNum_Text))

        button_plusandload = QPushButton(self)
        button_plusandload.setText('Load +1')
        button_plusandload.setMinimumWidth(200)
        button_plusandload.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #if globals.scn_res == 1:
        #    button_plusandload.move(650,420)
        #elif globals.scn_res == 2:
        #    button_plusandload.move(350,250)
        #else:
        #    button_plusandload.move(650,420)
        layout.addWidget(button_plusandload, 6, 2)

        button_plusandload.clicked.connect(lambda: self.Incr_RunNumandload(RunNum_Text.text(),RunNum_Text))

        button_minus = QPushButton(self)
        button_minus.setText('-1')
        button_minus.setMinimumWidth(200)
        button_minus.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #if globals.scn_res == 1:
        #    button_minus.move(50, 350)
        #elif globals.scn_res == 2:
        #    button_minus.move(50, 200)

        #else:
        #    button_minus.move(50, 350)
        layout.addWidget(button_minus, 5, 0)

        button_minus.clicked.connect(lambda: self.Decr_RunNum(RunNum_Text))

        button_minusandload = QPushButton(self)
        button_minusandload.setText('Load -1')
        button_minusandload.setMinimumWidth(200)
        button_minusandload.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #if globals.scn_res == 1:
        #    button_minusandload.move(50, 420)
        #elif globals.scn_res == 2:
        #    button_minusandload.move(50, 250)
        #else:
        #    button_minusandload.move(50, 420)
        layout.addWidget(button_minusandload, 6, 0)

        button_minusandload.clicked.connect(lambda: self.Decr_RunNumandload(RunNum_Text.text(),RunNum_Text))


        button_load = QPushButton(self)
        button_load.setText('Load')
        button_load.setMinimumWidth(200)
        button_load.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #if globals.scn_res == 1:
        #    button_load.move(350, 420)
        #elif globals.scn_res == 2:
        #    button_load.move(200, 250)
        #else:
        #    button_load.move(350, 420)
        layout.addWidget(button_load, 6, 1)

        button_load.clicked.connect(lambda: self.loadrunandcom(
            RunNum_Text.text()))
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def PeakFit(self):
        print('hello in PeakFit')
        globals.whichdet = 'All'
        PeakFit.PeakFit()

    def PeakFit_GE1(self):
        print('hello in PeakFit ge1')
        globals.whichdet = 'GE1'

        PeakFit.PeakFit()

    def PeakFit_GE2(self):
        print('hello in PeakFit ge2')
        globals.whichdet = 'GE2'
        PeakFit.PeakFit()

    def PeakFit_GE3(self):
        print('hello in PeakFitge 3')
        globals.whichdet = 'GE3'

        PeakFit.PeakFit()

    def PeakFit_GE4(self):
        print('hello in PeakFit ge4')
        globals.whichdet = 'GE4'

        PeakFit.PeakFit()

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

    def show_manual(self):
        """ Display Manual page"""
        print("showing manual")
        if globals.wManual is None:
            globals.wManual = manual_window.ManualWindow()

        globals.wManual.show()


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
            self.PeakFit_menu.setDisabled(False)



    def Show_Plot_Window(self):

        print('in Show_plot_window')
        print(self.wp)

        if self.wp is None:
            self.wp = Plot_Window.PlotWindow()
            print('self,wp = none')
           # self.wp.resize(850, 550)
            self.wp.setWindowTitle("Plot Window: " + globals.RunNum)
            self.wp.showMaximized()

        else:
            print('window exists')
            self.wp = Plot_Window.PlotWindow()
            print('self,wp = none')
            #self.wp.resize(850, 550)
            self.wp.setWindowTitle("Plot Window" + globals.RunNum)
            self.wp.showMaximized()




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
