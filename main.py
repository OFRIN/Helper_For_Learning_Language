import os
import cv2
import sys
import time
import platform

from PyQt5.Qt import Qt

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QPushButton

from core import english_modules
from core.devices import mouse_api, keyboard_api

from tools import english_utils
from tools import qt_utils

class Collector(QMainWindow):
    def __init__(self):
        super().__init__()

        #####################################################################################
        # Variables
        #####################################################################################
        self.image_dir = './data/images/'
        self.chrome_path = './data/chromedriver.exe'
        
        #####################################################################################
        # PyQt5
        #####################################################################################
        self.build_UI()

        #####################################################################################
        # Customized Libraries
        #####################################################################################
        self.build_listner()

        self.crawler = english_modules.NAVER_Dictionary_Crawler(image_dir='./data/images/', chrome_path='./data/chromedriver.exe', delay=1.0)

        # info_dic = read_json('./data/private_information.json')
        # self.papago = Papago(**info_dic['papago'])
    
    def build_UI(self):
        # ui
        self.setWindowTitle('Helper For Learning Language')
        self.resize(550, 80)
        
        self.check_detecting_mouse = qt_utils.make_checkbox(self, 'Detect mouse events', (10, 10), self.detecting_mouse)
        self.check_automatic_searching = qt_utils.make_checkbox(self, 'Search meaning automatically', (10, 30), self.automatic_searching)

        self.edi_word = qt_utils.make_edit(self, '', (10, 50))

        x, y, width, height = qt_utils.get_width_and_height(self.edi_word)
        self.btn_naver = qt_utils.make_push_button(self, '', (x + width + 10, y), self.search, './resources/naver_dictionary.jpg')

        # flag
        self.flag_detecting_mouse = self.check_detecting_mouse.isChecked()
        self.flag_automatic_searching = self.check_automatic_searching.isChecked()

        print('# detecting mouse : {}'.format(self.flag_detecting_mouse))
        print('# automatic searching : {}'.format(self.flag_automatic_searching))

        # option
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # connection
        QApplication.clipboard().dataChanged.connect(self.event_clipboard)

    def build_listner(self):
        hotkey_dictionary = {
            '<ctrl>+<shift>+<space>' : None
        }
        self.keyboard_listner = keyboard_api.Customized_Keyboard_Listener(hotkey_dictionary)
        
        functions = {
            'drag' : self.mouse_event_drag,
            'left_up' : self.mouse_event_left_up,
            'right_up' : self.mouse_event_right_up,
            'double_click' : self.mouse_event_double_click
        }
        self.mouse_listner = mouse_api.Customized_Mouse_Listener(functions)
        
    ##################################################################
    # Customized Functions
    ##################################################################
    def search(self):
        self.btn_naver.setDisabled(True)
        
        image = self.crawler(self.edi_word.text())
        if image is not None:
            cv2.imshow('NAVER', image)
            cv2.waitKey(0)
            cv2.destroyWindow('NAVER')
        
        self.btn_naver.setDisabled(False)
    
    def detecting_mouse(self, state):
        self.flag_detecting_mouse = self.check_detecting_mouse.isChecked()
        print('# detecting mouse : {}'.format(self.flag_detecting_mouse))

    def automatic_searching(self, state):
        self.flag_automatic_searching = self.check_automatic_searching.isChecked()
        print('# automatic searching : {}'.format(self.flag_automatic_searching))

    ##################################################################
    # Mouse Event Handler
    ##################################################################
    def mouse_event_drag(self, status):
        if self.flag_detecting_mouse:
            print('[DRAG]', status)
            self.keyboard_listner.copy()
    
    def mouse_event_double_click(self, status):
        if self.flag_detecting_mouse:
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
        text = QApplication.clipboard().text()

        if len(text) > 0:
            # exception 1. kindle
            text = english_utils.remove_kindle_option(text)
            
            # exception 2. wrong keyword
            text = english_utils.remove_wrong_keyword(text)

            self.edi_word.setText(text)

            if self.flag_automatic_searching:
                self.btn_naver.click()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()

if __name__ == '__main__':
    App = QApplication(sys.argv)

    window = Collector()
    window.show()

    sys.exit(App.exec())

