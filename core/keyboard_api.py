
from pynput import keyboard

class Customized_Keyboard_Listener:
    def __init__(self, hotkey_dictionary):
        self.controller = keyboard.Controller()
        
        self.listener = keyboard.GlobalHotKeys(hotkey_dictionary)
        self.listener.start()
    
    def copy(self):
        with self.controller.pressed(keyboard.Key.ctrl_l):
            self.controller.press('c')
