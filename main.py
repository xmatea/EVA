# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import PyQt5 as qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
import sys


import WelcomeScreen as WS
import MainWindow as MW

import loadsettings as ls

import LoadDatabaseFile as ldf

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    # Show welcome GUI
    app_welcome = QApplication(sys.argv)
    # Create a Qt widget, which will be our window.
    window_welcome = WS.WelcomeWindow()
    window_welcome.show()  # IMPORTANT!!!!! Windows are hidden by default.
    # Start the event loop.
    app_welcome.exec()

    # load settings file
    ls.loadsettings()
    print(ls.settings_info)
    print('here')

    # load database file
    peakdata=ldf.loadDatabaseFile()
    for key, value in peakdata.items():
        print(key, ":", value)


    # Close welcome screen
    print('hello')

    app_welcome.exit(0)
    print('dam')

    # launch main window
    app_main = QApplication(sys.argv)
    # Create a Qt widget, which will be our window.
    window_main = MW.MainWindow()
    window_main.show()  # IMPORTANT!!!!! Windows are hidden by default.
    # Start the event loop.
    print('here')

    app_main.exec()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
