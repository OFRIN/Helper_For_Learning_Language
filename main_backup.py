import os
import sys
import time
import platform

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QPushButton

from core.english_modules import Manager

from core.devices.mouse_api import Customized_Mouse_Listener
from core.devices.keyboard_api import Customized_Keyboard_Listener

from tools.qt_utils import make_label
from registration_window import Registration_Window

class Collector(QMainWindow):
    def __init__(self):
        super().__init__()

        hotkey_dictionary = {
            '<ctrl>+<shift>+<space>' : self.onoff_switch
        }
        self.keyboard_listner = Customized_Keyboard_Listener(hotkey_dictionary)
        
        functions = {
            'drag' : self.mouse_event_drag,
            'left_up' : self.mouse_event_left_up,
            'right_up' : self.mouse_event_right_up,
            'double_click' : self.mouse_event_double_click
        }
        self.mouse_listner = Customized_Mouse_Listener(functions)

        self.manager = Manager()
        self.manager.start()

        QApplication.clipboard().dataChanged.connect(self.event_clipboard)

        self.setWindowTitle('Helper For Learning Language')

        # other scenario
        self.word = make_label(self, self.text_in_clipboard, (10, 10), bold=True, font_size=20)

        self.btn_searching = QPushButton(self)
        self.btn_searching.setText("검색")
        self.btn_searching.move(*(10, 50))
        self.btn_searching.clicked.connect(self.search)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start()
    
    def update_ui(self):
        self.word.setText(self.text_in_clipboard)
        self.word.adjustSize()

    def search(self):
        if self.text_in_clipboard is 'Empty':
            return

        data = self.google_dict.get(self.text_in_clipboard)
        if isinstance(data, list):
            print(data)

            re_window = Registration_Window(data[0]['word'], data[0]['phonetics'], data[0]['meaning'])
            re_window.show()
    
    ##################################################################
    # On and Off
    ##################################################################
    def onoff_switch(self):
        if self.is_running:
            self.is_running = False
            self.hide()
        else:
            self.is_running = True
            self.show()
    
    ##################################################################
    # Translate
    ##################################################################
    def print_fn(self, result):
        print(result)
    
    ##################################################################
    # Mouse Event Handler
    ##################################################################
    def mouse_event_drag(self, status):
        print('[DRAG]', status)
        self.keyboard_listner.copy()
    
    def mouse_event_double_click(self, status):
        print('[DOUBLE]', status)
        self.keyboard_listner.copy()
        
    def mouse_event_left_up(self, status):
        pass

    def mouse_event_right_up(self, status):
        pass
    
    ##################################################################
    # Functions using PyQt5 
    ##################################################################
    def event_clipboard(self):
        if self.is_running:
            text = QApplication.clipboard().text()

            self.text_in_clipboard = text
            self.btn_searching.click()
            print(self.text_in_clipboard)

if __name__ == '__main__':
    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

    App = QApplication(sys.argv)

    window = Collector()
    window.show()
    # window.hide()

    sys.exit(App.exec())

