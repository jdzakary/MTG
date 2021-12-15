from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import MainWindow
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from Database_Files.data_download import data_download
from Database_Files.data_insert import data_insert
from Database_Files.download_images import download_images
from Database_Files.update_prices import update_prices
from time import sleep


class Thread(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, version: int, source: PriceUpdater):
        super(Thread, self).__init__()
        self.version = version
        self.source = source

    def __del__(self):
        self.wait()

    def run(self):
        if self.version == 1:
            i = 1
            while self.source.updating:
                self.signal.emit({'Caller': self, 'Content': i})
                i += 1
                sleep(1)
        elif self.version == 2:
            data_download('Database_Files/')
            self.signal.emit({'Caller': self, 'Content': 2})
            data_insert('Database_Files/')
            self.signal.emit({'Caller': self, 'Content': 3})
            update_prices('Database_Files/')
            self.signal.emit({'Caller': self, 'Content': 4})
            download_images('Database_Files/')
            self.signal.emit({'Caller': self, 'Content': 5})


class PriceUpdater(QDialog):
    def __init__(self, source: MainWindow):
        super(PriceUpdater, self).__init__()
        self.source = source
        self.setWindowTitle('Price Updater')
        self.setGeometry(int(self.source.scr_w / 2) - int(1000 * self.source.scr_w_r / 2),
                         int(self.source.scr_h / 2) - int(600 * self.source.scr_h_r / 2),
                         int(1000 * self.source.scr_w_r), int(600 * self.source.scr_h_r))
        self.setFixedSize(int(1000 * self.source.scr_w_r), int(600 * self.source.scr_h_r))
        self.updating = False
        self.progress = '(Phase 1)'
        self.create_layout()
        self.setModal(True)
        self.show()

    def create_layout(self):
        layout = QGridLayout()
        header = QLabel('Download and Update Prices', self)
        header.setProperty('window_header', True)
        header.setAlignment(Qt.AlignCenter)
        body = QLabel('This will download new data from Scryfall and update the prices of all your collections. '
                      'Depending on your internet speed, your computer speed, and the size of your collections, it may '
                      'take a while to complete', self)
        body.setFont(QFont('Times New Roman', 14))
        body.setAlignment(Qt.AlignCenter)
        body.setWordWrap(True)
        self.status_text = QLabel('', self)
        self.status_text.setStyleSheet("color: red")
        self.status_text.setAlignment(Qt.AlignCenter)
        self.status_text.setFont(QFont('Times New Roman', 14))
        self.submit = QPushButton('Start Update', self)
        self.submit.clicked.connect(self.start_update)
        layout.addWidget(header, 0, 0)
        layout.addWidget(body, 1, 0)
        layout.addWidget(self.status_text, 2, 0)
        layout.addWidget(self.submit, 3, 0)
        self.setLayout(layout)

    def start_update(self):
        self.updating = True
        self.thread_1 = Thread(1, self)
        self.thread_2 = Thread(2, self)
        self.thread_1.signal.connect(self.signal_accept)
        self.thread_2.signal.connect(self.signal_accept)
        self.thread_1.start()
        self.thread_2.start()
        self.submit.setEnabled(False)

    def signal_accept(self, msg: dict):
        if msg['Caller'] == self.thread_1:
            self.status_text.setText(f'Update in Progress {self.progress}: {msg["Content"]} seconds')
        elif msg['Caller'] == self.thread_2:
            if msg['Content'] == 5:
                self.status_text.setText('Update Complete!')
                self.submit.setEnabled(True)
                self.updating = False
            else:
                self.progress = f'(Phase {msg["Content"]})'

    def closeEvent(self, a0):
        if self.updating:
            a0.ignore()
        return
