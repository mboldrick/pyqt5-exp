import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class FormWindow(qtw.QWidget):
    submitted = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())

        self.edit = qtw.QLineEdit()
        self.submit = qtw.QPushButton("Submit", clicked=self.onSubmit)

        self.layout().addWidget(self.edit)
        self.layout().addWidget(self.submit)

    def onSubmit(self):
        self.submitted.emit(self.edit.text())
        self.close()


class MainWindow(qtw.QWidget):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()

        self.setLayout(qtw.QVBoxLayout())

        self.label = qtw.QLabel("Click 'Change' to change this text.")
        self.change = qtw.QPushButton("Change", clicked=self.onChange)
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.change)

        self.show()

    @qtc.pyqtSlot()
    def onChange(self):
        self.formwindow = FormWindow()
        self.formwindow.submitted.connect(self.label.setText)
        self.formwindow.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
