import matplotlib.pyplot as plt

import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as sc
from scipy.interpolate import interp1d
import os  # used to execute external programs

from srim import TRIM, Ion, Layer, Target, Material
#from srim.output import Results


# from degrader_dictionary2 import *


"""
    Calculates the stopping profile of muons in a sample.

    Needs srim to be installed goto www.srim.org


"""

def RunTRIM():
    SimPara = TRIMInit()
    print(SimPara)

def TRIMInit():

    """
        Initialises the 'DepthCalcLayersIntensity' class properties in the Mantid algorithm,
        including the input parameters such as sample thickness, materials and
        simulation type that are needed to calculate the profile.

    """

    # all length scales are in mm

    # target input
    #self.declareProperty("Sample Name", "Cu", direction=Direction.Input,doc="Sample Name")
    SimPara = {}
    print('hello')
    SimPara['SampleName'] = "Cu"

    #self.declareProperty("Sample Thickness (mm)", 5.0, direction=Direction.Input,doc="Target thickness in mm.")

    SimPara['SampleThickness'] = 1.0

    #self.declareProperty("Sample Density (g/cm^2)", 8.96, direction=Direction.Input)

    SimPara['SampleDensity'] = 8.96

    # Momentum Sim input
    #self.declareProperty("Simulation Type", "Both", StringListValidator(["Both", "Mono", "Momentum Spread"]),
    # direction=Direction.Input)

    SimPara['SimType'] = "MomSpread"

    #self.declareProperty("Momentum", 27.0, direction=Direction.Input, doc="in MeV/c")

    SimPara['Mom'] = 27.0

    #self.declareProperty("Momentum spread", 4.0, direction=Direction.Input, doc="in %")

    SimPara['MomSpread'] = 4.0

    #self.declareProperty("Scan Momentum", "No", StringListValidator(["No", "Yes"]),direction=Direction.Input)

    SimPara['ScanMom'] = False

    #self.declareProperty("Min Momentum", 15.0, direction=Direction.Input, doc="in MeV/c")

    SimPara['MinMom'] = 15.0

    #self.declareProperty("Max Momentum", 30.0, direction=Direction.Input, doc="in MeV/c")

    SimPara['MaxMom'] = 30.0

    #self.declareProperty("Step Momentum", 5.0, direction=Direction.Input, doc="in MeV/c")

    SimPara['StepMom'] = 5.0

    #self.declareProperty("SRIM.exe directory", "C:/SRIM-2013", direction=Direction.Input)

    SimPara['SRIMdir'] = "C:/SRIM-2013"

    #self.declareProperty("TRIM output directory", "C:/SRIM-2013/SRIM Outputs", direction=Direction.Input)

    SimPara['TRIMOutputDir'] = "C:/SRIM-2013/SRIM Outputs"

    #self.declareProperty("Stats for final run", 1000, direction=Direction.Input)

    SimPara['Stats'] = 1000

    return SimPara


def TRIMExec():

    """
        This function executes the Mantid algortihm.

    """

    def fermifunc(x, b, c, d):

        """
            Function that returns a standard logistic function. Called a fermi function.
        """

        return 1 / (1 + np.exp(-c * (x - b))) + d

    def inversefermi(x, b, c, d):

        """
            Retruns the inverse of a logistic function.
        """

        return b - (1 / c) * np.log((1 / (x - d)) - 1)

    def gaussian(x, amp, mean, sigma):

        """
            Function that returns the standard Gaussian distribution with mean,
            standard deviation and Gaussian amplitude as input parameters.
        """

        return amp * np.exp(-0.5 * ((x - mean) ** 2) / (sigma ** 2))

    def exp(x, a, b):

        """
            Returns an exponential function which passes through (0,0.)
        """
    return np.exp(a * x - b) + -np.exp(-b)

    def invexp(x, a, b):

        """
            Returns inverse of an exponential function that passes through (0,0).
        """

        return (1 / a) * (np.log(x + np.exp(-b)) + b)

    def matdef(mat, rho, width):
        """
                Define material for simulation
        """

        matlayer1 = Layer.from_formula(mat, density=rho, width=thickness * 1e7, phase=0)
        sample = Target([matlayer1])

        return sample

    def matdef2(mat, rho, thickness):

        """
                Define material for simulation
        """

        LayerThickness = [0.05, 0.067, 0.05, thickness]
        LayerLabels = ['Window', 'air (compressed)', 'Al', 'Cu', 'Total']
        print(LayerLabels)

        beamwindow = Layer({'H': {'stoich': 8, 'E_d': 10, 'lattice': 3, 'surface': 2
                                      },
                                'C': {'stoich': 10, 'E_d': 28.0, 'lattice': 3.0,
                                      'surface': 7.41
                                      },
                                'O': {'stoich': 4, 'E_d': 28.0, 'lattice': 3.0,
                                      'surface': 2.0}},
                               density=1.4, width=LayerThickness[0] * 1e7, phase=0)

        # sample.append(beamwindow)

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
                                'surface': 2.0}}, density=1500 * 1.20479e-3, width=LayerThickness[1] * 1e7,
                        # air layer compressed from 150mm to 0.1mm to optimise bins
                        phase=1)

        # sample.append(air)

        Al_sample_holder = Layer.from_formula('Al', density=2.7, width=LayerThickness[2] * 1e7,
                                                  phase=0)  # 0.016 mm = 160000Athick sample holder

        # sample.append(Al_sample_holder)

        matlayer1 = Layer.from_formula(mat, density=rho, width=LayerThickness[3] * 1e7, phase=0)

        # sample.append(matlayer1)
        sample = Target([beamwindow, air, Al_sample_holder, matlayer1])

        return sample, LayerThickness, LayerLabels

    def iondef(Mom):
        # muon properties
        muM = 105.6583745  # mass o muon in MeV/c^2
        muMA = muM / 931.5  # mass of muon in atomic mass units
        # kintetic energy associatd with the momentum (relitavistic)
        Ek = np.sqrt(105.6583745 ** 2 + Mom ** 2) - 105.6583745

        print('Momentum=' + str(Mom) + ' Energy=' + str(Ek))

        # corresponding SRIM muon ion definitions
        muon_ion = Ion('H', Ek * 1e6,
                           muMA)  # define muon as Hydrogen ion with mass of muon, with a given kinetic energy

        return muon_ion
