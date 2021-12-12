from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.name = 'Main Window'
        self.show()

    def create_loading(self):
        pass

    def create_home(self, collection_name: str):
        pass

    def create_aspect(self, aspect_name: str):
        pass

    def create_menu(self):
        pass

    def open_dialog(self, dialog_name: str):
        pass

    def close_tab(self, index: int):
        pass

    def change_default(self):
        pass

    def resizeEvent(self, event):
        return super(MainWindow, self).resizeEvent(event)
