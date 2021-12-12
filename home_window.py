from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import MainWindow
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

from collection_viewer import CollectionViewer
from card_viewer import CardViewer


class HomeWindow(QWidget):
    def __init__(self, name: str, source: MainWindow):
        super(HomeWindow, self).__init__()
        self.source = source
        self.name = name
        self.collection_file = self.source.config['table_mapping'][self.name]
        layout = QGridLayout()
        self.table_1 = CollectionViewer(self.name, self)
        self.viewer_1 = CardViewer(self.name, self)
        self.welcome_message = QLabel('Welcome to the Home Page')
        self.welcome_message.setProperty('window_header', True)
        self.welcome_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.welcome_message, 0, 0, 1, 2)
        layout.addWidget(self.table_1, 1, 0)
        layout.addWidget(self.viewer_1, 1, 1)
        self.setLayout(layout)

    def refresh_collection(self):
        self.table_1.refresh_collection()
        self.viewer_1.refresh_collection()
