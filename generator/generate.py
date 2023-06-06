from slitherlink import Cell, Junction, Edge
import random
from shared.enums import LoopStatus
from abc import ABC, abstractmethod


class Generate(ABC):
    """
    An abstract class for generating slitherlink puzzles
    """

    size: int | tuple[int, int]
    cells: list[Cell]
    junctions: list[Junction]
    edges: list[Edge]
    available: list[Cell]
    loop: dict[Cell, LoopStatus]

    def __init__(
        self,
        cells: list[Cell],
        junctions: list[Junction],
        edges: list[Edge],
        size: int | tuple[int, int]
    ):
        """_summary_

        :param cells: '_description_'
        :type cells: list[Cell]
        :param junctions: _description_
        :type junctions: list[Junction]
        """

        self.size = size
        self.cells = cells[:]
        self.junctions = junctions
        self.edges = edges
        self.available = []
        self.loop = {k: LoopStatus.UNKNOWN for k in dict.fromkeys(cells)}

    @abstractmethod
    def pick_first_cell(self) -> Cell:
        return random.choice(self.cells)

    @abstractmethod
    def print_ascii(self):
        return NotImplemented

    @abstractmethod
    def print_numbers(self):
        return NotImplemented

    @classmethod
    def generate(cls, size: int | tuple[int, int]):
        return NotImplemented

    def gen_loop(self) -> dict[Cell, LoopStatus]:
        self.available.append(self.pick_first_cell())

        while len(self.available) > 0:
            cell = random.choice(self.available)
            self.available.remove(cell)

            next_cell = self.add_cell(cell)

            if self.loop[cell] == LoopStatus.EXP:
                self.add_available(cell)

            if self.loop[next_cell] == LoopStatus.EXP:
                self.add_available(next_cell)

        for keys in self.loop.keys():
            if self.loop[keys] == LoopStatus.UNKNOWN:
                self.loop[keys] = LoopStatus.OUT
        return self.loop

    def add_cell(self, cell: Cell) -> Cell:
        # can loop expand from current cell?
        if not self.is_expandable(cell):
            return cell

        new_cell = self.pick_direction(cell)

        if self.loop[new_cell] != LoopStatus.UNKNOWN:
            return cell

        new_neighbours = self.get_adjacent(new_cell)
        if not any(new_neighbours):
            self.loop[new_cell] = LoopStatus.OUT
            return new_cell

        if self.valid_cell(new_cell, cell):
            self.loop[new_cell] = LoopStatus.EXP
        else:
            self.loop[new_cell] = LoopStatus.OUT

        return new_cell

    def is_expandable(self, cell: Cell) -> bool:
        neighbours = self.get_adjacent(cell)

        if not any(neighbours):
            self.loop[cell] = LoopStatus.NOEXP
            return False

        return True

    def pick_direction(self, cell: Cell) -> Cell:
        return random.choice(cell.get_neighbours(self.cells))

    def get_adjacent(self, cell: Cell) -> list[bool]:
        neighbours = cell.get_neighbours(self.cells)
        return [self.valid_cell(n, cell) for n in neighbours]

    def add_available(self, cell: Cell) -> None:
        for c in self.available:
            if c is cell:
                return
        self.available.append(cell)

    def valid_cell(self, next_cell: Cell, cell: Cell) -> bool:
        valid = True

        valid = valid and self.loop[next_cell] != LoopStatus.NOEXP
        valid = valid and self.loop[next_cell] != LoopStatus.OUT
        valid = valid and self.loop[next_cell] != LoopStatus.EXP

        for n in cell.get_cells_opposite_side(next_cell):
            valid = valid and self.cell_open(n)

        if not valid and self.loop[next_cell] == LoopStatus.UNKNOWN:
            self.loop[next_cell] = LoopStatus.OUT

        return valid

    def cell_open(self, cell: Cell) -> bool:
        return self.loop[cell] in [LoopStatus.UNKNOWN, LoopStatus.OUT]

    def foo(self, listA: list) -> None:
        for i, item in enumerate(listA):
            if (i + 1) % self.w == 0:
                if item == 8:
                    print("  ")
                elif item == 4:
                    print("▓▓")
                elif item == 2:
                    print("--")
                else:
                    print("÷÷")
            else:
                if item == 8:
                    print("  ", end="")
                elif item == 4:
                    print("▓▓", end="")
                elif item == 2:
                    print("--", end="")
                else:
                    print("÷÷", end="")


def flatten(lst: list[list]) -> list:
    return [item for sublist in lst for item in sublist]


def split(lst: list) -> list:
    res = []
    temp = []
    for elem in lst:
        if elem:
            temp.append(elem)
        elif temp:
            res.append(temp)
            temp = []
    if temp and not lst[0]:
        res.append(temp)
    return res
