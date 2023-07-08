from __future__ import annotations

from shared.enums import EdgeStatus, ConstraintStatus, LoopStatus


class Edge:
    ident: int
    status: EdgeStatus
    cells: set[Cell]
    junctions: set[Junction]

    def __init__(self, ident):
        self.ident = ident
        self.status = EdgeStatus.EMPTY
        self.cells = set()
        self.junctions = set()

    def setup_variables(self, cells, junctions):
        for cell in cells:
            if self in cell.edges:
                self.cells.add(cell)
        for junction in junctions:
            if self in junction.edges:
                self.junctions.add(junction)

    def update(self):
        self.iterate_status()

    def iterate_status(self):
        self.status = EdgeStatus((2 * self.status.value) % 7)

    def is_selected(self):
        return self.status == EdgeStatus.SELECTED

    def should_be_selected(self):
        arr = [c.loop_status for c in self.cells]
        if len(arr) == 1:
            return arr[0] == LoopStatus.NOEXP
        return arr[0] != arr[1]

    def are_neighbour(self, other: Edge) -> bool:
        return Edge.are_neighbours(self, other)

    @staticmethod
    def are_neighbours(e1: Edge, e2: Edge) -> bool:
        for j in e1.junctions:
            if j in e2.junctions:
                return True
        return False

    @staticmethod
    def num_selected_edges(arr: list[Edge]) -> int:
        return sum([1 for e in arr if e.status == EdgeStatus.SELECTED])


class Cell:
    ident: int
    neighbours: set[Cell]
    junctions: set[Junction]
    edges: set[Edge]
    sides: int
    constraint: int | None
    status: ConstraintStatus | None
    loop_status: LoopStatus

    def __init__(self, edges, ident, sides):
        self.ident = ident
        self.neighbours = set()
        self.junctions = set()
        self.edges = edges
        self.sides = sides
        self.constraint = None
        self.loop_status = LoopStatus.UNKNOWN

    def setup_variables(self):
        for edge in self.edges:
            for cell in edge.cells:
                if cell is self:
                    continue
                self.neighbours.add(cell)
                break

            for junction in edge.junctions:
                self.junctions.add(junction)

    def num_selected_edges_at_cell(self) -> int:
        return sum([1 for e in self.edges if e.is_selected()])

    def set_contraint(self) -> None:
        if self.loop_status == LoopStatus.OUT:
            self.constraint = 0
        else:
            self.constraint = len(self.edges) - len(self.neighbours)
        for cell in self.neighbours:
            if cell.loop_status != self.loop_status:
                self.constraint += 1

    def is_constraint(self) -> ConstraintStatus | None:
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
        self.status = self.is_constraint()

    def get_cells_opposite_side(self, cell: Cell) -> list[Cell]:
        res = set(flatten([j.cells for j in cell.junctions]))
        res = res - set(flatten([j.cells for j in self.junctions]))
        return list(res)

    def junction_intersection(self, cell: Cell) -> list[Cell]:
        res = []
        for j in list(set(self.junctions) & set(cell.junctions)):
            j.get_surrounding_cells()
            for c in j.cells:
                if c is self or c is cell:
                    continue
                if c not in res:
                    if self not in c.neighbours:
                        res.append(c)
        return res

    def get_neighbours(self) -> list[Cell]:
        res = []
        for edge in self.edges:
            res.extend(edge.cells - {self})
            # for cell in cells:
            #     if cell is self:
            #         continue
            #     if edge in cell.edges:
            #         res.append(cell)
        return res

    def print_edge(self):
        print(self.edges)


class Junction:
    edges: set[Edge]
    cells: set[Cell]
    ident: int

    def __init__(self, edges, ident):
        self.edges = edges
        self.ident = ident
        self.cells = set()

    def setup_variables(self):
        for edge in self.edges:
            for cell in edge.cells:
                if cell not in self.cells:
                    self.cells.add(cell)

    def get_surrounding_cells(self) -> list[Cell]:
        """Get the surrounding cells in traversable order.

        :return: A list of cells that surround the junction, in order.
        """
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

    def _get_surrounding_cells_with_start(self, cell: Cell) -> list[Cell]:
        cells = self.get_surrounding_cells()
        return shift_and_remove(cells, cell)

    def is_valid(self) -> bool:
        return Edge.num_selected_edges(self.edges) in [0, 2]

    def update(self):
        pass

    def print_edge(self):
        print(self.edges)


def sgn(n: int):
    if n < 0:
        return -1
    elif n == 0:
        return 0
    else:
        return 1


def flatten(lst):
    return [item for sublist in lst for item in sublist]


# https://stackoverflow.com/questions/30399534/shift-elements-in-a-list-by-n-indices
def shift(seq: list, n=0) -> list:
    a = n % len(seq)
    return seq[-a:] + seq[:-a]


def shift_and_remove(lst: list, val) -> list:
    return shift(lst, -lst.index(val))[1:]
