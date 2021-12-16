from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from utility_functions import fetch_graph
from Graphs.value_stats import value_stats


class CollectionValue(QWidget):
    def __init__(self, name: str, source: HomeWindow, scale: float):
        super(CollectionValue, self).__init__()
        self.name = name
        self.source = source
        self.scale = scale
        self.create_graphs()
        self.create_layout()

    def create_layout(self):
        layout = QGridLayout()
        graph_1 = self.load_graph('value_by_color')
        graph_2 = self.load_graph('value_by_price_group')
        graph_3 = self.load_graph('value_by_type')
        graph_4 = self.load_graph('distribution_of_price')
        layout.addWidget(graph_1, 0, 0)
        layout.addWidget(graph_2, 0, 1)
        layout.addWidget(graph_3, 1, 0)
        layout.addWidget(graph_4, 1, 1)
        self.setLayout(layout)

    def create_graphs(self):
        value_stats(self.source.collection_file, 1, 'Graphs/')

    def load_graph(self, desired_graph: str) -> QLabel:
        graph = QLabel(self)
        data = fetch_graph(self.source.collection_file, desired_graph)
        pix_map = QPixmap()
        pix_map.loadFromData(data)
        pix_map = pix_map.scaledToWidth(640 * self.scale)
        graph.setAlignment(Qt.AlignCenter)
        graph.setPixmap(pix_map)
        return graph
