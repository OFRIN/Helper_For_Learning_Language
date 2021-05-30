import os
import cv2
import sys
import time
import socket
import platform

from PyQt5.Qt import Qt

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QPushButton

from core import english_modules
from core.devices import mouse_api, keyboard_api

from tools import english_utils
from tools import qt_utils

class Downloader(QtCore.QThread):
    show_image = QtCore.pyqtSignal(str)

    def __init__(self, image_dir, chrome_path, delay, parent=None):
        super().__init__(parent=parent)
        
        self.working = True
        self.text = None

        self.crawler = english_modules.NAVER_Dictionary_Crawler(image_dir, chrome_path, delay)

        self.start()

    def set_text(self, text):
        self.text = text

    def run(self):
        while self.working:
            if self.text is None:
                continue
            elif len(self.text) == 0:
                self.show_image.emit('Empty String')
                self.text = None

            else:
                image_path = self.crawler(self.text)

                self.show_image.emit(image_path)
                self.text = None
    
    def close(self):
        self.working = False

        self.quit()
        self.wait(1000)

class Collector(QMainWindow):
    def __init__(self):
        super().__init__()

        #####################################################################################
        # Variables
        #####################################################################################
        self.image_dir = './data/images/'
        self.chrome_path = './data/chromedriver.exe'
        self.delay = 1.0

        self.width = 550
        self.height = 80

        # self.normal_icon_path = './resources/green.png'
        # self.search_icon_path = './resources/red.png'

        self.normal_icon_path = './resources/bookmark_G.png'
        self.search_icon_path = './resources/bookmark_R.png'

        self.btn_icon_path = './resources/naver_dictionary.png'

        self.window_name = 'Helper'

        if not os.path.isdir(self.image_dir):
            os.makedirs(self.image_dir)
        
        #####################################################################################
        # PyQt5
        #####################################################################################
        self.build_UI()

        #####################################################################################
        # Customized Libraries
        #####################################################################################
        self.build_listner()

        self.downloader = Downloader(image_dir=self.image_dir, chrome_path=self.chrome_path, delay=self.delay, parent=self)
        self.downloader.show_image.connect(self.show_image)

    def normal_icon(self):
        self.setWindowIcon(QtGui.QIcon(self.normal_icon_path))

    def search_icon(self):
        self.setWindowIcon(QtGui.QIcon(self.search_icon_path))
    
    def build_UI(self):
        # ui
        self.normal_icon()
        self.setWindowTitle('Helper For Learning Language')

        self.setFixedSize(self.width, self.height)
        
        self.check_detecting_mouse = qt_utils.make_checkbox(self, 'Detect mouse events', (10, 10), self.detecting_mouse)
        self.check_automatic_searching = qt_utils.make_checkbox(self, 'Search meaning automatically', (10, 30), self.automatic_searching)

        self.edi_word = qt_utils.make_edit(self, '', (10, 50))

        x, y, width, height = qt_utils.get_width_and_height(self.edi_word)
        self.btn_naver = qt_utils.make_push_button(self, '', (x + width + 10, y), self.search, self.btn_icon_path)

        # flag
        self.flag_detecting_mouse = self.check_detecting_mouse.isChecked()
        self.flag_automatic_searching = self.check_automatic_searching.isChecked()

        print('# detecting mouse : {}'.format(self.flag_detecting_mouse))
        print('# automatic searching : {}'.format(self.flag_automatic_searching))

        # option
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # connection
        QApplication.clipboard().dataChanged.connect(self.event_clipboard)

    def build_listner(self):
        hotkey_dictionary = {
            # '<ctrl>+<shift>+<space>' : None
            '<ctrl>+<shift>+s' : self.search,
            '<ctrl>+<shift>+d' : self.close_window
        }
        self.keyboard_listner = keyboard_api.Customized_Keyboard_Listener(hotkey_dictionary)
        
        functions = {
            'drag' : self.mouse_event_drag,
            'left_up' : self.mouse_event_left_up,
            'right_up' : self.mouse_event_right_up,
            'double_click' : self.mouse_event_double_click
        }
        self.mouse_listner = mouse_api.Customized_Mouse_Listener(functions)
        
    ##################################################################
    # Customized Functions
    ##################################################################
    def show_window(self, image, cropped=True):
        if cropped:
            h, w, c = image.shape

            xmin, ymin = 462, 242
            xmax, ymax = 1152, h - 1

            image = image[ymin:ymax, xmin:xmax]

        cv2.imshow(self.window_name, image)
        key = cv2.waitKey(0)
        self.close_window()

        return key

    def close_window(self):
        cv2.destroyWindow(self.window_name)

    def search(self):
        self.search_icon()
        self.btn_naver.setDisabled(True)
        
        text = self.edi_word.text()
        self.downloader.set_text(text)

    @QtCore.pyqtSlot(str)
    def show_image(self, image_path):
        self.normal_icon()
        self.btn_naver.setDisabled(False)
        
        image = cv2.imread(image_path)
        if image is None:
            print('# Not found image ({})'.format(image_path))
        else:
            key = self.show_window(image)
            if key == ord('r'):
                os.remove(image_path)
    
    def detecting_mouse(self, state):
        self.flag_detecting_mouse = self.check_detecting_mouse.isChecked()
        print('# detecting mouse : {}'.format(self.flag_detecting_mouse))

    def automatic_searching(self, state):
        self.flag_automatic_searching = self.check_automatic_searching.isChecked()
        print('# automatic searching : {}'.format(self.flag_automatic_searching))

    ##################################################################
    # Mouse Event Handler
    ##################################################################
    def mouse_event_drag(self, status):
        if self.flag_detecting_mouse:
            print('[DRAG]', status)
            self.keyboard_listner.copy()
    
    def mouse_event_double_click(self, status):
        if self.flag_detecting_mouse:
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
        text = QApplication.clipboard().text()

        if len(text) > 0:
            print(text)

            # exception 1. kindle
            text = english_utils.remove_kindle_option(text)
            
            # exception 2. wrong keyword
            text = english_utils.remove_wrong_keyword(text)

            self.edi_word.setText(text)

            if self.flag_automatic_searching:
                self.btn_naver.click()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, e):
        self.hide()
        self.downloader.close()

if __name__ == '__main__':
    App = QApplication(sys.argv)

    window = Collector()
    window.show()

    sys.exit(App.exec())

