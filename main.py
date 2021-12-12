from main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import ctypes

my_app_id = 'neuralnova.mtgcollectionmanager.v1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

app = QApplication([])
screen_list = app.screens()
screen_size = screen_list[0].size()
scr_w = int(screen_size.width())
scr_h = int(screen_size.height())

window = MainWindow(scr_w, scr_h)
window.set_style('Styles/style.css')
sys.exit(app.exec())
