from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget


class CardSearch(QWidget):
    def __init__(self, name, source: HomeWindow):
        super(CardSearch, self).__init__()
        self.name = name
        self.source = source

    def create_layout(self):
        pass

    def refresh_table(self):
        pass

    def create_filters(self):
        pass

    def apply_filter(self):
        pass
