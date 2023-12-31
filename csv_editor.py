import sys
import csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import QModelIndex


class CsvTableModel(qtc.QAbstractTableModel):
    """Model for CSV table"""

    def __init__(self, csv_file):
        super().__init__()
        self.filename = csv_file
        with open(self.filename) as fh:
            csvreader = csv.reader(fh)
            self._headers = next(csvreader)
            self._data = list(csvreader)

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        if role in (qtc.Qt.DisplayRole, qtc.Qt.EditRole):
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()  # needs to be emitted before a sort
        self._data.sort(key=lambda x: x[column])
        if order == qtc.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()  # needs to be emitted after a sort

    def flags(self, index):
        return super().flags(index) | qtc.Qt.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid() and role == qtc.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def insertRows(self, position, rows, parent):
        self.beginInsertRows(
            parent or qtc.QModelIndex(),
            position,
            position + rows - 1,
        )
        for i in range(rows):
            default_row = [""] * len(self._headers)
            self._data.insert(position, default_row)
        self.endInsertRows()

    def removeRows(self, position, rows, parent):
        self.beginRemoveRows(
            parent or qtc.QModelIndex(),
            position,
            position + rows - 1,
        )
        for i in range(rows):
            del self._data[position]
        self.endRemoveRows()

    def save_data(self):
        with open(self.filename, "w", encodeing="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(self._headers)
            writer.writerows(self._data)


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code goes here
        self.tableview = qtw.QTableView()
        self.tableview.setSortingEnabled(True)
        self.setCentralWidget(self.tableview)

        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction("Open…", self.select_file)
        file_menu.addAction("Save", self.save_file)

        edit_menu = menu.addMenu("Edit")
        edit_menu.addAction("Insert Row Above", self.insert_above)
        edit_menu.addAction("Insert Row Below", self.insert_below)
        edit_menu.addAction("Remove Rows", self.remove_rows)
        # End main UI code
        self.show()

    def select_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a CSV file to open…",
            qtc.QDir.homePath(),
            "CSV Files (*.csv) ;; All Files (*)",
        )
        if filename:
            self.model = CsvTableModel(filename)
            self.tableview.setModel(self.model)
            # self.tableview.resizeColumnsToContents()
            # self.tableview.resizeRowsToContents()
            # self.tableview.sortByColumn(0, qtc.Qt.AscendingOrder)
            # self.model.dataChanged.connect(self.model.save_data)

    def save_file(self):
        if self.model:
            self.model.save_data()

    def insert_above(self):
        selected = self.tableview.selectedIndexes()
        row = selected[0].row() if selected else 0
        self.model.insertRows(row, 1, None)

    def insert_below(self):
        selected = self.tableview.selectedIndexes()
        row = selected[-1].row() if selected else self.model.rowCount(None)
        self.model.insertRows(row + 1, 1, None)

    def remove_rows(self):
        selected = self.tableview.selectedIndexes()
        if selected:
            self.model.removeRows(selected[0].row(), len(selected), None)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
