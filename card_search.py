from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QLineEdit, QComboBox, QCheckBox
from PyQt5.QtWidgets import QPushButton, QRadioButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from utility_functions import fetch_image
from math import ceil


class CardSearch(QWidget):
    def __init__(self, name, source: HomeWindow):
        super(CardSearch, self).__init__()
        self.name = name
        self.source = source
        self.constraints = "where ae.name = 'Fury Sliver'"
        self.create_layout()

    def create_layout(self):
        layout = QGridLayout()
        self.waiting_text = QLabel('')
        self.waiting_text.setStyleSheet("color: red")
        self.table_1 = QTableWidget()
        # self.table_1.cellClicked.connect(self._get_details)
        self.refresh_table()
        self.create_filters()
        layout.addWidget(self.table_1, 0, 0)
        layout.addWidget(self.filter_box, 0, 1)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

    def refresh_table(self):
        with open('Database_Files/SQL_Files/card_search.sql') as file1:
            query = file1.read()
        query += ' ' + self.constraints
        data = self.source.source.fetch_data(query)
        image_list = [[x[1]['set_type'], x[1]['set_name'], x[1]['scryfall_uri']] for x in data.iterrows()]
        self.table_1.clear()
        self.waiting_text.setText('Fetching Images from the hard drive... this may take a few moments')
        self.repaint()
        self.table_1.setColumnCount(6)
        self.table_1.setRowCount(ceil(len(image_list) / 6) * 2)
        row = 1
        column = 0
        for item in image_list:
            this_image = QLabel()
            try:
                image_data = fetch_image(item[0], item[1], item[2])
                pix_map = QPixmap()
                pix_map.loadFromData(image_data)
                if pix_map.width() == 488:
                    this_image.setPixmap(pix_map)
                else:
                    this_image.setText('Oversized Card')
            except FileNotFoundError:
                this_image.setText('File not Found')
            self.table_1.setCellWidget(row, column, this_image)
            if column < 5:
                column += 1
            else:
                column = 0
                row += 2
        self.table_1.resizeColumnsToContents()
        self.table_1.resizeRowsToContents()
        row = 0
        column = 0
        for item in image_list:
            self.table_1.setItem(row, column, QTableWidgetItem(item[2]))
            if column < 5:
                column += 1
                self.table_1.setRowHidden(row, True)
            else:
                column = 0
                row += 2
        self.waiting_text.setText('')
        self.table_1.setSortingEnabled(False)
        self.table_1.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def create_filters(self):
        self.filter_box = QWidget()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.filter_box.setFixedWidth(650)
        self.edit_name = QLineEdit(self.filter_box)
        self.edit_set = QLineEdit(self.filter_box)
        self.edit_set_type = QComboBox(self.filter_box)
        self.edit_min = QLineEdit(self.filter_box)
        self.edit_max = QLineEdit(self.filter_box)
        self.edit_rarity = QWidget(self.filter_box)
        self.edit_set_type.addItems(['', 'archenemy', 'box', 'commander', 'core', 'draft_innovation', 'duel_deck',
                                     'expansion', 'from_the_vault', 'funny', 'masterpiece', 'masters', 'memorabilia',
                                     'planechase', 'premium_deck', 'promo', 'spellbook', 'starter', 'token',
                                     'treasure_chest', 'vanguard'])
        rarity_layout = QGridLayout()
        column = 0
        for rarity in ['Mythic', 'Rare', 'Uncommon', 'Common']:
            local_check = QCheckBox(rarity, self.edit_rarity)
            local_check.setChecked(True)
            rarity_layout.addWidget(local_check, 0, column)
            column += 1
        self.edit_rarity.setLayout(rarity_layout)
        filter_titles = [QLabel('Card Name:', self.filter_box), QLabel('Set Name:', self.filter_box),
                         QLabel('Set Type:', self.filter_box), QLabel('Min Price:', self.filter_box),
                         QLabel('Max Price:', self.filter_box), QLabel('Rarity:', self.filter_box)]
        for i in range(len(filter_titles)):
            item_1 = filter_titles[i]
            item_1.setProperty('table_filter', True)
            layout.addWidget(item_1, i * 2, 0, 1, 2)
        filter_boxes = [self.edit_name, self.edit_set, self.edit_set_type, self.edit_min, self.edit_max, self.edit_rarity]
        for i in range(len(filter_boxes)):
            item_1 = filter_boxes[i]
            layout.addWidget(item_1, i * 2 + 1, 0, 1, 2)
        submit = QPushButton('Submit Search', self.filter_box)
        layout.addWidget(submit, (len(filter_titles) + 1) * 2, 0, 1, 2)
        submit.clicked.connect(self.apply_filter)
        self.order_name = QRadioButton('Order By Name', self.filter_box)
        self.order_set = QRadioButton('Order By Set', self.filter_box)
        layout.addWidget(self.order_name, (len(filter_titles) + 1) * 2 + 1, 0)
        layout.addWidget(self.order_set, (len(filter_titles) + 1) * 2 + 1, 1)
        self.filter_box.setLayout(layout)

    def apply_filter(self):
        desired_name = self.edit_name.text()
        desired_set = self.edit_set.text()
        desired_set_type = self.edit_set_type.currentText()
        min_value = self.edit_min.text()
        max_value = self.edit_max.text()
        rarity_constraint = []
        for item in self.edit_rarity.children():
            if 'QCheckBox' in str(type(item)):
                if item.isChecked():
                    rarity_constraint.append(item.text().lower())
        constraints = f""" where rarity in ({' ,'.join(["'" + x + "'" for x in rarity_constraint])})"""
        if desired_name != '':
            constraints += f" and instr(ae.name, '{desired_name}')"
        if desired_set != '':
            constraints += f" and instr(set_name, '{desired_set}')"
        if desired_set_type != '':
            constraints += f" and set_type = '{desired_set_type}'"
        if min_value != '':
            constraints += f' and value >= {float(min_value)}'
        if max_value != '':
            constraints += f' and value <= {float(max_value)}'
        if self.order_name.isChecked():
            constraints += " order by ae.name, set_name"
        elif self.order_set.isChecked():
            constraints += " order by set_name, ae.name"
        self.constraints = constraints
        self.table_1.clear()
        self.refresh_table()
