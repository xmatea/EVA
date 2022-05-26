from PyQt5.QtWidgets import (
    QCheckBox,
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QGridLayout,
    QComboBox,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QApplication,
)
import PyQt5.QtGui
import globals
import numpy as np
from srim import TRIM, Ion, Layer, Target, Material
from srim.output import Results
import matplotlib.pyplot as plt


class RunSimTRIMSRIM(QWidget):

    def __init__(self, parent = None):
        print('here')
        super(RunSimTRIMSRIM, self).__init__(parent)
        print('here')

        self.resize(1400, 1400)
        self.setMinimumSize(1400, 1400)
        self.setWindowTitle("TRIM Simulations")

        # setting up buttons
        self.RunTrimSimulation = QPushButton("Run Simulations")
        self.RunTrimSimulation.clicked.connect(
            lambda: self.RunTrimSim(SampleName,
                                    SimType,
                                    Momentum,
                                    MomentumSpread,
                                    ScanType,
                                    MinMomentum,
                                    MaxMomentum,
                                    StepMomentum,
                                    SRIMdir,
                                    TRIMOutDir,
                                    Stats,
                                    ))

        print('done a button')

        # Setting up defaults (to add load from file)
        SampleName = QLineEdit('Cu')
        SimType = QComboBox()
        SimType.addItem('Mono')
        SimType.addItem('Momentum Spread')
        Momentum = QLineEdit('27.0')
        MomentumSpread = QLineEdit('4.0')
        ScanType = QComboBox()
        ScanType.addItem('No')
        ScanType.addItem('Yes')
        MinMomentum = QLineEdit('21.0')
        MaxMomentum = QLineEdit('30.0')
        StepMomentum = QLineEdit('1.0')
        SRIMdir = QLineEdit('c:/SRIM2013')
        TRIMOutDir = QLineEdit('c:/SRIM2013/SRIM Outputs')
        Stats = QLineEdit('100')



        self.layout = QGridLayout()
        self.layout.addWidget(QLabel('Sample Name'), 1, 0)
        self.layout.addWidget(QLabel('Simulation Type'), 2, 0)
        self.layout.addWidget(QLabel('Momentum'), 3, 0)
        self.layout.addWidget(QLabel('Momentum Spread'), 4, 0)
        self.layout.addWidget(QLabel('Scan Momentum'), 5, 0)
        self.layout.addWidget(QLabel('Min Momentum'), 6, 0)
        self.layout.addWidget(QLabel('Max Momentum'), 7, 0)
        self.layout.addWidget(QLabel('Momentum Step'), 8, 0)
        self.layout.addWidget(QLabel('SRIM.exe directory'), 9, 0)
        self.layout.addWidget(QLabel('TRIM output directory'), 10, 0)
        self.layout.addWidget(QLabel('Stats for optimal Run'), 11, 0)

        self.layout.addWidget(SampleName, 1, 1)
        self.layout.addWidget(SimType, 2, 1)
        self.layout.addWidget(Momentum, 3, 1)
        self.layout.addWidget(MomentumSpread, 4, 1)
        self.layout.addWidget(ScanType, 5, 1)
        self.layout.addWidget(MinMomentum, 6, 1)
        self.layout.addWidget(MaxMomentum, 7, 1)
        self.layout.addWidget(StepMomentum, 8, 1)
        self.layout.addWidget(SRIMdir, 9, 1)
        self.layout.addWidget(TRIMOutDir, 10, 1)
        self.layout.addWidget(Stats, 11, 1)
        print(SampleName.text())


        self.layout.addWidget(self.RunTrimSimulation, 12, 0)

        print('done a button')

        # Initialize tab screen
        print('initialising tabs')
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(1200, 1200)
        self.tabs.move(0, 0)


        # Add tabs
        self.tabs.addTab(self.tab1, "Layers")
        self.tabs.addTab(self.tab2, "Results")
        self.tabs.resize(1000, 1000)

        self.tab1.table_TRIMsetup = QTableWidget(self.tab1)
        self.tab1.table_TRIMsetup.resize(1000,500)
        self.tab1.table_TRIMsetup.setShowGrid(True)
        self.tab1.table_TRIMsetup.setColumnCount(3)
        self.tab1.table_TRIMsetup.setRowCount(10)

        self.tab1.table_TRIMsetup.setHorizontalHeaderLabels(['Sample', 'Thickness (mm)', 'Density'])
        self.tab1.table_TRIMsetup.setItem(0, 0, QTableWidgetItem('Beamline Window'))
        self.tab1.table_TRIMsetup.setItem(0, 1, QTableWidgetItem('0.05'))
        self.tab1.table_TRIMsetup.setItem(1, 0, QTableWidgetItem('Air (compressed)'))
        self.tab1.table_TRIMsetup.setItem(1, 1, QTableWidgetItem('0.067'))
        self.tab1.table_TRIMsetup.setItem(2, 0, QTableWidgetItem('Al'))
        self.tab1.table_TRIMsetup.setItem(2, 1, QTableWidgetItem('0.05'))
        self.tab1.table_TRIMsetup.setItem(2, 2, QTableWidgetItem('2.7'))
        self.tab1.table_TRIMsetup.setItem(3, 0, QTableWidgetItem('Cu'))
        self.tab1.table_TRIMsetup.setItem(3, 1, QTableWidgetItem('0.5'))
        self.tab1.table_TRIMsetup.setItem(3, 2, QTableWidgetItem('6.7'))

        self.tab2.table_PlotRes = QTableWidget(self.tab2)
        self.tab2.table_PlotRes.resize(1000,500)
        self.tab2.table_PlotRes.setShowGrid(True)
        self.tab2.table_PlotRes.setColumnCount(4)
        self.tab2.table_PlotRes.setRowCount(100)


        self.tab2.table_PlotRes.setHorizontalHeaderLabels(
            ['Momentum', '% Component', 'Plot Results (Com)', 'Plot Results2'])

        for index in range(self.tab2.table_PlotRes.rowCount()):
            for col in range(2):
                btn = QPushButton()
                btn.clicked.connect(lambda _, r=index, c= col+2: RunSimTRIMSRIM.PlotSim(self, r, c))
                if col == 0:
                    btn.setText('Plot Com' + str(index + 1))
                else:
                    btn.setText('Plot Whole' + str(index + 1))
                self.tab2.table_PlotRes.setCellWidget(index, col+2, btn)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.show()

    def closeEvent(self, event):
        # close window cleanly
        #print(event)
        globals.wTrim = None
        return None



    def RunTrimSim(self, SampleName, SimType, Momentum, MomentumSpread, ScanType, MinMomentum, MaxMomentum,
                   StepMomentum, SRIMdir, TRIMOutDir, Stats):

        #Get Sim Info
        Noofmuons = int(Stats.text())
        SRIMexedir = SRIMdir.text()
        TRIMoutputdir = TRIMOutDir.text()
        Mom = float(Momentum.text())
        MonoorSpread = SimType.currentText()
        MomSpread = float(MomentumSpread.text())
        MomMin = float(MinMomentum.text())
        MomMax = float(MaxMomentum.text())
        MomStep = float(StepMomentum.text())

        # Get Sample information
        Sample_layer, TotalThickness = RunSimTRIMSRIM.SetupSample(self)

        targetsample = Target(Sample_layer)

        globals.TRIMRes_x = []
        globals.TRIMRes_y = []

        if ScanType.currentText() == 'No':
            #if No then single momentum used

            if MonoorSpread == 'Mono':
                # get muon information
                muon_ion = RunSimTRIMSRIM.iondef(Mom)
                x, y, e = RunSimTRIMSRIM.RunTRIM(targetsample, TotalThickness, muon_ion,Noofmuons,SRIMexedir,TRIMoutputdir)
            elif MonoorSpread == 'Momentum Spread':
                x, y = RunSimTRIMSRIM.CalcProfileWithMomBite(
                    targetsample, TotalThickness, Mom, Noofmuons, MomSpread, SRIMexedir, TRIMoutputdir)
            else:
                print('error')

            globals.TRIMRes_x.append(x)
            globals.TRIMRes_y.append(y)

            if MonoorSpread == 'Mono':
                self.tab2.table_PlotRes.setItem(0, 0, QTableWidgetItem(str(Mom)))
            else:
                self.tab2.table_PlotRes.setItem(0, 0, QTableWidgetItem(str(Mom) + ' +/- ' + str(MomSpread)))
            # break to components to get %
            xposlist = RunSimTRIMSRIM.getxpos(self)
            comp = RunSimTRIMSRIM.getcomp(self, xposlist, 0)
            perlayer = RunSimTRIMSRIM.getperlayer(self, comp)
            outstr = ''
            for index in range(len(globals.sample_layers)):
                outstr += '[' + str(index + 1) + '] ' + str(round(perlayer[index], 3)) + ' '

            self.tab2.table_PlotRes.setItem(0, 1, QTableWidgetItem(outstr))


        elif ScanType.currentText() == 'Yes':
            MomIndex = 0
            for Mom in RunSimTRIMSRIM.my_range(MomMin, MomMax, MomStep):
                if MonoorSpread == 'Mono':
                    # get muon information
                    muon_ion = RunSimTRIMSRIM.iondef(Mom)
                    x, y, e = RunSimTRIMSRIM.RunTRIM(targetsample, TotalThickness, muon_ion, Noofmuons, SRIMexedir,
                                                     TRIMoutputdir)
                elif MonoorSpread == 'Momentum Spread':
                    x, y = RunSimTRIMSRIM.CalcProfileWithMomBite(
                        targetsample, TotalThickness, Mom, Noofmuons, MomSpread, SRIMexedir, TRIMoutputdir)
                else:
                    print('error')

                globals.TRIMRes_x.append(x)
                globals.TRIMRes_y.append(y)
                # globals.TRIMRes_e.append(e)

                self.tab2.table_PlotRes.setItem(MomIndex, 0, QTableWidgetItem(str(Mom)))

                # break to components to get %
                xposlist = RunSimTRIMSRIM.getxpos(self)
                comp = RunSimTRIMSRIM.getcomp(self, xposlist, MomIndex)
                perlayer = RunSimTRIMSRIM.getperlayer(self, comp)
                outstr = ''
                for index in range(len(globals.sample_layers)):
                    outstr += '[' + str(index + 1) + '] ' + str(round(perlayer[index], 3)) + ' '

                self.tab2.table_PlotRes.setItem(MomIndex, 1, QTableWidgetItem(outstr))

                MomIndex += 1
            else:
                print('Error in Scan')


        return

    def my_range(start, end, step):
        # sets a reange of momenta
        while start <= end:
            yield start
            start += step

    def SetupSample(self):
        ''' Sets up the sample layers and get information from the table
        '''

        i = 0
        Sample_layer = []
        TotalThickness = 0.0
        try:

            while i < 10:

                sampleName = self.tab1.table_TRIMsetup.item(i, 0).text()
                if sampleName == 'Beamline Window':
                    LayerThickness = float(self.tab1.table_TRIMsetup.item(i, 1).text())
                    TotalThickness =+ LayerThickness
                    beamwindow = Layer({'H': {'stoich': 8, 'E_d': 10, 'lattice': 3, 'surface': 2
                                              },
                                        'C': {'stoich': 10, 'E_d': 28.0, 'lattice': 3.0,
                                              'surface': 7.41
                                              },
                                        'O': {'stoich': 4, 'E_d': 28.0, 'lattice': 3.0,
                                              'surface': 2.0}},
                                       density=1.4, width=LayerThickness * 1e7, phase=0)
                    Sample_layer.append(beamwindow)
                    globals.sample_name.append('Beamline Window')

                elif sampleName == 'Air (compressed)':

                    LayerThickness = float(self.tab1.table_TRIMsetup.item(i, 1).text())
                    TotalThickness =+ LayerThickness

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
                                        'surface': 2.0}}, density=1500 * 1.20479e-3, width=LayerThickness * 1e7,
                                # air layer compressed from 150mm to 0.1mm to optimise bins
                                phase=1)
                    Sample_layer.append(air)
                    globals.sample_name.append('Air (compressed)')
                    print('done air')
                    print(Sample_layer)
                else:
                    sampledensity = float(self.tab1.table_TRIMsetup.item(i, 2).text())
                    samplethickness = float(self.tab1.table_TRIMsetup.item(i, 1).text())
                    TotalThickness = + LayerThickness
                    thislayer = Layer.from_formula(sampleName, density=sampledensity, width=samplethickness * 1e7,
                                                          phase=0)

                    Sample_layer.append(thislayer)  # 0.016 mm = 160000Athick sample holder
                    globals.sample_name.append(sampleName)

                i += 1

        except:
           print('error in setting up the table')

        globals.sample_layers = Sample_layer

        return Sample_layer, TotalThickness



    def iondef(Mom:float):
        '''muon properties, mass and energy'''
        muM = 105.6583745  # mass o muon in MeV/c^2
        muMA = muM / 931.5  # mass of muon in atomic mass units
        # kintetic energy associatd with the momentum (relitavistic)
        Ek = np.sqrt(105.6583745 ** 2 + Mom ** 2) - 105.6583745

        print('Momentum=' + str(Mom) + ' Energy=' + str(Ek))

        # corresponding SRIM muon ion definitions
        muon_ion = Ion('H', Ek * 1e6,
                       muMA)  # define muon as Hydrogen ion with mass of muon, with a given kinetic energy

        return muon_ion

    def RunTRIM(target, TotalThickness, muon_ion, number_muon, SRIMdirectory, output_directory):
        '''Run TRIM and output results in x1, y1, e1'''
        print('in runtrim')

        trimsim = TRIM(target, muon_ion, number_ions=number_muon, calculation=1)

        trimdataoutput = trimsim.run(SRIMdirectory)  # Simulation run by executing SRIM.exe in directory

        TRIM.copy_output_files(SRIMdirectory,
                               output_directory)  # ouput files from SRIM copied to desired output directory

        trimdata = trimdataoutput.range

        x1 = list(trimdata.depth / 1e7)  # muon ranges, converted from angstroms to mm.

        y1 = list(trimdata.ions)  # SRIM has weird units for y axis

        y1 = RunSimTRIMSRIM.CorrectToCounts(TotalThickness, y1,number_muon)

        e1 = list(trimdata.ions)

        return x1, y1, e1

    def CorrectToCounts(thickness, y1, TotalSimCounts):
        ''' output of SRIM is odd this corrects it to counts'''
        finalbins = thickness / 100.0
        for i in range(len(y1)):
            y1[i] = y1[i] * finalbins * TotalSimCounts
        return y1

    def PlotSim(self, x, y, ):
        ''' Plots the results of the srim but depends on whihc button is pressed'''

        try:
            if y == 2:
                # plot components
                figt = plt.figure()
                axx = figt.subplots()
                axx.plot(globals.TRIMRes_x[x], globals.TRIMRes_y[x])
                axx.set_xlabel('Depth ($mm$)')
                axx.set_ylabel('Number of muons')
                axx.set_title('SRIM Simulation at ' + self.tab2.table_PlotRes.item(x,0).text() + ' MeV/c')

                xposlist = RunSimTRIMSRIM.getxpos(self)

                #plot layers out plot
                sumdis = 0.0
                for i in range(len(globals.sample_layers)):
                    sumdis += xposlist[i+1]

                    plt.axvline(x=sumdis, color='k', linestyle='--')
                    plt.text(sumdis, 0, globals.sample_name[i], horizontalalignment='left', rotation='vertical')

                # break output down to components
                comp = RunSimTRIMSRIM.getcomp(self, xposlist, x)

                # plot layers
                for i in range(len(globals.sample_layers)):
                    axx.plot(globals.TRIMRes_x[0], comp[i])

                plt.show()

            else:
                figt = plt.figure()
                axx = figt.subplots()
                axx.plot(globals.TRIMRes_x[x], globals.TRIMRes_y[x])
                axx.set_xlabel('Depth ($mm$)')
                axx.set_ylabel('Number of muons')
                axx.set_title('SRIM Simulation at ')
                xposlist = RunSimTRIMSRIM.getxpos(self)

                # plot layers out plot
                sumdis = 0.0
                for i in range(len(globals.sample_layers)):
                    sumdis += xposlist[i + 1]

                    plt.axvline(x=sumdis, color='k', linestyle='--')
                    plt.text(sumdis, 0, globals.sample_name[i], horizontalalignment='left', rotation='vertical')

                plt.show()


        except:
            print('plot error')

        return

    def CalcProfileWithMomBite(sample, TotalThickness, Mom, NFinal, Mombite, SRIMdirectory, output_directory):
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
            muon_ion = RunSimTRIMSRIM.iondef(P)


            NE = int(NFinal * (1.0 / (np.sqrt(2.0 * np.pi) * MomSigma)) * np.exp(
                -0.5 * (P - Mom) ** 2 / (MomSigma ** 2)))
            print('Number of Counts', NE)

            x1, y1, e1 = RunSimTRIMSRIM.RunTRIM(sample, TotalThickness,  muon_ion, NE, SRIMdirectory, output_directory)

            if i == 0:
                yres =  y1
                xres =  x1
            else:
                for index in range (0, len (y1)):
                    yres[index] = yres[index] + y1[index]

        return xres, yres

    def getxpos(self):
        '''gets xpos from layers must be an easier way'''
        xposlist = []
        xposlist.append(0.0)
        for i in range(len(globals.sample_layers)):
            temp = globals.sample_layers[i]
            loc = str(temp).find('width:')
            xpos = float(str(temp)[loc + 6:].strip('>')) / 1e7
            xposlist.append(xpos)
        return xposlist

    def getcomp(self, xposlist, MomIndex):
        ''' break the SRIM output into components'''
        comp = []
        sum1 = 0.0
        sum2 = 0.0
        for i in range(len(globals.sample_layers)):
            templist = []
            sum1 += xposlist[i]
            sum2 = sum1 + xposlist[i+1]
            for j in range(len(globals.TRIMRes_y[MomIndex])):
                if globals.TRIMRes_x[MomIndex][j] >= sum1 and globals.TRIMRes_x[MomIndex][j] < sum2 :
                    templist.append(globals.TRIMRes_y[MomIndex][j])
                else:
                    templist.append(0.0)
            comp.append(templist)
        return comp

    def getperlayer(self,comp):
        ''' gets the number of muons in a layer (normalised)'''
        perlayer = []
        totalsumlayer = 0.0

        for index in range(len(globals.sample_layers)):
            sumlayer = np.sum(comp[index])
            perlayer.append(sumlayer)
            totalsumlayer += sumlayer

        for index in range(len(globals.sample_layers)):
            perlayer[index] = perlayer[index] / totalsumlayer

        return perlayer



