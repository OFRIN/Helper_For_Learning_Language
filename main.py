import os
import sys
import time
import platform

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu

from core.mouse_api import Customized_Mouse_API
from core.keyboard_api import Customized_Keyboard_API

from data.manager import *

from utility import * 

class Collector(QMainWindow):
    def __init__(self):
        super().__init__()

        hotkey_dictionary = {
            '<ctrl>+<shift>+<space>' : self.onoff_switch
        }
        self.keyboard = Customized_Keyboard_API(hotkey_dictionary)
        
        functions = {
            'drag' : self.mouse_event_drag,
            'left_up' : self.mouse_event_left_up,
            'right_up' : self.mouse_event_right_up,
            'double_click' : self.mouse_event_double_click
        }
        self.mouse = Customized_Mouse_API(functions)
        self.mouse_controller = mouse.Controller()

        option = {
            'print_fn' : self.print_fn
        }
        self.manager = Manager(**option)
        # self.manager.start()

        self.is_running = False

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
        print(json.dumps(result, indent='\t'))

    ##################################################################
    # Mouse Event Handler
    ##################################################################
    def mouse_event_drag(self, status):
        self.create_context_menu(QPoint(status['x'], status['y']))

    def mouse_event_double_click(self, status):
        # self.create_context_menu(QPoint(status['x'], status['y']))
        pass

    def mouse_event_left_up(self, status):
        pass

    def mouse_event_right_up(self, status):
        pass
    
    ##################################################################
    # Functions using PyQt5 
    ##################################################################
    # Context Menu가 종료된 후 왜 double click 이벤트가 발생하는지 확인 필요
    
    def event_clipboard(self):
        if self.is_running:
            text = QApplication.clipboard().text()
            self.manager.push(text)

    def create_context_menu(self, position):
        if self.is_running:
            contextMenu = QMenu(self)
            
            action_of_word = contextMenu.addAction("Word")
            action_of_sentence = contextMenu.addAction("Sentence")
            
            action = contextMenu.exec_(position)

            if action == action_of_word:
                print('Word')
                
            elif action == action_of_sentence:
                print('Sentence')

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Collector()

    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

    sys.exit(App.exec())

