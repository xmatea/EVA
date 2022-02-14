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
)
from PyQt5.QtGui import QPalette, QColor

import sys

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
        w=QWidget()
        w.resize(900,600)
        w.setWindowTitle("Elemental Analysis")

        # setting up the menu bar

        bar = QMenuBar(w)
        file = bar.addMenu('File')
        file_loaddef = file.addAction('Load Default Setting')
        file_exit = file.addAction('Exit')
        plot = bar.addMenu('Plot')
        plot_set = plot.addAction('Plot Settings')
        TRIM = bar.addMenu('SRIM/TRIM')
        Trim_sim = TRIM.addAction('SRIM/TRIM Simulation')

        # setting up the actions

        file_exit.triggered.connect(quit)

        # setting up the layout

        label_RN = QLabel(w)
        label_RN.setText("Run Number")
        label_RN.move(100, 130)
        label_RN.show()

        label_Com = QLabel(w)
        label_Com.setText("Comment")
        label_Com.move(100, 180)
        label_Com.show()

        label_Start = QLabel(w)
        label_Start.setText("Start Time")
        label_Start.move(100, 230)
        label_Start.show()

        label_End = QLabel(w)
        label_End.setText("End Time")
        label_End.move(100, 280)
        label_End.show()

        # setting up the buttons



        button_load = QPushButton(w)
        button_load.setText('Load')
        button_load.move(320,420)
        button_load.clicked.connect()





        w.show()
        sys.exit(app.exec_())

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





