import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from widget import Ui_Widget
from PyQt5.QtGui import QIcon, QPixmap


class othelloGame(Ui_Widget):
    def __init__(self):
        Ui_Widget.__init__(self)
        self.size = (8, 8)
        self.setupUi(boardsize=self.size)
        print(self.current_player)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = othelloGame()
    ex.show()
    sys.exit(app.exec_())
