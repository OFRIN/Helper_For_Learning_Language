import time

from pynput import mouse

class Customized_Mouse_API:
    def __init__(self, functions, debug=False):
        self.debug = debug
        self.functions = functions

        self.status = {
            'x' : -1,
            'y' : -1,

            'moving_count' : 0,
            'pressed' : False,

            'last_clicked_time' : 0,
        }

        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
        )
        self.listener.start()

    def on_move(self, x, y):
        self.status['x'] = x
        self.status['y'] = y

        if self.status['pressed']:
            self.status['moving_count'] += 1
    
    def on_click(self, x, y, button, pressed):
        self.status['x'] = x
        self.status['y'] = y
        self.status['pressed'] = pressed

        print(button, pressed)
        
        if button == mouse.Button.left:
            if self.status['pressed']:
                pass
            else:
                if self.status['moving_count'] > 20:
                    self.functions['drag'](self.status)
                else:
                    interval = float(time.time() - self.status['last_clicked_time'])
                    if interval < 0.5:
                        self.functions['double_click'](self.status)
                    else:
                        self.functions['left_up'](self.status)

        elif button == mouse.Button.right and not pressed:
            self.functions['right_up'](self.status)

        if not pressed and mouse.Button.left:
            self.status['last_clicked_time'] = time.time()
            self.status['moving_count'] = 0
        
if __name__ == '__main__':
    obj = Customized_Mouse_API()

    while True:
        pass