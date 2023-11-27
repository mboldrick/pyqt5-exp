import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        # Start main UI code

        ######################
        # The central widget #
        ######################
        self.textedit = qtw.QTextEdit()
        self.setCentralWidget(self.textedit)

        ##################
        # The status bar #
        ##################
        self.statusBar().showMessage("Welcome to my text editor")

        # Add a widget to the status bar
        charcount_label = qtw.QLabel("Chars: 0")
        self.textedit.textChanged.connect(
            lambda: charcount_label.setText(
                "Chars: " + str(len(self.textedit.toPlainText()))
            )
        )
        self.statusBar().addPermanentWidget(charcount_label)

        ###################
        # The menu system #
        ###################
        menubar = self.menuBar()

        # Add submenus
        file_menu = menubar.addMenu("&File")
        edit_menu = menubar.addMenu("&Edit")
        help_menu = menubar.addMenu("&Help")

        # End main UI code
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
