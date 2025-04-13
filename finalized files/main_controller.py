from nebula_heaven_ui import Ui_MainWindow
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
        self.thread_pool = QThreadPool.globalInstance()
        self.loadFiles()

        # connecting buttons to functions
        self.ui.pushButton.clicked.connect(self.addFile)
        self.ui.pushButton_3.clicked.connect(self.downloadFile)
        self.ui.pushButton_2.clicked.connect(self.deleteFile)

        # adding icon and title to the window
        self.setWindowTitle("NebulaHeaven")

    def addFile(self):
        """ Add files to MongoDB instead of local storage """
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")  # ✅ Pass self instead of self.ui
        if files:
            for file in files:
                self.db.add_file(file)  # Store file in MongoDB
                filename = os.path.basename(file)
                self.ui.file_list.addItem(filename)  # Add filename to UI list


    def downloadFile(self):
        """ Download file from MongoDB and save it locally """
        selected_item = self.ui.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            save_path, _ = QFileDialog.getSaveFileName(self, "Save File As", file_name)
            if save_path:
                worker = Worker(self.db.download_file, file_name, os.path.dirname(save_path))
                self.thread_pool.start(worker)  # Run in a separate thread
                QMessageBox.information(self, "Download", f"File saved to {save_path}")
        else:
            QMessageBox.warning(self, "Warning", "No file selected to download.")

    def deleteFile(self):
        """ Delete file from MongoDB """
        selected_item = self.ui.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            self.db.delete_file(file_name)  # Remove from MongoDB
            self.ui.file_list.takeItem(self.ui.file_list.row(selected_item))  # Remove from UI
        else:
            QMessageBox.warning(self, "Warning", "No file selected to delete.")
    def loadFiles(self):
        files = self.db.get_all_files()  
        for file in files:
            self.ui.file_list.addItem(file["filename"])

