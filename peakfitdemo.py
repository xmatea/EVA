import matplotlib.pyplot as plt2
import scipy.optimize
import numpy as np

# demo on fixing parameters in scipy

def gaussian(x, mu, sigma):
    return 1 / sigma / np.sqrt(2 * np.pi) * np.exp(-(x - mu) ** 2 / 2 / sigma ** 2)

def gaussian_bck(x, mu, sigma, a, c):
    return a / sigma / np.sqrt(2 * np.pi) * np.exp(-(x - mu) ** 2 / 2 / sigma ** 2) + c


def peakfitdemo():
    # Create sample data
    x = np.linspace(0, 2, 200)
    print('x',x)
    y = gaussian(x, 1, 0.1) + np.random.rand(*x.shape) - 0.5
    print('sample created')

    plt2.figure()

    plt2.plot(x, y, label="sample data")
    print('here')

    # Fit with original fit function
    popt, _ = scipy.optimize.curve_fit(gaussian, x, y)
    print('1st fit', popt)
    plt2.plot(x, gaussian(x, *popt), label="gaussian")
    print('here')

    # Fit with custom fit function with fixed `sigma`
    sfix = 0.05
    custom_gaussian = lambda x, mu, a, c: gaussian_bck(x, mu, sfix, a, c)
    print('1')
    popt, _ = scipy.optimize.curve_fit(custom_gaussian, x, y)
    print('2nd fit', popt)
    plt2.plot(x, custom_gaussian(x, *popt), label="custom_gaussian")

    plt2.legend()
    plt2.show()
