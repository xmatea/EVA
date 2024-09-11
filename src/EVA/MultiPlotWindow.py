from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
)

from EVA import MultiPlot, GenReadList, ReadMultiRun, PlotWidget

class MultiPlotWindow(QWidget):
    """
        This window is the GUI for the multiplot window

        """


    def __init__(self, parent = None):
        super(MultiPlotWindow,self).__init__(parent)

        self.setWindowTitle("Multi-Plot Window ")

        # set up containers and layouts
        self.layout = QGridLayout()
        self.side_panel = QWidget()
        self.settings_form = QWidget()
        self.settings_form_layout = QFormLayout()
        self.side_panel_layout = QVBoxLayout()

        # set size constraints
        self.side_panel.setMaximumWidth(380)

        # create empty plot widget
        self.plot = PlotWidget.PlotWidget()

        # sets up button
        self.plot_multi = QPushButton('Load and Plot Multi Spectra')
        self.plot_multi.clicked.connect(lambda: self.loadandplot())

        # label for offset
        self.lab_multi_offset = QLabel('Offset')

        # input for the value of the y-axis offset
        self.val_multi_offset = QLineEdit('0.0')

        # makes the table for the list of run numbers to plot
        self.RunListTable = QTableWidget()
        self.RunListTable.setColumnCount(3)
        #self.RunListTable.setMinimumSize(800,700)
        self.RunListTable.setRowCount(50)
        self.RunListTable.setHorizontalHeaderLabels(['Start', 'End', 'Step'])


        # sets each point in the table to a blank
        for i in range(3):
            for j in range(50):

                self.RunListTable.setItem(j,i,QTableWidgetItem(''))

        # add all components to layout
        self.settings_form.setLayout(self.settings_form_layout)
        self.settings_form_layout.addRow(self.lab_multi_offset, self.val_multi_offset)
        self.settings_form_layout.addRow(self.plot_multi)

        self.side_panel.setLayout(self.side_panel_layout)
        self.side_panel_layout.addWidget(self.settings_form)
        self.side_panel_layout.addWidget(self.RunListTable)

        self.setLayout(self.layout)
        self.layout.addWidget(self.side_panel, 0, 0)
        self.layout.addWidget(self.plot, 0, 1)


    def loadandplot(self):
        #print('hello')
        line = []

        #read table from GUI

        for i in range(50):
            try:
                start = int(self.RunListTable.item(i,0).text())
            except:
                start = 0
            #print('start', start)
            try:
                end = int(self.RunListTable.item(i,1).text())
                #print('end',end)
            except:
                end = 0
            #print('end', end)
            try:
                step = int(self.RunListTable.item(i,2).text())
            except:
                step = 0
            line.append([start,end,step])

        #print('line')
        #print(line)
        # generates a list of runs to load and plot
        RunList = GenReadList.GenReadList(line)
        #print('RunList', RunList)
        # reads offset from GUI
        offset = float(self.val_multi_offset.text())
        #print('offset', offset)

        # reads data and returns as each detector and as an array

        datax_GE1, datay_GE1, datax_GE2, datay_GE2, datax_GE3, datay_GE3, datax_GE4, datay_GE4\
            = ReadMultiRun.ReadMultiRun(RunList)

        # plots multiple runs from the runlist and with a y offset

        fig, ax, plt = MultiPlot.MultiPlot(datax_GE1, datay_GE1, datax_GE2, datay_GE2, datax_GE3, datay_GE3, datax_GE4, datay_GE4,
                            RunList, offset)

        self.plot.update_plot(axs=ax, fig=fig)

