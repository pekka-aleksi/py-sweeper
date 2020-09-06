import unittest

from my_globals import State
from test_coordinate import Coordinate


class Board:
    def __init__(self, default_state=State.NO_CLICK_NO_MINE):
        # we should really be mocking this for testing purposes
        self.board = [[Coordinate(state=default_state)]]

    def click(self, x, y):
        self.board[x][y].click()


class TestBoard(unittest.TestCase):

    def testDEFAULTBoard_is_OneCoordinateWithoutMine(self):
        b = Board()
        self.assertEqual(State.NO_CLICK_NO_MINE, b.board[0][0].state)

    def testClickNewBoardWithOneCoordinateWithMine(self):
        b = Board(default_state=State.NO_CLICK_YES_MINE)
        b.click(0, 0)
        self.assertEqual(State.YES_CLICK_YES_MINE, b.board[0][0].state)

    def testClickNewBoardWithOneCoordinateWithoutMine(self):
        b = Board(default_state=State.YES_CLICK_NO_MINE)
        self.assertEqual(State.YES_CLICK_NO_MINE, b.board[0][0].state)
