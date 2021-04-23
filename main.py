import os
import sys
import time
import platform

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu

from core.english_modules import Manager, Google_Dictionary

from core.devices.mouse_api import Customized_Mouse_Listener
from core.devices.keyboard_api import Customized_Keyboard_Listener

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

        # option = {
        #     'print_fn' : self.print_fn
        # }
        # self.manager = Manager(**option)
        # self.manager.start()

        self.google_dict = Google_Dictionary()

        self.is_running = True

        QApplication.clipboard().dataChanged.connect(self.event_clipboard)

        self.setWindowTitle('Collector_v1.2.0')
        self.resize(500, 700)
    
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

            data = self.google_dict.get(text)
            if isinstance(data, list):
                print(data[0])

                re_window = Registration_Window(data[0]['word'], data[0]['phonetics'], data[0]['meaning'])
                re_window.show()
    
    # def create_context_menu(self, position):
    #     if self.is_running:
    #         contextMenu = QMenu(self)
            
    #         action_of_word = contextMenu.addAction("Word")
    #         action_of_sentence = contextMenu.addAction("Sentence")
            
    #         action = contextMenu.exec_(position)

    #         if action == action_of_word:
    #             print('Word')
                
    #         elif action == action_of_sentence:
    #             print('Sentence')

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Collector()
    
    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

    sys.exit(App.exec())

