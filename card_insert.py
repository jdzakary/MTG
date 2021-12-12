from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget, QTableWidgetItem


class CardInsert(QWidget):
    def __init__(self, name: str, source: HomeWindow):
        super(CardInsert, self).__init__()
        self.name = name
        self.source = source

    def create_layout(self):
        pass

    def create_form_1(self):
        pass

    def create_form_2(self):
        pass

    def refresh_table(self, initial: bool = False):
        pass

    def get_details(self, row: int, column: int):
        pass

    def change_value(self):
        pass

    def insert_card(self):
        pass

    def open_link(self, item: QTableWidgetItem):
        pass
