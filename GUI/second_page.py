from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget
from GUI.newQLabel import QLabel_new
from Logic.game import *
import numpy as np
from Logic.player import HeuristicPlayer
import re
import sys
import time


class SecondPage:

    def __init__(self, widget, board_size=(8, 8)):
        self.user_color = 'b'
        self.computer_color = 'w'
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
        self.board_size = board_size
        self.board_pixel_size = 500
        self.widget = widget

        self.computer_player = HeuristicPlayer('Beginner', self.board_size[0], self.computer_color)

        self.black_pixmap = QPixmap('res/black.png')
        self.white_pixmap = QPixmap('res/white.png')

        self.bg = QtWidgets.QLabel(widget)
        self.bg.setGeometry(0, 0, 800, 600)
        self.bg.setText("")
        self.bg.setStyleSheet("border-image: url(res/wooden-background.jpg); background-size: cover;")
        self.bg.setObjectName("background")

        self.board = QtWidgets.QLabel(widget)
        self.board.setGeometry(QtCore.QRect(20, 20, self.board_pixel_size, self.board_pixel_size))
        self.board.setText("")
        board_pic = 'res/Board' + str(self.board_size[0]) + '.jpg'
        self.board.setPixmap(QtGui.QPixmap(board_pic))
        self.board.setScaledContents(True)
        self.board.setObjectName("label")

        self.white_Score = QtWidgets.QLabel(widget)
        self.white_Score.setGeometry(QtCore.QRect(570, 50, 181, 21))
        self.white_Score.setText("White's Score: ")
        self.white_Score.setObjectName("white_Score")
        self.white_Score.setStyleSheet(self.label_style)

        self.black_Score = QtWidgets.QLabel(widget)
        self.black_Score.setGeometry(QtCore.QRect(570, 90, 181, 29))
        self.black_Score.setText("Black's Score: ")
        self.black_Score.setObjectName("black_Score")
        self.black_Score.setStyleSheet(self.label_style)

        self.turn_label = QtWidgets.QLabel(widget)
        self.turn_label.setGeometry(QtCore.QRect(570, 130, 181, 29))
        self.turn_label.setText("Black's turn ")
        self.turn_label.setObjectName("turn_label")
        self.turn_label.setStyleSheet(self.label_style)

        self.reset_button = QtWidgets.QPushButton('Reset Game', widget)
        self.reset_button.setGeometry(570, 200, 170, 50)
        self.reset_button.clicked.connect(self.on_reset_click)
        self.reset_button.setStyleSheet(self.button_style)

        self.int_to_str = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven',
                           8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen'}
        self.str_to_int = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
                           'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13}

        width = (self.board_pixel_size / self.board_size[0]) - 0.15
        width2 = (self.board_pixel_size / self.board_size[0]) - 4
        starting_point = (23, 23)

        for i in range(board_size[0]):
            for j in range(board_size[1]):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + '= QLabel_new(widget)')
                exec('self.' + name + '.setGeometry(QtCore.QRect(starting_point[0]+width*j, '
                                      'starting_point[1]+width*i, width2, width2))')
                exec('self.' + name + ".clicked.connect(lambda self=self: self.player_clicked('" + name + "'))")

        self.init_board()

        QtCore.QMetaObject.connectSlotsByName(widget)
        widget.show()

    def init_board(self):
        center = (int(self.board_size[0] / 2), int(self.board_size[1] / 2))
        # current_board is a matrix of zeros. 1 is for black and 2 is for white stones
        self.current_board = np.zeros((self.board_size[0], self.board_size[1]), dtype=int)
        self.current_player = 'b'
        self.turn_label.setText("Black's turn ")
        self.move_validity_check = np.zeros((self.board_size[0], self.board_size[1]), dtype=int)
        self.place_stone('b', (center[0] - 1, center[1]))
        self.place_stone('w', (center[0], center[1]))
        self.place_stone('b', (center[0], center[1] - 1))
        self.place_stone('w', (center[0] - 1, center[1] - 1))
        if self.computer_color == self.current_player:
            loc = self.computer_player.move(self.current_board)
            self.place_stone(self.computer_color, loc)
        self.show_valid_moves()

    def on_reset_click(self):
        buttonReply = QtWidgets.QMessageBox.question(self.widget, "Warning",
                                                     "Are you sure you want to clear the board?",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        if buttonReply == QtWidgets.QMessageBox.Yes:
            print('Game is reset')
            self.clear_board()
            self.init_board()

    def player_clicked(self, label_name):
        pattern = re.compile(r'(.*)_(.*)')
        result = pattern.match(label_name)
        if self.current_player == self.user_color:
            self.place_stone(self.current_player, (self.str_to_int[result.group(1)], self.str_to_int[result.group(2)]))
            self.widget.repaint()
        if self.current_player == self.computer_color:
            time.sleep(1)
            loc = self.computer_player.move(self.current_board)
            self.place_stone(self.computer_color, loc)
            self.widget.repaint()

    def clear_board(self):
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + '.clear()')

    def place_stone(self, color, loc):
        """
        :param color: b -> black, w -> white
        :param loc: Tuple of location the stone should be places
        """
        if color == 'b':
            self.current_board[loc[0]][loc[1]] = 1
            self.current_board = flip_opponent_stones(loc, self.current_board, self.board_size[0], player_num=1, opponent=2)
            self.current_player = 'w'
            self.turn_label.setText("White's turn ")
        elif color == 'w':
            self.current_board[loc[0]][loc[1]] = 2
            self.current_board = flip_opponent_stones(loc, self.current_board, self.board_size[0], player_num=2, opponent=1)
            self.current_player = 'b'
            self.turn_label.setText("Black's turn ")
        else:
            raise ValueError('invalid color')

        self.clear_board()
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                if self.current_board[i][j] == 1:
                    exec('pixmap_smaller = QPixmap.scaled(self.black_pixmap, self.' + name +
                         '.width(), self.' + name + '.height())')
                    exec('self.' + name + '.setAlignment(QtCore.Qt.AlignCenter)')
                    exec('self.' + name + '.setPixmap(pixmap_smaller)')
                elif self.current_board[i][j] == 2:
                    exec('pixmap_smaller = QPixmap.scaled(self.white_pixmap, self.' + name +
                         '.width()-4, self.' + name + '.height()-4)')
                    exec('self.' + name + '.setAlignment(QtCore.Qt.AlignCenter)')
                    exec('self.' + name + '.setPixmap(pixmap_smaller)')
        # self.widget.repaint()
        self.update_scores()
        if sum(sum(self.current_board == 0)) == 0:
            black_score = sum(sum(self.current_board == 1))
            white_score = sum(sum(self.current_board == 2))
            if black_score > white_score:
                message = 'Black won!'
            elif black_score < white_score:
                message = 'white won!'
            else:
                message = 'Tie!'
            buttonReply = QtWidgets.QMessageBox.information(self.widget, "Result", message, QtWidgets.QMessageBox.Ok)
            if buttonReply == QtWidgets.QMessageBox.Ok:
                print('Game is reset')
                self.clear_board()
                self.init_board()
        self.move_validity_check = np.zeros((self.board_size[0], self.board_size[1]), dtype=int)
        self.show_valid_moves()
        if sum(sum(self.move_validity_check)) == 0 and sum(sum(self.current_board)) > 1:
            buttonReply = QtWidgets.QMessageBox.information(self.widget, "Warning", "No possible move, changing player",
                                                            QtWidgets.QMessageBox.Ok)
            if buttonReply == QtWidgets.QMessageBox.Ok:
                self.show_valid_moves()
                if self.current_player == 'b':
                    self.current_player = 'w'
                    self.turn_label.setText("White's turn ")
                elif self.current_player == 'w':
                    self.current_player = 'b'
                    self.turn_label.setText("Black's turn ")
                self.show_valid_moves()

    def update_scores(self):
        black_score = sum(sum(self.current_board == 1))
        self.black_Score.setText("Black's Score: " + str(black_score))
        white_score = sum(sum(self.current_board == 2))
        self.white_Score.setText("White's Score: " + str(white_score))

    def show_valid_moves(self):
        self.move_validity_check = find_valid_moves(self.current_player, self.current_board, self.board_size[0])
        rows, columns = np.where(self.move_validity_check == 1)
        pixmap = QPixmap('res/red.png')
        for i in range(len(rows)):
            name = self.int_to_str[rows[i]] + '_' + self.int_to_str[columns[i]]
            exec('pixmap_smaller = QPixmap.scaled(pixmap, self.' + name + '.width()/4, self.' + name + '.height()/4)')
            exec('self.' + name + '.clear()')
            exec('self.' + name + '.setAlignment(QtCore.Qt.AlignCenter)')
            exec('self.' + name + '.setPixmap(pixmap_smaller)')

    def hide(self):
        self.bg.hide()
        self.board.hide()
        self.white_Score.hide()
        self.black_Score.hide()
        self.turn_label.hide()
        self.reset_button.hide()
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + '.hide()')

    def show(self):
        self.bg.show()
        self.board.show()
        self.white_Score.show()
        self.black_Score.show()
        self.turn_label.show()
        self.reset_button.show()
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + '.show()')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = SecondPage(dialog)
    dialog.show()
    sys.exit(app.exec_())
