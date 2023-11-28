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

        # Without using model and view
        # # List Widget
        # listwidget = qtw.QListWidget()
        # listwidget.addItems(data)

        # # Combobox
        # combobox = qtw.QComboBox()
        # combobox.addItems(data)

        # container.layout().addWidget(listwidget)
        # container.layout().addWidget(combobox)

        # # Make list widget items editable
        # for i in range(listwidget.count()):
        #     item = listwidget.item(i)
        #     item.setFlags(item.flags() | qtc.Qt.ItemIsEditable)

        # Using model and view
        model = qtc.QStringListModel(data)
        listview = qtw.QListView()
        listview.setModel(model)

        model_combobox = qtw.QComboBox()
        model_combobox.setModel(model)

        container.layout().addWidget(listview)
        container.layout().addWidget(model_combobox)

        # End main UI code
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
