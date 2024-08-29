from PyQt6.QtWidgets import (
    QWidget,
)


class PlotWindow(QWidget):
    """
        This "window" is a QWidget. If it has no parent, it
        will appear as a free-floating window as we want.
        """


    def __init__(self):
        super().__init__()
        '''layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)'''

        wPlot = QWidget()
        wPlot.resize(1200, 600)
        wPlot.setWindowTitle("Plot Window")
