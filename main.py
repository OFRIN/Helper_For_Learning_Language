
import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu

from core.mouse_api import Customized_Mouse_API
from core.keyboard_api import Customized_Keyboard_API

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
        mouse = Customized_Mouse_API(functions)

        QApplication.clipboard().dataChanged.connect(self.event_clipboard)
    
    def mouse_event_drag(self):
        self.keyboard.copy()

    def mouse_event_double_click(self):
        self.keyboard.copy()

    def mouse_event_left_up(self):
        pass

    def mouse_event_right_up(self):
        pass

    def event_clipboard(self):
        text = QApplication.clipboard().text()

        if check_string_type(text):
            text = preprocessing_for_string(text)
            if len(text) > 0:
                print(text)

    def create_context_menu(self, position):
        contextMenu = QMenu(self)
        
        newAct = contextMenu.addAction("New")
        openAct = contextMenu.addAction("Open")
        quitAct = contextMenu.addAction("Quit")
        
        action = contextMenu.exec_(position)
        if action == quitAct:
            self.close()

App = QApplication(sys.argv)
window = Collector()
sys.exit(App.exec())

