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

        # Add actions
        open_action = file_menu.addAction("Open")
        save_action = file_menu.addAction("Save")

        # Add a separator
        file_menu.addSeparator()

        # Add an action with a callback
        quit_action = file_menu.addAction("Quit", self.destroy)

        # Connect to a Qt slot
        edit_menu.addAction("Undo", self.textedit.undo)

        # Create a QAction manually
        redo_action = qtw.QAction("Redo", self)
        redo_action.triggered.connect(self.textedit.redo)
        edit_menu.addAction(redo_action)

        ###########################
        # The toobar and QActions #
        ###########################
        toolbar = self.addToolBar("File")
        # toolbar.addAction(open_action)
        # toolbar.addAction("Save")

        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(qtc.Qt.TopToolBarArea | qtc.Qt.BottomToolBarArea)

        # Add icons
        open_icon = self.style().standardIcon(qtw.QStyle.SP_DirOpenIcon)
        save_icon = self.style().standardIcon(qtw.QStyle.SP_DriveHDIcon)

        open_action.setIcon(open_icon)
        toolbar.addAction(open_action)
        toolbar.addAction(
            save_icon, "Save", lambda: self.statusBar().showMessage("File saved")
        )

        help_action = qtw.QAction(
            self.style().standardIcon(qtw.QStyle.SP_DialogHelpButton),
            "Help",
            self,  # important to pass the parent!
            triggered=lambda: self.statusBar().showMessage("Sorry, no help yet"),
        )
        toolbar.addAction(help_action)

        # Create a toolbar in another part of the scren
        toolbar2 = qtw.QToolBar("Edit")
        toolbar2.addAction("Copy", self.textedit.copy)
        toolbar2.addAction("Cut", self.textedit.cut)
        toolbar2.addAction("Paste", self.textedit.paste)
        self.addToolBar(qtc.Qt.RightToolBarArea, toolbar2)

        ################
        # Dock Widgets #
        ################
        dock = qtw.QDockWidget("Replace")
        self.addDockWidget(qtc.Qt.LeftDockWidgetArea, dock)

        # Force the dock to stay open
        dock.setFeatures(
            qtw.QDockWidget.DockWidgetMovable | qtw.QDockWidget.DockWidgetFloatable
        )

        replace_widget = qtw.QWidget()
        replace_widget.setLayout(qtw.QVBoxLayout())
        dock.setWidget(replace_widget)
        self.search_text_inp = qtw.QLineEdit(placeholderText="Search for…")
        self.replace_text_inp = qtw.QLineEdit(placeholderText="Replace with…")
        search_and_replace_btn = qtw.QPushButton(
            "Search and Replace", clicked=self.search_and_replace
        )
        replace_widget.layout().addWidget(self.search_text_inp)
        replace_widget.layout().addWidget(self.replace_text_inp)
        replace_widget.layout().addWidget(search_and_replace_btn)
        replace_widget.layout().addStretch()

        #############################
        # Message Boxes and Dialogs #
        #############################

        # QMessageBox
        help_menu.addAction("About", self.showAboutDialog)

        # response = qtw.QMessageBox.question(
        #     self,
        #     "My Text Editor",
        #     "This is beta software. Do you want to continue?",
        #     qtw.QMessageBox.Yes | qtw.QMessageBox.Abort,
        # )
        # if response == qtw.QMessageBox.Abort:
        #     self.close()
        #     sys.exit()

        # Splash Screen (custom message box)
        splash_screen = qtw.QMessageBox()
        splash_screen.setWindowTitle("My Text Editor")
        splash_screen.setText("BETA SOFTWARE WARNING!")
        splash_screen.setInformativeText(
            "This is beta software." "Are you sure you really want to use it?"
        )
        splash_screen.setDetailedText(
            "This editor was written for pedagogical purposes only."
        )
        splash_screen.setWindowModality(qtc.Qt.WindowModal)
        splash_screen.addButton(qtw.QMessageBox.Yes)
        splash_screen.addButton(qtw.QMessageBox.Abort)
        response = splash_screen.exec()
        if response == qtw.QMessageBox.Abort:
            self.close()
            sys.exit()

        # QFileDialog
        open_action.triggered.connect(self.openFile)
        save_action.triggered.connect(self.saveFile)

        # End main UI code
        self.show()

    def search_and_replace(self):
        s_text = self.search_text_inp.text()
        r_text = self.replace_text_inp.text()

        if s_text:
            self.textedit.setText(self.textedit.toPlainText().replace(s_text, r_text))

    def showAboutDialog(self):
        qtw.QMessageBox.about(
            self, "About text_editor.py", "This is a text editor written in PyQt5."
        )

    def openFile(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            "Select a file to open…",
            qtc.QDir.homePath(),
            "Text files (*.txt);;Python files (*.py);;All files (*.*)",
            "Python files (*.py)",
            qtw.QFileDialog.DontUseNativeDialog | qtw.QFileDialog.DontResolveSymlinks,
        )
        if filename:
            try:
                with open(filename, "r") as fh:
                    self.textedit.setText(fh.read())
            except Exception as e:
                qtw.QMessageBox.critical(None, "Error", f"Could not open file: {e}")

    def saveFile(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Select a file to save to…",
            qtc.QDir.homePath(),
            "Text files (*.txt);;Python files (*.py);;All files (*.*)",
        )
        if filename:
            try:
                with open(filename, "w") as fh:
                    fh.write(self.textedit.toPlainText())
            except Exception as e:
                qtw.QMessageBox.critical(None, "Error", f"Could not save file: {e}")

    def set_font(self):
        current = self.textedit.currentFont()
        font, accepted = qtw.QFontDialog.getFont(current, self)
        if accepted:
            self.textedit.setCurrentFont(font)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
