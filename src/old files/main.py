# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt6.QtWidgets import QApplication
import sys


#import WelcomeScreen as WS


from EVA import globals, MainWindow as MW, loadgamma as lg, loadsettings as ls, LoadDatabaseFile as ldf


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print('hope you are having fun!')

    # Show welcome GUI
    app_welcome = QApplication(sys.argv)
    # Create a Qt widget, which will be our window.
    window_welcome = WS.WelcomeWindow()
    window_welcome.show()  # IMPORTANT!!!!! Windows are hidden by default.
    # Start the event loop.
    app_welcome.exec()

    # load settings file
    ls.loadsettings()

    # load database file
    ldf.loadDatabaseFile()
    lg.loadgamma()

    for key, value in globals.peakdata.items():
        print(key, ":", value)


    # Close welcome screen

    app_welcome.exit(0)

    # launch main window
    app_main = QApplication(sys.argv)
    # Create a Qt widget, which will be our window.
    window_main = MW.MainWindow()
    window_main.show()  # IMPORTANT!!!!! Windows are hidden by default.
    # Start the event loop.

    app_main.exec()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
