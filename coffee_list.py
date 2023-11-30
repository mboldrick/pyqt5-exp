import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts


class CoffeeForm(qtw.QWidget):
    def __init__(self, roasts):
        super().__init__()
        self.setLayout(qtw.QFormLayout())
        self.coffee_brand = qtw.QLineEdit()
        self.layout().addRow("Brand:", self.coffee_brand)
        self.coffee_name = qtw.QLineEdit()
        self.layout().addRow("Name:", self.coffee_name)
        self.roast = qtw.QComboBox()
        self.roast.addItems(roasts)
        self.layout().addRow("Roast:", self.roast)
        self.reviews = qtw.QTableWidget(columnCount=3)
        self.reviews.horizontalHeader().setSectionResizeMode(2, qtw.QHeaderView.Stretch)
        self.layout().addRow(self.reviews)

    def show_coffee(self, coffee_data, reviews):
        self.coffee_brand.setText(coffee_data.get("coffee_brand"))
        self.coffee_name.setText(coffee_data.get("coffee_name"))
        self.roast.setCurrentIndex(coffee_data.get("roast_id"))
        self.reviews.clear()
        self.reviews.setHorizaontalHeaderLabels(["Reviewer", "Date", "Review"])
        self.reviews.setRowCount(len(reviews))
        for i, review in enumerate(reviews):
            for j, value in enumerate(review):
                self.reviews.setItem(i, j, qtw.QTableWidgetItem(value))


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code goes here

        # End main UI code
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
