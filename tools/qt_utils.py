from PyQt5 import QtCore, QtGui, QtWidgets

def make_label(address, string, position):
    label = QtWidgets.QLabel(address)
    label.setText(string)
    label.adjustSize()
    label.move(*position)
    return label