import random
from typing import Self

from shared.slitherlink import Cell, Edge, Junction
from generator.generator import Generator


class Hexagon(Generator):
    size: int

    def __init__(
        self, cells: list[Cell], junctions: list[Junction], edges: set[Edge], size: int
    ):
        super().__init__(cells, junctions, edges, size)

    def pick_first_cell(self) -> Cell:
        cell_widths = list(range(self.size)) + list(range(self.size - 1))[::-1]
        xss = [self.probability_line(self.size + width) for width in cell_widths]
        ys = self.probability_line(2 * self.size - 1)
        probabilities = [ys[i] * x for i, xs in enumerate(xss) for x in xs]
        return random.choices(list(self.cells), weights=probabilities, k=1)[0]

    def print_ascii(self):
        return super().print_ascii()

    def print_numbers(self):
        return super().print_numbers()

    @classmethod
    def generate(cls, size: int) -> Self:
        num_edges = sum([6 * i for i in range(1, 3 * size, 3)])
        edges = [Edge(i) for i in range(num_edges)]

        offset = 0
        last_row = 0
        vertical_lines_done = 0
        cells = []
        for index, (row, width) in enumerate(get_rows(size)):
            if row != last_row:
                offset += width
                last_row = row
                vertical_lines_done += width - 1

            # The middle row
            connected_indices = [
                2 * index + offset,  # up left
                2 * index + offset + 1,  # up right
                2 * width + index + vertical_lines_done + offset + 1,  # right
                3 * width + 1 + 2 * index + offset + 1,  # down right
                3 * width + 1 + 2 * index + offset,  # down left
                2 * width + index + vertical_lines_done + offset,  # left
            ]

            # Above the middle row
            if row < size - 1:
                connected_indices[3] += 1
                connected_indices[4] += 1
            # Below the middle row
            elif row > size - 1:
                connected_indices[0] += 4 * (row - size + 1) - 1  # up left
                connected_indices[1] += 4 * (row - size + 1) - 1  # up right
                connected_indices[2] += 6 * (row - size + 1)  # right
                connected_indices[3] += 4 * (row - size + 1)  # down right
                connected_indices[4] += 4 * (row - size + 1)  # down left
                connected_indices[5] += 6 * (row - size + 1)  # left

            connected_edges = [edges[k] for k in connected_indices]
            cells.append(Cell(connected_edges, index, 6))

        offset = 0
        last_row = 0
        junctions = []
        vertical_lines_done = 0
        last_width = 0
        add = 0
        for index, (row, width, col) in enumerate(get_junctions(size)):
            if row > 2 * size - 1:
                add = 1
            if row != last_row:
                offset = offset + width
                last_row = row
                if last_width == width:
                    vertical_lines_done += width
                last_width = width

            connected_indices = []
            pos = index + vertical_lines_done - row // 2
            if row % 2 == 0:
                if row != 0:  # up
                    connected_indices.append(pos - width)
                if row < 2 * size or col != 0:  # down left
                    connected_indices.append(pos + col - add)
                if row < 2 * size or col != width - 1:  # down right
                    connected_indices.append(pos + col - add + 1)

            else:
                if row > 2 * size or col != 0:  # up left
                    connected_indices.append(pos + col - add - width)
                if row > 2 * size or col != width - 1:  # up right
                    connected_indices.append(pos + col - add - width + 1)
                if row != 4 * size - 1:  # down
                    connected_indices.append(pos + width - 1)

            connected_edges = [edges[k] for k in connected_indices]
            junctions.append(Junction(connected_edges, index))

        return Hexagon(cells, junctions, {e for e in edges}, size)


def get_rows(size: int) -> list[tuple[int, int]]:
    """Returns a list of tuples containing the row index, the length of the row
    and the column index of the first cell in the row.

    :param size: how many cells on one side of the hexagon
    :return: (row index, column length, column index)
    """
    num_cells = 1 + sum([6 * i for i in range(1, size)])
    upperhalf = size * (size + (size - 1)) - (size - 1) * (size) // 2
    row = 0
    j = 0
    rows = []
    k = 0
    row2 = 1
    for i in range(num_cells):
        if i < upperhalf:
            if j >= row + size:
                row += 1
                j = 0
            rows.append((row, row + size))
            j += 1
        else:
            if k >= row - row2 + size:
                row2 += 1
                k = 0
            rows.append((row + row2, row - row2 + size))
            k += 1
    return rows


def get_junctions(size: int) -> list[tuple[int, int, int]]:
    """Returns a list of tuples containing the row index, the length of the row
    and the column index of the first cell in the row.

    :param size: how many cells on one side of the hexagon
    :return: (row index, column length, column index)
    """
    num_junctions = sum([6 * i for i in range(1, 2 * size, 2)])
    upperhalf = num_junctions // 2
    row = 0
    j = 0
    junctions = []
    width = 0
    increased = False
    for _ in range(upperhalf):
        if j >= width + size:
            if not increased:
                width += 1
                increased = True
            else:
                increased = False
            j = 0
            row += 1
        junctions.append((row, width + size, j))
        j += 1

    temp = junctions[:]
    temp.reverse()
    temp = [(4 * size - 1 - t[0], t[1], t[1] - t[2] - 1) for t in temp]
    junctions.extend(temp)
    return junctions
