
from core.keyboard_api import Customized_Keyboard_Listener

def function():
    print('hotkey')

hotkey_dictionary = {
    '<ctrl>+<shift>+<space>' : function
}
keyboard = Customized_Keyboard_Listener(hotkey_dictionary)

while True:
    pass

