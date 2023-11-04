import sys
import typing
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class ChoiceSpinBox(qtw.QSpinBox):
    """A spinbox for selecting choices."""

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super().__init__(
            *args,
            maximum=len(self.choices) - 1,
            minimum=0,
            **kwargs,
        )

    def valueFromText(self, text):
        return self.choices.index(text)

    def textFromValue(self, value):
        try:
            return self.choices[value]
        except IndexError:
            return "!Error!"

    def validate(self, string, index):
        if string in self.choices:
            state = qtg.QValidator.Acceptable
        elif any([v.startswith(string) for v in self.choices]):
            state = qtg.QValidator.Intermediate
        else:
            state = qtg.QValidator.Invalid
        return (state, string, index)


class IPv4Validator(qtg.QValidator):
    """Enforce entry of IPv4 addresses"""

    def validate(self, string, index):
        octets = string.split(".")
        if len(octets) > 4:
            state = qtg.QValidator.Invalid
        elif not all([x.isdigit() for x in octets if x != ""]):
            state = qtg.QValidator.Invalid
        elif not all([0 <= int(x) <= 255 for x in octets if x != ""]):
            state = qtg.QValidator.Invalid
        elif len(octets) < 4:
            state = qtg.QValidator.Intermediate
        elif any([x == "" for x in octets]):
            state = qtg.QValidator.Intermediate
        else:
            state = qtg.QValidator.Acceptable
        return (state, string, index)


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

        # Create a grid layout and put it ina container widget
        container = qtw.QWidget(self)
        grid_layout = qtw.QGridLayout()
        # layout.addLayout(grid_layout)
        container.setLayout(grid_layout)

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

        # Set the spinbox to a fixed width
        spinbox.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Preferred)

        # Set the textedit to expand
        textedit.setSizePolicy(
            qtw.QSizePolicy.MinimumExpanding,
            qtw.QSizePolicy.MinimumExpanding,
        )
        textedit.sizeHint = lambda: qtc.QSize(500, 500)

        # Use the stretch factor
        stretch_layout = qtw.QHBoxLayout()
        layout.addLayout(stretch_layout)
        stretch_layout.addWidget(qtw.QLineEdit("Short"), 1)
        stretch_layout.addWidget(qtw.QLineEdit("Long"), 2)

        #####################
        # Container Widgets #
        #####################

        # QTabWidget
        tab_widget = qtw.QTabWidget(
            movable=True,
            tabPosition=qtw.QTabWidget.West,
            tabShape=qtw.QTabWidget.Triangular,
        )
        layout.addWidget(tab_widget)

        tab_widget.addTab(container, "Tab the first")
        tab_widget.addTab(subwidget, "Tab the second")

        # QGroupBox
        groupbox = qtw.QGroupBox(
            "Buttons",
            checkable=True,
            checked=True,
            alignment=qtc.Qt.AlignHCenter,
            flat=True,
        )
        groupbox.setLayout(qtw.QHBoxLayout())
        groupbox.layout().addWidget(qtw.QPushButton("OK"))
        groupbox.layout().addWidget(qtw.QPushButton("Cancel"))
        layout.addWidget(groupbox)

        ##############
        # Validation #
        ##############

        line_edit.setText("0.0.0.0")
        line_edit.setValidator(IPv4Validator())

        ratingbox = ChoiceSpinBox(
            ["bad", "average", "good", "awesome"],
            self,
        )
        sublayout.addWidget(ratingbox)

        # End main UI code
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
