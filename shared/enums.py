from enum import Enum


class EdgeStatus(Enum):
    EMPTY = 1
    SELECTED = 2
    MARKED = 4


class ConstraintStatus(Enum):
    LESS = 1
    EXACT = 2
    MORE = 4


class LoopStatus(Enum):
    UNKNOWN = 1
    EXP = 2
    NOEXP = 4
    OUT = 8
