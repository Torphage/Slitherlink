from Slitherlink import Cell, Junction, Edge
from enum import Enum
from typing import Self
import os
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
        self.available.append(random.choice(self.cells))
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

        for keys in self.loop.keys():
            if self.loop[keys] == LoopStatus.UNKNOWN:
                self.loop[keys] = LoopStatus.OUT
        return self.loop

    def add_cell(self, cell: Cell) -> Cell:
        # can loop expand from current cell?
        if not self.is_expandable(cell):
            return cell

        new_cell = self.pick_direction(cell)
        Rectangle.generate(10, 10)
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
            # print(foo([" "," "," "," "," "," "," "," "," "," "]+[val.value for val in list(self.loop.values())]))
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
        # valid = valid and self.loop[next_cell] != LoopStatus.EXP

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

        cells = cell.junction_intersection(next_cell)

class Rectangle(Generate):
    def __init__(self, cells: list[Cell], junctions: list[Junction]):
        if os.path.exists("demofile.txt"):
            os.remove("demofile.txt")
        if os.path.exists("hst.txt"):
            os.remove("hst.txt")
        super().__init__(cells, junctions)

    @classmethod
    def generate(cls, w: int, h: int) -> Self:
        edges = []
        for i in range(2 * w * h + w + h):
            edges.append(Edge(i))
        length = len(edges) // 2

        cells = []
        # for i in range(w * h):
        for j in range(h):
            for i in range(w):
                index = i + w * j
                cells.append(
                    Cell(
                        [
                            edges[index],
                            edges[length + i * w + j],
                            edges[index + w],
                            edges[length + i * w + w + j],
                        ],
                        index,
                    )
                )
                # with open('demofile.txt', 'a') as fd:
                #     fd.write(f'\n{edges[index].ident} {edges[index + w].ident} {edges[length + i*w + j].ident} {edges[length + i*w + w + j].ident}')
        # right = []
        # for i in range(w + 1):
        #     temp = edges[length + 10*i]
        #     for j in range(h + 1):
        #         pass

        junctions = []
        # for i in range(w * h + w + h):
        #     junctions.append(Junction)
        s = ""
        index = 0
        for j in range(h + 1):
            for i in range(w + 1):
                if i == 0 and j == 0:
                    junctions.append(Junction([edges[0], edges[length]], index))
                    # s = "0,0: " + str(edges[0].ident) + "  " + str(edges[length].ident)
                elif i == w and j == h:
                    junctions.append(
                        Junction([edges[length - 1], edges[2 * length - 1]], index)
                    )
                    # s = "w,h: " + str(edges[length-1].ident) + "  " + str(edges[2*length-1].ident)
                elif i == w and j == 0:
                    junctions.append(
                        Junction([edges[w - 1], edges[length + j + h * i]], index)
                    )
                    # s = "w,0: " + str(edges[w-1].ident) + "  " + str(edges[length + j + h*i].ident)
                elif i == 0 and j == h:
                    junctions.append(
                        Junction([edges[length - w], edges[length + h - 1]], index)
                    )
                    # s = "0,h: " + str(edges[length-w].ident) + "  " + str(edges[length+h-1].ident)
                elif i == 0:
                    junctions.append(
                        Junction(
                            [edges[w * j], edges[length + j - 1], edges[length + j]],
                            index,
                        )
                    )
                    # s = "0,?: " + str(edges[w*j].ident) + "  " + str(edges[length + j - 1].ident) + "  " + str(edges[length + j].ident)
                elif j == 0:
                    junctions.append(
                        Junction([edges[i - 1], edges[i], edges[length + j]], index)
                    )
                    # s = "?,0: " + str(edges[i-1].ident) + "  " + str(edges[i].ident) + "  " + str(edges[length + j + h*i].ident)
                elif i == w:
                    junctions.append(
                        Junction(
                            [
                                edges[w * j + i - 1],
                                edges[2 * length - w + j - 1],
                                edges[2 * length - w + j],
                            ],
                            index,
                        )
                    )
                    # s = "w,?: " + str(edges[w*j + i-1].ident) + "  " + str(edges[2*length - w + j - 1].ident) + "  " + str(edges[2*length - w + j].ident)
                elif j == h:
                    junctions.append(
                        Junction(
                            [
                                edges[length - w + i - 1],
                                edges[length - w + i],
                                edges[length + w + h * i - 1],
                            ],
                            index,
                        )
                    )
                    # s = "?,h: " + str(edges[length - w + i - 1].ident) + "  " + str(edges[length - w + i].ident) + "  " + str(edges[length + w + h*i - 1].ident)
                else:
                    junctions.append(
                        Junction(
                            [
                                edges[w * j + i - 1],
                                edges[w * j + i],
                                edges[length + i * h + j - 1],
                                edges[length + i * h + j],
                            ],
                            index,
                        )
                    )
                    # s = "?,?: " + str(edges[w*j + i-1].ident) + "  " + str(edges[w*j + i].ident) + "  " + str(edges[length + i*h + j - 1].ident) + "  " + str(edges[length + i*h + j].ident)
                index += 1
                # with open('hst.txt', 'a') as fd:
                #     fd.write(f'\n{s}')
        return Rectangle(cells, junctions)


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def foo(listA):
    for i, item in enumerate(listA):
        if (i + 1) % 20 == 0:
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
