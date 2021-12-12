from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QGroupBox, QComboBox, QRadioButton, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from utility_functions import fetch_image


class CardViewer(QWidget):
    def __init__(self, name, source: HomeWindow):
        super(CardViewer, self).__init__()
        self.name = name
        self.source = source
        data = self.source.source.fetch_data(f'select collection_id from {self.source.collection_file}')
        self.desired_id = data.at[0, 'collection_id']
        self.refresh_attributes()
        self.setFixedWidth(int(1200 * self.source.source.scr_w_r))
        self.create_layout()

    def refresh_attributes(self):
        with open('Database_Files/SQL_Files/card_viewer.sql') as file1:
            query = file1.read()
        query = query.format(self.source.collection_file, self.desired_id)
        data = self.source.source.fetch_data(query)
        self.scryfall = data.at[0, 'scryfall_uri']
        self.oracle_id = data.at[0, 'oracle_id']
        self.card_name = data.at[0, 'name']
        self.card_set = data.at[0, 'set_name']
        self.set_type = data.at[0, 'set_type']
        self.card_location = data.at[0, 'Location']
        self.card_value = data.at[0, 'value']
        self.purchased = data.at[0, 'purchased']
        self.foil = bool(data.at[0, 'Foil'])
        self.oracle_text_1 = data.at[0, 'oracle_text_1']
        self.oracle_text_2 = data.at[0, 'oracle_text_2']

    def create_layout(self):
        profit_raw = round(self.card_value - self.purchased, 2)
        profit_percent = round((self.card_value - self.purchased) / self.purchased * 100, 2)
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        title = QLabel('Individual Card Viewer')
        title.setProperty('secondary_title', True)
        title.setAlignment(Qt.AlignCenter)
        image_item_1 = QLabel(self)
        image_item_2 = QLabel(self)
        data = self.source.source.fetch_data(f"select downloaded from all_entries where scryfall_uri = '{self.scryfall}'")
        download_status = bool(data.at[0, 'downloaded'])
        if download_status:
            image_data_1 = fetch_image(self.set_type, self.card_set, self.scryfall)
            pix_map_1 = QPixmap()
            pix_map_1.loadFromData(image_data_1)
            image_item_1.setAlignment(Qt.AlignCenter)
            image_item_1.setPixmap(pix_map_1)
            try:
                if '//' in self.card_name:
                    image_data_2 = fetch_image(self.set_type, self.card_set, self.scryfall + 'Back', back=True)
                    pix_map_2 = QPixmap()
                    pix_map_2.loadFromData(image_data_2)
                    image_item_2.setPixmap(pix_map_2)
                    image_item_2.setAlignment(Qt.AlignCenter)
            except FileNotFoundError:
                pass
        else:
            image_item_1.setText('Unable to Find File')
        group_box = QGroupBox('Card Details')
        this_layout = QGridLayout(group_box)
        left_layout = QGridLayout()
        left_layout.setAlignment(Qt.AlignTop)
        right_layout = QGridLayout()
        right_layout.setAlignment(Qt.AlignTop)
        self.locations_box = QComboBox(group_box)
        self.locations_box.addItems([x['name'] for x in self.source.source.config['collections'][self.name]['locations']])
        self.locations_box.setCurrentText(self.card_location)
        self.locations_box.currentIndexChanged.connect(self.change_location)
        self.confirm_delete = QRadioButton('Confirm Deletion', group_box)
        submit = QPushButton('Delete this Card', group_box)
        submit.clicked.connect(self.delete_card)
        body_components = {'Card Name': [QLabel('Name:', group_box), QLabel(self.card_name, group_box)],
                           'Card Set': [QLabel('Set:', group_box), QLabel(self.card_set, group_box)],
                           'Card Location': [QLabel('Location:', group_box), self.locations_box],
                           'Card Value': [QLabel('Current Value:', group_box), QLabel(str(self.card_value), group_box)],
                           'Purchased Value': [QLabel('Purchased Value:', group_box), QLabel(str(self.purchased), group_box)],
                           'Price Increase': [QLabel('Price Increase:', group_box), QLabel(f'{profit_raw} = {profit_percent}%', group_box)],
                           'Foil': [QLabel('Foil:', group_box), QLabel(str(self.foil), group_box)],
                           'Delete Card': [self.confirm_delete, submit],
                           'Oracle ID': [QLabel('Oracle ID:', group_box), QLabel(self.oracle_id, group_box)],
                           'Oracle Front': [QLabel('Oracle Front:', group_box), QLabel(str(self.oracle_text_1), group_box)],
                           'Oracle Back': [QLabel('Oracle Back:', group_box), QLabel(str(self.oracle_text_2), group_box)]}
        body_right = ['Oracle ID', 'Oracle Front', 'Oracle Back']
        row_left = 0
        row_right = 0
        for key, value in body_components.items():
            if key in ['Delete Card']:
                pass
            else:
                value[0].setProperty('viewer_body', True)
                value[0].setAlignment(Qt.AlignTop)
            if key in ['Card Location', 'Delete Card']:
                pass
            else:
                value[1].setAlignment(Qt.AlignTop)
                value[1].setWordWrap(True)
            value[1].setProperty('viewer_body', True)
            value[1].setFixedWidth(int(350 * self.source.source.scr_w_r))
            if key in body_right:
                right_layout.addWidget(value[0], row_right, 0)
                right_layout.addWidget(value[1], row_right, 1)
                row_right += 1
            else:
                left_layout.addWidget(value[0], row_left, 0)
                left_layout.addWidget(value[1], row_left, 1)
                row_left += 1
        this_layout.addLayout(left_layout, 0, 0)
        this_layout.addLayout(right_layout, 0, 1)
        group_box.setLayout(this_layout)
        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(image_item_1, 1, 0)
        layout.addWidget(image_item_2, 1, 1)
        layout.addWidget(group_box, 2, 0, 1, 2)
        self.setLayout(layout)

    def load_card(self, desired_id: int):
        self.desired_id = desired_id
        self._refresh_attributes()
        QWidget().setLayout(self.layout())
        self.create_layout()

    def change_location(self):
        with open('Database_Files/SQL_Files/change_location.sql') as file:
            query = file.read()
        query = query.format(self.source.collection_file, self.locations_box.currentText(), self.desired_id)
        self.source.source.execute_cursor(query)
        self.source.refresh_collection()

    def refresh_collection(self):
        data = self.source.source.fetch_data(f'select collection_id from {self.source.collection_file}')
        self.desired_id = data.at[0, 'collection_id']
        self.refresh_attributes()

    def delete_card(self):
        if self.confirm_delete.isChecked():
            with open('Database_Files/SQL_Files/delete_card.sql') as file:
                query = file.read()
            query = query.format(self.source.collection_file, self.desired_id)
            self.source.source.execute_cursor(query)
            self.source.refresh_collection()
