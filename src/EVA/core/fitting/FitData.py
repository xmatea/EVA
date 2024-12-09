import numpy as np
from lmfit.models import GaussianModel, LinearModel, QuadraticModel

from EVA.util.Trimdata import Trimdata


def gaussian(x, mu, sigma, a, c):
    return a / sigma / np.sqrt(2 * np.pi) * np.exp(-(x - mu) ** 2 / 2 / sigma ** 2) + c

def multiGaussianFunc(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params) - 3, 3):
        ctr = params[i]
        amp = params[i + 1]
        wid = params[i + 2]
        y = y + amp / wid / np.sqrt(2 * np.pi) * np.exp(-((x - ctr) / 2 / wid) ** 2)
    a = params[len(params) - 3]
    b = params[len(params) - 2]
    c = params[len(params) - 1]

    y = y + a + b * x + c * x * x
    return y

def fit_gaussian_lmfit(x_data, y_data, params):
    background = params["background"]

    model = QuadraticModel(prefix="background_", nan_policy="omit")
    model.set_param_hint("a", **background["a"])
    model.set_param_hint("b", **background["b"])
    model.set_param_hint("c", **background["c"])

    for name, params in params.items():
        if name == "background": # ignore background parameters
            continue

        peak_model = GaussianModel(prefix=f"{name}_", nan_policy="omit")
        peak_model.set_param_hint("center", **params["center"])
        peak_model.set_param_hint("sigma", **params["sigma"])
        peak_model.set_param_hint("amplitude", **params["amplitude"])

        model += peak_model

    if len(model.param_names) > len(x_data):
        raise TypeError("Not enough points")

    fit_res = model.fit(y_data, x=x_data, weights=1/np.sqrt(y_data))
    return fit_res

def fit_spectra_lmfit(self, mean, sigma, area):

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
    '''
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
    '''

