from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import MainWindow
from PyQt5.QtWidgets import QWidget


class HomeWindow(QWidget):
    def __init__(self, name: str, source: MainWindow):
        super(HomeWindow, self).__init__()
        self.source = source
        self.name = name

    def refresh_collection(self):
        pass
