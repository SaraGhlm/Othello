import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

import GUI.first_page as FirstPage
import GUI.second_page as SecondPage


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        scale = 2
        self.widget_size = (int(resolution.width()/scale), int((resolution.width()/scale)*0.7))
        self.title = 'Othello'
        self.setWindowTitle(self.title)
        self.setFixedSize(self.widget_size[0], self.widget_size[1])
        self.center()
        self.setup_page = FirstPage.FirstPage(self, self.widget_size)
        self.game_page = SecondPage.SecondPage(self, self.widget_size, 1, init=True)
        self.game_page.hide()
        self.first = None
        self.second = None

    def start_game(self):
        """
            Start the game with the specified settings. Move to the second page of the game
        """

        self.board_size = int(self.setup_page.board_size_combo_box.currentText())
        self.user_color = 'b' if self.setup_page.colors_combo_box.currentText() == 'Black' else 'w'
        if self.setup_page.one_player_radio_button.isChecked():
            player_num = 1
            self.first = self.setup_page.first_player_combo_box.currentText()
        elif self.setup_page.two_player_radio_button.isChecked():
            player_num = 2
        else:
            player_num = 0
            self.first = self.setup_page.first_player_combo_box.currentText()
            self.second = self.setup_page.second_player_combo_box.currentText()
        self.setup_page.hide()
        self.game_page.__init__(self, self.widget_size, player_num, board_size=self.board_size,
                                user_color=self.user_color, first_player_name=self.first,
                                second_player_name=self.second, init=False)
        self.game_page.show()

    def back_to_setup_page(self):
        """
            In game page, if back to setup page button is clicked, first page is shown
        """
        self.board_size = int(self.setup_page.board_size_combo_box.currentText())
        self.game_page.hide()
        self.setup_page.__init__(self, self.widget_size)
        self.setup_page.show()

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
    sys.exit(app.exec_())
