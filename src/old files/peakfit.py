import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton
from lmfit.models import GaussianModel, QuadraticModel
from scipy.optimize import curve_fit

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QTabWidget,
    QErrorMessage,
    QFileDialog,
)

from EVA.widgets.plot import plot_widget
from EVA.core.app import get_app, get_config
from EVA.core.plot import plotting
from EVA.util import Trimdata

class PeakFit(QWidget):
    def __init__(self, detector):
        super().__init__()

        conf = get_config()
        self.run_num = conf["general"]["run_num"]
        self.detector = detector

        self.setMinimumSize(1200, 800)
        self.setWindowTitle("Peak Fitting Window: Run Number " + self.run_num + " Det: " + self.detector)

        # set up plot widget
        self.title_lab = "Analysis of RunNum: " + self.run_num + "Det: " + self.detector
        self.init_gui()

    def init_gui(self):
        app = get_app()

        # Set up containers and layouts
        layout = QGridLayout()
        self.setLayout(layout)

        fit_settings_form = QWidget()
        fit_settings_form_layout = QFormLayout()

        fitting_panel = QWidget()
        fitting_panel_layout = QVBoxLayout()

        tabs = QTabWidget()

        tab1 = QWidget()
        tab1_layout = QVBoxLayout()

        tab2 = QWidget()
        tab2_layout = QVBoxLayout()

        # set size constraints
        fitting_panel.setMaximumWidth(700)
        tabs.setMinimumWidth(650)
        fit_settings_form.setMaximumWidth(400)

        # Set up fit settings form
        fit_settings_form_title = QLabel("Set fitting range")
        xrange_min_line_edit = QLineEdit('180.0')
        xrange_max_line_edit = QLineEdit('200.0')
        fit_button = QPushButton('Fit Currently loaded Spectra')

        fit_button.clicked.connect(lambda: self.fit_spectra_lmfit())

        # add all form components to form layout
        fit_settings_form.setLayout(fit_settings_form_layout)
        fit_settings_form_layout.addWidget(fit_settings_form_title)
        fit_settings_form_layout.addRow(QLabel("Start"), xrange_min_line_edit)
        fit_settings_form_layout.addRow(QLabel("Stop"), xrange_max_line_edit)
        fit_settings_form_layout.addWidget(fit_button)

        # Set up tab view
        tabs.addTab(tab1, "Individual Peak Fit")
        #self.tabs.addTab(self.tab2, "Element Search")

        tab1.label_Element1 = QLabel("Peaks:")

        tab1.table_clickpeaks = QTableWidget(tab1)
        tab1.table_clickpeaks.setShowGrid(True)
        tab1.table_clickpeaks.setColumnCount(6)
        tab1.table_clickpeaks.setRowCount(100)

        tab1.table_clickpeaks.verticalScrollBar()
        tab1.table_clickpeaks.setHorizontalHeaderLabels(
            ['Position (keV)','Error', 'Area','Error', 'Width', 'Error'])

        tab1.table_clickpeaks.cellClicked.connect(self.settinggaussian)


        tab1.label_Element2 = QLabel("Polynomial Background:")

        # table for background polynomial

        tab1.table_poly = QTableWidget(tab1)
        tab1.table_poly.setShowGrid(True)
        tab1.table_poly.setColumnCount(6)
        tab1.table_poly.setRowCount(1)
        tab1.table_poly.verticalScrollBar()

        tab1.table_poly.setHorizontalHeaderLabels(
            ['Const','Error','1st','Error', '2nd','Error'])

        tab1.table_poly.setItem(0,0, QTableWidgetItem(str(25)))
        tab1.table_poly.setItem(0, 2, QTableWidgetItem(str(0.001)))
        tab1.table_poly.setItem(0, 4, QTableWidgetItem(str(0.0)))
        tab1.table_poly.cellClicked.connect(self.settingploy)


        tab1.savebut = QPushButton('Save As')
        tab1.savebut.clicked.connect(lambda: self.savefunction())

        tab1.loadbut = QPushButton('Load')
        tab1.loadbut.clicked.connect(lambda: self.loadfunction())

        # restrict size of load and save buttons
        #self.tab1.loadbut.setMaximumWidth(200)
        #self.tab1.savebut.setMaximumWidth(200)

        # add all tab1 components to tab1 layout
        tab1.setLayout(tab1_layout)
        tab1_layout.addWidget(tab1.label_Element1)
        tab1_layout.addWidget(tab1.table_clickpeaks)
        tab1_layout.addWidget(tab1.label_Element2)
        tab1_layout.addWidget(tab1.table_poly)
        tab1_layout.addWidget(tab1.savebut)
        tab1_layout.addWidget(tab1.loadbut)

        # add peak fit form and tables to left panel widget
        fitting_panel.setLayout(fitting_panel_layout)
        fitting_panel_layout.addWidget(fit_settings_form)
        fitting_panel_layout.addWidget(tabs)


        # Plot and embed figure as plot widget
        fig, ax = plotting.plot_run(app.loaded_run, show_detectors=[self.detector],
                                    colour=app.config["plot"]["fill_colour"], title=self.title_lab)

        plot = plot_widget.PlotWidget(fig, ax)
        plot.canvas.mpl_connect('button_press_event', self.on_click) # connects plot click events to on_click

        # add all components to main layout
        layout.addWidget(plot, 0, 1)
        layout.addWidget(fitting_panel, 0, 0)

    def on_fitbutton_click(self):
        self.s_fitbutton_clicked.emit()




    def savefunction(self):
        print('in save function')
        name = QFileDialog.getSaveFileName(self, 'Save File', directory=globals.workingdirectory)

        if name != ('', ''):
            pp = []
            pp_status = []
            ph = []
            ph_status = []
            pw = []
            pw_status = []
            EMin = float(self.xrange_min_line_edit.text())
            EMax = float(self.xrange_max_line_edit.text())
            pp_len = 0
            for i in range(int(self.tab1.table_clickpeaks.rowCount())):
                try:
                    print(self.tab1.table_clickpeaks.item(i, 0).text())
                    pp.append(float(self.tab1.table_clickpeaks.item(i, 0).text()))
                    try:
                        if self.tab1.table_clickpeaks.item(i,1).text() == 'fixed':
                            pp_status.append('fixed')
                        else:
                            pp_status.append('vary')
                    except:
                        pp_status.append('vary')


                    pp_len += 1
                except:
                    #print('end of line',i)
                    temp = 1

            #checks reading the table

            if self.tab1.table_clickpeaks.item(0, 0) is None:
                # pop up box to say no peaks in the table
                error_message = QErrorMessage(self)
                error_message.setWindowTitle("Peak Setup Error")
                error_message.showMessage("Error: No peaks in the peak table")

            else:
                # fitting bit
                for i in range(pp_len+1):
                    try:
                        ph.append(float(self.tab1.table_clickpeaks.item(i, 2).text()))
                        try:
                            if self.tab1.table_clickpeaks.item(i, 3).text() == 'fixed':
                                ph_status.append('fixed')
                            else:
                                ph_status.append('vary')
                        except:
                            ph_status.append('vary')

                        pw.append(float(self.tab1.table_clickpeaks.item(i, 4).text()))
                        try:
                            if self.tab1.table_clickpeaks.item(i, 5).text() == 'fixed':
                                pw_status.append('fixed')
                            elif self.tab1.table_clickpeaks.item(i,5).text() == 'shared':
                                pw_status.append('shared')
                            else:
                                pw_status.append('vary')
                        except:
                            pw_status.append('vary')

                    except:
                        temp = 1

                #get backgorund info
                back = []
                try:
                    back.append(float(self.tab1.table_poly.item(0, 0).text()))
                    back.append(float(self.tab1.table_poly.item(0, 2).text()))
                    back.append(float(self.tab1.table_poly.item(0, 4).text()))
                except:
                    temp = 1

            try:
                if self.tab1.table_poly.item(0,1).text() == 'fixed':
                    avary = 'fixed'
                else:
                    avary = 'vary'
            except:
                avary = 'vary'

            try:
                if self.tab1.table_poly.item(0, 3).text() == 'fixed':
                    bvary = 'fixed'
                else:
                    bvary = 'vary'
            except:
                bvary = 'vary'

            try:
                if self.tab1.table_poly.item(0, 5).text() == 'fixed':
                    cvary = 'fixed'
                else:
                    cvary = 'vary'
            except:
                cvary = 'vary'

            print('got info')



            print(name)
            print(name[0])
            print(globals.workingdirectory)
            file = open(name[0], 'w')

            file.write('Energy Range\n')
            file.write(str(EMin)+' '+str(EMax)+'\n')
            file.write('Number of Guassians\n')
            file.write(str(pp_len)+'\n')
            file.write('Gaussian Parameters\n')
            for i in range(pp_len):
                file.write(str(pp[i])+' '+str(pp_status[i] +
                                              ' '+str(ph[i])+' '+str(ph_status[i]) +
                                              ' '+str(pw[i])+' '+str(pw_status[i])+'\n'))
            file.write('Background\n')
            file.write(str(back[0])+' '+ avary+'\n')
            file.write(str(back[1])+' '+ bvary+'\n')
            file.write(str(back[2])+' '+ cvary+'\n')
            file.close()

    def settinggaussian(self, row, col):
        try:
            print('row, col', row, col)
            # get info from table
            if col == 1 or col == 3 or col == 5:
                print('error column')
                try:
                    temp = self.tab1.table_clickpeaks.item(row, col-1).text()
                    try:
                        errorcontents = self.tab1.table_clickpeaks.item(row, col).text()

                        # Toggle peak width between shared, fixed and free
                        if errorcontents == 'fixed' and row >= 1 and col == 5:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('shared'))
                        elif errorcontents == 'shared' and row >= 1 and col == 5:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('1.0'))
                        elif errorcontents != 'fixed' and errorcontents != 'shared' and row >= 1 and col == 5:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('fixed'))

                        if errorcontents == 'fixed' and row == 0 and col == 5:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('1.0'))
                        elif errorcontents != 'fixed' and row == 0 and col == 5:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('fixed'))

                        #Toggle peak position and peak height between fixed and free

                        if errorcontents == 'fixed' and col == 1:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('1.0'))
                        elif errorcontents != 'fixed' and col == 1:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('fixed'))
                        if errorcontents == 'fixed' and col == 3:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('1.0'))
                        elif errorcontents != 'fixed' and col == 3:
                            self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('fixed'))

                    except:
                        print('ummm')
                        self.tab1.table_clickpeaks.setItem(row, col, QTableWidgetItem('fixed'))
                except:
                    temp = 1
        except:
            temp = 1

        return


    def settingploy(self, row, col):
        try:
            print('row, col', row, col)
            # get info from table
            if col == 1 or col == 3 or col == 5:
                print('error column')
                try:
                    errorcontents = self.tab1.table_poly.item(row,col).text()
                except:
                    errorcontents = '1.0'
                if errorcontents == 'fixed':
                    self.tab1.table_poly.setItem(row, col, QTableWidgetItem('1.0'))
                else:
                    self.tab1.table_poly.setItem(row, col, QTableWidgetItem('fixed'))


        except:
            temp = 1

        return


    def on_click(self, event):
        print("clicked!")
        if event.button is MouseButton.RIGHT:
            # Find possible gamma peaks
            x, y = event.xdata, event.ydata
            print('x,y', x, y)
            if event.inaxes:
                ax = event.inaxes  # the axes instance
                print(ax)
                yesno = QWidget()
                yesno.title = "Add peak"
                yesno.left = 100
                yesno.top = 100
                yesno.width = 320
                yesno.height = 200
                yesno.setWindowTitle(yesno.title)
                yesno.setGeometry(yesno.left, yesno.top, yesno.width, yesno.height)

                buttonReply = QMessageBox.question(yesno, 'AddPeak',
                                                   "Do you wish to add a Fit peak at "
                                                   + "{:.1f}".format(x) + " keV",
                                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
                if buttonReply == QMessageBox.StandardButton.Yes:
                    print('Yes clicked.')
                    noofrows = self.tab1.table_clickpeaks.rowCount()
                    print('noofrows', noofrows)
                    #print('item', self.tab1.table_clickpeaks.item(0,0).text())
                    i = 0
                    foundfirstblank = 0
                    std_width=0.2
                    for i in range(noofrows):
                        #print('here', self.tab1.table_clickpeaks.item(i, 0))
                        if self.tab1.table_clickpeaks.item(i, 0) == None:
                            if foundfirstblank == 0:
                                self.tab1.table_clickpeaks.setItem(i, 0,
                                                                   QTableWidgetItem(str("{:.1f}".format(x))))
                                foundfirstblank = 1
                                area = (y * std_width) * math.sqrt(2*math.pi)
                                self.tab1.table_clickpeaks.setItem(i, 2,
                                                                   QTableWidgetItem(str("{:.1f}".format(area))))
                                self.tab1.table_clickpeaks.setItem(i, 4,
                                                                   QTableWidgetItem(str(std_width)))
                else:
                    print('No clicked.')

                yesno.show()

    def fit_spectra(self):

        def gaussian(x, mu, sigma, a, c):
            return a / sigma / np.sqrt(2 * np.pi) * np.exp(-(x - mu) ** 2 / 2 / sigma ** 2) + c

        def multiGaussianFunc(x, *params):
            y = np.zeros_like(x)
            for i in range(0, len(params)-3, 3):
                ctr = params[i]
                amp = params[i+1]
                wid = params[i+2]
                y = y + amp / wid / np.sqrt(2 * np.pi) * np.exp(-((x - ctr) / 2/ wid) ** 2)
            a = params[len(params)-3]
            b = params[len(params)-2]
            c = params[len(params)-1]
            y = y + a + b * x + c * x * x
            return y

        # get information from the table and store in arrays
        pp = []
        ph = []
        pw = []
        EMin = float(self.xrange_min_line_edit.text())
        EMax = float(self.xrange_max_line_edit.text())
        pp_len = 0
        for i in range(int(self.tab1.table_clickpeaks.rowCount())):
            try:
                print(self.tab1.table_clickpeaks.item(i, 0).text())
                pp.append(float(self.tab1.table_clickpeaks.item(i, 0).text()))
                pp_len += 1
            except:
                #print('end of line',i)
                temp = 1

        #checks reading the table

        if self.tab1.table_clickpeaks.item(0, 0) is None:
            # pop up box to say no peaks in the table
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("Peak Setup Error")
            error_message.showMessage("Error: No peaks in the peak table")
            return

        else:
            # fitting bit
            for i in range(pp_len+1):
                try:
                    ph.append(float(self.tab1.table_clickpeaks.item(i, 2).text()))
                    pw.append(float(self.tab1.table_clickpeaks.item(i, 4).text()))
                except:
                    temp = 1

            #get backgorund info
            back = []
            try:
                back.append(float(self.tab1.table_poly.item(0, 0).text()))
                back.append(float(self.tab1.table_poly.item(0, 2).text()))
                back.append(float(self.tab1.table_poly.item(0, 4).text()))
            except:
                temp = 1


            # get and trim the correct data

            if globals.whichdet == 'GE1':
                datax, datay = Trimdata.Trimdata(self.data_x_GE1, self.data_y_GE1, EMin, EMax)
            elif globals.whichdet == 'GE2':
                datax, datay = Trimdata.Trimdata(self.data_x_GE2, self.data_y_GE2, EMin, EMax)
            elif globals.whichdet == 'GE3':
                datax, datay = Trimdata.Trimdata(self.data_x_GE3, self.data_y_GE3, EMin, EMax)
            elif globals.whichdet == 'GE4':
                datax, datay = Trimdata.Trimdata(self.data_x_GE4, self.data_y_GE4, EMin, EMax)


            #define initial guess

            iniguess = []
            for i in range(pp_len):
                iniguess.append(pp[i])
                iniguess.append(ph[i])
                iniguess.append(pw[i])

            iniguess.append(back[0])
            iniguess.append(back[1])
            iniguess.append(back[2])



            #define bounds for parameters

            bound_all = peakfit_bounds_define.define_bounds(pp_len, EMin, EMax, back)

            #custom_gaussian = lambda datax, mu, sigma, a, c: gaussian(datax, mu, sigma, a, c)
            #custom_gaussian = lambda x, iniguess: multiGaussianFunc(x, iniguess)
            # set x to be within the limits


            popt, pcov = curve_fit(multiGaussianFunc, datax, datay,
                                   sigma=np.sqrt(datay), p0=iniguess,
                                   absolute_sigma=True, bounds=bound_all)
            #popt, pcov = curve_fit(custom_gaussian, datax, datay, p0=[mu,sigma, a,c])

            print('popt',popt)
            print('pcov',pcov)

            #calc errors on parameters
            perr = np.sqrt(np.diag(pcov))
            print('perr',perr)

            #calc chisq

            r = datay - multiGaussianFunc(datax, *popt)
            chisq = sum((r / np.sqrt(datay)) ** 2)/len(datax)
            print('Chisq=',chisq)

            #write results to GUI
            for i in range(0, pp_len):
                try:
                    pos = i*3
                    self.tab1.table_clickpeaks.setItem(i, 0, QTableWidgetItem(str(popt[pos])))
                    self.tab1.table_clickpeaks.setItem(i, 2, QTableWidgetItem(str(popt[pos+1])))
                    self.tab1.table_clickpeaks.setItem(i, 4, QTableWidgetItem(str(popt[pos+2])))

                    self.tab1.table_clickpeaks.setItem(i, 1, QTableWidgetItem(str(perr[pos])))
                    self.tab1.table_clickpeaks.setItem(i, 3, QTableWidgetItem(str(perr[pos+1])))
                    self.tab1.table_clickpeaks.setItem(i, 5, QTableWidgetItem(str(perr[pos+2])))



                except:
                    temp = 1
            para_len = len(popt)
            print(para_len)
            self.tab1.table_poly.setItem(0, 0, QTableWidgetItem(str(popt[para_len - 3])))
            self.tab1.table_poly.setItem(0, 2, QTableWidgetItem(str(popt[para_len - 2])))
            self.tab1.table_poly.setItem(0, 4, QTableWidgetItem(str(popt[para_len - 1])))
            self.tab1.table_poly.setItem(0, 1, QTableWidgetItem(str(perr[para_len - 3])))
            self.tab1.table_poly.setItem(0, 3, QTableWidgetItem(str(perr[para_len - 2])))
            self.tab1.table_poly.setItem(0, 5, QTableWidgetItem(str(perr[para_len - 1])))

            #plot results
            plt.plot(datax, multiGaussianFunc(datax, *popt), label="gaussian")
            plt.axvline(EMin, color='red', linestyle='--')
            plt.axvline(EMax, color='red', linestyle='--')
            plt.legend()
            #plt.show()
            self.plot.canvas.draw()

            # Generate function
            # Guassians


    def fit_spectra_lmfit(self):

        # get information from the table and store in arrays
        pp = []
        pp_status = []
        ph = []
        ph_status = []
        pw = []
        pw_status = []
        EMin = float(self.xrange_min_line_edit.text())
        EMax = float(self.xrange_max_line_edit.text())
        pp_len = 0
        for i in range(int(self.tab1.table_clickpeaks.rowCount())):
            try:
                print(self.tab1.table_clickpeaks.item(i, 0).text())
                pp.append(float(self.tab1.table_clickpeaks.item(i, 0).text()))
                try:
                    if self.tab1.table_clickpeaks.item(i,1).text() == 'fixed':
                        pp_status.append(False)
                    else:
                        pp_status.append(True)
                except:
                    pp_status.append(True)


                pp_len += 1
            except:
                #print('end of line',i)
                temp = 1

        #checks reading the table

        if self.tab1.table_clickpeaks.item(0, 0) is None:
            # pop up box to say no peaks in the table
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("Peak Setup Error")
            error_message.showMessage("Error: No peaks in the peak table")
            return

        else:
            # fitting bit
            for i in range(pp_len+1):
                try:
                    ph.append(float(self.tab1.table_clickpeaks.item(i, 2).text()))
                    try:
                        if self.tab1.table_clickpeaks.item(i, 3).text() == 'fixed':
                            ph_status.append(False)
                        else:
                            ph_status.append(True)
                    except:
                        ph_status.append(True)

                    pw.append(float(self.tab1.table_clickpeaks.item(i, 4).text()))
                    try:
                        if self.tab1.table_clickpeaks.item(i, 5).text() == 'fixed':
                            pw_status.append(False)
                        elif self.tab1.table_clickpeaks.item(i,5).text() == 'shared':
                            pw_status.append('shared')
                        else:
                            pw_status.append(True)
                    except:
                        pw_status.append(True)

                except:
                    temp = 1

            #get backgorund info
            back = []
            try:
                back.append(float(self.tab1.table_poly.item(0, 0).text()))
                back.append(float(self.tab1.table_poly.item(0, 2).text()))
                back.append(float(self.tab1.table_poly.item(0, 4).text()))
            except:
                temp = 1


        # get and trim the correct data

        if globals.whichdet == 'GE1':
            datax, datay = Trimdata.Trimdata(self.data_x_GE1, self.data_y_GE1, EMin, EMax)
        elif globals.whichdet == 'GE2':
            datax, datay = Trimdata.Trimdata(self.data_x_GE2, self.data_y_GE2, EMin, EMax)
        elif globals.whichdet == 'GE3':
            datax, datay = Trimdata.Trimdata(self.data_x_GE3, self.data_y_GE3, EMin, EMax)
        elif globals.whichdet == 'GE4':
            datax, datay = Trimdata.Trimdata(self.data_x_GE4, self.data_y_GE4, EMin, EMax)

        print('data trimmed')

        def make_model(pp_len, pp, ph, pw, num, EMin, EMax, pp_status, ph_status, pw_status):
            pref = "f{0}_".format(num)
            model = GaussianModel(prefix=pref)
            print(ph_status)
            print(ph_status[num])
            print(pp_status)
            print(pp_status[num])
            print(pw_status)
            print(pw_status[num])

            model.set_param_hint(pref+'amplitude', value=ph[num], min=0, vary=ph_status[num])
            print('here')
            model.set_param_hint(pref+'center', value=pp[num], min = EMin, max=EMax, vary=pp_status[num])
            print('here2')
            if pw_status[num] == True:
                model.set_param_hint(pref+'sigma', value=pw[num], min = 0.01, max = 3.0 ,vary=True)
            elif pw_status[num] == 'shared':
                # need to add sharing
                #model.set_param_hint(pref+'sigma', value=pw[num], min = 0.01, max = 3.0, vary=True)
                model.set_param_hint(pref+'sigma', expr='f0_sigma')
            elif pw_status[num] == False:
                model.set_param_hint(pref+'sigma', value=pw[num], min = 0.01, max = 3.0, vary=False)
            return model

        # setting up the model

        mod = None
        for i in range(pp_len):
            this_mod = make_model(pp_len, pp, ph, pw, i, EMin, EMax, pp_status, ph_status, pw_status)
            if mod is None:
                mod = this_mod
            else:
                mod = mod + this_mod


        backgrd = QuadraticModel()
        # get fixed or not
        try:
            if self.tab1.table_poly.item(0,1).text() == 'fixed':
                avary = False
            else:
                avary = True
        except:
            avary = True

        try:
            if self.tab1.table_poly.item(0, 3).text() == 'fixed':
                bvary = False
            else:
                bvary = True
        except:
            bvary = True

        try:
            if self.tab1.table_poly.item(0, 5).text() == 'fixed':
                cvary = False
            else:
                cvary = True
        except:
            cvary = True

        backgrd.set_param_hint('a', value=back[2], vary=avary)
        backgrd.set_param_hint('b', value=back[1], vary=bvary)
        backgrd.set_param_hint('c', value=back[0], vary=cvary)

        # final model

        mod = mod + backgrd

        # fitting

        result = mod.fit(datay, x=datax, weights=1.0/np.sqrt(datay))

        print('results',result)
        print(result.fit_report())
        print(result.best_values["f0_amplitude"])
        print(result.best_values["f0_amplitude"])
        print(result.chisqr)
        print(result.covar)
        print('values',result.values)
        print('best values',result.best_values)
        print('error',result.params)

        # if unable to establish covariance, display error message
        if result.covar is None:
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("Peak Fit Error")
            error_message.showMessage("Error: Fit did not converge.")
            return

        else:
            print(f'{result.params["f0_amplitude"].value:11.5f} {result.params["f0_amplitude"].stderr:11.5f}')
            #calc chisq

            r = datay - result.best_fit
            chisq = sum((r / np.sqrt(datay)) ** 2)/len(datax)
            print('Chisq=',chisq)

        #write results to GUI
        for i in range(0, pp_len):
            try:
                pref = "f{0}_".format(i)
                self.tab1.table_clickpeaks.setItem(i, 0, QTableWidgetItem(
                    str("{:.3f}".format(result.best_values[pref+"center"]))))
                self.tab1.table_clickpeaks.setItem(i, 2, QTableWidgetItem(
                    str("{:.2f}".format(result.best_values[pref+"amplitude"]))))
                self.tab1.table_clickpeaks.setItem(i, 4, QTableWidgetItem(
                    str("{:.3f}".format(result.best_values[pref+"sigma"]))))


                if pp_status[i] == True:
                    self.tab1.table_clickpeaks.setItem(i, 1, QTableWidgetItem(
                        str("{:.3f}".format(result.params[pref+"center"].stderr))))

                if ph_status[i] == True:
                    self.tab1.table_clickpeaks.setItem(i, 3, QTableWidgetItem(
                        str("{:.1f}".format(result.params[pref+"amplitude"].stderr))))

                if pw_status[i] == True:
                    self.tab1.table_clickpeaks.setItem(i, 5, QTableWidgetItem(
                        str("{:.3f}".format(result.params[pref + "sigma"].stderr))))

            except:
                temp = 1

        self.tab1.table_poly.setItem(0, 0, QTableWidgetItem(
            str("{:.2f}".format(result.best_values["c"]))))
        self.tab1.table_poly.setItem(0, 2, QTableWidgetItem(
            str("{:.2f}".format(result.best_values["b"]))))
        self.tab1.table_poly.setItem(0, 4, QTableWidgetItem(
            str("{:.3f}".format(result.best_values["a"]))))
        if cvary:
            try:
                self.tab1.table_poly.setItem(0, 1, QTableWidgetItem(
                    str("{:.2f}".format(result.params["c"].stderr))))
            except:
                temp = 1
        if bvary:
            try:
                self.tab1.table_poly.setItem(0, 3, QTableWidgetItem(
                    str("{:.2f}".format(result.params["b"].stderr))))
            except:
                temp = 1

        if avary:
            try:
                self.tab1.table_poly.setItem(0, 5, QTableWidgetItem(
                    str("{:.3f}".format(result.params["a"].stderr))))
            except:
                temp = 1


        #plot results

        # removes previous plot if it exists
        try:
            self.ln.remove()
            self.lnr.remove()
            self.ln, = plt.plot(datax, result.best_fit, label="best fit")
            self.lnr, = plt.plot(datax, datay - result.best_fit, label='Residual')
        except:
            self.ln, = plt.plot(datax, result.best_fit, label="best fit")
            self.lnr, = plt.plot(datax, datay - result.best_fit, label='Residual')

        plt.draw()
        #print(np.min(datay-result.best_fit))
        if np.max(datay)> np.max(result.best_fit):
            maxy = np.max(datay)+0.05*np.max(datay)
        else:
            maxy = np.max(result.best_fit)+0.05*np.max(result.best_fit)

        self.axs_ana[0].set_ylim(
            [np.min(datay-result.best_fit)-0.05*(np.min(datay-result.best_fit)), maxy])
        plt.axvline(EMin, color='red', linestyle='--')
        plt.axvline(EMax, color='red', linestyle='--')
        plt.legend()

        self.plot.canvas.draw()


        # write results to file

        # Summary output

        fname = globals.workingdirectory + '/' + str(globals.RunNum) + '_' + globals.whichdet + '.sum'
        print(fname)

        with open(fname, 'w') as f:
            f.write('Analysis Summary')
            f.write(result.fit_report())
            f.writelines(" " + "\n")
            f.writelines(" " + "\n")
            f.write("Best fit results" + "\n")
            norows = len(datax)
            for i in range(norows):
                line = str(datax[i]) + ' ' + str(result.best_fit[i]) + "\n"
                f.writelines(line)

        f.close()

        # writing fit results to a separate file

        fname = globals.workingdirectory + '/' + str(globals.RunNum) + '_' + globals.whichdet + '.fit'
        print(fname)
        with open(fname, 'w') as f:
            norows = len(datax)
            for i in range(norows):
                line = str(datax[i])+' '+str(result.best_fit[i])+"\n"
                f.writelines(line)
        f.close()








