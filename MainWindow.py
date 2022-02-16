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
)
from PyQt5.QtGui import QPalette, QColor

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        file_exit.triggered.connect(quit)
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
        if flag == 0:
            print('yeah')




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

        '''self.setWindowTitle("Elemental Analysis")
        # labels for the run information

        label1 = QLabel("Run Number")
        label1.setAlignment(Qt.AlignCenter)
        label2 = QLabel("Title")
        label2.setAlignment(Qt.AlignCenter)
        label3 = QLabel("Start:")
        label3.setAlignment(Qt.AlignCenter)
        label4 = QLabel("End:")
        label4.setAlignment(Qt.AlignCenter)
        label5 = QLabel("Events:")
        label5.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))
        layout.addWidget(Color('blue'))

        widget = QWidget()
        widget.setLayout(layout)
        widget.resize(600,600)
        self.setCentralWidget(widget)

        self.setCentralWidget(label1)
        self.setCentralWidget(label2)
        self.setCentralWidget(label3)
        self.setCentralWidget(label4)
        self.setCentralWidget(label5)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "&Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)'''

    def onMyToolBarButtonClick(self, s):
        print("click", s)
