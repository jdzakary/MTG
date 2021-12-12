from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget


class CollectionValue(QWidget):
    def __init__(self, name: str, source: HomeWindow):
        super(CollectionValue, self).__init__()
        self.name = name
        self.source = source

    def create_layout(self):
        pass

    def create_header(self):
        pass

    def create_graph_1(self):
        pass
