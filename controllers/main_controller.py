from ui.nebula_heaven_ui import Ui_MainWindow
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from database import Database
import shutil
import os
from PyQt5.QtCore import QRunnable, QThreadPool

class Worker(QRunnable):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)

class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()

        # connecting buttons to functions
        self.ui.pushButton.clicked.connect(self.add_files)
        self.ui.pushButton_3.clicked.connect(self.download_files)
        self.ui.pushButton_2.clicked.connect(self.delete_files)

    # creating neccesarry functions
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")
        for file in files:
            self.ui.file_list.addItem(file)
            # Will add the database later
    def download_files(self):
        selected_item = self.ui.file_list.currentItem()
        if selected_item:
            save_path = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
            if save_path:
                self.db.download_file(selected_item.text(), save_path)
                QMessageBox.information(self, "Success", "File downloaded successfully")
        else:
            QMessageBox.warning(self, "Warning", "No file selected")
    def delete_files(self):
        selected_item = self.ui.file_list.currentItem()
        if selected_item:
            self.db.delete_file(selected_item.text())
            QMessageBox.information(self, "Success", "File deleted successfully")
        else:
            QMessageBox.warning(self, "Warning", "No file selected")