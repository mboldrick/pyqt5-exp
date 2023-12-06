import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts


class CoffeeForm(qtw.QWidget):
    """Form to display/edit all info about a coffee"""

    def __init__(self, coffees_model, reviews_model):
        super().__init__()
        self.setLayout(qtw.QFormLayout())

        # Coffee Fields
        self.coffee_brand = qtw.QLineEdit()
        self.layout().addRow("Brand:", self.coffee_brand)
        self.coffee_name = qtw.QLineEdit()
        self.layout().addRow("Name:", self.coffee_name)
        self.roast = qtw.QComboBox()
        self.layout().addRow("Roast:", self.roast)

        # Map the coffee fields
        self.coffees_model = coffees_model
        self.mapper = qtw.QDataWidgetMapper(self)
        self.mapper.setModel(self.coffees_model)
        self.mapper.setItemDelegate(qts.QSqlRelationalDelegate(self))
        self.mapper.addMapping(
            self.coffee_brand, coffees_model.fieldIndex("coffee_brand")
        )
        self.mapper.addMapping(
            self.coffee_name, coffees_model.fieldIndex("coffee_name")
        )
        self.mapper.addMapping(self.roast, coffees_model.fieldIndex("description"))

        # Retrieve a model for the roasts and set up the combobox
        roasts_model = coffees_model.relationModel(self.coffees_ odel.fieldIndex("description"))
        self.roast.setModel(roasts_model)
        self.roast.setModelColumn(1)


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
                f"Missing tables, please repair DB: {missing_tables}",
            )
            sys.exit(1)
        else:
            print("Database connection successful.")

        # Create the models
        self.reviews_model = qts.QSqlTableModel()
        self.reviews_model.setTable("reviews")

        self.coffees_model = qts.QSqlRelationalTableModel()
        self.coffees_model.setTable("coffees")
        self.coffees_model.setRelation(
            self.coffees_model.fieldIndex("roast_id"),
            qts.QSqlRelation("roasts", "id", "description"),
        )
        self.coffees_model.select()

        # self.coffees_model.setEditStrategy(0)
        # self.coffees_model.dataChanged.connect(print)
        self.coffee_list = qtw.QTableView()
        self.coffee_list.setModel(self.coffees_model)
        self.coffee_list.setItemDelegate(qts.QSqlRelationalDelegate())
        self.stack.addWidget(self.coffee_list)

        # Create a toolbar
        toolbar = self.addToolBar("Controls")
        toolbar.addAction("Delete Coffee(s)", self.delete_coffee)
        toolbar.addAction("Add Coffee", self.add_coffee)

        # End main UI code
        self.show()

    def delete_coffee(self):
        selected = self.coffee_list.selectedIndexes()
        for index in selected or []:
            self.coffees_model.removeRow(index.row())

    def add_coffee(self):
        self.stack.setCurrentWidget(self.coffee_list)
        self.coffees_model.insertRows(self.coffees_model.rowCount(), 1)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
