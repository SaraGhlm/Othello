from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget
from newQLabel import QLabel_new
import numpy as np
import re


class SecondPage():

    def __init__(self, widget, boardsize=(8, 8)):
        # self.setObjectName("Widget")
        # self.setWindowTitle("Othello")
        # self.setFixedSize(680, 427)
        self.board_size = boardsize
        self.widget = widget

        self.bg = QtWidgets.QLabel(widget)
        self.bg.setGeometry(0, 0, 800, 600)
        self.bg.setText("")
        self.bg.setStyleSheet("border-image: url(res/wooden-background.jpg); background-size: cover;")
        self.bg.setObjectName("background")

        self.board = QtWidgets.QLabel(widget)
        self.board.setGeometry(QtCore.QRect(20, 20, 371, 381))
        self.board.setText("")
        self.board.setPixmap(QtGui.QPixmap("res/greengrid.jpg"))
        self.board.setScaledContents(False)
        self.board.setObjectName("label")

        self.white_Score = QtWidgets.QLabel(widget)
        self.white_Score.setGeometry(QtCore.QRect(450, 50, 181, 21))
        self.white_Score.setText("White's Score: ")
        self.white_Score.setObjectName("white_Score")

        self.black_Score = QtWidgets.QLabel(widget)
        self.black_Score.setGeometry(QtCore.QRect(450, 90, 181, 29))
        self.black_Score.setText("Black's Score: ")
        self.black_Score.setObjectName("black_Score")

        self.turn_label = QtWidgets.QLabel(widget)
        self.turn_label.setGeometry(QtCore.QRect(450, 130, 181, 29))
        self.turn_label.setText("Black's turn ")
        self.turn_label.setObjectName("turn_label")

        self.int_to_str = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven'}
        self.str_to_int = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7}
        for i in range(boardsize[0]):
            for j in range(boardsize[1]):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                exec('self.' + name + '= QLabel_new(widget)')
                exec('self.' + name + '.setGeometry(QtCore.QRect(23+45.5*j, 31+45.5*i, 41, 41))')
                exec('self.' + name + ".clicked.connect(lambda self=self: self.player_clicked('" + name + "'))")
        self.reset_button = QtWidgets.QPushButton('Reset Game', widget)
        self.reset_button.move(450, 200)
        self.reset_button.clicked.connect(self.on_reset_click)
        # self.reset_button.setStyleSheet("QPushButton {"
        #                                 "}")

        self.init_board()

        QtCore.QMetaObject.connectSlotsByName(widget)
        widget.show()
        # print ('done with setup')

    def init_board(self):
        center = (int(self.board_size[0] / 2), int(self.board_size[1] / 2))
        self.current_board = np.zeros((self.board_size[0], self.board_size[1]), dtype=int)
        self.current_player = 'b'
        self.turn_label.setText("Black's turn ")
        self.move_validity_check = np.zeros((self.board_size[0], self.board_size[1]), dtype=int)
        self.place_stone('b', (center[0] - 1, center[1]))
        self.place_stone('w', (center[0], center[1]))
        self.place_stone('b', (center[0], center[1] - 1))
        self.place_stone('w', (center[0] - 1, center[1] - 1))
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
        if self.move_validity_check[self.str_to_int[result.group(1)], self.str_to_int[result.group(2)]] == 1:
            self.place_stone(self.current_player, (self.str_to_int[result.group(1)], self.str_to_int[result.group(2)]))

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
            self.flip_opponent_stones(loc, player_num=1, opponent=2)
            self.current_player = 'w'
            self.turn_label.setText("White's turn ")
        elif color == 'w':
            self.current_board[loc[0]][loc[1]] = 2
            self.flip_opponent_stones(loc, player_num=2, opponent=1)
            self.current_player = 'b'
            self.turn_label.setText("Black's turn ")
        else:
            raise ValueError('invalid color')

        self.clear_board()
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                name = self.int_to_str[i] + '_' + self.int_to_str[j]
                if self.current_board[i][j] == 1:
                    pixmap = QPixmap('res/black.png')
                    exec(
                        'pixmap_smaller = QPixmap.scaled(pixmap, self.' + name + '.width(), self.' + name + '.height())')
                    exec('self.' + name + '.setAlignment(QtCore.Qt.AlignCenter)')
                    exec('self.' + name + '.setPixmap(pixmap_smaller)')
                    # exec()
                elif self.current_board[i][j] == 2:
                    pixmap = QPixmap('res/white.png')
                    exec(
                        'pixmap_smaller = QPixmap.scaled(pixmap, self.' + name + '.width()-4, self.' + name + '.height()-4)')
                    exec('self.' + name + '.setAlignment(QtCore.Qt.AlignCenter)')
                    exec('self.' + name + '.setPixmap(pixmap_smaller)')
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

    def flip_opponent_stones(self, loc, player_num, opponent):
        # flip stones above current stone
        opponent_stones = 0
        for i in range(loc[0] - 1, -1, -1):
            if self.current_board[i][loc[1]] == 0:
                break
            elif self.current_board[i][loc[1]] == opponent:
                opponent_stones += 1
            elif self.current_board[i][loc[1]] == player_num and opponent_stones != 0:
                for j in range(i, loc[0] + 1):
                    self.current_board[j][loc[1]] = player_num
                break
        # flip stones bellow current stone
        opponent_stones = 0
        for i in range(loc[0] + 1, self.board_size[0]):
            if self.current_board[i][loc[1]] == 0:
                break
            elif self.current_board[i][loc[1]] == opponent:
                opponent_stones += 1
            elif self.current_board[i][loc[1]] == player_num and opponent_stones != 0:
                for j in range(loc[0], i + 1):
                    self.current_board[j][loc[1]] = player_num
                break

        # flip stones at the right of current stone
        opponent_stones = 0
        for i in range(loc[1] + 1, self.board_size[1]):
            if self.current_board[loc[0]][i] == 0:
                break
            elif self.current_board[loc[0]][i] == opponent:
                opponent_stones += 1
            elif self.current_board[loc[0]][i] == player_num and opponent_stones != 0:
                for j in range(loc[1], i + 1):
                    self.current_board[loc[0]][j] = player_num
                break
        # flip stones at the left of current stone
        opponent_stones = 0
        for i in range(loc[1] - 1, -1, -1):
            if self.current_board[loc[0]][i] == 0:
                break
            elif self.current_board[loc[0]][i] == opponent:
                opponent_stones += 1
            elif self.current_board[loc[0]][i] == player_num and opponent_stones != 0:
                for j in range(i, loc[1] + 1):
                    self.current_board[loc[0]][j] = player_num
                break
        # flip stones at the top right of current stone
        opponent_stones = 0
        try:
            for i in range(1, min(loc[0], self.board_size[1] - loc[1]) + 1):
                if self.current_board[loc[0] - i][loc[1] + i] == 0:
                    break
                elif self.current_board[loc[0] - i][loc[1] + i] == opponent:
                    opponent_stones += 1
                elif self.current_board[loc[0] - i][loc[1] + i] == player_num and opponent_stones != 0:
                    for j in range(0, i):
                        self.current_board[loc[0] - j][loc[1] + j] = player_num
                    break
        except:
            pass
        # flip stones at the top left of current stone
        opponent_stones = 0
        try:
            for i in range(1, min(loc[0], loc[1]) + 1):
                if self.current_board[loc[0] - i][loc[1] - i] == 0:
                    break
                elif self.current_board[loc[0] - i][loc[1] - i] == opponent:
                    opponent_stones += 1
                elif self.current_board[loc[0] - i][loc[1] - i] == player_num and opponent_stones != 0:
                    for j in range(0, i):
                        self.current_board[loc[0] - j][loc[1] - j] = player_num
                    break
        except:
            pass
        # flip stones at the bottom left of current stone
        opponent_stones = 0
        try:
            for i in range(1, min(self.board_size[0] - loc[0], loc[1]) + 1):
                if self.current_board[loc[0] + i][loc[1] - i] == 0:
                    break
                elif self.current_board[loc[0] + i][loc[1] - i] == opponent:
                    opponent_stones += 1
                elif self.current_board[loc[0] + i][loc[1] - i] == player_num and opponent_stones != 0:
                    for j in range(0, i):
                        self.current_board[loc[0] + j][loc[1] - j] = player_num
                    break
        except:
            pass
        # flip stones at the bottom right of current stone
        opponent_stones = 0
        try:
            for i in range(1, min(self.board_size[0] - loc[0], self.board_size[0] - loc[1]) + 1):
                if self.current_board[loc[0] + i][loc[1] + i] == 0:
                    break
                elif self.current_board[loc[0] + i][loc[1] + i] == opponent:
                    opponent_stones += 1
                elif self.current_board[loc[0] + i][loc[1] + i] == player_num and opponent_stones != 0:
                    for j in range(0, i):
                        self.current_board[loc[0] + j][loc[1] + j] = player_num
                    break
        except:
            pass

    def show_valid_moves(self):
        if self.current_player == 'b':
            rows, columns = np.where(self.current_board == 1)
            opponent = 2
        elif self.current_player == 'w':
            rows, columns = np.where(self.current_board == 2)
            opponent = 1
        else:
            raise ValueError('invalid location')
        for i in range(len(rows)):
            # check for valid moves above current stone
            opponent_stones = 0
            for j in range(rows[i] - 1, -1, -1):
                if self.current_board[j][columns[i]] != opponent:
                    if opponent_stones != 0 and self.current_board[j][columns[i]] == 0:
                        self.move_validity_check[j][columns[i]] = 1
                    break
                else:
                    opponent_stones += 1
            # check for valid moves bellow current stone
            opponent_stones = 0
            for j in range(rows[i] + 1, self.board_size[0]):
                if self.current_board[j][columns[i]] != opponent:
                    if opponent_stones != 0 and self.current_board[j][columns[i]] == 0:
                        self.move_validity_check[j][columns[i]] = 1
                    break
                else:
                    opponent_stones += 1
            # check for valid moves at the right of current stone
            opponent_stones = 0
            for j in range(columns[i] + 1, self.board_size[1]):
                if self.current_board[rows[i]][j] != opponent:
                    if opponent_stones != 0 and self.current_board[rows[i]][j] == 0:
                        self.move_validity_check[rows[i]][j] = 1
                    break
                else:
                    opponent_stones += 1
            # check for valid moves at the left of current stone
            opponent_stones = 0
            for j in range(columns[i] - 1, -1, -1):
                if self.current_board[rows[i]][j] != opponent:
                    if opponent_stones != 0 and self.current_board[rows[i]][j] == 0:
                        self.move_validity_check[rows[i]][j] = 1
                    break
                else:
                    opponent_stones += 1
            # check for valid moves at the right and above the current stone
            opponent_stones = 0
            try:
                for j in range(1, min(rows[i], self.board_size[1] - columns[i]) + 1):
                    if self.current_board[rows[i] - j][columns[i] + j] != opponent:
                        if opponent_stones != 0 and self.current_board[rows[i] - j][columns[i] + j] == 0:
                            self.move_validity_check[rows[i] - j][columns[i] + j] = 1
                        break
                    else:
                        opponent_stones += 1
            except:
                pass
            # check for valid moves at the right and below the current stone
            opponent_stones = 0
            try:
                for j in range(1, min(self.board_size[0] - rows[i], self.board_size[1] - columns[i]) + 1):
                    if self.current_board[rows[i] + j][columns[i] + j] != opponent:
                        if opponent_stones != 0 and self.current_board[rows[i] + j][columns[i] + j] == 0:
                            self.move_validity_check[rows[i] + j][columns[i] + j] = 1
                        break
                    else:
                        opponent_stones += 1
            except:
                pass
            # check for valid moves at the left and above the current stone
            opponent_stones = 0
            try:
                for j in range(1, min(rows[i], columns[i]) + 1):
                    if self.current_board[rows[i] - j][columns[i] - j] != opponent:
                        if opponent_stones != 0 and self.current_board[rows[i] - j][columns[i] - j] == 0:
                            self.move_validity_check[rows[i] - j][columns[i] - j] = 1
                        break
                    else:
                        opponent_stones += 1
            except:
                pass
            # check for valid moves at the left and below the current stone
            opponent_stones = 0
            try:
                for j in range(1, min(self.board_size[0] - rows[i], columns[i]) + 1):
                    if self.current_board[rows[i] + j][columns[i] - j] != opponent:
                        if opponent_stones != 0 and self.current_board[rows[i] + j][columns[i] - j] == 0:
                            self.move_validity_check[rows[i] + j][columns[i] - j] = 1
                        break
                    else:
                        opponent_stones += 1
            except:
                pass
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
