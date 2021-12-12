from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QAbstractItemView, QLabel, QComboBox, QLineEdit, QCheckBox, QTableWidgetItem
from PyQt5.QtCore import Qt


class CollectionViewer(QWidget):
    def __init__(self, name, source: HomeWindow):
        super(CollectionViewer, self).__init__()
        self.name = name
        self.source = source
        self.create_layout()

    def create_layout(self):
        layout = QGridLayout()
        self.table = QTableWidget()
        self.table.setSortingEnabled(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.refresh_viewer)
        self.refresh_table('')
        self.create_filters()
        layout.addWidget(self.filter_box, 0, 1)
        layout.addWidget(self.table, 0, 0)
        self.setLayout(layout)

    def create_filters(self):
        self.filter_box = QWidget()
        self.filter_box.setFixedWidth(int(800 * self.source.source.scr_w_r))
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.edit_name = QLineEdit(self.filter_box)
        self.edit_set = QLineEdit(self.filter_box)
        self.edit_set_type = QComboBox(self.filter_box)
        self.edit_location = QLineEdit(self.filter_box)
        self.edit_type = QComboBox(self.filter_box)
        self.edit_sub = QComboBox(self.filter_box)
        self.edit_min = QLineEdit(self.filter_box)
        self.edit_max = QLineEdit(self.filter_box)
        self.edit_foil = QComboBox(self.filter_box)
        self.edit_rarity = QWidget(self.filter_box)
        self.edit_type.addItems(['', 'Deck', 'Storage'])
        self.edit_sub.addItems([''])
        self.edit_foil.addItems(['', 'True', 'False'])
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
                         QLabel('Set Type:', self.filter_box), QLabel('Location Name:', self.filter_box),
                         QLabel('Location Type:', self.filter_box), QLabel('Location Subtype:', self.filter_box),
                         QLabel('Min Price:', self.filter_box), QLabel('Max Price:', self.filter_box),
                         QLabel('Foil:', self.filter_box), QLabel('Rarity:', self.filter_box)]
        for i in range(0, len(filter_titles)):
            item_1 = filter_titles[i]
            item_1.setProperty('table_filter', True)
            layout.addWidget(item_1, i * 2, 0)
        filter_boxes = [self.edit_name, self.edit_set, self.edit_set_type, self.edit_location, self.edit_type,
                        self.edit_sub, self.edit_min, self.edit_max, self.edit_foil, self.edit_rarity]
        for i in range(0, len(filter_boxes)):
            item_1 = filter_boxes[i]
            layout.addWidget(item_1, i * 2 + 1, 0)
            for item in [item_1]:
                if 'QLineEdit' in str(type(item)):
                    item.textChanged.connect(self.apply_filter)
                elif 'QComboBox' in str(type(item)):
                    item.currentIndexChanged.connect(self.apply_filter)
        self.edit_type.currentIndexChanged.connect(self.fill_sub)
        for item in self.edit_rarity.children():
            if 'QCheckBox' in str(type(item)):
                item.stateChanged.connect(self.apply_filter)
        self.filter_box.setLayout(layout)

    def fill_sub(self):
        self.edit_sub.clear()
        if self.edit_type.currentIndex() == 1:
            self.edit_sub.addItems(['', 'Standard', 'Modern', 'Commander', 'Vintage'])
        elif self.edit_type.currentIndex() == 2:
            self.edit_sub.addItems(['', 'Binder', 'Box', 'Bin', 'Crate'])
        else:
            self.edit_sub.addItems([''])

    def refresh_table(self, criteria: str):
        with open('Database_Files/SQL_Files/collection_viewer.sql') as file1:
            query = file1.read()
        query = query.replace('collection_1', self.source.collection_file)
        query += ' ' + criteria
        data = self.source.source.fetch_data(query)
        self.table.setColumnCount(5)
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(['Card Name', 'Set', 'Location', 'Value'])
        this_index = 0
        for row in data.iterrows():
            card_name = QTableWidgetItem(row[1]['name'])
            card_set = QTableWidgetItem(row[1]['set_name'])
            card_location = QTableWidgetItem(row[1]['Location'])
            card_value = QTableWidgetItem()
            card_id = QTableWidgetItem()
            card_value.setData(Qt.DisplayRole, row[1]['value'])
            card_value.setTextAlignment(Qt.AlignRight)
            card_id.setData(Qt.DisplayRole, row[1]['collection_id'])
            self.table.setItem(this_index, 0, card_name)
            self.table.setItem(this_index, 1, card_set)
            self.table.setItem(this_index, 2, card_location)
            self.table.setItem(this_index, 3, card_value)
            self.table.setItem(this_index, 4, card_id)
            this_index += 1
        self.table.setColumnHidden(4, True)
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(3, int(150 * self.source.source.scr_w_r))
        self.table.item(0, 0)

    def refresh_viewer(self, row: int, column: int):
        desired_id = self.table.item(row, 4).text()
        self.source.viewer_1.load_card(desired_id)

    def apply_filter(self):
        desired_name = self.edit_name.text()
        desired_set = self.edit_set.text()
        desired_set_type = self.edit_set_type.currentText()
        min_value = self.edit_min.text()
        max_value = self.edit_max.text()
        desired_type = self.edit_type.currentText()
        desired_sub = self.edit_sub.currentText()
        desired_location = self.edit_location.text()
        desired_locations = [x['name'] for x in self.source.source.config['collections'][self.name]['locations'] if
                             (x['type'] == desired_type or desired_type == '') and
                             (x['sub_type'] == desired_sub or desired_sub == '')]
        desired_foil = self.edit_foil.currentText()
        constraints = f"""where Location in ({" ,".join(["'" + x + "'" for x in desired_locations])})"""
        if desired_name != '':
            constraints += f""" and instr(name, '{desired_name}')"""
        if desired_location != '':
            constraints += f""" and instr(Location, '{desired_location}')"""
        if desired_set != '':
            constraints += f" and instr(set_name, '{desired_set}')"
        if desired_set_type != '':
            constraints += f" and set_type = '{desired_set_type}'"
        if min_value != '':
            constraints += f' and value >= {float(min_value)}'
        if max_value != '':
            constraints += f' and value <= {float(max_value)}'
        if desired_foil != '':
            constraints += f" and nt.Foil = {desired_foil}"
        rarity_constraint = []
        for item in self.edit_rarity.children():
            if 'QCheckBox' in str(type(item)):
                if item.isChecked():
                    rarity_constraint.append(item.text().lower())
        constraints += f"""and rarity in ({" ,".join(["'" + x + "'" for x in rarity_constraint])})"""
        self.table.clear()
        self.refresh_table(constraints)

    def refresh_collection(self):
        self.apply_filter()
