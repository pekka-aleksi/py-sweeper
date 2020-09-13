import math
import random
import unittest
from itertools import product
from test_ndarray import NdArray
import collections

OUR_SEED = 0

from my_globals import State
from test_coordinate import Coordinate


class OutOfBoundsError(Exception):
    pass


class Board:

    def __init__(self, shape=(1, 1,), minelist=(), minecount=0, default_state=State.NO_CLICK_NO_MINE,
                 seed=0):

        self.shape = shape
        data = [Coordinate(default_state) for _ in range(math.prod(shape))]
        self.board = NdArray(shape, data=data)

        random.seed(seed)
        self.minesd = minelist

        if minecount:
            self.mines = random.sample(range(math.prod(shape)), minecount)
            self.minesd = self.board.index_to_coordinate(self.mines)

        for mine in self.minesd:
            self.board[mine].state = State.NO_CLICK_YES_MINE

    def click(self, coordinate):

        mine = self.board[coordinate].click()

        if mine == -1:
            return mine

        self.board[coordinate].neighbors = self.get_neighbors(coordinate=coordinate)

        counter = collections.defaultdict(lambda: collections.defaultdict(int))
        #
        #   {
        #       (0,0) : State.NO_CLICK_YES_MINE,
        #       (0,1) : 2,
        #       (0,2) : State.NO_CLICK_YES_MINE
        #   }
        #
        for neighboring_coordinate in self.board[coordinate].neighbors:
            neighbor = self.board[neighboring_coordinate]
            counter[neighboring_coordinate][neighbor.state] += 1

        minecount = sum([counts.get(State.NO_CLICK_YES_MINE, 0) for coord, counts in counter.items()])

        self.board[coordinate].orthogonal_neighbors = self.get_neighbors(coordinate, orthogonal=True)

        # here we keep solving the next mines

        for neighboring_coordinate in self.board[coordinate].orthogonal_neighbors:

            try:
                neighbor_state = self.board[neighboring_coordinate].state
            except AttributeError:
                neighbor_state = self.board[neighboring_coordinate]

            if neighbor_state == State.NO_CLICK_NO_MINE:
                self.click(neighboring_coordinate)

        self.board[coordinate].state = minecount
        return minecount

    def get_neighbors(self, coordinate, orthogonal=False):

        if len(coordinate) != len(self.shape):
            raise ValueError(coordinate)
        if any(x < 0 for x in coordinate):
            raise ValueError(coordinate)
        if any(x >= self.shape[i] for i, x in enumerate(coordinate)):
            raise ValueError(coordinate)

        if not orthogonal:
            neighbors = list(product((0, -1, +1), repeat=len(coordinate)))

            neighbors = {tuple(min(max(x + C, 0), self.shape[i] - 1)
                               for i, (x, C) in enumerate(zip(neighbor, coordinate)))
                         for neighbor in neighbors}
            return neighbors - {coordinate}

        if orthogonal:

            # (1,1) -> (1+1, 1), (1-1, 1) ja (1, 1+1), (1, 1-1)
            # (1,1,1) -> (1+1, 1, 1), (1-1, 1, 1) ja (1, 1+1, 1), (1, 1-1, 1), ja (1, 1, 1+1), (1, 1, 1-1)

            orthogonal_neighbors = set()

            for i, _ in enumerate(coordinate):
                first_one = list(coordinate)
                first_one[i] += 1

                second_one = list(coordinate)
                second_one[i] -= 1

                first_one = [min(max(c, 0), self.shape[i] - 1) for i, c in enumerate(first_one)]
                second_one = [min(max(c, 0), self.shape[i] - 1) for i, c in enumerate(second_one)]

                orthogonal_neighbors.add(tuple(first_one))
                orthogonal_neighbors.add(tuple(second_one))

            return orthogonal_neighbors

    def get_followups(self, neighbors):

        followups = set()

        for neighbor in neighbors:
            neighbor_state = self.board[neighbor].state
            if neighbor_state == State.NO_CLICK_NO_MINE:
                followups.add(neighbor)

        return followups


class TestBoard(unittest.TestCase):

    def testclick(self):
        b = Board((50, 9), minecount=200)#, minelist=[(0, 1), (1, 1), (1, 0)])
        print(b.click((5, 5)))
        print(b.board)

    def testFollowUps(self):
        with self.subTest('3 in corner'):
            b = Board((9, 9), minelist=[(0, 1), (1, 1), (1, 0)])
            neighbors = b.get_neighbors((0, 0), orthogonal=True)

            followups = b.get_followups(neighbors)
            self.assertEqual(set(), followups)

        with self.subTest('diagonally in corner'):
            b = Board((2, 2), minelist=[(0, 1), (1, 0)])
            neighbors = b.get_neighbors((0, 0), orthogonal=True)

            followups = b.get_followups(neighbors)
            self.assertEqual(set(), followups)

        with self.subTest('diagonal-with-no-reach'):
            b = Board((3, 3), minelist=[(0, 0), (0, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
            neighbors = b.get_neighbors((1, 1), orthogonal=True)
            followups = b.get_followups(neighbors)
            self.assertEqual({(1, 0)}, followups)

        with self.subTest('3-3-with-reach'):
            b = Board((3, 3), minelist=[(0, 0), (0, 1), (2, 0), (2, 1), (2, 2)])
            neighbors = b.get_neighbors((1, 1), orthogonal=True)
            followups = b.get_followups(neighbors)
            self.assertEqual({(1, 0), (1, 2), (0, 2)}, followups)


        with self.subTest('3-3-with-no-mines'):
            b = Board(shape=(3, 3))

            neighbors = b.get_neighbors((1, 1), orthogonal=True)
            N = b.get_followups(neighbors)

            self.assertEqual({(0, 0), (0, 1), (0, 2),
                              (1, 0), (1, 2),
                              (2, 0), (2, 1), (2, 2)}, N)

    def testGetNeighbors(self):
        with self.subTest('10, 1, 2'):
            b = Board(shape=(10, 1, 2))
            N = b.get_neighbors((1, 0, 1))
            self.assertEqual({(0, 0, 0), (0, 0, 1),
                              (1, 0, 0),
                              (2, 0, 0), (2, 0, 1)}, N)

        with self.subTest('3, 3'):
            b = Board(shape=(3, 3))
            N = b.get_neighbors((1, 1))
            self.assertEqual({(0, 0), (0, 1), (0, 2),
                              (1, 0), (1, 2),
                              (2, 0), (2, 1), (2, 2)}, N)

    def test2DBoard(self):

        with self.subTest('3 in corner'):
            b = Board((9, 9), minelist=[(0, 1), (1, 1), (1, 0)])
            self.assertEqual(3, b.click((0, 0)))

        with self.subTest('5 in border'):
            b = Board((9, 9), minelist=[(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)])
            self.assertEqual(5, b.click((0, 1)))

        with self.subTest('8 all around'):
            b = Board((9, 9), minelist=[(0, 0), (0, 1), (0, 2),
                                        (1, 0), (1, 2),
                                        (2, 0), (2, 1), (2, 2)])

            self.assertEqual(8, b.click((1, 1)))

    def testDEFAULTBoard_is_OneCoordinateWithoutMine(self):
        b = Board()
        self.assertEqual(State.NO_CLICK_NO_MINE, b.board[(0, 0)].state)

    def testClickNewBoardWithOneCoordinateWithMine(self):
        b = Board(default_state=State.NO_CLICK_YES_MINE)

        b.click((0, 0))
        self.assertEqual(State.YES_CLICK_YES_MINE, b.board[(0, 0)].state)

    def testClickNewBoardWithOneCoordinateWithoutMine(self):
        b = Board(minecount=0, default_state=State.NO_CLICK_NO_MINE)
        b.click((0, 0))
        self.assertEqual(0, b.board[(0, 0)].state)

    def testOneDimensionalBoard(self):
        b = Board(shape=(5, 1), default_state=State.NO_CLICK_NO_MINE)
        self.assertRaises(IndexError, b.click, (1, 1))

    def testOneDBoardCorner(self):

        with self.subTest('0'):
            b = Board(shape=(1, 5), minelist=[[1]], default_state=State.NO_CLICK_NO_MINE)
            cX___ = b.click((0, 0))
            self.assertEqual(1, cX___)

        with self.subTest('1'):
            b = Board(shape=(1, 5), minelist=[[1]], default_state=State.NO_CLICK_NO_MINE)
            _X___ = b.click((0, 1))
            self.assertEqual(-1, _X___)

        with self.subTest('2'):
            b = Board(shape=(1, 5), minelist=[[1]], default_state=State.NO_CLICK_NO_MINE)
            _Xc__ = b.click((0, 2))
            self.assertEqual(1, _Xc__)


            expected_state = [[State.NO_CLICK_NO_MINE,
                               State.NO_CLICK_YES_MINE,
                               1,
                               0,
                               0
                               ]]

            self.assertEqual(expected_state, None)

        with self.subTest('3'):
            b = Board(shape=(1, 5), minelist=[[1]], default_state=State.NO_CLICK_NO_MINE)
            _X_c_ = b.click((0, 3))
            self.assertEqual(0, _X_c_)

        with self.subTest('4'):
            b = Board(shape=(1, 5), minelist=[[1]], default_state=State.NO_CLICK_NO_MINE)
            _X__c = b.click((0, 4))
            self.assertEqual(0, _X__c)

    def testOneDimensionalBoardWithRandomMines(self):

        expected_mines = [0, 6, 9]
        b = Board(shape=(1, 10), minecount=(len(expected_mines)), seed=OUR_SEED)

        empty_board = [State.NO_CLICK_NO_MINE for _ in range(10)]

        for i in expected_mines:
            empty_board[i] = State.NO_CLICK_YES_MINE

        B_state = [C.state for C in b.board.data]

        self.assertEqual(empty_board, B_state)

    def testTwoDimensionalBoardWithRandomMines(self):
        expected_mines = [5, 12, 17, 27, 32, 33, 36, 38, 45, 49, 51, 53, 61, 62, 64, 65, 74, 79, 96, 97]
        W, H = 10, 10

        # expected_mines = [1, 4, 5, 6, 7, 8, 12, 13, 15, 19]
        # W, H = 4, 5

        b = Board(shape=(W, H), minecount=(len(expected_mines)), seed=OUR_SEED)

        empty_board = NdArray(shape=(W, H), data=[State.NO_CLICK_NO_MINE for _ in range(W * H)])

        for mine in expected_mines:
            div = mine
            coordinate = list()

            for dimension in (W, H):
                div, mod = divmod(div, dimension)
                coordinate.append(mod)

            empty_board[coordinate] = State.NO_CLICK_YES_MINE

        expected_state = [e for e in empty_board.data]
        state = [i.state for i in b.board.data]

        self.assertEqual(expected_state, state)

    def testThreeDimensionalBoardWithRandomMines(self):
        expected_mines = [1, 6, 8, 9, 11, 12, 13, 15, 16, 20, 24, 26]

        shape = (3, 3, 3)
        b = Board(shape=shape, minecount=(len(expected_mines)), seed=OUR_SEED)

        expected_board = NdArray(shape=shape, data=[State.NO_CLICK_NO_MINE for _ in range(math.prod(shape))])
        coordinates = expected_board.index_to_coordinate(expected_mines)

        for mine in coordinates:
            expected_board[mine] = State.NO_CLICK_YES_MINE

        self.assertEqual(expected_board.data, [c.state for c in b.board.data])
