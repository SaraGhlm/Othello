from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from Logic.game import Game
import numpy as np
from Logic.player import Player
from Logic.random_player import RandomPlayer
from Logic.playground_thread import Playground
import re
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal


class SecondPage:

    def __init__(self, widget, player_num, board_size=8, user_color='b', level="Hard", mode=False, opponent_type=None,
                 init=False):
        self.player_num = player_num
        self.user_color = user_color
        self.level = level
        self.mode = mode
        self.computer_color = 'w' if user_color == 'b' else 'b'
        self.label_style = """QLabel {
                            color: rgba(0, 0, 0, 0.7);
                            font-size: 20px;}"""
        self.button_style = """QPushButton {
                            font-size: 20px;
                            color: rgba(1, 1, 1, 0.7);
                            border: 2px solid #8f8f91;
                            border-radius: 6px;
                            background-color: rgba(255, 255, 255, 0.3);
                            min-width: 80px;}
                            QPushButton:hover {
                            background-color: rgba(255, 255, 255, 0.5);}
                            QPushButton:pressed {
                            background-color: rgba(255, 255, 255, 0.7);}
                            QPushButton:flat {
                            border: none; /* no border for a flat push button */}
                            QPushButton:default {
                            border-color: navy; /* make the default button prominent */}"""

        self.board_style = """QPushButton { 
                                background-color: rgba(255, 255, 255, 0);} 
                                QPushButton:disabled {
                                background-color: rgba(255, 255, 255, 0);}
                                """

        self.notification_style = """QLabel {
                                    background: rgba(200, 0, 0, 0.7);
                                    font-size: 20px;
                                    color: rgba(255, 255, 255, 1);
                                    border-radius: 5px;
                                    padding: 3px;}"""
        self.board_size = board_size
        self.board_pixel_size = 500
        self.widget = widget

        self.opponent_player = None
        if opponent_type is not None:
            # self.opponent_player = RandomPlayer(board_size, 'w')
            self.opponent_player = Player(self.level, self.board_size, 'w')
            self.computer_color = 'b'

        self.computer_player = Player(self.level, self.board_size, self.computer_color)
        self.game = Game(self.board_size)

        self.black_pixmap = QPixmap('res/black.png')
        self.white_pixmap = QPixmap('res/white.png')
        self.red_pixmap = QPixmap('res/red.png')

        self.background_label = QtWidgets.QLabel(widget)
        self.background_label.setGeometry(0, 0, 800, 600)
        self.background_label.setText("")
        self.background_label.setStyleSheet("border-image: url(res/wooden-background.jpg); background-size: cover;")
        self.background_label.setObjectName("background")

        self.board_label = QtWidgets.QLabel(widget)
        self.board_label.setGeometry(QtCore.QRect(20, 20, self.board_pixel_size, self.board_pixel_size))
        self.board_label.setText("")
        board_pic = 'res/Board' + str(self.board_size) + '.jpg'
        self.board_label.setPixmap(QtGui.QPixmap(board_pic))
        self.board_label.setScaledContents(True)
        self.board_label.setObjectName("label")

        self.white_score_label = QtWidgets.QLabel(widget)
        self.white_score_label.setGeometry(QtCore.QRect(570, 50, 181, 21))
        self.white_score_label.setText("White's Score: ")
        self.white_score_label.setObjectName("white_Score")
        self.white_score_label.setStyleSheet(self.label_style)

        self.black_score_label = QtWidgets.QLabel(widget)
        self.black_score_label.setGeometry(QtCore.QRect(570, 90, 181, 29))
        self.black_score_label.setText("Black's Score: ")
        self.black_score_label.setObjectName("black_Score")
        self.black_score_label.setStyleSheet(self.label_style)

        self.turn_label = QtWidgets.QLabel(widget)
        self.turn_label.setGeometry(QtCore.QRect(570, 130, 181, 29))
        self.turn_label.setText("Black's turn ")
        self.turn_label.setObjectName("turn_label")
        self.turn_label.setStyleSheet(self.label_style)

        self.reset_button = QtWidgets.QPushButton('Reset Game', widget)
        self.reset_button.setGeometry(570, 200, 210, 50)
        self.reset_button.clicked.connect(self.on_reset_click)
        self.reset_button.setStyleSheet(self.button_style)

        self.go_to_setup_page_button = QtWidgets.QPushButton('Back to Setup Page', widget)
        self.go_to_setup_page_button.setGeometry(570, 270, 210, 50)
        self.go_to_setup_page_button.clicked.connect(self.on_go_to_setup_page_button_click)
        self.go_to_setup_page_button.setStyleSheet(self.button_style)

        self.notification_label = QtWidgets.QLabel(widget)
        self.notification_label.setGeometry(QtCore.QRect(570, 350, 181, 100))
        self.notification_label.setText("Hi!")
        self.notification_label.setStyleSheet(self.notification_style)

        self.int_to_str = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven',
                           8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen'}
        self.str_to_int = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
                           'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13}

        width = (self.board_pixel_size / self.board_size) - 0.15
        width2 = (self.board_pixel_size / self.board_size) - 4
        starting_point = (23, 23)

        # Initializing the push buttons for all locations in the board
        for i in range(board_size):
            for j in range(board_size):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + "= QtWidgets.QPushButton('', widget)")
                exec('self.' + name + '.setGeometry(QtCore.QRect(starting_point[0]+width*j, '
                                      'starting_point[1]+width*i, width2, width2))')
                exec('self.' + name + ".clicked.connect(lambda x, self=self: self.player_clicked('" + name + "'))")
                exec('self.' + name + ".setStyleSheet(self.board_style)")
                if self.player_num == 1:
                    exec('self.' + name + ".setEnabled(False)")

        self.init_board()

        QtCore.QMetaObject.connectSlotsByName(widget)
        widget.show()

        if init is False and mode is True:
            self._turn = True
            self.playground_thread = Playground(self.board_size, self.computer_player, self.opponent_player,
                                                self.current_board, turn=True)
            self.playground_thread.signal.connect(self.auto_play)
            self.playground_thread.start()

    def auto_play(self, loc):
        if self._turn:
            self.place_stone(self.computer_color, loc)
            self._turn = False
            self.playground_thread.turn = True if self.current_player == self.computer_color else False
        else:
            self.place_stone(self.opponent_player.computer_color, loc)
            self._turn = True
            self.playground_thread.turn = True if self.current_player == self.computer_color else False

    def init_board(self):
        """
            Initializes the board with 4 stones in the center. If the computer player is the first player, it plays.
        """
        center = (int(self.board_size / 2), int(self.board_size / 2))
        # current_board is a matrix of zeros. 1 is for black and 2 is for white stones
        self.current_board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 'b'
        self.turn_label.setText("Black's turn ")
        self.move_validity_check = np.zeros((self.board_size, self.board_size), dtype=int)
        self.place_stone('b', (center[0] - 1, center[1]))
        self.place_stone('w', (center[0], center[1]))
        self.place_stone('b', (center[0], center[1] - 1))
        self.place_stone('w', (center[0] - 1, center[1] - 1))
        if self.player_num == 1:
            if self.computer_color == self.current_player:
                loc = self.computer_player.move(self.current_board)
                self.place_stone(self.computer_color, loc)
            self.show_valid_moves()


    def on_reset_click(self):
        """
            This function in called when reset button is clicked.
            It shows a message box to make sure user has not clicked the button accidentally.
            If not, it resets and initializes the board
        """
        button_reply = QtWidgets.QMessageBox.question(self.widget, "Warning",
                                                      "Are you sure you want to clear the board?",
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        if button_reply == QtWidgets.QMessageBox.Yes:
            self.clear_board()
            self.init_board()

    def on_go_to_setup_page_button_click(self):
        """
            This function in called when the setup page button is clicked.
            It shows a message box to make sure user has not clicked the button accidentally.
            If not, it goes to the setup page.
        """
        button_reply = QtWidgets.QMessageBox.question(self.widget, "Warning",
                                                      "The game will end. Are you sure?",
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        if button_reply == QtWidgets.QMessageBox.Yes:
            self.widget.back_to_setup_page()

    def player_clicked(self, label_name):
        """
            This function in called whenever one of the board locations are clicked by the user.
            Based on the current player and the location that was clicked, it places a stone in that
            location if the move is valid. Then if computer should play next, it plays.
        """
        pattern = re.compile(r'(.*)_(.*)')
        result = pattern.match(label_name)
        if self.current_player == self.user_color or self.player_num == 2:
            finished = self.place_stone(self.current_player,
                                        (self.str_to_int[result.group(1)], self.str_to_int[result.group(2)]))
            if self.player_num == 1 and finished is False and self.current_player == self.computer_color:
                time.sleep(1)
                loc = self.computer_player.move(self.current_board)
                self.place_stone(self.computer_color, loc)

    def clear_board(self):
        """
            Clears all the board location push buttons
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + '.setIcon(QtGui.QIcon())')

    def stop_board(self):
        """
            Makes all the board location push buttons unclickable
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + ".setEnabled(False)")

    def start_board(self):
        """
            If we are in the two player mode, it makes all the current player's possible valid moves clickable.
            If we are in the one player mode, it makes all the current player's possible valid moves clickable
            only if the user in the current player.
        """
        if self.player_num == 2:
            rows, columns = np.where(self.move_validity_check == 1)
            for i in range(len(rows)):
                name = self.int_to_str[rows[i]] + '_' + self.int_to_str[columns[i]]
                exec('self.' + name + '.setEnabled(True)')
        elif self.current_player == self.user_color:
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.move_validity_check[i][j] == 1:
                        name = self.int_to_str[i] + '_' + self.int_to_str[j]
                        exec('self.' + name + ".setEnabled(True)")
        else:
            self.stop_board()

    def show_board(self):
        """
            Based on the current_board matrix it displays all the stones that are played in the board.
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                if self.current_board[i][j] == 1:
                    icon = QtGui.QIcon()
                    icon.addPixmap(self.black_pixmap, QIcon.Normal)
                    icon.addPixmap(self.black_pixmap, QIcon.Disabled)
                    exec('self.' + name + '.setIcon(icon)')
                    exec('self.' + name + '.setIconSize(QtCore.QSize(self.' + name +
                         '.width(), self.' + name + '.height()))')
                elif self.current_board[i][j] == 2:
                    icon = QtGui.QIcon()
                    icon.addPixmap(self.white_pixmap, QIcon.Normal)
                    icon.addPixmap(self.white_pixmap, QIcon.Disabled)
                    exec('self.' + name + '.setIcon(icon)')
                    exec('self.' + name + '.setIconSize(QtCore.QSize(self.' + name +
                         '.width() - 4, self.' + name + '.height() - 4))')

    def place_stone(self, player_color, loc):
        """
            Places a stone in the given location based on the color of the player and changes the status of the game.
            It also checks whether the game is finished after the move and checks whether the next player has a
            possible move or not.
        :param player_color: A letter representing the player ( 'b' for black player, 'w' for white player)
        :param loc: Tuple of location the stone should be places
        """
        self.notification_label.hide()
        self.stop_board()
        if player_color == 'b':
            self.current_board[loc[0]][loc[1]] = 1
            self.current_board = self.game.flip_opponent_stones(loc, self.current_board, self.board_size,
                                                                player_num=1, opponent=2)
            self.current_player = 'w'
            self.turn_label.setText("White's turn ")
        elif player_color == 'w':
            self.current_board[loc[0]][loc[1]] = 2
            self.current_board = self.game.flip_opponent_stones(loc, self.current_board, self.board_size,
                                                                player_num=2, opponent=1)
            self.current_player = 'b'
            self.turn_label.setText("Black's turn ")
        else:
            raise ValueError('invalid color')

        self.clear_board()
        self.show_board()
        self.update_scores()

        # Is the game finished after this move?
        is_finished, message = self.game.game_over(self.current_board)
        if is_finished and sum(sum(self.current_board)) > 1:
            button_reply = QtWidgets.QMessageBox.information(self.widget, "Result", message, QtWidgets.QMessageBox.Ok)
            self.playground_thread.is_finished = True
            if button_reply == QtWidgets.QMessageBox.Ok:
                self.clear_board()
                self.init_board()
                return True

        # Does the next player has possible valid moves? If not, the other player should make a move
        self.move_validity_check = np.zeros((self.board_size, self.board_size), dtype=int)
        self.show_valid_moves()

        if sum(sum(self.move_validity_check)) == 0 and sum(sum(self.current_board)) > 1:
            if self.mode is True:
                self.notification_label.setText("No possible move, changing player")
                self.notification_label.show()
                self.show_valid_moves()
                if self.current_player == 'b':
                    self.current_player = 'w'
                    self.turn_label.setText("White's turn ")
                elif self.current_player == 'w':
                    self.current_player = 'b'
                    self.turn_label.setText("Black's turn ")
                self.show_valid_moves()
            else:
                button_reply = QtWidgets.QMessageBox.information(self.widget, "Warning",
                                                                 "No possible move, changing player",
                                                                 QtWidgets.QMessageBox.Ok)
                if button_reply == QtWidgets.QMessageBox.Ok:
                    self.show_valid_moves()
                    if self.current_player == 'b':
                        self.current_player = 'w'
                        self.turn_label.setText("White's turn ")
                    elif self.current_player == 'w':
                        self.current_player = 'b'
                        self.turn_label.setText("Black's turn ")
                    self.show_valid_moves()
                    if self.current_player == self.computer_color and self.player_num == 1:
                        loc = self.computer_player.move(self.current_board)
                        self.place_stone(self.computer_color, loc)
        self.widget.repaint()
        self.start_board()
        return False

    def update_scores(self):
        """
            Based on the status of the board it updates the scores in the GUI
        """
        black_score = sum(sum(self.current_board == 1))
        self.black_score_label.setText("Black's Score: " + str(black_score))
        white_score = sum(sum(self.current_board == 2))
        self.white_score_label.setText("White's Score: " + str(white_score))

    def show_valid_moves(self):
        """
            Based on the possible valid moves of the current player, it displays the red dots in the GUI.
        """
        self.move_validity_check = self.game.find_valid_moves(self.current_player, self.current_board, self.board_size)
        rows, columns = np.where(self.move_validity_check == 1)
        icon = QtGui.QIcon()
        icon.addPixmap(self.red_pixmap, QIcon.Normal)
        icon.addPixmap(self.red_pixmap, QIcon.Disabled)
        for i in range(len(rows)):
            name = self.int_to_str[rows[i]] + '_' + self.int_to_str[columns[i]]
            exec('self.' + name + '.setIcon(icon)')
            exec(
                'self.' + name + '.setIconSize(QtCore.QSize(self.' + name + '.width()/4, self.' + name + '.height()/4))')

    def hide(self):
        """
            Hides all the components of the game page.
            Is used in the main file to show the setup page.
        """
        self.background_label.hide()
        self.board_label.hide()
        self.white_score_label.hide()
        self.black_score_label.hide()
        self.turn_label.hide()
        self.notification_label.hide()
        self.reset_button.hide()
        self.go_to_setup_page_button.hide()
        for i in range(self.board_size):
            for j in range(self.board_size):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + '.hide()')

    def show(self):
        """
            Shows all the components of the game page.
            Is used in the main file to show the game page.
        """
        self.background_label.show()
        self.board_label.show()
        self.white_score_label.show()
        self.black_score_label.show()
        self.turn_label.show()
        self.reset_button.show()
        self.go_to_setup_page_button.show()
        for i in range(self.board_size):
            for j in range(self.board_size):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + '.show()')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = SecondPage(dialog)
    dialog.show()
    sys.exit(app.exec_())
