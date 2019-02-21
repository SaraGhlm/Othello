import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt

import first_page
import second_page

class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Othello'
        self.setWindowTitle(self.title)
        self.setFixedSize(800, 600)
        self.center()
        self.setup_page = first_page.FirstPage(self)
        self.game_page = second_page.SecondPage(self)
        self.game_page.hide()

    def start_game(self):
        """
            Start the game with the specified settings. Move to the second page of the game
        """
        self.setup_page.clear()
        self.game_page.show()
        print("after 2nd")

    def center(self):
        """
            Center the window on the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    # ex.show()
    sys.exit(app.exec_())
