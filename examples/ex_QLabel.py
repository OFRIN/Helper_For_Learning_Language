from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5.QtGui import * 
import sys
  
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
  
  
        # set the title
        self.setWindowTitle("Label")
  
        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)
  
        # creating a label widget
        self.label_1 = QLabel("== Normal Label ====", self)
  
        # moving position
        self.label_1.move(100, 100)
  
        # setting up border
        self.label_1.setStyleSheet("border: 1px solid black;")
        
        # creating a label widget
        # self.label_2 = QLabel("====== Adjusted label =====", self)
        self.label_2 = QLabel("====== Normal label =====", self)
  
        # moving position
        self.label_2.move(100, 150)
  
        # setting up border
        self.label_2.setStyleSheet("border: 1px solid black;")
  
        # adjusting the size of label
        self.label_2.adjustSize()
  
  
        # show all the widgets
        self.show()
  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# start the app
sys.exit(App.exec())