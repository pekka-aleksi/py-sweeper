import unittest

from my_globals import State
from test_board import Board


class Game:
    def __init__(self, board=None):
        self.board = board or Board()

        self.state = "undecided"

    def click(self, x, y):
        self.board.click(x, y)

        if self.board.board[x][y].state == State.YES_CLICK_NO_MINE:
            self.state = 'WIN'
        else:
            self.state = 'LOSS'


class TestGame(unittest.TestCase):

    def testNewGameWithOneCoordinateWithoutMine(self):
        g = Game()
        g.click(0, 0)
        self.assertEqual('WIN', g.state)

    def testNewGameWithOneCoordinateWithMine(self):
        b = Board(default_state=State.NO_CLICK_YES_MINE)
        g = Game(board=b)
        g.click(0, 0)
        self.assertEqual('LOSS', g.state)
