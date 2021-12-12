from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget


class CollectionViewer(QWidget):
    def __init__(self, name, source: HomeWindow):
        super(CollectionViewer, self).__init__()
        self.name = name
        self.source = source

    def create_layout(self):
        pass

    def create_filters(self):
        pass

    def fill_sub(self):
        pass

    def refresh_table(self, criteria: str):
        pass

    def refresh_viewer(self, row: int, column: int):
        pass

    def apply_filter(self):
        pass

    def refresh_collection(self):
        pass
