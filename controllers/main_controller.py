from ui.nebula_heaven_ui import Ui_MainWindow
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from database import Database
import shutil
import os
from PyQt5.QtCore import QRunnable, QThreadPool

STORAGE_DIR = "./Storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

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
        # self.db = Database()
        self.thread_pool = QThreadPool.globalInstance()

        # connecting buttons to functions
        self.ui.pushButton.clicked.connect(self.addFile)
        self.ui.pushButton_3.clicked.connect(self.downloadFile)
        self.ui.pushButton_2.clicked.connect(self.deleteFile)

    # creating neccesarry functions
    def addFile(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")
        if files:
            for file in files:
                filename = os.path.basename(file)
                dest_path = os.path.join(STORAGE_DIR, filename)
                shutil.copy(file, dest_path)  # Copy file to storage directory
                self.ui.file_list.addItem(filename)  # Add filename to UI list

    def downloadFile(self):
        selected_item = self.ui.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            file_path = os.path.join(STORAGE_DIR, file_name)
            if os.path.exists(file_path):
                save_path, _ = QFileDialog.getSaveFileName(self, "Save File As", file_name)
                if save_path:
                    worker = Worker(shutil.copy, file_path, save_path)
                    self.thread_pool.start(worker)  # Run in a separate thread
                    QMessageBox.information(self, "Download", f"File saved to {save_path}")
            else:
                QMessageBox.warning(self, "Error", "File not found in storage.")
        else:
            QMessageBox.warning(self, "Warning", "No file selected to download.")

    def deleteFile(self):
        selected_item = self.ui.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            file_path = os.path.join(STORAGE_DIR, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete file from storage
            self.ui.file_list.takeItem(self.ui.file_list.row(selected_item))  # Remove from UI
        else:
            QMessageBox.warning(self, "Warning", "No file selected to delete.")
