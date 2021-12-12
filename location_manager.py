from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import MainWindow
from PyQt5.QtWidgets import QDialog


class LocationManager(QDialog):
    def __init__(self, source: MainWindow):
        super(LocationManager, self).__init__()
        self.source = source

    def create_table(self):
        pass

    def create_layout(self):
        pass

    def create_form_1(self):
        pass

    def create_form_2(self):
        pass

    def create_form_3(self):
        pass

    def fill_combobox(self):
        pass

    def insert_location(self):
        pass

    def remove_location(self):
        pass

    def refactor_location(self):
        pass
