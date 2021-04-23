import time

from pynput import mouse

class Customized_Mouse_Listener:
    def __init__(self, functions, moving_threshold=20, double_click_interval=0.5):
        self.functions = functions

        self.status = {
            'x' : -1,
            'y' : -1,

            'direction': 'left',
            'pressed' : False,
            
            'moving_count' : 0,
            'last_clicked_time' : 0,
        }

        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
        )
        self.listener.start()
        
        self.moving_threshold = moving_threshold
        self.double_click_interval = double_click_interval

    def on_move(self, x, y):
        self.status['x'] = x
        self.status['y'] = y

        if self.status['pressed']:
            self.status['moving_count'] += 1
    
    def on_click(self, x, y, button, pressed):
        self.status['x'] = x
        self.status['y'] = y
        self.status['direction'] = 'right' if button == mouse.Button.right else 'left'
        self.status['pressed'] = pressed

        variables = [self.status['direction'], self.status['pressed'], self.status['x'], self.status['y']]
        event_format = 'event_name={}, direction={}, pressed={}, x={}, y={}'
        
        if self.status['direction'] == 'left':
            if self.status['pressed']:
                pass
            else:
                if self.status['moving_count'] > self.moving_threshold:
                    # print(self.status['last_clicked_time'], time.time(), 'DRAG')
                    self.functions['drag'](self.status)
                else:
                    interval = float(time.time() - self.status['last_clicked_time'])
                    # print(self.status['last_clicked_time'], time.time(), interval)

                    if interval < self.double_click_interval:
                        self.functions['double_click'](self.status)
                    else:
                        self.functions['left_up'](self.status)

        elif button == mouse.Button.right and not pressed:
            self.functions['right_up'](self.status)

        if not pressed and mouse.Button.left:
            self.status['last_clicked_time'] = time.time()
            self.status['moving_count'] = 0
