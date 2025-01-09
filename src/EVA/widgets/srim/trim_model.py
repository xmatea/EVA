from random import sample

import numpy as np
from PyQt6.QtCore import pyqtSignal, QObject
from matplotlib import pyplot as plt

from EVA.core.app import get_config
from srim import TRIM, Ion, Layer, Target


class TrimModel(QObject):
    simulation_error_s = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # SRIM result
        self.result_x = []
        self.result_y = []

        # Layer information
        self.sample_layers = None
        self.sample_names = []
        self.total_thickness = 0

        self.components = []
        self.momentum = []

    def trim_simulation(self, sample_name, stats, srim_dir, output_dir, momentum, momentum_spread, sim_type,
                        min_momentum, max_momentum, step_momentum, scan_type, layers):

        # update config to save the directory
        config = get_config()
        config["SRIM"]["installation_directory"] = srim_dir
        config["SRIM"]["output_directory"] = output_dir

        # Set up sample from layers
        self.SetupSample(layers)
        targetsample = Target(self.sample_layers)

        # Calculate momentum if momentum scan is wanted
        if scan_type == 'Yes':
            self.momentum = list(self.my_range(min_momentum, max_momentum, step_momentum))
        else:
            self.momentum = [momentum]

        # Run TRIM for each momentum
        self.components = []
        self.result_x = []
        self.result_y = []

        for momentum_index, mom in enumerate(self.momentum):
            if sim_type == 'Mono':
                # get muon information
                muon_ion = self.iondef(mom)
                x, y, e = self.RunTRIM(targetsample, self.total_thickness, muon_ion, stats, srim_dir,
                                                 output_dir)
            elif sim_type == 'Momentum Spread':
                x, y = self.CalcProfileWithMomBite(
                    targetsample, self.total_thickness, mom, stats, momentum_spread, srim_dir, output_dir)
            else:
                raise ValueError("Invalid simulation type specified")

            self.result_x.append(x)
            self.result_y.append(y)

            # break to components to get %
            xposlist = self.getxpos()
            comp = self.getcomp(xposlist, momentum_index)
            perlayer = self.getperlayer(comp)
            outstr = ''
            for index in range(len(self.sample_layers)):
                outstr += '[' + str(index + 1) + '] ' + str(round(perlayer[index], 3)) + ' '

            self.components.append(outstr)

        print(len(self.components))
        print(len(self.momentum))

    def my_range(self, start, end, step):
        # sets a reange of momenta
        while start <= end:
            yield start
            start += step

    def SetupSample(self, layers):
        ''' Sets up the sample layers '''

        i = 0
        sample_layers = []
        sample_names = []
        total_thickness = 0.0

        for layer in layers:
            sample_name = layer["name"]
            if sample_name == 'Beamline Window':
                layer_thickness = layer["thickness"]
                total_thickness =+ layer_thickness
                beamwindow = Layer({'H': {'stoich': 8, 'E_d': 10, 'lattice': 3, 'surface': 2
                                          },
                                    'C': {'stoich': 10, 'E_d': 28.0, 'lattice': 3.0,
                                          'surface': 7.41
                                          },
                                    'O': {'stoich': 4, 'E_d': 28.0, 'lattice': 3.0,
                                          'surface': 2.0}},
                                   density=1.4, width=layer_thickness * 1e7, phase=0)
                sample_layers.append(beamwindow)
                sample_names.append('Beamline Window')

            elif sample_name == 'Air (compressed)':

                layer_thickness = layer["thickness"]
                total_thickness =+ total_thickness

                air = Layer({'C': {'stoich': 1.24e-2, 'E_d': 28.0, 'lattice': 3.0,
                                   'surface': 7.41
                                   },
                             'O': {'stoich': 23.1781, 'E_d': 28.0, 'lattice': 3.0,
                                   'surface': 2.0
                                   },
                             'N': {'stoich': 75.5268, 'E_d': 28.0, 'lattice': 3.0,
                                   'surface': 2.0
                                   },
                             'Ar': {'stoich': 1.2827, 'E_d': 5.0, 'lattice': 1.0,
                                    'surface': 2.0}}, density=1500 * 1.20479e-3, width=layer_thickness * 1e7,
                            # air layer compressed from 150mm to 0.1mm to optimise bins
                            phase=1)
                sample_layers.append(air)
                sample_names.append('Air (compressed)')
                print('done air')
                print(sample_layers)
            else:
                sampledensity = layer["density"]
                layer_thickness = layer["thickness"]
                total_thickness = + layer_thickness
                thislayer = Layer.from_formula(sample_name, density=sampledensity, width=layer_thickness * 1e7,
                                                      phase=0)

                sample_layers.append(thislayer)  # 0.016 mm = 160000Athick sample holder
                sample_names.append(sample_name)

        self.sample_layers = sample_layers
        self.sample_names = sample_names
        self.total_thickness = total_thickness

    def iondef(self, Mom:float):
        '''muon properties, mass and energy'''
        muM = 105.6583745  # mass o muon in MeV/c^2
        muMA = muM / 931.5  # mass of muon in atomic mass units
        # kintetic energy associatd with the momentum (relitavistic)
        Ek = np.sqrt(105.6583745 ** 2 + Mom ** 2) - 105.6583745

        print('Momentum=' + str(Mom) + ' Energy=' + str(Ek))

        # corresponding SRIM muon ion definitions
        muon_ion = Ion('H', Ek * 1e6,
                       muMA)  # define muon as Hydrogen ion with mass of muon, with a given kinetic energy

        print('muon_ion', muon_ion, muMA)


        return muon_ion


    def RunTRIM(self, target, TotalThickness, muon_ion, number_muon, SRIMdirectory, output_directory):
        '''Run TRIM and output results in x1, y1, e1'''
        print('in runtrim')

        print(muon_ion)
        print(number_muon)
        print('dir', SRIMdirectory)

        trimsim = TRIM(target, muon_ion, number_ions=number_muon, calculation=1)


        try:
            trimdataoutput = trimsim.run(SRIMdirectory)  # Simulation run by executing SRIM.exe in directory

            TRIM.copy_output_files(SRIMdirectory,
                                   output_directory)  # ouput files from SRIM copied to desired output directory
        except FileNotFoundError:
            return

        trimdata = trimdataoutput.range

        x1 = list(trimdata.depth / 1e7)  # muon ranges, converted from angstroms to mm.

        y1 = list(trimdata.ions)  # SRIM has weird units for y axis

        y1 = self.CorrectToCounts(TotalThickness, y1,number_muon)

        e1 = list(trimdata.ions)

        return x1, y1, e1

    def CorrectToCounts(self, thickness, y1, TotalSimCounts):
        ''' output of SRIM is odd this corrects it to counts'''
        finalbins = thickness / 100.0
        for i in range(len(y1)):
            y1[i] = y1[i] * finalbins * TotalSimCounts
        return y1

    def CalcProfileWithMomBite(self, sample, TotalThickness, Mom, NFinal, Mombite, SRIMdirectory, output_directory):
        # Calculate the stopping profile for a nomial momentum with a % momentum bite defined
        # in BeamParameters

        print('in here')

        sigmastep = 12  # 12 runs per momentum
        MomSigma = 0.01 * Mombite * Mom

        xres = []
        yres = []
        eres = []

        for i in range(sigmastep + 1):
            P = Mom - 3 * MomSigma + i * 0.5 * MomSigma  # momentum for each iteration
            print('P', P)

            # Number of simulated muons dependent on Gaussian distribution of muon momentum
            # get muon information
            muon_ion = self.iondef(P)

            NE = int(NFinal * (1.0 / (np.sqrt(2.0 * np.pi) * MomSigma)) * np.exp(
                -0.5 * (P - Mom) ** 2 / (MomSigma ** 2)))
            print('Number of Counts', NE)

            x1, y1, e1 = self.RunTRIM(sample, TotalThickness, muon_ion, NE, SRIMdirectory, output_directory)

            if i == 0:
                yres = y1
                xres = x1
            else:
                for index in range(0, len(y1)):
                    yres[index] = yres[index] + y1[index]

        return xres, yres

    def getxpos(self):
        '''gets xpos from layers must be an easier way'''
        xposlist = []
        xposlist.append(0.0)

        for i in range(len(self.sample_layers)):
            temp = self.sample_layers[i]
            loc = str(temp).find('width:')
            xpos = float(str(temp)[loc + 6:].strip('>')) / 1e7
            xposlist.append(xpos)
        # print('xposlist', xposlist)
        return xposlist

    def getcomp(self, xposlist, MomIndex):
        ''' break the SRIM output into components'''
        comp = []
        sum1 = 0.0
        sum2 = 0.0
        print('result x', self.result_x)
        print('result y', self.result_y)
        for i in range(len(self.sample_layers)):
            templist = []
            sum1 += xposlist[i]
            sum2 = sum1 + xposlist[i + 1]
            for j in range(len(self.result_y[MomIndex])):
                if self.result_x[MomIndex][j] >= sum1 and self.result_x[MomIndex][j] < sum2:
                    templist.append(self.result_y[MomIndex][j])
                else:
                    templist.append(0.0)
            comp.append(templist)
        print('comp', comp)
        return comp

    def getperlayer(self, comp):
        ''' gets the number of muons in a layer (normalised)'''
        perlayer = []
        totalsumlayer = 0.0

        for index in range(len(self.sample_layers)):
            sumlayer = np.sum(comp[index])
            perlayer.append(sumlayer)
            totalsumlayer += sumlayer

        for index in range(len(self.sample_layers)):
            perlayer[index] = perlayer[index] / totalsumlayer
        print('perlayer', perlayer)

        return perlayer

    def plot_whole(self, row, momentum):
        figt, axx = plt.subplots()
        axx.plot(self.result_x[row], self.result_y[row])
        axx.set_xlabel('Depth ($mm$)')
        axx.set_ylabel('Number of muons')
        axx.set_title('SRIM Simulation at ' + momentum + ' MeV/c')
        xposlist = self.getxpos()

        # plot layers out plot
        sumdis = 0.0
        for i in range(len(self.sample_layers)):
            sumdis += xposlist[i + 1]

            axx.axvline(x=sumdis, color='k', linestyle='--')
            axx.text(sumdis, 5, self.sample_names[i], horizontalalignment='left', rotation='vertical')
            print('sample_layers', self.sample_layers[i])

        return figt, axx

    def plot_components(self, momentum_index, momentum):
        # plot components
        figt, axx = plt.subplots()
        axx.plot(self.result_x[momentum_index], self.result_y[momentum_index])
        axx.set_xlabel('Depth ($mm$)')
        axx.set_ylabel('Number of muons')
        axx.set_title('SRIM Simulation at ' + momentum + ' MeV/c')

        xposlist = self.getxpos()

        # plot layers out plot
        sumdis = 0.0
        for i in range(len(self.sample_layers)):
            sumdis += xposlist[i + 1]

            axx.axvline(x=sumdis, color='k', linestyle='--')
            axx.text(sumdis, 5, self.sample_names[i], horizontalalignment='left', rotation='vertical')

        # break output down to components
        comp = self.getcomp(xposlist, momentum_index)

        # plot layers
        for i in range(len(self.sample_layers)):
            axx.plot(self.result_x[0], comp[i])

        return figt, axx

    def save_sim(self, row):
        '''
        :param x: button layer
        :param y: button column
        :return:
        writes the results of SRIM TRIM calcs
        '''
        momentum = str(self.momentum[row])
        print(get_config()["general"]["working_directory"])
        print('working dir', print(get_config()["general"]["working_directory"]))
        print('')
        save_file = get_config()["general"]["working_directory"] + '/SRIM_' + momentum + '_MeVc.dat'
        print('Sve_file',save_file)
        file2 = open(save_file, "w")

        sumdis = 0.0
        xposlist = self.getxpos()

        for i in range(len(self.sample_layers)):
            sumdis += xposlist[i + 1]
            print(self.sample_names[i] + ' = ' + str(sumdis) + '\n')
            file2.writelines(self.sample_names[i] + ' = ' + str(sumdis) + '\n')


        for i in range(len(self.result_x[row])):
            file2.writelines(str(self.result_x[row][i]) + ',' + str(self.result_y[row][i]) + '\n')
        '''file2.writelines(str(srim_settings.TRIMRes_x[x]) + ',' + str(srim_settings.TRIMRes_y[x]))
        '''
        file2.close()
        print('save_file_fin')

        print('In WriteSim')
        print(get_config()["general"]["working_directory"])
        print('')
        print('')
        comp = self.getcomp(xposlist, row)

        # plot layers
        for i in range(len(self.sample_layers)):

            save_file = (get_config()["general"]["working_directory"] + '/SRIM_'
                         + momentum + '_MeVc_' + str(i) + '.dat')
            print('Sve_file', save_file)
            file2 = open(save_file, "w")

            sumdis = 0.0
            xposlist = self.getxpos()

            for k in range(len(self.sample_layers)):
                sumdis += xposlist[k + 1]
                print(self.sample_names[k] + ' = ' + str(sumdis) + '\n')
                file2.writelines(self.sample_names[k] + ' = ' + str(sumdis) + '\n')

            for j in range(len(self.result_x[row])):
                file2.writelines(str(self.result_y[row][j]) + ',' + str(comp[i][j]) + '\n')
        '''file2.writelines(str(srim_settings.TRIMRes_x[x]) + ',' + str(srim_settings.TRIMRes_y[x]))
        '''
        file2.close()
        print('save_file_fin')