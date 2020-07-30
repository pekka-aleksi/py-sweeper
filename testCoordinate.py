import unittest

# the board consists of coordinates with states
# the board has borders which have coordinates but do not have states
# there is an action that toggles the state


# the mines are randomly laid out AFTER the first click

from enum import Enum


class State(Enum):
    RED = 1  # * NOT clicked and doesn't contain a mine
    GREEN = 2  # * NOT clicked and does contain a mine
    BLUE = 3  # * flagged and doesn't contain a mine
    BLACK = 4  # * flagged and does contain a mine
    YELLOW = 5  # * clicked and doesn't contain a mine
    ORANGE = 6  # * clicked and does contain a mine

    MAGENTA = 7  # * revealed because a neighbor was clicked


class Coordinate:
    def __init__(self, state=State.RED):
        self.state = state

    def flag(self):
        if self.state == State.RED:
            self.state = State.BLUE
        elif self.state == State.GREEN:
            self.state = State.BLACK

    def click(self):
        if self.state == State.RED or self.state == State.BLUE:
            self.state = State.YELLOW
        if self.state == State.GREEN or self.state == State.BLACK:
            self.state = State.ORANGE


class TestCoordinate(unittest.TestCase):
    def testNewCoordinateWithoutMine(self):
        c = Coordinate()
        assert c.state == State.RED

    def testNewCoordinateWithMine(self):
        c = Coordinate(state=State.GREEN)
        assert c.state == State.GREEN

    def testFlagCoordinateWithoutMine(self):
        c = Coordinate()
        c.flag()
        assert c.state == State.BLUE

    def testFlagCoordinateWithMine(self):
        c = Coordinate(state=State.GREEN)
        c.flag()
        assert c.state == State.BLACK

    def testClickCoordinateWithoutMine(self):
        c = Coordinate()
        c.click()
        assert c.state == State.YELLOW

    def testClickCoordinateWithMine(self):
        c = Coordinate(state=State.GREEN)
        c.click()
        assert c.state == State.ORANGE

    def testFlagAndClickCoordinateWithoutMine(self):
        c = Coordinate()
        c.flag()
        c.click()
        assert c.state == State.YELLOW

    def testFlagAndClickCoordinateWithMine(self):
        c = Coordinate(state=State.GREEN)
        c.flag()
        c.click()
        assert c.state == State.ORANGE



class Board:
    def __init__(self):
        self.cols = 1
        self.rows = 1


class TestBoard(unittest.TestCase):

    def testNewBoardWithOneCoordinate(self):
        b = Board()
        assert b.cols == 1 and b.rows == 1


