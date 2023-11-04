import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QWidget):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Main UI code goes here

        #########################
        # Create widget objects #
        #########################

        # QWidget
        subwidget = qtw.QWidget(self, toolTip="This is my widget")
        subwidget.setToolTip("This is YOUR widget")
        print(subwidget.toolTip())

        # QLabel
        label = qtw.QLabel("<b>Hello Widgets!</b>", self, margin=10)

        # QLineEdit
        line_edit = qtw.QLineEdit(
            "default value",
            self,
            placeholderText="Type here",
            clearButtonEnabled=True,
            maxLength=20,
        )

        # QPushButton
        button = qtw.QPushButton(
            "Push Me",
            self,
            checkable=True,
            checked=True,
            shortcut=qtg.QKeySequence("Ctrl+p"),
        )

        # QComboBox
        combobox = qtw.QComboBox(
            self, editable=True, insertPolicy=qtw.QComboBox.InsertAtTop
        )
        combobox.addItem("Lemon", 1)
        combobox.addItem("Peach", "Ohh I like Peaches")
        combobox.addItem("Strawberry", qtw.QWidget)
        combobox.insertItem(1, "Radish", 2)

        # QSpinBox
        spinbox = qtw.QSpinBox(
            self,
            value=12,
            maximum=100,
            minimum=10,
            prefix="$",
            suffix=" + Tax",
            singleStep=5,
        )

        # QDateTImeEdit
        import datetime

        datetimebox = qtw.QDateTimeEdit(
            self,
            date=datetime.date.today(),
            time=datetime.time(12, 30),
            # date=qtc.QDate.currentDate(),
            # time=qtc.QTime(12, 30),
            calendarPopup=True,
            maximumDate=datetime.date(2024, 1, 1),
            maximumTime=datetime.time(17, 0),
            # maximumDate=qtc.QDate(2030, 1, 1),
            # maximumTime=qtc.QTime(17, 0),
            displayFormat="yyyy-MM-dd HH:mm",
        )

        # QTextEdit
        textedit = qtw.QTextEdit(
            self,
            acceptRichText=False,
            lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
            lineWrapColumnOrWidth=25,
            placeholderText="Enter your text here",
        )

        ##################
        # Layout objects #
        ##################

        # Create a layout and add widgets to it
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(label)
        layout.addWidget(line_edit)

        # Add a layout to the layout
        sublayout = qtw.QHBoxLayout()
        layout.addLayout(sublayout)

        sublayout.addWidget(button)
        sublayout.addWidget(combobox)

        # Create a grid layout
        grid_layout = qtw.QGridLayout()
        layout.addLayout(grid_layout)

        grid_layout.addWidget(spinbox, 0, 0)
        grid_layout.addWidget(datetimebox, 0, 1)
        grid_layout.addWidget(textedit, 1, 0, 2, 2)

        # Create a form layout
        form_layout = qtw.QFormLayout()
        layout.addLayout(form_layout)

        form_layout.addRow("Item 1", qtw.QLineEdit(self))
        form_layout.addRow("Item 2", qtw.QLineEdit(self))
        form_layout.addRow(qtw.QLabel("<b>This is a label-only row</b>"))

        ################
        # Size Control #
        ################

        # Fix at 150 pixels wide by 40 pixels high
        label.setFixedSize(150, 40)

        # Setting minimum and maximum sizes
        line_edit.setMinimumSize(150, 15)
        line_edit.setMaximumSize(500, 50)

        # End main UI code
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
