from __future__ import annotations
from typing import TypedDict
from enum import Enum
import random
import pprint
# from generator import Generate

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
    
class Data(TypedDict):
    edges: list[Edge]
    cells: list[Cell]
    junctions: list[Junction]

class Edge():
    status: EdgeStatus
    cells: list[int]
    
    def __init__(self):
        self.status = EdgeStatus.EMPTY
        
    def set_cells(self, cells):
        self.cells = cells    
    
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
        return len(e1.junctions.intersection(e2.junctions)) > 0
    
    @staticmethod
    def num_selected_edges(arr: list[Edge]) -> int:
        return sum([1 for e in arr if e.status == EdgeStatus.SELECTED])


class Cell():
    edges: list[Edge]
    constraint: int
    status: ConstraintStatus | None
    loop_status: LoopStatus
    
    def __init__(self, edges, constraint):
        self.edges = edges
        self.constraint = constraint
        self.loop_status = LoopStatus.UNKNOWN
        
    def num_selected_edges_at_cell(self) -> int:
        return sum([1 for e in self.edges if e.is_selected()])
    
    def get_constraint(self) -> ConstraintStatus | None:
        if self.constraint == None:
            return None
        match sgn(self.num_selected_edges_at_cell() - self.constraint):
            case -1: return ConstraintStatus.LESS
            case  0: return ConstraintStatus.EXACT
            case  1: return ConstraintStatus.MORE
            
    def is_solved(self):
        return self.status in [None, ConstraintStatus.EXACT]
    
    def update(self, edges):
        self.status = self.get_constraint()
        
    def get_neighbours(self, cells) -> list[Cell]:
        # temp = self.edges[:]
        res = []
        # print("Pre",  self)
        for cell in cells:
            if cell is self: continue
            for edge in self.edges:
                if edge in cell.edges:
                    res.append(cell)
        # print("Post", res)
        return res

    def print_edge(self):
        print(self.edges)

class Junction():
    edges: list[Edge]
    
    def __init__(self, edges):
        self.edges = edges
    
    def is_valid(self) -> bool:
        return Edge.num_selected_edges(self.edges) in [0, 2]
    
    def update(self, edges):
        pass

    def print_edge(self):
        print(self.edges)


class Game():
    data: Data

    def __init__(self):
        pass

    def set_puzzle(self):
        pass
    
    ## Check solution
    
    def solved(self) -> bool:
        return self.solved_cells() and self.valid_junctions()
        
    def solved_cells(self) -> bool:
        return all([c.is_solved() for c in self.data["cells"]])
    
    def valid_junctions(self) -> bool:
        return all([j.is_valid() for j in self.data["junctions"]])
        

    ## Update the grid
    
    def update(self, index: int):
        edge = self.data["edges"][index]
        edge.update()
        for c in edge.cells:
            c.update(self.data["edges"])
        for j in edge.junctions:
            j.update(self.data["edges"])

    
    @staticmethod
    def parse(arr: list[str]) -> Game:
        return Game()
    
    def generate_random(shape: str) -> Game:
        match shape:
            case "square": Generate.random_square(10)
            case "hexagon": pass
            case _: pass
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
  


