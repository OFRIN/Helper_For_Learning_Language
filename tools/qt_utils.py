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

def make_push_button(address, string, position, click_fn, icon_path=None):
    btn = QtWidgets.QPushButton(address)
    btn.setText(string)
    btn.move(*position)

    btn.clicked.connect(click_fn)

    if icon_path is not None:
        btn.setIcon(QtGui.QIcon(icon_path))

    btn.adjustSize()

    return btn

def make_edit(address, string, position):
    edit = QtWidgets.QLineEdit(address)
    edit.setText(string)
    edit.move(*position)
    edit.resize(500, 20)
    # edit.adjustSize()
    return edit

def make_checkbox(address, string, position, check_fn):
    chb = QtWidgets.QCheckBox(address)
    chb.setText(string)
    chb.move(*position)

    chb.clicked.connect(check_fn)
    chb.adjustSize()

    return chb

def get_width_and_height(obj):
    geo = obj.geometry()
    return geo.x(), geo.y(), geo.width(), geo.height()