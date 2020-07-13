
from pynput import keyboard

class Customized_Keyboard_API:
    def __init__(self, debug=False):
        self.controller = keyboard.Controller()
    
    def copy(self):
        with self.controller.pressed(keyboard.Key.ctrl_l):
            self.controller.press('c')
