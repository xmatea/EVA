from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

from EVA.core.app import get_app


class CopyableQTableWidget(QTableWidget):
    """
    this class extends QTableWidget
    * supports copying multiple cells text onto the clipboard
    * formatted specifically to work with multiple-cell paste into programs
      like google sheets, excel, or numbers

    taken from: https://stackoverflow.com/questions/60715462/how-to-copy-and-paste-multiple-cells-in-qtablewidget-in-pyqt5
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def copy_selection(self):
        copied_cells = sorted(self.selectedIndexes())

        copy_text = ''
        max_column = copied_cells[-1].column()
        for c in copied_cells:
            cell_item = self.item(c.row(), c.column())

            if cell_item is None:
                copy_text += ""
            else:
                copy_text += cell_item.text()

            if c.column() == max_column:
                copy_text += '\n'
            else:
                copy_text += '\t'

        get_app().clipboard().setText(copy_text)

    def paste_selection(self):
        copied_cells = sorted(self.selectedIndexes())

        # Paste clipboard contents from the first cell that was selected, and expand down and right
        first_row = copied_cells[0].row()
        first_column = copied_cells[0].column()

        clipboard_text = get_app().clipboard().text()

        rows = clipboard_text.split("\n")
        if len(rows) + first_row > self.rowCount():  # add rows if needed
            self.setRowCount(first_row + len(rows))

        for row_ix, row in enumerate(rows):
            rowdata = row.split("\t")
            if len(rowdata) + first_column > self.columnCount():  # add columns if needed
                self.setColumnCount(first_column + len(rowdata))

            for col_ix, text in enumerate(rowdata):
                self.setItem(row_ix + first_row, col_ix + first_column, QTableWidgetItem(text))

    def delete_selection(self):
        copied_cells = sorted(self.selectedIndexes())
        for cell in copied_cells:
            # set all cells to be a blank QTableWidgetItem
            self.setItem(cell.row(), cell.column(), QTableWidgetItem())


    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        # Copying
        if event.key() == Qt.Key.Key_C and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.copy_selection()

        # Pasting
        if event.key() == Qt.Key.Key_V and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.paste_selection()

        # Cutting
        if event.key() == Qt.Key.Key_X and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.copy_selection()
            self.delete_selection()

        # Deleting
        if event.key() == Qt.Key.Key_Delete:
            self.delete_selection()






