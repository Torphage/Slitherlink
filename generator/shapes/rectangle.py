from slitherlink import Cell, Edge, Junction
from generator.generator import Generator
from typing import Self
import random
import scipy
import numpy as np


class Rectangle(Generator):
    """A subtype of Generator that generates
    a rectangle of cells and junctions.

    :param Generator: The parent class
    """

    def __init__(
        self,
        cells: list[Cell],
        junctions: list[Junction],
        edges: list[Edge],
        w: int,
        h: int,
    ):
        """Initialises a rectangular shaped slitherlink puzzle
        that takes the cells and junctions as parameters.

        :param cells:
        :param junctions: _description_
        """

        super().__init__(cells, junctions, edges, (w, h))
        self.w = w
        self.h = h

    def pick_first_cell(self) -> Cell:
        xs = scipy.stats.norm.pdf(np.linspace(-3, 3, self.w))
        ys = scipy.stats.norm.pdf(np.linspace(-3, 3, self.h))
        probabilities = [y * x for y in ys for x in xs]
        return random.choices(self.cells, weights=probabilities, k=1)[0]

    def print_ascii(self):
        lst = [val.value for val in self.loop.values()]
        for i, item in enumerate(lst):
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

    def print_numbers(self):
        lst = [val.value for val in self.loop.values()]
        for i, item in enumerate(lst):
            if (i + 1) % self.w == 0:
                print(f"{self.cells[i].constraint} ")
            else:
                print(f"{self.cells[i].constraint} ", end="")

    @classmethod
    def generate(cls, size: tuple[int, int]) -> Self:
        w, h = size
        length = w * h + w
        edges = [Edge(i) for i in range(2 * length + h)]

        cells = []
        for j in range(h):
            for i in range(w):
                index = j * w + i  # index of the cell
                connected_indices = [
                    index,  # up
                    length + index + j + 1,  # right
                    index + w,  # down
                    length + index + j,  # left
                ]
                connected_edges = [edges[k] for k in connected_indices]
                cells.append(Cell(connected_edges, index))

        junctions = []
        for j in range(h + 1):
            for i in range(w + 1):
                index = j * (w + 1) + i  # index of the junction
                connected_indices = []
                if j != 0:  # up
                    connected_indices.append(length + index - w - 1)
                if i != w:  # right
                    connected_indices.append(index - j)
                if j != h:  # down
                    connected_indices.append(length + index)
                if i != 0:  # left
                    connected_indices.append(index - j - 1)

                connected_edges = [edges[k] for k in connected_indices]
                junctions.append(Junction(connected_edges, index))

        return Rectangle(cells, junctions, edges, w, h)
