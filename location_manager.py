from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import HomeWindow
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QGridLayout, QLabel, QRadioButton, QComboBox, QLineEdit
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt
from functools import partial
from utility_functions import contains_any


class LocationManager(QDialog):
    def __init__(self, source: HomeWindow):
        super(LocationManager, self).__init__()
        self.source = source
        self.name = source.name
        self.setGeometry(int(self.source.source.scr_w / 2) - int(1000 * self.source.source.scr_w_r / 2),
                         int(self.source.source.scr_h / 2) - int(1500 * self.source.source.scr_h_r / 2),
                         int(1000 * self.source.source.scr_w_r), int(1500 * self.source.source.scr_h_r))
        self.setWindowTitle('Locations Manager')
        self.setFixedWidth(int(1050 * self.source.source.scr_w_r))
        self.create_layout()
        self.setModal(True)
        self.show()

    def create_table(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        query = f"select Location, count(collection_id) from {self.source.collection_file} group by Location"
        data = self.source.source.fetch_data(query)
        self.table.setRowCount(len(self.source.source.config['collections'][self.name]['locations']))
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Sub-Type', 'Cards in Location'])
        for row in range(len(self.source.source.config['collections'][self.name]['locations'])):
            this_location = self.source.source.config['collections'][self.name]['locations'][row]
            cards_quantity = data[data['Location'] == this_location['name']]['count(collection_id)']
            if len(cards_quantity) == 0:
                cards_quantity = 0
            quantity = QTableWidgetItem()
            quantity.setData(Qt.DisplayRole, int(cards_quantity))
            self.table.setItem(row, 0, QTableWidgetItem(this_location['name']))
            self.table.setItem(row, 1, QTableWidgetItem(this_location['type']))
            self.table.setItem(row, 2, QTableWidgetItem(this_location['sub_type']))
            self.table.setItem(row, 3, quantity)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)

    def create_layout(self):
        layout = QGridLayout()
        header = QLabel('Current Locations', self)
        subheaders = [QLabel('Add a Location', self), QLabel('Remove a Location', self), QLabel('Refactor a Location', self)]
        header.setProperty('window_header', True)
        for item in subheaders:
            item.setProperty('secondary_title', True)
            layout.addWidget(item, subheaders.index(item) * 2 + 2, 0)
        header.setAlignment(Qt.AlignCenter)
        self.create_table()
        self.create_form_1()
        self.create_form_2()
        self.create_form_3()
        layout.addWidget(header, 0, 0)
        layout.addWidget(self.table, 1, 0)
        forms = [self.form_1, self.form_2, self.form_3]
        for item in forms:
            layout.addWidget(item, forms.index(item) * 2 + 3, 0)
        self.setLayout(layout)

    def create_form_1(self):
        self.form_1 = QWidget()
        this_layout = QGridLayout()
        self.name_edit = QLineEdit(self.form_1)
        self.type_edit_1 = QRadioButton('Deck', self.form_1)
        self.type_edit_2 = QRadioButton('Storage', self.form_1)
        self.subtype_edit = QComboBox(self.form_1)
        self.name_edit.setFixedWidth(int(300 * self.source.source.scr_w_r))
        self.type_edit_1.setFixedWidth(int(150 * self.source.source.scr_w_r))
        self.type_edit_2.setFixedWidth(int(150 * self.source.source.scr_w_r))
        self.subtype_edit.setFixedWidth(int(300 * self.source.source.scr_w_r))
        submit = QPushButton('Insert', self.form_1)
        self.error_text = QLabel('', self.form_1)
        self.error_text.setStyleSheet("color: red;")
        this_layout.addWidget(QLabel('Name', self.form_1), 0, 0)
        this_layout.addWidget(QLabel('Type', self.form_1), 0, 1, 1, 2)
        this_layout.addWidget(QLabel('Subtype', self.form_1), 0, 3)
        this_layout.addWidget(self.name_edit, 1, 0)
        this_layout.addWidget(self.type_edit_1, 1, 1)
        this_layout.addWidget(self.type_edit_2, 1, 2)
        this_layout.addWidget(self.subtype_edit, 1, 3)
        this_layout.addWidget(submit, 2, 3)
        this_layout.addWidget(self.error_text, 2, 0, 1, 2)
        self.form_1.setLayout(this_layout)
        self.type_edit_1.clicked.connect(partial(self.fill_combobox, 1))
        self.type_edit_2.clicked.connect(partial(self.fill_combobox, 2))
        submit.clicked.connect(self.insert_location)

    def create_form_2(self):
        self.form_2 = QWidget()
        this_layout = QGridLayout()
        self.name_remove = QLineEdit(self.form_2)
        self.name_remove.setFixedWidth(int(300 * self.source.source.scr_w_r))
        self.error_text_2 = QLabel('', self.form_2)
        self.error_text_2.setStyleSheet("color: red;")
        submit = QPushButton('Delete', self.form_2)
        submit.setFixedWidth(int(300 * self.source.source.scr_w_r))
        this_layout.addWidget(QLabel('Name'), 0, 0)
        this_layout.addWidget(self.name_remove, 1, 0)
        this_layout.addWidget(QLabel('', self.form_2), 1, 1)
        this_layout.addWidget(submit, 1, 2)
        this_layout.addWidget(self.error_text_2, 2, 0)
        self.form_2.setLayout(this_layout)
        submit.clicked.connect(self.remove_location)

    def create_form_3(self):
        self.form_3 = QWidget()
        this_layout = QGridLayout()
        self.old_name = QLineEdit(self.form_3)
        self.new_name = QLineEdit(self.form_3)
        self.error_text_3 = QLabel('', self.form_3)
        self.error_text_3.setStyleSheet("color: red")
        submit = QPushButton('Refactor', self.form_3)
        self.error_text_2.setStyleSheet("color: red;")
        this_layout.addWidget(QLabel('Cards in Location:', self.form_3), 0, 0)
        this_layout.addWidget(QLabel('Move to Location:', self.form_3), 0, 1)
        this_layout.addWidget(self.old_name, 1, 0)
        this_layout.addWidget(self.new_name, 1, 1)
        this_layout.addWidget(submit, 1, 2)
        this_layout.addWidget(self.error_text_3, 2, 0, 1, 3)
        submit.setFixedWidth(int(300 * self.source.source.scr_w_r))
        self.form_3.setLayout(this_layout)
        submit.clicked.connect(self.refactor_location)

    def fill_combobox(self, activator: int):
        if activator == 1:
            self.subtype_edit.clear()
            self.subtype_edit.addItems(['Standard', 'Modern', 'Commander', 'Vintage'])
        elif activator == 2:
            self.subtype_edit.clear()
            self.subtype_edit.addItems(['Binder', 'Box', 'Bin', 'Crate'])

    def insert_location(self):
        contents = self.name_edit.text()
        subtype = self.subtype_edit.currentIndex()
        name_list = [x['name'] for x in self.source.source.config['collections'][self.name]['locations']]
        if contents == '':
            self.error_text.setText('Invalid Entry!')
        elif subtype == -1:
            self.error_text.setText('You must select a type!')
        elif contents in name_list:
            self.error_text.setText('Name Already in use!')
        elif contains_any(contents, [':', '?', '/', '\\', '*', '"', "'", '!', '@', '(', ')', '+']):
            self.error_text.setText('Name contains reserved character!')
        else:
            self.error_text.setText('')
            if self.type_edit_1.isChecked():
                this_type = 'Deck'
            else:
                this_type = 'Storage'
            self.source.source.config['collections'][self.name]['locations'].append(
                {"name": contents, "type": this_type, 'sub_type': self.subtype_edit.currentText()})
            self.source.source.write_config('Configs/config.json')
            self.name_edit.clear()
            QWidget().setLayout(self.layout())
            self.create_layout()

    def remove_location(self):
        contents = self.name_remove.text()
        name_list = [x['name'] for x in self.source.source.config['collections'][self.name]['locations']]
        data = self.source.source.fetch_data(f"select Location from {self.source.collection_file}")
        in_use = list(data['Location'])
        if contents not in name_list:
            self.error_text_2.setText('Invalid Entry!')
        elif contents in in_use:
            self.error_text_2.setText("Can't remove location with cards assigned to it!")
        else:
            self.error_text_2.setText('')
            self.source.source.config['collections'][self.name]['locations'].remove(
                next(x for x in self.source.source.config['collections'][self.name]['locations'] if x['name'] == contents))
            self.source.source.write_config('Configs/config.json')
            self.name_remove.clear()
            QWidget().setLayout(self.layout())
            self.create_layout()

    def refactor_location(self):
        name_list = [x['name'] for x in self.source.source.config['collections'][self.name]['locations']]
        if self.old_name.text() == '':
            self.error_text_3.setText('Please enter the name of old collection')
        elif self.new_name.text() == '':
            self.error_text_3.setText('Please enter the destination')
        elif self.old_name.text() not in name_list or self.new_name.text() not in name_list:
            self.error_text_3.setText('Both locations must already Exist!')
        else:
            self.error_text_3.setText('')
            query = f"update {self.source.collection_file} set Location = '{self.new_name}' where Location = '{self.old_name}'"
            self.source.source.execute_cursor(query)
            self.source.refresh_collection()
            QWidget().setLayout(self.layout())
            self.create_layout()
