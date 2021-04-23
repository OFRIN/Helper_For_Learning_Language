import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from tools.qt_utils import make_label

class Tab_Window(QtWidgets.QWidget):
    def __init__(self, meanings):
        super().__init__()
        
        # Convert 1D meanings to 2D meanings
        self.groups = []
        self.max_column = 3

        for index, meaning in enumerate(meanings):
            if index % self.max_column == 0:
                self.groups.append([
                    {
                        'index' : index,
                        'meanings' : meanings
                    }
                ])
            else:
                self.groups[-1].append(
                    {
                        'index' : index,
                        'meanings' : meanings
                    }
                )

        # define width and height
        self.width = 0
        self.height = 0

        # make groups
        margin = 20

        start_x = 10
        start_y = 20
        
        default_width = 300
        default_height = 200

        base_rect = QtCore.QRect(start_x, start_y, default_width, default_height)
        
        
        
        for group_per_column in groups:
            for group in group_per_column:
                group_of_meaning = QtWidgets.QGroupBox(f'{group['index'] + 1}', self)
                group_of_meaning.setGeometry(base_rect)
                
                en_definition = make_label(
                        group_of_meaning, 
                        '# meaning\n' + '- ' + group['meaning']['definition'], 
                        (10, 20)
                )
                rect_of_define = en_definition.geometry()

                en_example = make_label(
                        group_of_meaning, 
                        '# example\n' + '- ' + group['meaning']['example'], 
                        (10, rect_of_define.y() + rect_of_define.height() + margin)
                )
                
                group_of_meaning.adjustSize()
                
                rect_of_group = group_of_meaning.geometry()
                
                self.coord_x += 1
                if self.coord_x == self.max_width:
                        self.coord_x = 0
                        self.coord_y += 1
                
                base_rect.setY(rect_of_group.y() + rect_of_group.height() + margin)
                base_rect.setHeight(default_height)

                width = rect_of_group.width() + margin
                if self.width < width:
                        self.width = width
                
                self.groups.append(group_of_meaning)

        rect_of_final_group = self.groups[-1].geometry()
        self.height = rect_of_final_group.y() + rect_of_final_group.height() + margin
        
        self.adjustSize()

class Registration_Window(QtWidgets.QWidget):
    def __init__(self, word, phonetics, meanings):
        super().__init__()

        self.minimum_width = 300
        
        self.setWindowTitle("Registration")
        self.setGeometry(QtCore.QRect(10, 10, self.minimum_width, 300))
        
        self.word = QtWidgets.QLabel(self)
        self.word.setText('# Word : ' + word)
        self.word.adjustSize()
        self.word.move(10, 10)
        
        self.make_groupbox_for_phonetics(phonetics)
        self.make_tablewidget_for_meanings(meanings)

        self.adjustSize()

        if self.geometry().width() < self.minimum_width:
            self.setFixedWidth(self.minimum_width)

    def make_groupbox_for_phonetics(self, phonetics):
        self.group_of_phonetics = QtWidgets.QGroupBox('Phonetics', self)
        self.group_of_phonetics.setGeometry(QtCore.QRect(10, 40, 250, 80))
        
        margin = 20
        rect_of_group = self.group_of_phonetics.geometry()

        for i in range(3):
            phonetics.append(phonetics[0])

        for index, phonetic in enumerate(phonetics):
            x, y = rect_of_group.x(), 15 + (index) * margin
            w, h = None, None
            
            self.label_phonetic = QtWidgets.QLabel(self.group_of_phonetics)
            self.label_phonetic.setText(phonetic['text'])
            self.label_phonetic.adjustSize()
            self.label_phonetic.move(rect_of_group.x(), 15 + (index) * margin)

            rect_of_label = self.label_phonetic.geometry()
            w, h = rect_of_label.width(), rect_of_label.height()
            
            self.btn_play = QtWidgets.QPushButton(self.group_of_phonetics)
            self.btn_play.setGeometry(QtCore.QRect(x + 50, y, 100, h))
            self.btn_play.setIcon(QtGui.QIcon('./resoures/mx-player-icon.png'))
            self.btn_play.clicked.connect(lambda:self.play_mp3_from_url(phonetic['audio']))

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
            tab = Tab_Window(meanings[tag])

            table_width = max(table_width, tab.width)
            table_height = max(table_height, tab.height)

            self.table_of_meanings.addTab(tab, tag)
            table_index += 1
        
        self.table_of_meanings.setFixedWidth(table_width)
        self.table_of_meanings.setFixedHeight(table_height)

        # self.table_of_meanings.adjustSize()
    
    def play_mp3_from_url(self, mp3_url):
        print(mp3_url)

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

    re_window = Registration_Window(data[0]['word'], data[0]['phonetics'], data[0]['meaning'])
    re_window.show()
    sys.exit( app.exec_() )