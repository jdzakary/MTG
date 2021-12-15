from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from home_window import HomeWindow
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QGridLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtWidgets import QComboBox, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from math import ceil
from utility_functions import fetch_image
from time import sleep
import webbrowser


class CardInsert(QWidget):
    def __init__(self, name: str, source: HomeWindow):
        super(CardInsert, self).__init__()
        self.name = name
        self.source = source
        self.create_layout()

    def create_layout(self):
        self.table_1 = QTableWidget()
        self.table_1.cellClicked.connect(self.get_details)
        self.create_form_1()
        self.create_form_2()
        self.refresh_table(initial=True)
        self.welcome_message = QLabel(f'Add Cards to {self.name}', self)
        self.welcome_message.setProperty('window_header', True)
        self.welcome_message.setAlignment(Qt.AlignCenter)
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.welcome_message, 0, 0, 1, 2)
        layout.addWidget(self.form_1, 1, 0)
        layout.addWidget(self.form_2, 1, 1)
        layout.addWidget(self.table_1, 2, 0, 1, 2)
        self.setLayout(layout)

    def create_form_1(self):
        self.form_1 = QGroupBox('Search for card Pictures')
        self.card_name = QLineEdit(self.form_1)
        self.waiting_text = QLabel('', self.form_1)
        submit = QPushButton('Search', self.form_1)
        self.use_text = QRadioButton('Text Lookup', self.form_1)
        self.use_graphic = QRadioButton('Graphic Lookup', self.form_1)
        self.waiting_text.setStyleSheet("color: red")
        layout = QGridLayout()
        layout.addWidget(self.card_name, 0, 0, 1, 2)
        layout.addWidget(submit, 0, 2)
        layout.addWidget(self.use_text, 1, 0)
        layout.addWidget(self.use_graphic, 1, 1)
        layout.addWidget(self.waiting_text, 2, 0, 1, 3)
        self.form_1.setLayout(layout)
        self.form_1.setFixedWidth(1000)
        submit.clicked.connect(self.refresh_table)

    def create_form_2(self):
        self.form_2 = QGroupBox('Add Selected Card to Collection')
        layout = QGridLayout()
        self.sel_name = QLabel('Selected Name will Appear Here', self.form_2)
        self.sel_set = QLabel('Selected Set will Appear Here', self.form_2)
        self.sel_value = QLabel('Selected Value will Appear Here', self.form_2)
        self.foil = QComboBox(self.form_2)
        self.purchased = QLineEdit(self.form_2)
        self.location = QComboBox(self.form_2)
        submit = QPushButton('Insert', self.form_2)
        self.error_text = QLabel('', self.form_2)
        self.error_text.setStyleSheet("color: red")
        self.foil.addItems(['False', 'True'])
        self.location.addItems([x['name'] for x in self.source.source.config['collections'][self.name]['locations']])
        self.purchased.setFixedWidth(int(200 * self.source.source.scr_w_r))
        labels = [QLabel('Selected Name:', self.form_2), QLabel('Selected Set:', self.form_2),
                  QLabel('Selected Value:', self.form_2), QLabel('Foil:', self.form_2),
                  QLabel('Price You Paid:', self.form_2), QLabel('Location:', self.form_2)]
        details = [self.sel_name, self.sel_set, self.sel_value, self.foil, self.purchased, self.location, submit]
        for item in labels:
            layout.addWidget(item, 0, labels.index(item))
        for item in details:
            layout.addWidget(item, 1, details.index(item))
        layout.addWidget(self.error_text, 2, 0, 1, 7)
        self.form_2.setLayout(layout)
        self.foil.currentIndexChanged.connect(self.change_value)
        submit.clicked.connect(self.insert_card)

    def refresh_table(self, initial: bool = False):
        if initial:
            desired_name = 'Fury Sliver'
        else:
            desired_name = self.card_name.text()
        query = f"select set_type, set_name, scryfall_uri from all_entries where instr(name, '{desired_name}') order by name"
        data = self.source.source.fetch_data(query)
        image_list = list(data.values)
        self.table_1.clear()
        if self.use_graphic.isChecked():
            self.waiting_text.setText('Fetching Images from the hard drive... this may take a few moments')
            self.repaint()
            self.table_1.setColumnCount(7)
            self.table_1.setRowCount(ceil(len(image_list) / 7) * 2)
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
                        this_image.setAlignment(Qt.AlignCenter)
                        this_image.setProperty('secondary_title', True)
                except FileNotFoundError:
                    this_image.setText('File not Found')
                self.table_1.setCellWidget(row, column, this_image)
                if column < 6:
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
                if column < 6:
                    column += 1
                    self.table_1.setRowHidden(row, True)
                else:
                    column = 0
                    row += 2
            self.waiting_text.setText('')
            self.table_1.setSortingEnabled(False)
        elif self.use_text.isChecked():
            query = f"select name, set_name, scryfall_uri, usd, usd_foil from all_entries where instr(name, '{desired_name}')"
            data = self.source.source.fetch_data(query)
            self.text_list = list(data.values)
            self.waiting_text.setText('')
            self.table_1.setColumnCount(5)
            self.table_1.setHorizontalHeaderLabels(['Name', 'Set', 'Scryfall (Double Click)', 'Regular', 'Foil'])
            self.table_1.setRowCount(len(self.text_list))
            row = 0
            for item in self.text_list:
                price_regular = QTableWidgetItem()
                price_foil = QTableWidgetItem()
                price_regular.setData(Qt.DisplayRole, item[3])
                price_foil.setData(Qt.DisplayRole, item[4])
                self.table_1.setItem(row, 0, QTableWidgetItem(item[0]))
                self.table_1.setItem(row, 1, QTableWidgetItem(item[1]))
                self.table_1.setItem(row, 2, QTableWidgetItem(item[2]))
                self.table_1.setItem(row, 3, price_regular)
                self.table_1.setItem(row, 4, price_foil)
                row += 1
            self.table_1.resizeColumnsToContents()
            self.table_1.resizeRowsToContents()
            self.table_1.itemDoubleClicked.connect(self.open_link)
            self.table_1.setSortingEnabled(False)
        else:
            self.waiting_text.setText('Select a search version!')
        self.table_1.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def get_details(self, row: int, column: int):
        if self.use_graphic.isChecked():
            self.target = self.table_1.item(row - 1, column).text()
        elif self.use_text.isChecked():
            self.target = self.table_1.item(row, 2).text()
        query = f"select name, set_name, usd, usd_foil, oracle_id, scryfall_uri from all_entries where scryfall_uri = '{self.target}'"
        data = self.source.source.fetch_data(query)
        self.results = list(data.values)[0]
        self.sel_name.setText(self.results[0])
        self.sel_set.setText(self.results[1])
        self.sel_usd = str(self.results[2])
        self.sel_usd_foil = str(self.results[3])
        if self.foil.currentText() == 'True':
            self.sel_value.setText(self.sel_usd_foil)
        elif self.foil.currentText() == 'False':
            self.sel_value.setText(self.sel_usd)

    def change_value(self):
        if self.sel_name.text() == 'Selected Name will Appear Here':
            pass
        elif self.foil.currentText() == 'True':
            self.sel_value.setText(self.sel_usd_foil)
        elif self.foil.currentText() == 'False':
            self.sel_value.setText(self.sel_usd)

    def insert_card(self):
        if self.sel_name.text() == 'Selected Name will Appear Here':
            self.error_text.setText('Please Select a Card First!')
        elif self.sel_value.text() == '0.0':
            self.error_text.setText('Card Not Available in this Foil treatment!')
        elif self.purchased.text() == '':
            self.error_text.setText('Please enter a valid purchase price!')
        else:
            try:
                new_location = self.location.currentText()
                new_foil = self.foil.currentText()
                if new_foil == 'True':
                    new_foil = True
                else:
                    new_foil = False
                new_purchased = float(self.purchased.text())
                if new_purchased < 0.01:
                    new_purchased = 0.01
                with open('Database_Files/SQL_Files/create_card.sql', 'r') as file1:
                    query = file1.read()
                query = query.format(self.source.collection_file, self.results[5], self.results[4], new_location, new_purchased, new_foil)
                self.source.source.execute_cursor(query)
                self.source.refresh_collection()
                self.sel_name.setText('Selected Name will Appear Here')
                self.sel_set.setText('Selected Set will Appear Here')
                self.sel_value.setText('Selected Value will Appear Here')
                self.error_text.setText('Insertion Successful')
                self.repaint()
                sleep(2)
                self.error_text.setText('')
            except ValueError:
                self.error_text.setText('Please enter a valid purchase price!')

    @staticmethod
    def open_link(item: QTableWidgetItem):
        if item.column() == 2:
            webbrowser.open(item.text())
