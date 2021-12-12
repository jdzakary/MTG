from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget


class CardViewer(QWidget):
    def __init__(self, name, source: HomeWindow):
        super(CardViewer, self).__init__()
        self.name = name
        self.source = source

    def refresh_attributes(self):
        pass

    def create_layout(self):
        pass

    def load_card(self, desired_id: int):
        pass

    def change_location(self):
        pass

    def refresh_collection(self):
        pass

    def delete_card(self):
        pass
