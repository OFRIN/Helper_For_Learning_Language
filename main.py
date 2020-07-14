import os
import sys
import time
import platform

from pynput import mouse

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

        self.keyboard = Customized_Keyboard_API()
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
        self.manager.start()

        # self.is_open_context_menu = False

        QApplication.clipboard().dataChanged.connect(self.event_clipboard)
    
    def print_fn(self, result):
        print(json.dumps(result, indent='\t'))

    # for
    def mouse_event_drag(self):
        # self.keyboard.copy()
        pass

    def mouse_event_double_click(self):
        self.keyboard.copy()

    def mouse_event_left_up(self):
        pass

    def mouse_event_right_up(self, status):
        # self.create_context_menu(QPoint(status['x'], status['y']))
        pass

    def event_clipboard(self):
        text = QApplication.clipboard().text()
        self.manager.push(text)

    def create_context_menu(self, position):
        self.mouse_controller.click(mouse.Button.left, 1)

        contextMenu = QMenu(self)
        
        newAct = contextMenu.addAction("New")
        openAct = contextMenu.addAction("Open")
        quitAct = contextMenu.addAction("Quit")
        
        action = contextMenu.exec_(position)
        if action == quitAct:
            self.close()

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Collector()

    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

    sys.exit(App.exec())

