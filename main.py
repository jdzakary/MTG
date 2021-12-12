from main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import ctypes

my_app_id = 'neuralnova.mtgcollectionmanager.v1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

app = QApplication([])
screen_list = app.screens()
screen_size = screen_list[0].size()
scr_w = screen_size.width()
scr_h = screen_size.height()

window = MainWindow()
sys.exit(app.exec())
