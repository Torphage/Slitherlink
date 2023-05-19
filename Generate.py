from Slitherlink import Cell, Junction
from enum import Enum
import random


class LoopStatus(Enum):
    UNKNOWN = 1
    EXP = 2
    NOEXP = 4
    OUT = 8


class Generate:
    def __init__(self, cells: list[Cell], junctions: list[Junction]):
        self.cells = cells[:]
        self.junctions = junctions
        self.available: list[Cell] = []
        self.loop = {k: LoopStatus.UNKNOWN for k in dict.fromkeys(cells)}

    def gen_loop(self):
        self.available.append(self.cells[11])
        # cell = random.choice(self.available)
        # self.expandable.append(cell)
        # print(cell.get_neighbours(self.cells))
        # print(self.get_adjacent(cell))
        # i = 0
        while len(self.available) > 0:
            # i += 1
            # print(self.expandable)
            # pick_cell
            cell = random.choice(self.available)
            self.available.remove(cell)

            next_cell = self.add_cell(cell)

            if self.loop[cell] == LoopStatus.EXP:
                self.add_available(cell)

            if self.loop[next_cell] == LoopStatus.EXP:
                self.add_available(next_cell)

        return self.loop

    def add_cell(self, cell: Cell) -> Cell:
        # can loop expand from current cell?
        if not self.is_expandable(cell):  # # if no neighbouring cells are valid
            return cell

        new_cell = self.pick_direction(cell)

        new_neighbours = self.get_adjacent(new_cell)
        if not any(new_neighbours):  # # if no neighbouring cells are valid
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

    def pick_direction(self, cell: Cell):
        return random.choice(cell.get_neighbours(self.cells))

    def get_adjacent(self, cell: Cell):
        res = []
        neighbours = cell.get_neighbours(self.cells)
        for neighbour in neighbours:
            res.append(self.valid_cell(neighbour, cell))
        return res

    def add_available(self, cell):
        for c in self.available:
            if c is cell:
                return
        self.available.append(cell)

    def valid_cell(self, next_cell: Cell, cell: Cell) -> bool:
        valid = True

        valid = valid and self.loop[next_cell] != LoopStatus.NOEXP
        valid = valid and self.loop[next_cell] != LoopStatus.OUT
        valid = valid and self.loop[next_cell] != LoopStatus.EXP

        # ? jobbig funktion asså

        cells = cell.junction_intersection(next_cell)

        for c in cells:
            valid = valid and self.cell_open(c)

        if not valid and self.loop[next_cell] == LoopStatus.UNKNOWN:
            self.loop[next_cell] = LoopStatus.OUT

        return valid

    def cell_open(self, cell: Cell) -> bool:
        return self.loop[cell] in [LoopStatus.UNKNOWN, LoopStatus.OUT]


def foo(listA):
    for i, item in enumerate(listA):
        if (i + 1) % 10 == 0:
            if item == 8:
                print("#")
            elif item == 4:
                print(".")
            else:
                print(item)
        else:
            if item == 8:
                print("#", end=" ")
            elif item == 4:
                print(".", end=" ")
            else:
                print(item, end=" ")
