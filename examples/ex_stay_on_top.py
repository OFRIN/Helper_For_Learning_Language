import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QPoint
 
class mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
 
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
 
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
 
    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
 
app = QtWidgets.QApplication(sys.argv)
window = mainwindow()
window.show()
app.exec_()
