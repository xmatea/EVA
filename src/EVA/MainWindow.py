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
    QSizePolicy, )
from PyQt6.QtGui import QPalette, QColor

from EVA import (
    PeakFit,
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
    manual_window,
)

from EVA.app import get_app, get_config

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

        config = get_config()

        plot_which_det_GE1 = plot_det.addAction('GE1')
        plot_which_det_GE1.setCheckable(True)
        plot_which_det_GE1.setChecked(config.parser.getboolean("GE1", "show_plot"))
        plot_which_det_GE1.setShortcut("Alt+1")

        plot_which_det_GE2 = plot_det.addAction('GE2')
        plot_which_det_GE2.setCheckable(True)
        plot_which_det_GE2.setChecked(config.parser.getboolean("GE2", "show_plot"))
        plot_which_det_GE2.setShortcut("Alt+2")

        plot_which_det_GE3 = plot_det.addAction('GE3')
        plot_which_det_GE3.setCheckable(True)
        plot_which_det_GE3.setChecked(True)
        plot_which_det_GE3.setChecked(config.parser.getboolean("GE3", "show_plot"))
        plot_which_det_GE3.setShortcut("Alt+3")

        plot_which_det_GE4 = plot_det.addAction('GE4')
        plot_which_det_GE4.setCheckable(True)
        plot_which_det_GE4.setChecked(config.parser.getboolean("GE4", "show_plot"))
        plot_which_det_GE4.setShortcut("Alt+4")

        plot_multi.triggered.connect(lambda: self.multiplot())

        self.Normalise = bar.addMenu('Normalisation')
        self.Normalise_do_not = self.Normalise.addAction('Use Raw Data')
        self.Normalise_do_not.setCheckable(True)
        self.Normalise_do_not.setShortcut("Alt+D")
        self.Normalise_do_not.setChecked(config["general"]["normalisation"] == "none")
        self.Normalise_do_not.triggered.connect(lambda: self.N_do_not(self.Normalise_do_not.isChecked()))

        self.Normalise_total_counts = self.Normalise.addAction('Normalise by total Counts')
        self.Normalise_total_counts.setCheckable(True)
        self.Normalise_total_counts.setShortcut("Alt+C")
        self.Normalise_total_counts.setChecked(config["general"]["normalisation"] == "counts")
        self.Normalise_total_counts.triggered.connect(lambda: self.NTC(self.Normalise_total_counts.isChecked()))

        self.Normalise_total_spills = self.Normalise.addAction('Normalise by spills')
        self.Normalise_total_spills.setCheckable(True)
        self.Normalise_total_spills.setShortcut("Alt+S")
        self.Normalise_total_spills.setChecked(config["general"]["normalisation"] == "events")
        self.Normalise_total_spills.triggered.connect(lambda: self.NTS(self.Normalise_total_spills.isChecked()))

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
        config = get_config()
        file_exit.triggered.connect(lambda: self.close())
        file_browse_dir.triggered.connect(lambda: self.Browse_dir())
        file_loaddef.triggered.connect(config.restore_defaults)
        plot_which_det_GE1.triggered.connect(lambda: self.set_plot_detector(plot_which_det_GE1.isChecked(), "GE1"))
        plot_which_det_GE2.triggered.connect(lambda: self.set_plot_detector(plot_which_det_GE2.isChecked(), "GE2"))
        plot_which_det_GE3.triggered.connect(lambda: self.set_plot_detector(plot_which_det_GE3.isChecked(), "GE3"))
        plot_which_det_GE4.triggered.connect(lambda: self.set_plot_detector(plot_which_det_GE4.isChecked(), "GE4"))

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
        RunNum_Text.setText(config["general"]["run_num"])
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

        self.PeakFit_window = PeakFit.PeakFit()
        self.PeakFit_window.showMaximized()

    def PeakFit_GE2(self):
        print('hello in PeakFit ge2')
        globals.whichdet = 'GE2'
        self.PeakFit_window = PeakFit.PeakFit()
        self.PeakFit_window.showMaximized()

    def PeakFit_GE3(self):
        print('hello in PeakFitge 3')
        globals.whichdet = 'GE3'

        self.PeakFit_window = PeakFit.PeakFit()
        self.PeakFit_window.showMaximized()

    def PeakFit_GE4(self):
        print('hello in PeakFit ge4')
        globals.whichdet = 'GE4'

        self.PeakFit_window = PeakFit.PeakFit(self)
        self.PeakFit_window.showMaximized()

    def multiplot(self):
        print('hello in multiplot')
        self.multiplot_window = MultiPlotWindow.MultiPlotWindow()
        self.multiplot_window.showMaximized()

    def RunTrimExample(self):

        print('In TRIM')
        print('going to TRIM')
        RunTrimExample.RunTRIM_Start()

    def RunTrim(self):
        ''' Launch TRIM Window'''
        app = get_app()
        app.TRIM_window = TRIM_Window.RunSimTRIMSRIM()
        app.TRIM_window.showMaximized()

    def Corr_Eff(self):
        print('in Corr_Eff')
        app = get_app()

        #self.show(Correction_Energy())
        if app.efficiency_correction_window is None:
            app.efficiency_correction_window = Eff_Window.Correction_Eff()
            print('self,wp = none')
            #self.we.resize(1200, 600)
            #self.we.setWindowTitle("Plot Window: "+globals.RunNum)
            app.efficiency_correction_window.show()
        else:
            print('window exists')

    def Corr_Energy(self):
        print('in Corr_Energy')
        #self.show(Correction_Energy())
        app = get_app()

        if app.energy_correction_window is None:
            app.energy_correction_window = ECorr_Window.Correction_E()
            print('self,wp = none')
            #self.we.resize(1200, 600)
            #self.we.setWindowTitle("Plot Window: "+globals.RunNum)
            app.energy_correction_window.show()

        else:
            print('window exists')

    def show_manual(self):
        """ Display Manual page"""
        print("showing manual")
        app = get_app()
        if app.manual_window is None:
            app.manual_window = manual_window.ManualWindow()
            app.manual_window.show()

    def update_normalisation_menu(self):
        config = get_config()
        norm = config["general"]["normalisation"]
        self.Normalise_total_counts.setChecked(norm == "counts")
        self.Normalise_do_not.setChecked(norm == "none")
        self.Normalise_total_spills.setChecked(norm == "events")

    def N_do_not(self,checked):
        app = get_app()

        if checked:
            # Apply new normalisation to data (if data is already loaded)
            if app.loaded_run is not None:
                app.loaded_run.set_normalisation("none")

            app.config["general"]["normalisation"] = "none"

        self.update_normalisation_menu()

    def NTC(self,checked):
        app = get_app()

        if checked:
            # Apply new normalisation to data (if data is already loaded)
            if app.loaded_run is not None:
                app.loaded_run.set_normalisation("counts")

            app.config["general"]["normalisation"] = "counts"

        # update buttons
        self.update_normalisation_menu()

    def NTS(self,checked):
        app = get_app()

        if checked:
            # Apply new normalisation to data (if data is already loaded)
            if app.loaded_run is None:
                # if data is not loaded, only update normalisation in config
                app.config["general"]["normalisation"] = "events"

            else:
                flag = app.loaded_run.set_normalisation("events")
                if flag: # Normalisation failed - set normalisation to none instead
                    self.N_do_not(True)

                    # display error message to let user know what happened
                    err_str = "Cannot use normalisation by spills when comment file has not been loaded."

                    # this will block the program until user presses "ok"
                    _ = QMessageBox.critical(self, "Normalisation error", err_str,
                                             buttons=QMessageBox.StandardButton.Ok,
                                             defaultButton=QMessageBox.StandardButton.Ok)

                else:
                    app.config["general"]["normalisation"] = "events" # update config if all is ok

        # update gui elements
        self.update_normalisation_menu()

    def closeEvent(self, event):
        #close window cleanly
        widgetList = QApplication.topLevelWidgets()
        numWindows = len(widgetList)

        if numWindows > 0:
            if get_config().is_changed(): # Show save prompt window if any changes has been made to the config file
                quit_msg = "Would you like to save your changes?"
                reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.Yes)
                if reply == QMessageBox.StandardButton.Yes:
                    get_config().save_config()
                    event.accept()
                    QApplication.quit()

                elif reply == QMessageBox.StandardButton.No:
                    event.accept()
                    QApplication.quit()

                else:
                    event.ignore()
            else: # quit immediately if no changes have been made
                event.accept()
                QApplication.quit()

    def closeit(self):
        print('here')
        quit_msg = "Are you sure you want to quit?"
        reply = QMessageBox.question(self, 'Message', quit_msg,
                                               QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()
            return

    def set_plot_detector(self, value, detector):
        config = get_config()
        if value:
            config[detector]["show_plot"] = "yes"
        else:
            config[detector]["show_plot"] = "no"

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
        app = get_app()
        config = app.config

        flags = app.set_loaded_run(RunNum)

        if flags["no_files_found"]: #  no data was loaded - return now
            # Update GUI
            self.label_RN.setText("Run Number:   File load failed")
            self.label_Com.setText("Comment:      Comment file not found")
            self.label_Start.setText("Start Time:    ")
            self.label_End.setText("End Time:       ")
            self.label_Events.setText("Events:")
            return

        else: # update run number field in gui and in config
            self.label_RN.setText("Run Number:   " + str(RunNum))

            # Update run number in config
            config["general"]["run_num"] = RunNum

        if flags["comment_not_found"]: # Comment file was not found
            self.label_Com.setText("Comment:      Comment file not found")
            self.label_Start.setText("Start Time:    ")
            self.label_End.setText("End Time:       ")
            self.label_Events.setText("Events:")

        else: # write comment info to GUI
            mapping = dict.fromkeys(range(32))

            pr_str = app.loaded_run.start_time.translate(mapping)
            self.label_Start.setText("Start Time:    " + pr_str[20:] + "")

            pr_str = app.loaded_run.end_time.translate(mapping)
            self.label_End.setText("End Time:      " + pr_str[20:])

            pr_str = app.loaded_run.events_str.translate(mapping)
            self.label_Events.setText("Events:          " + pr_str[19:])

            pr_str = app.loaded_run.comment.translate(mapping)
            self.label_Com.setText("Comment:      " + pr_str[10:])

        if flags["norm_by_spills_error"]:  # normalisation by spills failed
            # set normalisation to none instead
            self.N_do_not(True)

            # display error message to let user know what happened
            err_str = ("Cannot use normalisation by spills when comment file has not been loaded. Normalisation has been "
                       "set to none.")

            # this will block the program until user presses "ok"
            _ = QMessageBox.critical(self, "Normalisation error", err_str,
                                           buttons=QMessageBox.StandardButton.Ok,
                                           defaultButton=QMessageBox.StandardButton.Ok)

        self.Show_Plot_Window()
        self.PeakFit_menu.setDisabled(False)

    def Show_Plot_Window(self):
        print('in Show_plot_window')
        app = get_app()
        config = app.config

        if app.plot_window is None:
            app.plot_window = Plot_Window.PlotWindow()
           # self.wp.resize(850, 550)
            app.plot_window.setWindowTitle("Plot Window: " + config["general"]["run_num"])
            app.plot_window.showMaximized()

        else:
            print('window exists')
            app.plot_window = Plot_Window.PlotWindow()
            print('self,wp = none')
            #self.wp.resize(850, 550)
            app.plot_window.setWindowTitle("Plot Window" + config["general"]["run_num"])
            app.plot_window.showMaximized()


    def Incr_RunNum(self, RunNum_text):
        print('plus 1')
        RunNum_text.setText(str(int(RunNum_text.text()) + 1))

    def Decr_RunNum(self, RunNum_text):
        print('minus 1e')
        RunNum_text.setText(str(int(RunNum_text.text()) - 1))

    def Browse_dir(self):
        config = get_config()
        dir_path = QFileDialog.getExistingDirectory(self, "Choose Directory", "C:\\")
        print(dir_path)
        config["general"]["working_directory"] = dir_path
        #config.save_config()

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

