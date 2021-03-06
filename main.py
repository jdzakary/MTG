from main_window import MainWindow
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import ctypes

my_app_id = 'neuralnova.mtgcollectionmanager.v1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

app = QApplication([])
screen_list = app.screens()
screen_size = screen_list[0].size()
scr_w = int(screen_size.width())
scr_h = int(screen_size.height())

splash_pix = QPixmap('Icons/Nova_Splash.png')
splash_pix = splash_pix.scaledToHeight(int(461 * scr_w / 1980))
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
splash.setMask(splash_pix.mask())
splash.show()
app.processEvents()

window = MainWindow(scr_w, scr_h)
window.set_style('Styles/style.css')
splash.finish(window)
sys.exit(app.exec())
