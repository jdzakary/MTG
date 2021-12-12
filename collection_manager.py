from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import MainWindow
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QWidget, QComboBox, QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from utility_functions import contains_any


class CollectionManager(QDialog):
    def __init__(self, source: MainWindow):
        super(CollectionManager, self).__init__()
        self.source = source
        self.setModal(True)
        self.setWindowTitle('Collection Manager')
        self.setGeometry(int(self.source.scr_w / 2) - int(800 * self.source.scr_w_r / 2),
                         int(self.source.scr_h / 2) - int(1200 * self.source.scr_h_r / 2),
                         int(800 * self.source.scr_w_r), int(1200 * self.source.scr_h_r))
        self.setFixedWidth(int(800 * self.source.scr_w_r))
        self.create_layout()
        self.show()

    def create_layout(self):
        layout = QGridLayout()
        header = QLabel('Current Collections')
        subheader_1 = QLabel('Open a Collection')
        subheader_2 = QLabel('Create a Collection')
        subheader_3 = QLabel('Rename a Collection')
        header.setProperty('window_header', True)
        subheader_1.setProperty('secondary_title', True)
        subheader_2.setProperty('secondary_title', True)
        subheader_3.setProperty('secondary_title', True)
        header.setAlignment(Qt.AlignCenter)
        self.create_table()
        self.create_form_1()
        self.create_form_2()
        self.create_form_3()
        components = [header, self.table, subheader_1, self.form_1, subheader_2, self.form_2, subheader_3, self.form_3]
        for item in components:
            layout.addWidget(item, components.index(item), 0)
        self.setLayout(layout)

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Name', 'Card Count'])
        self.table.setRowCount(len(self.source.config['collections'].keys()))
        row = 0
        for key in self.source.config['collections'].keys():
            collection_file = self.source.config['table_mapping'][key]
            data = self.source.fetch_data(f'select collection_id from {collection_file}')
            card_count = len(data)
            self.table.setItem(row, 0, QTableWidgetItem(key))
            self.table.setItem(row, 1, QTableWidgetItem(str(card_count)))
            row += 1
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)

    def create_form_1(self):
        self.form_1 = QWidget()
        layout = QGridLayout()
        self.name_select = QComboBox()
        self.name_select.addItem('')
        self.name_select.addItems([x for x in self.source.config['collections'].keys()])
        submit = QPushButton('Open', self.form_1)
        layout.addWidget(self.name_select, 0, 0)
        layout.addWidget(submit, 0, 1)
        self.form_1.setLayout(layout)
        submit.clicked.connect(self.open_collection)

    def create_form_2(self):
        self.form_2 = QWidget()
        layout = QGridLayout()
        self.name_enter = QLineEdit()
        self.name_enter.setFixedWidth(int(350 * self.source.scr_w_r))
        submit = QPushButton('Create')
        self.error_text = QLabel('')
        self.error_text.setStyleSheet("color: red")
        layout.addWidget(self.name_enter, 0, 0)
        layout.addWidget(submit, 0, 1)
        layout.addWidget(self.error_text, 1, 0, 1, 2)
        self.form_2.setLayout(layout)
        submit.clicked.connect(self.create_collection)

    def create_form_3(self):
        self.form_3 = QWidget()
        layout = QGridLayout()
        self.old_name = QComboBox()
        self.old_name.addItem('')
        self.old_name.addItems([x for x in self.source.config['collections'].keys()])
        self.old_name.setFixedWidth(int(233 * self.source.scr_w_r))
        self.rename = QLineEdit()
        self.rename.setFixedWidth(int(233 * self.source.scr_w_r))
        submit = QPushButton('Rename')
        submit.setFixedWidth(int(233 * self.source.scr_w_r))
        self.error_rename = QLabel('')
        self.error_rename.setStyleSheet("color: red")
        layout.addWidget(self.old_name, 0, 0)
        layout.addWidget(self.rename, 0, 1)
        layout.addWidget(submit, 0, 2)
        layout.addWidget(self.error_rename, 1, 0, 1, 3)
        self.form_3.setLayout(layout)
        submit.clicked.connect(self.rename_collection)

    def open_collection(self):
        value = self.name_select.currentText()
        if value == '':
            pass
        else:
            self.source.create_home(value)

    def create_collection(self):
        name = self.name_enter.text()
        if name == '':
            self.error_text.setText('Please Enter a Collection Name!')
        elif name in [x for x in self.source.config['collections'].keys()]:
            self.error_text.setText('Name already in use!')
        elif contains_any(name, [':', '?', '/', '\\', '*', '"', "'", '!', '@', '(', ')', '+', '&', '%', '^', '=']):
            self.error_text.setText('File name contains reserved character!')
        else:
            self.error_text.setText('')
            self.source.config['collections'][name] = {'locations': [{'name': 'Starter', 'type': 'Deck', 'sub_type': 'Standard'}]}
            collection_file = f"collection_{len(self.source.config['table_mapping']) + 1}"
            self.source.config['table_mapping'][name] = collection_file
            self.source.write_config('Configs/config.json')
            with open('Database_Files/SQL_Files/create_collection.sql') as file1:
                query_text = file1.read()
            query = query_text.format(collection_file)
            self.source.execute_cursor(query)
            with open('Database_Files/SQL_Files/create_card.sql') as file1:
                query_text = file1.read()
            test_scryfall = 'https://scryfall.com/card/mh2/267/counterspell?utm_source=api'
            test_oracle = 'cc187110-1148-4090-bbb8-e205694a39f5'
            test_location = 'Starter'
            test_purchased = 0.30
            test_foil = False
            query = query_text.format(collection_file, test_scryfall, test_oracle, test_location, test_purchased, test_foil)
            self.source.execute_cursor(query)
            QWidget().setLayout(self.layout())
            self.create_layout()

    def rename_collection(self):
        name = self.rename.text()
        old_name = self.old_name.currentText()
        if name == '':
            self.error_rename.setText('Please Enter a New Collection Name!')
        elif old_name == '':
            self.error_rename.setText('Please select a current collection!')
        elif name in [x for x in self.source.config['collections'].keys()]:
            self.error_rename.setText('Name already in use!')
        elif contains_any(name, [':', '?', '/', '\\', '*', '"', "'", '!', '@', '(', ')', '+', '&', '%', '^', '=']):
            self.error_rename.setText('File name contains reserved character!')
        else:
            self.error_rename.setText('')
            if self.source.config['primary_collection'] == old_name:
                self.source.config['primary_collection'] = name
            self.source.config['collections'][name] = self.source.config['collections'].pop(old_name)
            self.source.config['table_mapping'][name] = self.source.config['table_mapping'].pop(old_name)
            self.source.write_config('Configs/config.json')
            QWidget().setLayout(self.layout())
            self.create_layout()
