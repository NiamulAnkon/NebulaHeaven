from PyQt5.QtWidgets import QApplication
from main_controller import MainController
import sys

app = QApplication(sys.argv)
window = MainController()
window.show()
sys.exit(app.exec_())