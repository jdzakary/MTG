import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QGridLayout, QWidget, QLabel, QComboBox, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from json import load, dump
from functools import partial
import sqlalchemy as db

from card_insert import CardInsert
from card_search import CardSearch
from collection_value import CollectionValue
from collection_manager import CollectionManager
from location_manager import LocationManager
from price_updater import PriceUpdater
from home_window import HomeWindow


class MainWindow(QMainWindow):
    def __init__(self, scr_w: int, scr_h: int):
        super(MainWindow, self).__init__()
        app_icon = QIcon()
        app_icon.addFile('Icons/Main_Icon.png', QSize(128, 128))
        self.name = 'Main Window'
        self.engine = db.create_engine('sqlite:///Database_Files/main_database.db')
        self.scr_w, self.scr_h = scr_w, scr_h
        self.scr_w_r, self.scr_h_r = scr_w / 3840, scr_h / 2160
        self.read_config('Configs/config.json')
        self.primary = self.config['primary_collection']
        self.setGeometry(0, 50, scr_w, int(scr_h / 2))
        self.setWindowTitle('MTG Collection Manager')
        self.setWindowIcon(app_icon)
        self.c_widget = QTabWidget(self)
        self.c_widget.setTabsClosable(True)
        self.create_menu()
        self.create_loading()
        self.c_widget.addTab(self.loading_screen, 'Startup Screen')
        self.create_home(self.primary)
        self.setCentralWidget(self.c_widget)
        self.c_widget.tabCloseRequested.connect(self.close_tab)
        self.show()

    def create_loading(self):
        layout = QGridLayout()
        self.loading_screen = QWidget()
        self.loading_screen.name = 'loading_screen'
        welcome_message = QLabel('Open the collection Manager to Begin')
        warning_message = QLabel('Do not perform any other action or the application may crash')
        default = QLabel('Change which collection is opened at startup:')
        welcome_message.setProperty('window_header', True)
        warning_message.setProperty('secondary_title', True)
        default.setProperty('secondary_title', True)
        welcome_message.setAlignment(Qt.AlignCenter)
        warning_message.setAlignment(Qt.AlignCenter)
        self.default_select = QComboBox()
        self.default_select.addItem(self.primary)
        self.default_select.addItems([x for x in self.config['collections'].keys() if x != self.primary])
        layout.addWidget(welcome_message, 0, 0, 1, 2)
        layout.addWidget(warning_message, 1, 0, 1, 2)
        layout.addWidget(default, 2, 0)
        layout.addWidget(self.default_select, 2, 1)
        layout.setAlignment(Qt.AlignCenter)
        self.default_select.currentIndexChanged.connect(self.change_default)
        self.loading_screen.setLayout(layout)

    def create_home(self, collection_name: str):
        home_widget = HomeWindow(collection_name, self)
        self.c_widget.addTab(home_widget, collection_name)
        self.c_widget.setCurrentWidget(home_widget)

    def create_aspect(self, aspect_name: str):
        current_collection = self.c_widget.currentWidget().name
        current_parent = self.c_widget.currentWidget()
        if self.c_widget.currentWidget() == self.loading_screen:
            pass
        elif aspect_name == 'card_insert':
            insert_widget = CardInsert(current_collection, current_parent)
            self.c_widget.addTab(insert_widget, f'{current_collection} (Insert Cards)')
            self.c_widget.setCurrentWidget(insert_widget)
        elif aspect_name == 'collection_value':
            insert_widget = CollectionValue(current_collection, current_parent)
            self.c_widget.addTab(insert_widget, f'{current_collection} (Collection Value)')
            self.c_widget.setCurrentWidget(insert_widget)
        elif aspect_name == 'card_search':
            search_widget = CardSearch(current_collection, current_parent)
            self.c_widget.addTab(search_widget, 'Card Search')
            self.c_widget.setCurrentWidget(search_widget)

    def create_menu(self):
        app_exit = QAction('Exit', self)
        collection_manager = QAction('Collection Manager', self)
        location_manager = QAction('Location Manager', self)
        insert_card = QAction('Add Card to Collection', self)
        analyze_overview = QAction('Collection Stats', self)
        analyze_price = QAction('Value of Collection', self)
        price_manager = QAction('Update Prices', self)
        search_card = QAction('Visual Card Search', self)
        app_exit.triggered.connect(self.close)
        collection_manager.triggered.connect(partial(self.open_dialog, 'collection'))
        location_manager.triggered.connect(partial(self.open_dialog, 'location'))
        insert_card.triggered.connect(partial(self.create_aspect, 'card_insert'))
        analyze_price.triggered.connect(partial(self.create_aspect, 'collection_value'))
        price_manager.triggered.connect(partial(self.open_dialog, 'price_update'))
        search_card.triggered.connect(partial(self.create_aspect, 'card_search'))
        self.menu = self.menuBar()
        self.menu.addActions([app_exit, collection_manager, location_manager, insert_card, analyze_overview,
                              analyze_price, price_manager, search_card])

    def open_dialog(self, dialog_name: str):
        if dialog_name == 'collection':
            self.dialog_window = CollectionManager(self)
        elif dialog_name == 'price_update':
            self.dialog_window = PriceUpdater(self)
        elif self.c_widget.currentWidget() == self.loading_screen:
            pass
        else:
            if dialog_name == 'location':
                self.dialog_window = LocationManager(self.c_widget.currentWidget())

    def close_tab(self, index: int):
        if index == 0:
            pass
        else:
            self.c_widget.removeTab(index)

    def change_default(self):
        self.config['primary_collection'] = self.default_select.currentText()
        self.write_config('Configs/config.json')

    def set_style(self, filepath: str):
        with open(filepath, 'r') as file:
            style = file.read()
        self.setStyleSheet(style)

    def read_config(self, filepath: str):
        with open(filepath, 'r') as file:
            self.config = load(file)

    def write_config(self, filepath: str):
        with open(filepath, 'w') as file:
            dump(self.config, file, indent=2)

    def fetch_data(self, criteria: str) -> pd.DataFrame:
        data = pd.read_sql(criteria, self.engine)
        return data

    def execute_cursor(self, sql: str):
        with self.engine.connect() as connection:
            result = connection.execute(sql)

    def close_all_tabs(self):
        for i in range(self.c_widget.count()):
            self.c_widget.removeTab(1)

    def resizeEvent(self, event):
        return super(MainWindow, self).resizeEvent(event)
