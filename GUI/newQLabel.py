from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class QLabel_new(QLabel):
    clicked = pyqtSignal()

    # def __init__(self, parent=None):
    #     QLabel.__init__(self, parent)
    #
    # def mousePressEvent(self, ev):
    #     if self.is_clickable:
    #         self.clicked.emit()

    def __init__(self, is_clickable, parent=None):
        self.is_clickable = is_clickable
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        if self.is_clickable:
            self.clicked.emit()
