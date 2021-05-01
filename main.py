import os
import sys
import time
import platform
import webbrowser

from queue import Queue

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QPushButton

from word_forms.lemmatizer import lemmatize

from core.english_modules import Papago, Twinword, Google_Dictionary
from core.managing_modules import Manager

from core.devices.mouse_api import Customized_Mouse_Listener
from core.devices.keyboard_api import Customized_Keyboard_Listener

from tools.json_utils import dict_to_json, read_json, write_json
from tools.qt_utils import make_label, make_push_button, make_edit, get_width_and_height, make_checkbox

from registration_window import Registration_Window

class Collector(QMainWindow):
    def __init__(self):
        super().__init__()

        #####################################################################################
        # Variables
        #####################################################################################
        self.flag_debug = False
        self.flag_detect_mouse_events = False
        self.flag_auto_search = False
        self.flag_sentence = False

        # make listeners
        hotkey_dictionary = {
            # '<ctrl>+<shift>+<space>' : self.onoff_switch
        }
        self.keyboard_listner = Customized_Keyboard_Listener(hotkey_dictionary)
        
        functions = {
            'drag' : self.mouse_event_drag,
            'left_up' : self.mouse_event_left_up,
            'right_up' : self.mouse_event_right_up,
            'double_click' : self.mouse_event_double_click
        }
        self.mouse_listner = Customized_Mouse_Listener(functions)

        # make queue
        self.queue = Queue(maxsize=50)

        # make manger
        # self.manager = Manager(self.queue, self.custom_function)
        # self.manager.start()

        info_dic = read_json('./data/private_information.json')

        self.twin_model = Twinword(**info_dic['twinword'])
        self.google_dict = Google_Dictionary()

        #####################################################################################
        # UI (about PyQt5)
        #####################################################################################
        self.initUI()

        # connect function to detect text in clipboard
        QApplication.clipboard().dataChanged.connect(self.event_clipboard)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
    
    def initUI(self):
        self.setWindowTitle('Helper For Learning Language')
        self.resize(700, 120)
        
        self.check_logs = make_checkbox(self, 'Logs (ON/OFF)', (10, 10), self.show_logs)
        self.check_mouse = make_checkbox(self, 'Detect Mouse (ON/OFF)', (10, 30), self.detect_mouse_events)
        self.check_auto = make_checkbox(self, 'Auto Searching (ON/OFF)', (10, 50), self.auto_searching)
        self.check_sentence = make_checkbox(self, 'Word or Sentence', (10, 70), self.auto_searching)

        self.check_logs.setChecked(True)

        self.edi_word = make_edit(self, 'empty', (10, 90))

        x, y, width, height = get_width_and_height(self.edi_word)
        self.btn_search = make_push_button(self, 'Search', (x + width + 10, y), self.search, './resources/search.png')

        x, y, width, height = get_width_and_height(self.btn_search)
        self.btn_naver = make_push_button(self, 'NAVER', (x + width + 10, y), self.search_using_naver, './resources/naver_dictionary.jpg')

        # self.timer_to_adjust_ui = QTimer(self)
        # self.timer_to_adjust_ui.setInterval(1000)
        # self.timer_to_adjust_ui.timeout.connect(self.update_ui)
        # self.timer_to_adjust_ui.start()

        self.flag_debug = self.check_logs.isChecked()
        self.flag_detect_mouse_events = self.check_mouse.isChecked()

        # self.adjustSize()
        self.db_path = './data/db.json'
        self.tense_path = './data/tense.json'

        if os.path.isfile(self.db_path):
            self.db = read_json(self.db_path, 'utf-8')
        else:
            self.db = {}

        if os.path.isfile(self.tense_path):
            self.tense_dict = read_json(self.tense_path, 'utf-8')
        else:
            self.tense_dict = {}

    ##################################################################
    # Customized Functions
    ##################################################################
    def onoff_switch(self):
        pass

    def save(self):
        write_json(self.db_path, self.db, 'utf-8')
        write_json(self.tense_path, self.tense_dict, 'utf-8')
    
    def show_registration(self, data, korean_meaning):
        sub_window = Registration_Window(data[0]['word'], data[0]['phonetics'], data[0]['meaning'], korean_meaning)
        sub_window.show()

    def search(self):
        self.btn_search.setDisabled(True)

        word = self.edi_word.text()

        try:
            if word in self.tense_dict or word in self.db:
                if word in self.tense_dict:
                    word = self.tense_dict[word] 

                data_from_google = self.db[word]['google']
                data_from_twin = self.db[word]['twin']

            else:
                try:
                    word_forms_error = False
                    original_word = lemmatize(word)
                except ValueError:
                    # ValueError: Shutting is not a real word
                    original_word = word
                    word_forms_error = True
                
                data_from_google = self.google_dict.get(original_word)

                if word_forms_error:
                    original_word = data_from_google[0]['word']

                data_from_twin = self.twin_model.get(original_word)

                self.db[original_word] = {
                    'google' : data_from_google,
                    'twin' : data_from_twin
                }
                self.tense_dict[word] = original_word

                self.save()

            try:
                korean_meaning = data_from_twin['meaning']['korean']
            except KeyError:
                korean_meaning = ''

            self.show_registration(data_from_google, korean_meaning)

        except KeyError:
            print('Don\'t find this word : {}'.format(word))
        
        finally:
            self.btn_search.setDisabled(False)

    def search_using_naver(self):
        self.btn_naver.setDisabled(True)

        # data = self.google_dict.get(self.edi_word.text())
        # self.show_registration(data)

        url = 'https://en.dict.naver.com/#/search?query={}'.format(self.edi_word.text())

        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

        self.btn_naver.setDisabled(False)
    
    def show_logs(self, state):
        self.flag_debug = self.check_logs.isChecked()
    
    def detect_mouse_events(self, state):
        self.flag_detect_mouse_events = self.check_mouse.isChecked()

    def auto_searching(self, state):
        self.flag_auto_search = self.check_auto.isChecked()

    def check_sentence(self):
        self.flag_sentence = self.check_sentence.isChecked()

    ##################################################################
    # Mouse Event Handler
    ##################################################################
    def mouse_event_drag(self, status):
        if self.flag_detect_mouse_events:
            print('[DRAG]', status)
            self.keyboard_listner.copy()
    
    def mouse_event_double_click(self, status):
        if self.flag_detect_mouse_events:
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

        # search a word in kindle
        if 'Kindle' in text and not self.flag_sentence:
            text = text.replace('\n\n' + text.split('\n\n')[-1], '')
        
        # if the text is not sentence, this program will remove ',' and '.'.
        if not self.flag_sentence:
            text = text.replace(',', '').replace('.', '')

        if self.flag_debug:
            print(text, type(text), len(text))

        # for image or not
        if len(text) > 0:
            # self.queue.put(text)
            self.edi_word.setText(text)

            if self.flag_auto_search:
                self.btn_search.click()

if __name__ == '__main__':
    # if platform.system() == 'Linux':
    #     os.system('clear')
    # else:
    #     os.system('cls')

    App = QApplication(sys.argv)

    window = Collector()
    window.show()
    # window.hide()

    sys.exit(App.exec())

