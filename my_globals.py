from enum import Enum


class State(Enum):
    NO_CLICK_NO_MINE = 16  # * NOT clicked and doesn't contain a mine
    NO_CLICK_YES_MINE = 32  # * NOT clicked and does contain a mine
    FLAGGED_YES_MINE = 64  # * flagged and doesn't contain a mine
    FLAGGED_NO_MINE = 128  # * flagged and does contain a mine
    YES_CLICK_NO_MINE = 256  # * clicked and doesn't contain a mine
    YES_CLICK_YES_MINE = 512  # * clicked and does contain a mine
    REVEALED_OTHERWISE = 1024  # * revealed because a neighbor was clicked
