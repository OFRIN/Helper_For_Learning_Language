import sys
import vlc
import copy

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia

from tools.qt_utils import make_label

class Tab_Window(QtWidgets.QWidget):
    def __init__(self, meanings, limit_length=200, margin=20):
        super().__init__()
        
        # Convert 1D meanings to 2D meanings
        self.groups = []

        self.groups.append([])
        length_definition = 0

        for index, meaning in enumerate(meanings):
            # print(len(meaning['definition']), meaning['definition'])
            
            self.groups[-1].append(
                {
                    'index' : index,
                    'meaning' : meaning
                }
            )

            length_definition += len(meaning['definition'])
            if length_definition > limit_length:
                self.groups.append([])
                length_definition = 0
        
        # print('the number of meanings : {}'.format(len(meanings)))
        # print(f'the shape = ({len(self.groups[0])}x{len(self.groups)})')

        # define width and height
        self.width = 0
        self.height = 0

        # define default paramters
        start_x = 10
        start_y = 20
        
        default_width = 300
        default_height = 200
        
        for group_per_column in self.groups:
            default_rect_for_start_group = QtCore.QRect(start_x, start_y, default_width, default_height)

            default_rect = copy.deepcopy(default_rect_for_start_group)

            max_width_per_column = 0
            max_height_per_column = 0

            for group in group_per_column:
                # make GroupBox
                group_of_meaning = QtWidgets.QGroupBox(str(group['index'] + 1), self)
                group_of_meaning.setGeometry(default_rect)
                
                meaning_string = '# meaning\n' + '- ' + group['meaning']['definition']
                if 'kr_definition' in group['meaning']:
                    meaning_string += '\n' + '- ' + group['meaning']['kr_definition']

                en_definition = make_label(
                    group_of_meaning, 
                    meaning_string,
                    (10, 20)
                )
                previous_rect = en_definition.geometry()
                
                if 'synonyms' in group['meaning']:
                    en_synonyms = make_label(
                            group_of_meaning, 
                            '# synonyms : {}'.format(group['meaning']['synonyms'][:5]), 
                            (10, previous_rect.y() + previous_rect.height() + margin)
                    )
                    previous_rect = en_synonyms.geometry()
                
                if 'example' in group['meaning']:
                    example_string = '# example\n' + '- ' + group['meaning']['example']

                    if 'kr_example' in group['meaning']:
                        example_string += '\n' + '- ' + group['meaning']['kr_example']

                    en_example = make_label(
                            group_of_meaning, 
                            example_string, 
                            (10, previous_rect.y() + previous_rect.height() + margin)
                    )
                
                group_of_meaning.adjustSize()
                
                # get geometry of the GroupBox
                rect_of_group = group_of_meaning.geometry()

                # calculate width of the next GroupBox
                width_per_column = rect_of_group.x() + rect_of_group.width() + margin
                height_per_column = rect_of_group.y() + rect_of_group.height() + margin

                max_width_per_column = max(max_width_per_column, width_per_column)
                max_height_per_column = max(max_height_per_column, height_per_column)
                
                # update default_rect using the geometry
                default_rect.setX(width_per_column)
                default_rect.setWidth(default_width)
            
            # print(start_y, max_height_per_column)
            start_y = max_height_per_column
            
            self.width = max(self.width, max_width_per_column)
            self.height = max(self.height, max_height_per_column)

        self.height += margin
        
        self.adjustSize()

class MP3_Callback:
    def __init__(self, mp3_url):
        self.mp3_url = mp3_url

    def __call__(self):
        # print(self.mp3_url)

        p = vlc.MediaPlayer(self.mp3_url)
        p.play()
        
        # player = QtMultimedia.QMediaPlayer()
        # player.setMedia(QtCore.QUrl(self.mp3_url))
        # player.play()
        
        # QtMultimedia.QSound.play(self.mp3_url)

# class Registration_Window(QtWidgets.QWidget):
class Registration_Window(QtWidgets.QDialog):
    def __init__(self, word, phonetics, meanings, korean_meaning='', position=(10, 10)):
        super().__init__(parent=None)

        self.minimum_width = 300
        
        self.setWindowTitle("Registration")
        self.setGeometry(QtCore.QRect(10, 10, self.minimum_width, 300))
        
        if korean_meaning is not '':
            word += ' : ' + korean_meaning
            
        self.word = make_label(self, word, (10, 10), bold=True, font_size=20)
        
        self.make_groupbox_for_phonetics(phonetics)
        self.make_tablewidget_for_meanings(meanings)

        self.adjustSize()
        
        if self.geometry().width() < self.minimum_width:
            self.setFixedWidth(self.minimum_width)

        print(position)
        self.move(*position)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # |QtCore.Qt.FramelessWindowHint
        
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QtWidgets.QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())

    def make_groupbox_for_phonetics(self, phonetics):
        rect_of_word = self.word.geometry()
        
        self.group_of_phonetics = QtWidgets.QGroupBox('Phonetics', self)
        self.group_of_phonetics.setGeometry(QtCore.QRect(10, rect_of_word.y() + rect_of_word.height() + 20, 250, 80))
        
        margin = 20
        rect_of_group = self.group_of_phonetics.geometry()
        
        # for i in range(3):
        #     phonetics.append(phonetics[0])

        for index, phonetic in enumerate(phonetics):
            x, y = rect_of_group.x(), 15 + (index) * margin
            
            refined_phonetic = phonetic['text'].replace('/', '')
            self.label_phonetic = make_label(
                self.group_of_phonetics, 
                f'[{refined_phonetic}]', 
                (x, y), 
                bold=True, font_size=15
            )
            
            rect_of_label = self.label_phonetic.geometry()
            w, h = rect_of_label.width(), rect_of_label.height()
            
            self.btn_play = QtWidgets.QPushButton('PLAY', self.group_of_phonetics)
            self.btn_play.setGeometry(QtCore.QRect(rect_of_label.x() + w + 20, y, 100, h))
            self.btn_play.clicked.connect(MP3_Callback(phonetic['audio']))
            self.btn_play.setIcon(QtGui.QIcon('./resources/mx-player-icon.png'))
        
        self.group_of_phonetics.adjustSize()
        # self.group_of_phonetics.setFixedWidth(250)
    
    def make_tablewidget_for_meanings(self, meanings):
        rect_of_group = self.group_of_phonetics.geometry()
        y = rect_of_group.y()
        h = rect_of_group.height()

        self.table_of_meanings = QtWidgets.QTabWidget(self)
        self.table_of_meanings.setGeometry(QtCore.QRect(10, y + h + 10, 500, 600))

        table_index = 1
        tags = sorted(list(meanings.keys()))

        table_width = 0
        table_height = 0

        for tag in tags:
            tab = Tab_Window(meanings[tag], limit_length=200, margin=10)

            table_width = max(table_width, tab.width)
            table_height = max(table_height, tab.height)

            self.table_of_meanings.addTab(tab, tag)
            table_index += 1
        
        self.table_of_meanings.setFixedWidth(table_width)
        self.table_of_meanings.setFixedHeight(table_height)

        # self.table_of_meanings.adjustSize()

    def show(self):
        return super().exec_()

if __name__ == "__main__":
    data = [
            {
                    "word": "take",
                    "phonetics": [
                            {
                                    "text": "/teɪk/",
                                    "audio": "https://lex-audio.useremarkable.com/mp3/take_gb_1.mp3"
                            }
                    ],
                    "meaning": {
                            "verb": [
                                    {
                                            "definition": "Lay hold of (something) with one's hands; reach for and hold.",
                                            "synonyms": [
                                                    "lay hold of",
                                                    "take hold of",
                                                    "get hold of",
                                                    "get into one's hands"
                                            ],
                                            "example": "Mrs Morgan took another biscuit"
                                    },
                                    {
                                            "definition": "Remove (someone or something) from a particular place.",
                                            "synonyms": [
                                                    "remove",
                                                    "pull",
                                                    "draw",
                                                    "withdraw",
                                                    "extract",
                                                    "fish"
                                            ],
                                            "example": "he took an envelope from his inside pocket"
                                    },
                                    {
                                            "definition": "Carry or bring with one; convey.",
                                            "synonyms": [
                                                    "bring",
                                                    "carry",
                                                    "bear",
                                                    "transport",
                                                    "convey",
                                                    "move",
                                                    "transfer",
                                                    "shift",
                                                    "haul",
                                                    "drag",
                                                    "lug",
                                                    "cart",
                                                    "ferry"
                                            ],
                                            "example": "he took along a portfolio of his drawings"
                                    },
                                    {
                                            "definition": "Accept or receive (someone or something)",
                                            "synonyms": [
                                                    "accept",
                                                    "take up",
                                                    "take on",
                                                    "undertake"
                                            ],
                                            "example": "she was advised to take any job offered"
                                    },
                                    {
                                            "definition": "Consume as food, drink, medicine, or drugs.",
                                            "synonyms": [
                                                    "drink",
                                                    "imbibe"
                                            ],
                                            "example": "take an aspirin and lie down"
                                    },
                                    {
                                            "definition": "Make, undertake, or perform (an action or task)",
                                            "synonyms": [
                                                    "perform",
                                                    "execute",
                                                    "effect",
                                                    "discharge",
                                                    "carry out",
                                                    "accomplish",
                                                    "fulfil",
                                                    "complete",
                                                    "conduct",
                                                    "implement",
                                                    "do",
                                                    "make",
                                                    "have"
                                            ],
                                            "example": "Lucy took a deep breath"
                                    },
                                    {
                                            "definition": "Require or use up (a specified amount of time)",
                                            "synonyms": [
                                                    "last",
                                                    "continue for",
                                                    "go on for",
                                                    "carry on for",
                                                    "keep on for",
                                                    "run on for",
                                                    "endure for"
                                            ],
                                            "example": "the jury took an hour and a half to find McPherson guilty"
                                    },
                                    {
                                            "definition": "Be attracted or charmed by.",
                                            "synonyms": [
                                                    "captivate",
                                                    "enchant",
                                                    "charm",
                                                    "delight",
                                                    "attract",
                                                    "win over",
                                                    "fascinate",
                                                    "bewitch",
                                                    "beguile",
                                                    "enthral",
                                                    "entrance",
                                                    "lure",
                                                    "infatuate",
                                                    "seduce",
                                                    "dazzle",
                                                    "hypnotize",
                                                    "mesmerize"
                                            ],
                                            "example": "Billie was very taken with him"
                                    },
                                    {
                                            "definition": "(of a plant or seed) take root or begin to grow; germinate.",
                                            "example": "the fuchsia cuttings had taken and were looking good"
                                    },
                                    {
                                            "definition": "Have or require as part of the appropriate construction.",
                                            "example": "verbs which take both the infinitive and the finite clause as their object"
                                    }
                            ]
                    }
            }
    ]
    
    app = QtWidgets.QApplication(sys.argv)

    re_window = Registration_Window(data[0]['word'], data[0]['phonetics'], data[0]['meaning'], '', (-1000, 100))
    re_window.show()

#     data = {
#                 "meaning": {
#                         "korean": "비우다, 비어 있는, 빈",
#                         "noun": "(nou) a container that has been emptied",
#                         "verb": "(vrb) make void or empty of contents\n(vrb) become empty or void of its content\n(vrb) leave behind empty; move out of\n(vrb) remove\n(vrb) excrete or discharge from the body",
#                         "adverb": "",
#                         "adjective": "(adj) holding or containing nothing\n(adj) devoid of significance or point\n(adj) needing nourishment\n(adj) emptied of emotion"
#                 },
#                 "example": [
#                         "I always empty and clean ashtrays and wastebaskets.",
#                         "The higher the resolution the bigger the empty space.",
#                         "The more empty space, the more readily the humidity will drop.",
#                         "Gases always intermix since free molecules will always move into empty space.",
#                         "On the scale of the clumps within the rings there is much empty space.",
#             "On the scale of the clumps within the rings there is a lot of empty space.",
#             "An analogous case concerns the empty conjunction and the empty disjunction.",
#             "There were empty seats galore.",
#             "The streets are empty and desolate.",
#             "They did not empty the cruet."
#         ]
#     }

#     re_window = Registration_Window(data[0]['word'], data[0]['phonetics'], data[0]['meaning'])
#     re_window.show()
    
    sys.exit( app.exec_() )
    