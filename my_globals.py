from enum import Enum


class State(Enum):
    NO_CLICK_NO_MINE = 1  # * NOT clicked and doesn't contain a mine
    NO_CLICK_YES_MINE = 2  # * NOT clicked and does contain a mine
    FLAGGED_YES_MINE = 4  # * flagged and doesn't contain a mine
    FLAGGED_NO_MINE = 8  # * flagged and does contain a mine
    YES_CLICK_NO_MINE = 16  # * clicked and doesn't contain a mine
    YES_CLICK_YES_MINE = 32  # * clicked and does contain a mine
    REVEALED_OTHERWISE = 64  # * revealed because a neighbor was clicked
