import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts


class CoffeeForm(qtw.QWidget):
    """Form to display/edit all info about a coffee"""

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
        self.stack = qtw.QStackedWidget()
        self.setCentralWidget(self.stack)

        # Connect to the database
        self.db = qts.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("coffee.db")
        if not self.db.open():
            error = self.db.lastError().text()
            qtw.QMessageBox.critical(
                None, "DB Connection Error", f"Could not open database file: {error}"
            )
            sys.exit(1)

        # Check for missing tables
        required_tables = {"roasts", "coffees", "reviews"}
        tables = self.db.tables()
        missing_tables = required_tables - set(tables)
        if missing_tables:
            qtw.QMessageBox.critical(
                None,
                "DB Integrity Error",
                f"Missing tables: {missing_tables}. Please repair the database.",
            )
            sys.exit(1)

        # Make a query
        query = self.db.exec("SELECT count(*) FROM coffees")
        query.next()
        count = query.value(0)
        print(f"There are {count} coffees in the databae.")

        # End main UI code
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
