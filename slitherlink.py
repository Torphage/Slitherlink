from __future__ import annotations
from typing import TypedDict
from shared.enums import EdgeStatus, ConstraintStatus, LoopStatus


class Data(TypedDict):
    edges: list[Edge]
    cells: list[Cell]
    junctions: list[Junction]


class Edge:
    ident: int
    status: EdgeStatus
    cells: list[Cell]
    junctions: list[Junction]
    neighbours: list[Edge]

    def __init__(self, ident):
        self.ident = ident
        self.status = EdgeStatus.EMPTY
        self.cells = []
        self.junctions = []
        self.neighbours = []

    def setup_variables(self, cells, junctions, edges):
        for cell in cells:
            if self in cell.edges:
                self.cells.append(cell)
        for junction in junctions:
            if self in junction.edges:
                self.junctions.append(junction)
        for edge in edges:
            if self.are_neighbour(edge):
                self.neighbours.append(edge)

    def update(self):
        self.iterate_status()

    def iterate_status(self):
        self.status = EdgeStatus((2 * self.status.value) % 7)

    def is_selected(self):
        return self.status == EdgeStatus.SELECTED

    def are_neighbour(self, other: Edge) -> bool:
        return Edge.are_neighbours(self, other)

    @staticmethod
    def are_neighbours(e1: Edge, e2: Edge) -> bool:
        return len(set(e1.junctions).intersection(e2.junctions)) > 0

    @staticmethod
    def num_selected_edges(arr: list[Edge]) -> int:
        return sum([1 for e in arr if e.status == EdgeStatus.SELECTED])


class Cell:
    ident: int
    neighbours: list[Cell]
    junctions: list[Junction]
    edges: list[Edge]
    constraint: int | None
    status: ConstraintStatus | None
    loop_status: LoopStatus

    def __init__(self, edges, ident):
        self.ident = ident
        self.neighbours = []
        self.junctions = []
        self.edges = edges
        self.constraint = None
        self.loop_status = LoopStatus.UNKNOWN

    def setup_variables(self, cells, junctions):
        for cell in cells:
            for edge in cell.edges:
                if edge in self.edges and cell not in self.neighbours:
                    self.neighbours.append(cell)
        for junction in junctions:
            for edge in junction.edges:
                if edge in self.edges and junction not in self.junctions:
                    self.junctions.append(junction)

    def num_selected_edges_at_cell(self) -> int:
        return sum([1 for e in self.edges if e.is_selected()])

    def get_constraint(self) -> ConstraintStatus | None:
        if self.constraint is None:
            return None
        match sgn(self.num_selected_edges_at_cell() - self.constraint):
            case -1:
                return ConstraintStatus.LESS
            case 0:
                return ConstraintStatus.EXACT
            case 1:
                return ConstraintStatus.MORE

    def is_solved(self):
        return self.status in [None, ConstraintStatus.EXACT]

    def update(self):
        self.status = self.get_constraint()

    def connected_cells(self, cell: Cell) -> list[Cell]:
        res = set(flatten([j.cells for j in cell.junctions]))
        res = res - set([self, cell] + self.neighbours)
        return list(res)

    def junction_intersection(self, cell: Cell) -> list[Cell]:
        res = []
        for j in list(set(self.junctions) & set(cell.junctions)):
            j.get_ordered_cells()
            for c in j.cells:
                if c is self or c is cell:
                    continue
                if c not in res:
                    if self not in c.neighbours:
                        res.append(c)
        return res

    def get_neighbours(self, cells: list[Cell]) -> list[Cell]:
        res = []
        for edge in self.edges:
            for cell in cells:
                if cell is self:
                    continue
                if edge in cell.edges:
                    res.append(cell)
        return res

    def print_edge(self):
        print(self.edges)


class Junction:
    edges: list[Edge]
    cells: list[Cell]
    ident: int

    def __init__(self, edges, ident):
        self.edges = edges
        self.ident = ident
        self.cells = []

    def setup_variables(self, cells):
        for cell in cells:
            for edge in cell.edges:
                if edge in self.edges and cell not in self.cells:
                    self.cells.append(cell)

    def get_ordered_cells(self) -> list[Cell]:
        res = self.cells[:1]
        temp = self.cells[1:]
        i = 0
        while len(temp) > 0:
            if res[-1] in temp[i].neighbours:
                res.append(temp[i])
                temp.remove(temp[i])
                i = 0
            else:
                i += 1

        return res

    def is_valid(self) -> bool:
        return Edge.num_selected_edges(self.edges) in [0, 2]

    def update(self):
        pass

    def print_edge(self):
        print(self.edges)


class Game:
    data: Data

    def __init__(self, cells: list[Cell], junctions: list[Junction], edges: list[Edge]):
        self.data = {"cells": cells, "junctions": junctions, "edges": edges}

    def set_puzzle(self):
        pass

    # Check solution

    def solved(self) -> bool:
        return self.solved_cells() and self.valid_junctions()

    def solved_cells(self) -> bool:
        return all([c.is_solved() for c in self.data["cells"]])

    def valid_junctions(self) -> bool:
        return all([j.is_valid() for j in self.data["junctions"]])

    # Update the grid

    def setup_variables(self):
        for edge in self.data["edges"]:
            edge.setup_variables(
                self.data["cells"], self.data["junctions"], self.data["edges"]
            )
        for cell in self.data["cells"]:
            cell.setup_variables(self.data["cells"], self.data["junctions"])
        for junction in self.data["junctions"]:
            junction.setup_variables(self.data["cells"])

    def update(self, index: int):
        edge = self.data["edges"][index]
        edge.update()
        for c in edge.cells:
            c.update()
        for j in edge.junctions:
            j.update()

    @staticmethod
    def parse(arr: list[str]) -> Game:
        return Game()

    def generate_random(self, shape: str) -> Game:
        match shape:
            case "square":
                Generate.random_square(10)
            case "hexagon":
                pass
            case _:
                pass
        return Game()

    @staticmethod
    def generate_from_file(filename: str) -> Game:
        lines = []
        with open(filename) as file:
            lines = file.readlines()
        return Game.parse(lines)


# pprint.pprint(list(chunks(Generate.random_square(1),10)))


def sgn(n: int):
    if n < 0:
        return -1
    elif n == 0:
        return 0
    else:
        return 1


def flatten(lst):
    return [item for sublist in lst for item in sublist]


# def foo(arr)
#
# import importlib
# from Slitherlink import *
# importlib.reload(Slitherlink)
# from Slitherlink import *
# import Generate
# importlib.reload(Generate)
# import Generate
# edges = [Edge() for _ in range(220)]
# import data
# cells = data.cells(edges)
# junctions = data.junctions(edges)
# [c.update(edges) for c in cells]
# [j.update(edges) for j in junctions]
# gen = Generate.Generate(cells)
# Generate.foo([val.value for val in list(gen.gen_loop().values())])
# gen.gen_loop()


# cells = [Cell([edges[i] for i in [0,2,3,5]],4), Cell([edges[i] for i in [1,3,4,6]],1),Cell([edges[i] for i in [5,7,8,10]],1),Cell([edges[i] for i in [6,8,9,11]],0)]
# junctions = [Junction([edges[i] for i in [0,2]]),Junction([edges[i] for i in [0,1,3]]),Junction([edges[i] for i in [1,4]]),Junction([edges[i] for i in [2,5,7]]),Junction([edges[i] for i in [3,5,6,8]]),Junction([edges[i] for i in [4,6,9]]),Junction([edges[i] for i in [7,10]]),Junction([edges[i] for i in [8,10,11]]),Junction([edges[i] for i in [9,11]])]


# 1 2 3 0 1
# . 3 2 . 2
# . . 3 . .

# 1 2 3 .
#  3 1 .
# . . 3 2

#  1 2  3 4
# 2    .    1
#  2 3  1 .

# 1  6  1  2
#  1
#   1
# 3  4  2


# 1    1    1    1

#     1
# 1         1    1
#        1

# 1    1    1    1

# 1  1  1  1  1
# 1 2/2 1  1  1
# 1  1  1 2\1 1
# 1  1  1  1  1


# +---------+---------+---------+---------+---------+---------+
# |         |         |         |         |         |         |
# |         |         |         |         |         |         |
# |    1    |    1    |    1    |    1    |    1    |    1    |
# |         |         |         |         |         |         |
# +---------+---------+---------+---------+---------+---------+
# |         |        /|         |         |         |         |
# |         |  2   /  |         |         |         |         |
# |    1    |   /     |    1    |    1    |    1    |    1    |
# |         |/   2    |         |         |         |         |
# +---------+---------+---------+---------+---------+---------+
# |         |         |         |         | \       |         |
# |         |         |         |         |   \     |         |
# |    1    |    1    |    1    |    1    |  2 \ 1  |    1    |
# |         |         |         |         |      \  |         |
# +---------+---------+---------+---------+---------+---------+
# |         |         |         |         |         |         |
# |         |         |         |         |         |         |
# |    1    |    1    |    1    |    1    |    1    |    1    |
# |         |         |         |         |         |         |
# +---------+---------+---------+---------+---------+---------+
