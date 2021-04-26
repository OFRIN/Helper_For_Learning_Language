import os
import sys
import time
import platform

from queue import Queue

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QPushButton

from core.english_modules import Papago, Twinword, Google_Dictionary
from core.managing_modules import Manager

from core.devices.mouse_api import Customized_Mouse_Listener
from core.devices.keyboard_api import Customized_Keyboard_Listener

from tools.json_utils import dict_to_json
from tools.qt_utils import make_label, make_push_button, make_edit, get_width_and_height, make_checkbox

from registration_window import Registration_Window

class Collector(QMainWindow):
    def __init__(self):
        super().__init__()

        #####################################################################################
        # Variables
        #####################################################################################
        self.flag_debug = False
        self.flag_detect_mouse_events = False
        self.flag_auto_search = False

        # make listeners
        # hotkey_dictionary = {
        #     '<ctrl>+<shift>+<space>' : self.onoff_switch
        # }
        # self.keyboard_listner = Customized_Keyboard_Listener(hotkey_dictionary)
        
        functions = {
            'drag' : self.mouse_event_drag,
            'left_up' : self.mouse_event_left_up,
            'right_up' : self.mouse_event_right_up,
            'double_click' : self.mouse_event_double_click
        }
        self.mouse_listner = Customized_Mouse_Listener(functions)

        # make queue
        self.queue = Queue(maxsize=50)

        # make manger
        # self.manager = Manager(self.queue, self.custom_function)
        # self.manager.start()

        self.google_dict = Google_Dictionary()

        #####################################################################################
        # UI (about PyQt5)
        #####################################################################################
        self.initUI()

        # connect function to detect text in clipboard
        QApplication.clipboard().dataChanged.connect(self.event_clipboard)
    
    def initUI(self):
        self.setWindowTitle('Helper For Learning Language')
        self.resize(600, 120)

        self.check_logs = make_checkbox(self, 'Logs (ON/OFF)', (10, 10), self.show_logs)
        self.check_mouse = make_checkbox(self, 'Detect Mouse (ON/OFF)', (10, 30), self.detect_mouse_events)
        self.check_auto = make_checkbox(self, 'Auto Searching (ON/OFF)', (10, 50), self.auto_searching)

        self.check_logs.setChecked(True)

        self.edi_word = make_edit(self, 'empty', (10, 90))

        x, y, width, height = get_width_and_height(self.edi_word)
        self.btn_search = make_push_button(self, '검색', (x + width + 10, y), self.search)

        # self.timer_to_adjust_ui = QTimer(self)
        # self.timer_to_adjust_ui.setInterval(1000)
        # self.timer_to_adjust_ui.timeout.connect(self.update_ui)
        # self.timer_to_adjust_ui.start()

        self.flag_debug = self.check_logs.isChecked()
        self.flag_detect_mouse_events = self.check_mouse.isChecked()

        # self.adjustSize()

    ##################################################################
    # Customized Functions
    ##################################################################
    def onoff_switch(self):
        pass
    
    def show_registration(self, data):
        sub_window = Registration_Window(data[0]['word'], data[0]['phonetics'], data[0]['meaning'])
        sub_window.show()

    def search(self):
        self.btn_search.setDisabled(True)
        # self.queue.put(self.edi_word.text())

        data = self.google_dict.get(self.edi_word.text())
        self.show_registration(data)

        self.btn_search.setDisabled(False)
    
    def show_logs(self, state):
        self.flag_debug = self.check_logs.isChecked()
    
    def detect_mouse_events(self, state):
        self.flag_detect_mouse_events = self.check_mouse.isChecked()

    def auto_searching(self, state):
        self.flag_auto_search = self.check_auto.isChecked()

    ##################################################################
    # Mouse Event Handler
    ##################################################################
    def mouse_event_drag(self, status):
        if self.flag_detect_mouse_events:
            print('[DRAG]', status)
            # self.keyboard_listner.copy()
    
    def mouse_event_double_click(self, status):
        if self.flag_detect_mouse_events:
            print('[DOUBLE]', status)
            # self.keyboard_listner.copy()
        
    def mouse_event_left_up(self, status):
        pass

    def mouse_event_right_up(self, status):
        pass
    
    ##################################################################
    # Functions using PyQt5 
    ##################################################################
    def event_clipboard(self):
        text = QApplication.clipboard().text()

        if self.flag_debug:
            print(text, type(text), len(text))

        # for image or not
        if len(text) > 0:
            # self.queue.put(text)
            self.edi_word.setText(text)

            if self.flag_auto_search:
                self.btn_search.click()

if __name__ == '__main__':
    # if platform.system() == 'Linux':
    #     os.system('clear')
    # else:
    #     os.system('cls')

    App = QApplication(sys.argv)

    window = Collector()
    window.show()
    # window.hide()

    sys.exit(App.exec())

