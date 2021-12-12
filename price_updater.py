from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import MainWindow
from PyQt5.QtWidgets import QDialog


class PriceUpdater(QDialog):
    def __init__(self, source: MainWindow):
        super(PriceUpdater, self).__init__()
        self.source = source

    def create_layout(self):
        pass

    def start_update(self):
        pass

    def time_update(self):
        pass
