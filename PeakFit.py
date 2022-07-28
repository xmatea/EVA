import math

import Trimdata
import peakfit_bounds_define
from lmfit import Parameters, Model
from lmfit.models import GaussianModel, QuadraticModel

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QTabWidget,
    QErrorMessage,
)

import globals
import Plot_Spectra
import numpy as np
from scipy.optimize import curve_fit

import peakfit_bounds_define
import peakfitdemo


class PeakFit(QWidget):
    """
        This window is the GUI for the PeakFit window

        """


    def __init__(self, parent = None):
        super(PeakFit,self).__init__(parent)

        # get data and run info and store locally
        # move to a separate routine

        self.data_x_GE1 = 0
        self.data_x_GE2 = 0
        self.data_x_GE3 = 0
        self.data_x_GE4 = 0
        self.data_y_GE1 = 0
        self.data_y_GE2 = 0
        self.data_y_GE3 = 0
        self.data_y_GE4 = 0
        print('Norm', globals.Normalise_do_not,globals.Normalise_counts,globals.Normalise_spill)

        if globals.Normalise_do_not:
            if globals.plot_GE1:
                self.data_x_GE1 = globals.x_GE1
                self.data_y_GE1 = globals.y_GE1
            if globals.plot_GE2:
                self.data_x_GE2 = globals.x_GE2
                self.data_y_GE2 = globals.y_GE2
            if globals.plot_GE3:
                self.data_x_GE3 = globals.x_GE3
                self.data_y_GE3 = globals.y_GE3
            if globals.plot_GE4:
                self.data_x_GE4 = globals.x_GE4
                self.data_y_GE4 = globals.y_GE4
        elif globals.Normalise_counts:
            if globals.plot_GE1:
                self.data_x_GE1 = globals.x_GE1_Ncounts
                self.data_y_GE1 = globals.y_GE1_Ncounts
            if globals.plot_GE2:
                self.data_x_GE2 = globals.x_GE2_Ncounts
                self.data_y_GE2 = globals.y_GE2_Ncounts
            if globals.plot_GE3:
                self.data_x_GE3 = globals.x_GE3_Ncounts
                self.data_y_GE3 = globals.y_GE3_Ncounts
            if globals.plot_GE4:
                self.data_x_GE4 = globals.x_GE4_Ncounts
                print('GE4', self.data_x_GE4)
                self.data_y_GE4 = globals.y_GE4_Ncounts
        elif globals.Normalise_spill:
            if globals.plot_GE1:
                self.data_x_GE1 = globals.x_GE1_NEvents
                self.data_y_GE1 = globals.y_GE1_NEvents
            if globals.plot_GE2:
                self.data_x_GE2 = globals.x_GE2_NEvents
                self.data_y_GE2 = globals.y_GE2_NEvents
            if globals.plot_GE3:
                self.data_x_GE3 = globals.x_GE3_NEvents
                self.data_y_GE3 = globals.y_GE3_NEvents
            if globals.plot_GE4:
                self.data_x_GE4 = globals.x_GE4_NEvents
                self.data_y_GE4 = globals.y_GE4_NEvents

        self.resize(1200, 1100)
        self.setMinimumSize(1400, 1250)
        self.setWindowTitle("Peak Fitting Window: Run Number " + str(globals.RunNum) + " Det: " + globals.whichdet)

        # label for offset
        lab_multi_offset = QLabel(self)
        lab_multi_offset.setText('Fitting Range (Min, Max):')
        lab_multi_offset.move(550, 115)

        # XMin and XMax
        self.val_fit_XMin = QLineEdit(self)
        self.val_fit_XMin.setText('180.0')
        self.val_fit_XMin.move(650, 110)

        self.val_fit_XMax = QLineEdit(self)
        self.val_fit_XMax.setText('200.0')
        self.val_fit_XMax.move(850, 110)

        # sets up button
        plot_fit = QPushButton(self)
        plot_fit.setText('Fit Currently loaded Spectra')
        plot_fit.move(100,100)
        plot_fit.clicked.connect(
            lambda: self.fit_spectra_lmfit())
        '''plot_fit.clicked.connect(
            lambda: self.fit_spectra())'''

        # Initialize tab screen
        print('initialising tabs')
        self.tabs = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(1200, 1000)
        self.tabs.move(100,200)


        # Add tabs
        self.tabs.addTab(self.tab1, "Individual Peak Fit")
        self.tabs.addTab(self.tab2, "Element Search")

        self.tab1.label_Element = QLabel("Peaks:"
                                         , self.tab1)
        self.tab1.label_Element.move(10, 10)
        self.tab1.label_Element.show()

        # Create first tab
        # table for all peaks

        self.tab1.table_clickpeaks = QTableWidget(self.tab1)
        self.tab1.table_clickpeaks.setShowGrid(True)
        self.tab1.table_clickpeaks.setColumnCount(6)
        self.tab1.table_clickpeaks.setRowCount(100)
        self.tab1.table_clickpeaks.move(50,50)
        self.tab1.table_clickpeaks.setMinimumSize(1050,500)
        self.tab1.table_clickpeaks.verticalScrollBar()
        #self.tab1.table_clickpeaks.
        self.tab1.table_clickpeaks.setHorizontalHeaderLabels(
            ['Position (keV)','Error', 'Area','Error', 'Width', 'Error'])
        self.tab1.table_clickpeaks.setColumnWidth(0, 250)
        self.tab1.table_clickpeaks.setColumnWidth(1, 50)
        self.tab1.table_clickpeaks.setColumnWidth(2, 150)
        self.tab1.table_clickpeaks.setColumnWidth(3, 50)
        self.tab1.table_clickpeaks.setColumnWidth(4, 150)
        self.tab1.table_clickpeaks.setColumnWidth(5, 50)

        self.tab1.table_clickpeaks.show()

        self.tab1.label_Element = QLabel("Polynomial Background:"
                                         , self.tab1)
        self.tab1.label_Element.move(10, 560)
        self.tab1.label_Element.show()

        # table for background polynomial

        self.tab1.table_poly = QTableWidget(self.tab1)
        self.tab1.table_poly.setShowGrid(True)
        self.tab1.table_poly.setColumnCount(6)
        self.tab1.table_poly.setRowCount(1)
        self.tab1.table_poly.move(50,600)
        self.tab1.table_poly.setMinimumSize(1050,275)
        self.tab1.table_poly.verticalScrollBar()
        #self.tab1.table_clickpeaks.
        self.tab1.table_poly.setHorizontalHeaderLabels(
            ['Const','Error','1st','Error', '2nd','Error'])
        self.tab1.table_poly.setColumnWidth(0, 150)
        self.tab1.table_poly.setColumnWidth(1, 170)
        self.tab1.table_poly.setColumnWidth(2, 80)
        self.tab1.table_poly.setItem(0,0, QTableWidgetItem(str(25)))
        self.tab1.table_poly.setItem(0, 2, QTableWidgetItem(str(0.001)))
        self.tab1.table_poly.setItem(0, 4, QTableWidgetItem(str(0.0)))

        self.tab1.table_clickpeaks.show()



        print('here')
        title_lab = "Analysis of RunNum: " + str(globals.RunNum) + "Det: " + globals.whichdet

        # plot and activate cool plot
        PeakFit.PlotAnalysisSpectra(self,title_lab)

        print("return")

        self.show()

    def PlotAnalysisSpectra(self,title_lab):

        print('globals.whichdet', globals.whichdet)

        #gets current status of global plots

        memoryGE1 = globals.plot_GE1
        memoryGE2 = globals.plot_GE2
        memoryGE3 = globals.plot_GE3
        memoryGE4 = globals.plot_GE4

        if (globals.whichdet == 'GE1'):
            globals.plot_GE1 = True
            globals.plot_GE2 = False
            globals.plot_GE3 = False
            globals.plot_GE4 = False
        if (globals.whichdet == 'GE2'):
            globals.plot_GE1 = False
            globals.plot_GE2 = True
            globals.plot_GE3 = False
            globals.plot_GE4 = False
        if (globals.whichdet == 'GE3'):
            globals.plot_GE1 = False
            globals.plot_GE2 = False
            globals.plot_GE3 = True
            globals.plot_GE4 = False
        if (globals.whichdet == 'GE4'):
            globals.plot_GE1 = False
            globals.plot_GE2 = False
            globals.plot_GE3 = False
            globals.plot_GE4 = True

        print(self.data_x_GE1, self.data_y_GE1)

        self.fig_ana, self.axs_ana, self.plt_ana = Plot_Spectra.Plot_Spectra3(self.data_x_GE1, self.data_y_GE1,
                                                   self.data_x_GE2, self.data_y_GE2,
                                                   self.data_x_GE3, self.data_y_GE3,
                                                   self.data_x_GE4, self.data_y_GE4, title_lab)

        self.plt_ana.show()

        # changes the xlimits of each subplot
        i = 0
        for i in range(len(self.axs_ana)):
            self.axs_ana[i].set_xlim([float(self.val_fit_XMin.text())-5.0, float(self.val_fit_XMax.text())+5.0])
            i += 1

        self.plt_ana.show()

        # returns settings

        globals.plot_GE1 = memoryGE1
        globals.plot_GE2 = memoryGE2
        globals.plot_GE3 = memoryGE3
        globals.plot_GE4 = memoryGE4

        def on_click(event):

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
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if buttonReply == QMessageBox.Yes:
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

        self.plt_ana.connect('button_press_event', on_click)

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
        EMin = float(self.val_fit_XMin.text())
        EMax = float(self.val_fit_XMax.text())
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

        if pp_len == 0:
            # pop up box to say no peaks in the table
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("Peak Setup Error")
            error_message.showMessage("Error: No peaks in the peak table")

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
                datax, datay = Trimdata.Trimdata(self.data_x_GE1,self.data_y_GE1, EMin, EMax)
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

            bound_all = peakfit_bounds_define.define_bounds(pp_len,EMin,EMax,back)

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
            self.plt_ana.plot(datax, multiGaussianFunc(datax, *popt), label="gaussian")
            self.plt_ana.axvline(EMin, color='red', linestyle='--')
            self.plt_ana.axvline(EMax, color='red', linestyle='--')
            self.plt_ana.legend()
            self.plt_ana.show()
            self.fig_ana.canvas.draw()


            # Generate function
            # Guassians


    def fit_spectra_lmfit(self):

        def gaussian(x, mu, sigma, a, c):
            return a / sigma / np.sqrt(2 * np.pi) * np.exp(-(x - mu) ** 2 / 2 / sigma ** 2) + c

        def gaussian2(x, mu, sigma, a, c):
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

        def multiGaussianFunc_lmfit(x, *params):
            y = np.zeros_like(x)
            print('hello')
            print('params',params)
            print('len of params',len(params))
            for i in range(0, len(params)-3, 3):
                ctr = params[i]
                amp = params[i+1]
                wid = params[i+2]
                y = y + amp / wid / np.sqrt(2 * np.pi) * np.exp(-((x - ctr) / 2/ wid) ** 2)
            a = params[len(params)-3]
            '''b = params[len(params)-2]
            c = params[len(params)-1]'''
            y = y + a #+ b * x + c * x * x
            return y


        para = Parameters()
        para.add('mu',value=190,vary=True,min=180,max=220)
        para.add('a', value=200, vary=True, min=0)
        para.add('sigma', value= 1.5,vary=True,min=0.1,max=3.0)
        '''para.add('a',value=1,vary=True,min=0)
        para.add('b',value=1,vary=True,min=0)'''
        para.add('c',value=1,vary=True,min=0)


        # get information from the table and store in arrays
        pp = []
        ph = []
        pw = []
        EMin = float(self.val_fit_XMin.text())
        EMax = float(self.val_fit_XMax.text())
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

        if pp_len == 0:
            # pop up box to say no peaks in the table
            error_message = QErrorMessage(self)
            error_message.setWindowTitle("Peak Setup Error")
            error_message.showMessage("Error: No peaks in the peak table")

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
            datax, datay = Trimdata.Trimdata(self.data_x_GE1,self.data_y_GE1, EMin, EMax)
        elif globals.whichdet == 'GE2':
            datax, datay = Trimdata.Trimdata(self.data_x_GE2, self.data_y_GE2, EMin, EMax)
        elif globals.whichdet == 'GE3':
            datax, datay = Trimdata.Trimdata(self.data_x_GE3, self.data_y_GE3, EMin, EMax)
        elif globals.whichdet == 'GE4':
            datax, datay = Trimdata.Trimdata(self.data_x_GE4, self.data_y_GE4, EMin, EMax)

        print('data trimmed')

        def make_model(pp_len, pp, ph, pw, num, EMin, EMax):
            pref = "f{0}_".format(num)
            model = GaussianModel(prefix = pref)
            model.set_param_hint(pref+'amplitude', value=ph[num], min =0)
            model.set_param_hint(pref+'center', value=pp[num], min = EMin, max = EMax)
            model.set_param_hint(pref+'sigma', value=pw[num], min = 0.01, max = 3.0)
            return model

        mod = None


        for i in range(pp_len):
            this_mod = make_model(pp_len, pp, ph, pw, i, EMin, EMax)
            if mod is None:
                mod = this_mod
            else:
                mod = mod + this_mod


        backgrd = QuadraticModel()
        backgrd.set_param_hint('a', value = back[2])
        backgrd.set_param_hint('b', value = back[1])
        backgrd.set_param_hint('c', value = back[0])

        mod = mod + backgrd


        result = mod.fit(datay,x=datax)

        print('results',result)
        print(result.fit_report())







        #calc chisq

        '''r = datay - multiGaussianFunc(datax, *popt)
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
        self.tab1.table_poly.setItem(0, 5, QTableWidgetItem(str(perr[para_len - 1])))'''

        #plot results

        # removes previous plot if it exists
        try:
            self.ln.remove()
            self.lnr.remove()
            self.ln, = self.plt_ana.plot(datax, result.best_fit, label="best fit")
            self.lnr, = self.plt_ana.plot(datax, datay - result.best_fit, label='Residual')
        except:
            self.ln, = self.plt_ana.plot(datax, result.best_fit, label="best fit")
            self.lnr, = self.plt_ana.plot(datax, datay - result.best_fit, label='Residual')

        self.plt_ana.draw()
        #print(np.min(datay-result.best_fit))
        if np.max(datay)> np.max(result.best_fit):
            maxy = np.max(datay)+0.05*np.max(datay)
        else:
            maxy = np.max(result.best_fit)+0.05*np.max(result.best_fit)

        self.axs_ana[0].set_ylim(
            [np.min(datay-result.best_fit)-0.05*(np.min(datay-result.best_fit)), maxy])
        self.plt_ana.axvline(EMin, color='red', linestyle='--')
        self.plt_ana.axvline(EMax, color='red', linestyle='--')
        self.plt_ana.legend()
        self.plt_ana.show()
        self.fig_ana.canvas.draw()


            # Generate function
            # Guassians





