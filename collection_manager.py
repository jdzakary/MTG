from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import MainWindow
from PyQt5.QtWidgets import QDialog


class CollectionManager(QDialog):
    def __init__(self, source: MainWindow):
        super(CollectionManager, self).__init__()
        self.source = source

    def create_layout(self):
        pass

    def create_table(self):
        pass

    def create_form_1(self):
        pass

    def create_form_2(self):
        pass

    def create_form_3(self):
        pass

    def open_collection(self):
        pass

    def create_collection(self):
        pass

    def rename_collection(self):
        pass
