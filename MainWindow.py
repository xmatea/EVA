import matplotlib.pyplot as plt
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QMenuBar,
    QMenu,
    QHBoxLayout,
    QLineEdit,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QPalette, QColor, QCloseEvent
import sys
import loaddata
import loadcomment
import globals


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class PlotWindow(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
        """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wp = None

        app = QApplication(sys.argv)
        w = QWidget()
        w.resize(1200, 600)
        w.setWindowTitle("Elemental Analysis")

        # setting up the menu bar

        bar = QMenuBar(w)
        file = bar.addMenu('File')
        file_loaddef = file.addAction('Load Default Setting')
        file_browse_dir = file.addAction('Browse to Data Directory')
        file_exit = file.addAction('Exit')
        plot = bar.addMenu('Plot')
        plot_set = plot.addAction('Plot Settings')
        TRIM = bar.addMenu('SRIM/TRIM')
        Trim_sim = TRIM.addAction('SRIM/TRIM Simulation')

        # setting up the actions

        # file_exit.triggered.connect(quit)
        file_exit.triggered.connect(lambda: self.closeit(app))
        file_browse_dir.triggered.connect(lambda: self.Browse_dir())

        # setting up the layout

        self.label_RN = QLabel(w)
        self.label_RN.setText("Run Number                                            ")
        self.label_RN.move(100, 80)
        self.label_RN.show()

        self.label_Com = QLabel(w)
        self.label_Com.setText("Comment " +
             "                                                                                                  ")
        self.label_Com.move(100, 130)
        self.label_Com.show()

        self.label_Events = QLabel(w)
        self.label_Events.setText("Events                                            ")
        self.label_Events.move(100, 180)
        self.label_Events.show()

        self.label_Start = QLabel(w)
        self.label_Start.setText("Start Time                                            ")
        self.label_Start.move(100, 230)
        self.label_Start.show()

        self.label_End = QLabel(w)
        self.label_End.setText("End Time                                             ")
        self.label_End.move(100, 280)
        self.label_End.show()

        # setting up the buttons

        RunNum_Text = QLineEdit(w)
        RunNum_Text.setText('2630')
        RunNum_Text.move(350, 360)


        button_plus = QPushButton(w)
        button_plus.setText('+1')
        button_plus.move(750, 350)
        button_plus.clicked.connect(lambda: self.Incr_RunNum(RunNum_Text))

        button_minus = QPushButton(w)
        button_minus.setText('-1')
        button_minus.move(100, 350)
        button_minus.clicked.connect(lambda: self.Decr_RunNum(RunNum_Text))

        button_load = QPushButton(w)
        button_load.setText('Load')
        button_load.move(420, 420)
        button_load.clicked.connect(lambda: self.loadrunandcom(
            RunNum_Text.text()))

        w.show()
        sys.exit(app.exec_())

    def closeit(self, app):
        print('here')
        quit_msg = "Are you sure you want to quit?"
        reply = QMessageBox.question(self, 'Message', quit_msg,
                                               QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:

            print('Yes')
            sys.exit(app.exec_())

            return



    def loadrunandcom(self, RunNum):
        print('load data and comment')
        flag,rtn_str = loadcomment.loadcomment(RunNum)
        print(flag,rtn_str)
        if flag == 1:
            mapping = dict.fromkeys(range(32))

            pr_str = rtn_str[0].translate(mapping)
            self.label_Start.setText("Start Time:    " + pr_str[20:] + "")

            pr_str = rtn_str[1].translate(mapping)
            self.label_End.setText("End Time:      " + pr_str[20:])

            pr_str = rtn_str[2].translate(mapping)
            self.label_Events.setText("Events:          " + pr_str[19:])

            pr_str = rtn_str[3].translate(mapping)
            self.label_Com.setText("Comment:      " + pr_str[10:])
        else:
            self.label_Com.setText("Comment:      Comment file not found")
            self.label_Start.setText("Start Time:    ")
            self.label_End.setText("End Time:       ")
            self.label_Events.setText("Events:")

        flag = loaddata.loaddata(RunNum)
        if (globals.flag_d_GE1 == 0 or globals.flag_d_GE2 == 0 or globals.flag_d_GE3 == 0 or globals.flag_d_GE4 == 0):
            print('oh no')
            self.label_RN.setText("Run Number:   File load failed")
        else:
            print ('yeah!')
            self.label_RN.setText("Run Number:   " + str(RunNum))



            self.Show_Plot_Window()



    def Show_Plot_Window(self):

        print('in Show_plot_window')
        print(self.wp)

        if self.wp is None:
            self.wp = PlotWindow()
            self.wp.show()
            print('plotting')
            plt.fill_between(globals.x_GE1, globals.y_GE1, step='mid', color='yellow')
            plt.step(globals.x_GE1, globals.y_GE1, where='mid', color='black')
            plt.ylim(bottom=0.0)
            plt.xlabel("Energy")
            plt.ylabel("Intensity")
            plt.legend("yeah!")
            plt.title('Customized histogram')

            plt.show()



        print(self.wp)



    def Incr_RunNum(self, RunNum_text):
        print('plus 1')
        RunNum_text.setText(str(int(RunNum_text.text()) + 1))

    def Decr_RunNum(self, RunNum_text):
        print('minus 1e')
        RunNum_text.setText(str(int(RunNum_text.text()) - 1))

    def Browse_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Choose Directory", "C:\\")
        print(dir_path)
        globals.workingdirectory = dir_path

    def onMyToolBarButtonClick(self, s):
        print("click", s)

