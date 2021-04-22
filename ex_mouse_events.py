# pip install pynput
from pynput import mouse

from core.mouse_api import Customized_Mouse_Listener

def mouse_event_drag(status):
    print('DRAG', status)

def mouse_event_left_up(status):
    print('LEFT', status)

def mouse_event_right_up(status):
    print('RIGHT', status)

def mouse_event_double_click(status):
    print('DOUBLE', status)

functions = {
    'drag' : mouse_event_drag,
    'left_up' : mouse_event_left_up,
    'right_up' : mouse_event_right_up,
    'double_click' : mouse_event_double_click
}
mouse_obj = Customized_Mouse_Listener(functions)

while True:
    pass

