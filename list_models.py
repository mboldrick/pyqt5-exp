import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code goes here
        container = qtw.QWidget()
        container.setLayout(qtw.QVBoxLayout())
        self.setCentralWidget(container)

        data = [
            "Hamburger",
            "Cheeseburger",
            "Chicken Nuggets",
            "Hot Dog",
            "Fish Sandwich",
        ]
        # List Widget
        listwidget = qtw.QListWidget()
        listwidget.addItems(data)

        # Combobox
        combobox = qtw.QComboBox()
        combobox.addItems(data)

        container.layout().addWidget(listwidget)
        container.layout().addWidget(combobox)

        # Make list widget items editable
        for i in range(listwidget.count()):
            item = listwidget.item(i)
            item.setFlags(item.flags() | qtc.Qt.ItemIsEditable)

        # End main UI code
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
