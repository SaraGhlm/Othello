from PyQt5.QtCore import QThread, pyqtSignal
from Logic.game import Game


class Playground(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, board_size, player, opponent, board, turn=True):
        QThread.__init__(self)
        self.game = Game(board_size)
        self.player = player
        self.opponent = opponent
        self.board = board
        self.turn = turn

    def __del__(self):
        self.wait()

    def run(self):
        turn = True
        while True:
            is_finished, _ = self.game.game_over(self.board)
            if is_finished:
                break
            if turn:
                loc = self.player.move(self.board)
                turn = False
            else:
                turn = True
                loc = self.opponent.move(self.board)
            self.signal.emit(loc)
            self.sleep(2)

    def set_board(self, board):
        self.board = board
