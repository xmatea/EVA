from PyQt6.QtWidgets import QWidget, QHeaderView, QMessageBox


class BaseView(QWidget):
    """
    All EVA widgets should inherit from this view - it just provides some useful pre-defined methods to
    avoid code-duplication.

    """
    def __init__(self, parent=None):
        super().__init__(parent)


    def display_error_message(self, title="Error", message="", buttons=QMessageBox.StandardButton.Ok):
        _ = QMessageBox.critical(self, title, message, buttons)

    def display_message(self, title="Message", message="", buttons=QMessageBox.StandardButton.Ok):
        _ = QMessageBox.information(self, title, message, buttons)

    @staticmethod
    def stretch_horizontal_header(table):
        n_cols = table.columnCount()
        for i in range(n_cols):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
