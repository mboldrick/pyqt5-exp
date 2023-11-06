import sys
import typing
from PyQt5 import QtCore, QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QWidget


class CategoryWindow(qtw.QWidget):
    submitted = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__(None, modal=True)
        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(qtw.QLabel("Please enter a new category name:"))
        self.category_entry = qtw.QLineEdit()
        self.layout().addWidget(self.category_entry)
        self.submit_btn = qtw.QPushButton("Submit", clicked=self.onSubmit)
        self.layout().addWidget(self.submit_btn)
        self.cancel_btn = qtw.QPushButton("Cancel", clicked=self.close)
        self.layout().addWidget(self.cancel_btn)
        self.show()

    @qtc.pyqtSlot()
    def onSubmit(self):
        if self.category_entry.text():
            self.submitted.emit(self.category_entry.text())
        self.close()


class MainWindow(qtw.QWidget):
    events = {}

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        self.setWindowTitle("My Calendar App")
        self.resize(800, 600)

        self.calendar = qtw.QCalendarWidget()
        self.event_list = qtw.QListWidget()
        self.event_title = qtw.QLineEdit()
        self.event_category = qtw.QComboBox()
        self.event_time = qtw.QTimeEdit(qtc.QTime(8, 0))
        self.allday_check = qtw.QCheckBox("All Day")
        self.event_detail = qtw.QTextEdit()
        self.add_button = qtw.QPushButton("Add/Update")
        self.del_button = qtw.QPushButton("Delete")

        # Add event categories
        self.event_category.addItems(
            ["Select category…", "New…", "Work", "Meeting", "Doctor", "Family"]
        )
        # Disable the first category item
        self.event_category.model().item(0).setEnabled(False)

        # Arrange widgets
        main_layout = qtw.QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(self.calendar)

        self.calendar.setSizePolicy(
            qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding
        )

        right_layout = qtw.QVBoxLayout()
        main_layout.addLayout(right_layout)
        right_layout.addWidget(qtw.QLabel("Events on Date"))
        right_layout.addWidget(self.event_list)

        self.event_list.setSizePolicy(
            qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding
        )

        event_form = qtw.QGroupBox("Event")
        right_layout.addWidget(event_form)
        event_form_layout = qtw.QGridLayout()
        event_form.setLayout(event_form_layout)

        event_form_layout.addWidget(self.event_title, 1, 1, 1, 3)
        event_form_layout.addWidget(self.event_category, 2, 1)
        event_form_layout.addWidget(self.event_time, 2, 2)
        event_form_layout.addWidget(self.allday_check, 2, 3)
        event_form_layout.addWidget(self.event_detail, 3, 1, 1, 3)
        event_form_layout.addWidget(self.add_button, 4, 2)
        event_form_layout.addWidget(self.del_button, 4, 3)

        ##################
        # Connect Events #
        ##################

        # Disable time when "all day" is checked
        self.allday_check.toggled.connect(self.event_time.setDisabled)

        # Populate the event list when the calendar is clicked
        self.calendar.selectionChanged.connect(self.populate_list)

        # Populate the event form when an item is selectec
        self.event_list.itemSelectionChanged.connect(self.populate_form)

        # Save the event when the add button is clicked
        self.add_button.clicked.connect(self.save_event)

        # Delete the event when the delete button is clicked
        self.del_button.clicked.connect(self.delete_event)

        # Disable the delete button when no event is selected
        self.event_list.itemSelectionChanged.connect(self.check_delete_btn)

        # Start with the delete button disabled
        self.check_delete_btn()

        self.show()

    def clear_form(self):
        self.event_title.clear()
        self.event_category.setCurrentIndex(0)
        self.event_time.setTime(qtc.QTime(8, 0))
        self.allday_check.setChecked(False)
        self.event_detail.setPlainText("")

    def populate_list(self):
        self.event_list.clear()
        self.clear_form()
        date = self.calendar.selectedDate()
        for event in self.events.get(date, []):
            time = event["time"].toString("hh:mm") if event["time"] else "All Day"
            self.event_list.addItem(f"{time}: {event['title']}")

    def populate_form(self):
        self.clear_form()
        date = self.calendar.selectedDate()
        event_number = self.event_list.currentRow()
        if event_number == -1:
            return
        event_data = self.events.get(date)[event_number]
        self.event_category.setCurrentText(event_data["category"])
        if event_data["time"] is None:
            self.allday_check.setChecked(True)
        else:
            self.event_time.setTime(event_data["time"])
        self.event_title.setText(event_data["title"])
        self.event_detail.setPlainText(event_data["detail"])

    def save_event(self):
        event = {
            "category": self.event_category.currentText(),
            "time": None if self.allday_check.isChecked() else self.event_time.time(),
            "title": self.event_title.text(),
            "detail": self.event_detail.toPlainText(),
        }
        date = self.calendar.selectedDate()
        event_list = self.events.get(date, [])
        event_number = self.event_list.currentRow()

        if event_number == -1:
            event_list.append(event)
        else:
            event_list[event_number] = event

        event_list.sort(key=lambda x: x["time"] or qtc.QTime(0, 0))
        self.events[date] = event_list
        self.populate_list()

    def delete_event(self):
        date = self.calendar.selectedDate()
        row = self.event_list.currentRow()
        del self.events[date][row]
        self.event_list.setCurrentRow(-1)
        self.clear_form()
        self.populate_list()

    def check_delete_btn(self):
        self.del_button.setDisabled(self.event_list.currentRow() == -1)

    def add_category(self, category):
        self.event_category.addItem(category)
        self.event_category.setCurrentText(category)

    def on_category_change(self, text):
        print(text)
        if text == "New…":
            print("New category")
            dialog = CategoryWindow()
            dialog.submitted.connect(self.add_category)
            self.event_category.setCurrentIndex(0)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
