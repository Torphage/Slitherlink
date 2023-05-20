from slitherlink import Cell, Junction, Edge
import random
from shared.enums import LoopStatus


class Generate:
    """
    An abstract class for generating slitherlink puzzles
    """

    def __init__(
        self,
        cells: list[Cell],
        junctions: list[Junction],
        edges: list[Edge],
        w: int,
        h: int,
    ):
        """_summary_

        :param cells: '_description_'
        :type cells: list[Cell]
        :param junctions: _description_
        :type junctions: list[Junction]
        """

        self.w = w
        self.h = h
        self.cells = cells[:]
        self.junctions = junctions
        self.edges = edges
        self.available: list[Cell] = []
        self.loop = {k: LoopStatus.UNKNOWN for k in dict.fromkeys(cells)}

    def gen_loop(self):
        self.available.append(random.choice(self.cells))

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
        """Add a cell branching of from an existing cell

        :param cell: The cell we want to branch off from
        :return: ???
        """
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

        neib = set(self.cells).intersection(
            flatten([j.cells for j in next_cell.junctions])
        )
        neib = neib - set([cell, next_cell]) - set(cell.neighbours)
        neib = list(neib)

        for n in neib:
            valid = valid and self.cell_open(n)

        if not valid and self.loop[next_cell] == LoopStatus.UNKNOWN:
            self.loop[next_cell] = LoopStatus.OUT

        return valid

    def cell_open(self, cell: Cell) -> bool:
        return self.loop[cell] in [LoopStatus.UNKNOWN, LoopStatus.OUT]

    def foo(self, listA):
        for i, item in enumerate(listA):
            if (i + 1) % self.w == 0:
                if item == 8:
                    print(".")
                elif item == 4:
                    print("#")
                else:
                    print(item)
            else:
                if item == 8:
                    print(".", end=" ")
                elif item == 4:
                    print("#", end=" ")
                else:
                    print(item, end=" ")


def flatten(lst):
    return [item for sublist in lst for item in sublist]
