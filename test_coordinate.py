import unittest

from my_globals import State


class Coordinate:
    def __init__(self, state=State.NO_CLICK_NO_MINE):
        self.state = state

    def flag(self):
        if self.state == State.NO_CLICK_YES_MINE or self.state == State.YES_CLICK_YES_MINE:
            self.state = State.FLAGGED_YES_MINE
        elif self.state == State.NO_CLICK_NO_MINE or self.state == State.YES_CLICK_NO_MINE:
            self.state = State.FLAGGED_NO_MINE

    def click(self):
        if self.state == State.NO_CLICK_NO_MINE or self.state == State.FLAGGED_NO_MINE:
            self.state = State.YES_CLICK_NO_MINE

        if self.state == State.NO_CLICK_YES_MINE or self.state == State.FLAGGED_YES_MINE:
            self.state = State.YES_CLICK_YES_MINE


        return -1 if self.state == State.YES_CLICK_YES_MINE else 0

class TestCoordinate(unittest.TestCase):
    def testNewCoordinateWithoutMine(self):
        c = Coordinate()
        self.assertEqual(State.NO_CLICK_NO_MINE, c.state)

    def testNewCoordinateWithMine(self):
        c = Coordinate(state=State.NO_CLICK_YES_MINE)
        self.assertEqual(State.NO_CLICK_YES_MINE, c.state)

    def testFlagCoordinateWithoutMine(self):
        c = Coordinate()
        c.flag()
        self.assertEqual(State.FLAGGED_NO_MINE, c.state)

    def testClickCoordinateWithoutMine(self):
        c = Coordinate(State.NO_CLICK_NO_MINE)
        c.click()
        self.assertEqual(State.YES_CLICK_NO_MINE, c.state)

    def testClickCoordinateWithMine(self):
        c = Coordinate(state=State.NO_CLICK_YES_MINE)
        c.click()
        self.assertEqual(State.YES_CLICK_YES_MINE, c.state)

    def testFlagAndClickCoordinateWithoutMine(self):
        c = Coordinate()
        c.flag()
        c.click()
        self.assertEqual(State.YES_CLICK_NO_MINE, c.state)

    def testFlagAndClickCoordinateWithMine(self):
        c = Coordinate(state=State.NO_CLICK_YES_MINE)
        c.flag()
        c.click()
        self.assertEqual(State.YES_CLICK_YES_MINE, c.state)


    def testFlagCoordinateWithMine(self):
        c = Coordinate(state=State.NO_CLICK_YES_MINE)
        c.flag()
        self.assertEqual(State.FLAGGED_YES_MINE, c.state)