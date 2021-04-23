from PyQt5 import QtCore, QtGui, QtWidgets

def make_label(address, string, position, bold=False, font_size=0):
    label = QtWidgets.QLabel(address)
    label.setText(string)
    label.move(*position)

    if font_size > 0:
        font = QtGui.QFont('Consolas', font_size)
        font.setBold(bold)
        label.setFont(font)

    label.adjustSize()

    return label