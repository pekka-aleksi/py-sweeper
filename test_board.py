import math
import random
import unittest
from functools import reduce

OUR_SEED = 0

from my_globals import State
from test_coordinate import Coordinate


class OutOfBoundsError(Exception):
    pass


class Board:
    def __init__(self, shape=(1, 1,), mines=0, default_state=State.NO_CLICK_NO_MINE, seed=0):
        # we should really be mocking this for testing purposes

        random.seed(seed)
        self.mines = random.sample(range(math.prod(shape)), mines)

        self.minesd = list()

        for mine in self.mines:
            div = mine
            coordinate = list()

            for dimension in shape:
                div, mod = divmod(div, dimension)
                coordinate.append(mod)

            self.minesd.append(coordinate)


        self.board = [[Coordinate(default_state) for _ in range(shape[1])] for _ in range(shape[0])]

        for x, y in self.minesd:

            self.board[x][y].state = State.NO_CLICK_YES_MINE

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
        b = Board(default_state=State.NO_CLICK_NO_MINE)
        b.click(0, 0)
        self.assertEqual(State.YES_CLICK_NO_MINE, b.board[0][0].state)

    def testOneDimensionalBoard(self):
        b = Board(shape=(5, 1), default_state=State.NO_CLICK_NO_MINE)
        self.assertRaises(IndexError, b.click, 1, 1)

    def testOneDimensionalBoardWithRandomMines(self):

        expected_mines = [0, 6, 9]
        b = Board(shape=(1, 10), mines=len(expected_mines), seed=OUR_SEED)

        empty_board = [State.NO_CLICK_NO_MINE for _ in range(10)]

        for i in expected_mines:
            empty_board[i] = State.NO_CLICK_YES_MINE

        B_state = [C.state for C in b.board[0]]

        self.assertEqual(empty_board, B_state)

    def testTwoDimensionalBoardWithRandomMines(self):
        expected_mines = [5, 12, 17, 27, 32, 33, 36, 38, 45, 49, 51, 53, 61, 62, 64, 65, 74, 79, 96, 97]
        W, H = 10, 10

        # expected_mines = [1, 4, 5, 6, 7, 8, 12, 13, 15, 19]
        # W, H = 4, 5

        b = Board(shape=(W, H), mines=len(expected_mines), seed=OUR_SEED)

        empty_board = [[State.NO_CLICK_NO_MINE for i in range(H)] for j in range(W)]

        for mine in expected_mines:
            div = mine
            coordinate = list()

            for dimension in (W, H):
                div, mod = divmod(div, dimension)
                coordinate.append(mod)

            empty_board[coordinate[0]][coordinate[1]] = State.NO_CLICK_YES_MINE

        B_state = [[coordinate.state for coordinate in row] for row in b.board]

        self.assertEqual(empty_board, B_state)

    @unittest.skip("we're not doing 3d yet")
    def testThreeDimensionalBoardWithRandomMines(self):
        expected_mines = [1, 6, 8, 9, 11, 12, 13, 15, 16, 20, 24, 26]

        shape = (3, 3, 3)
        b = Board(shape=shape, mines=len(expected_mines), seed=OUR_SEED)

        empty_board = [[[State.NO_CLICK_NO_MINE for _ in range(shape[0])] for _ in range(shape[1])] for _ in
                       range(shape[2])]

        coordinates = list()
        for mine in expected_mines:

            div = mine

            coordinate = list()

            for dimension in shape:
                div, mod = divmod(div, dimension)
                coordinate.append(mod)

            coordinates.append(coordinate)

        for x, y, z in coordinates:
            empty_board[x][y][z] = State.NO_CLICK_YES_MINE

        self.assertTrue(False)
