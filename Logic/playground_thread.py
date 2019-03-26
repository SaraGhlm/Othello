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
        self.is_finished = False

    def __del__(self):
        self.wait()

    def run(self):
        self.turn = True
        while not self.is_finished:
            if self.turn:
                loc = self.player.move(self.board)
                self.signal.emit(loc)
            else:
                loc = self.opponent.move(self.board)
                self.signal.emit(loc)
            self.sleep(1)
        return



    def set_board(self, board):
        self.board = board
