from __future__ import annotations
from typing import Collection
from enum import Enum
from itertools import combinations

class EdgeStatus(Enum):
    EMPTY = 1
    SELECTED = 2
    MARKED = 4
    
class ConstraintStatus(Enum):
    LESS = 1
    EXACT = 2
    MORE = 4
    

class Edge():
    cells: set[int]
    junctions: set[int]
    status: EdgeStatus
    
    def __init__(self):
        self.status = EdgeStatus.EMPTY


    def is_neighbour(self, other: Edge) -> bool:
        return Edge.is_neighbours(self, other)

    def iterate_status(self):
        self.status = (2 * self.status.value) % 7 
        
    @staticmethod
    def is_neighbours(e1: Edge, e2: Edge) -> bool:
        return len(e1.junctions.intersection(e2.junctions)) > 0



class Cell():
    index: int
    constraint: int
    edges: set[int]
    status: ConstraintStatus | None


class Junction():
    index: int
    edges: set[int]
    valid: bool



class Game():
    cells: list[Cell]
    edges: list[Edge]
    junctions: list[Junction]

    def __init__(self):
        pass

    def set_puzzle(self):
        pass
    
    def solved(self) -> bool:
        return self.solved_cells() and self.solved_junctions()
        
    def solved_cells(self) -> bool:
        return all([self.valid_cell(i) for i in range(len(self.cells))])
    
    def solved_junctions(self) -> bool:
        return all([self.valid_junction(i) for i in range(len(self.junctions))])
        
    
    
    def handle_edge(self, index: int):
        self.toggle_edge(index)
        for i in self.edges[index].cells:
            self.update_cell(i)
        for i in self.edges[index].junctions:
            self.update_junction(i)
        

    def toggle_edge(self, index: int):
        self.edges[index].iterate_status()
        match self.edges[index].status:
            case EdgeStatus.EMPTY:
                self.clear_edge(index)
            case EdgeStatus.SELECTED:
                self.select_edge(index)
            case EdgeStatus.MARKED:
                self.mark_edge(index)

    def select_edge(self, index: int):
        self.edges[index].status = EdgeStatus.SELECTED

    def mark_edge(self, index: int):
        self.edges[index].status = EdgeStatus.MARKED
        
    def clear_edge(self, index: int):
        self.edges[index].status = EdgeStatus.EMPTY
        
    def num_selected_edges(self, arr: list[Edge]) -> int:
        return len([e for e in arr if e.status == EdgeStatus.SELECTED])
        
        
    # Cell

    def get_edges_at_cell(self, index: int) -> list[Edge]:
        cell = self.cells[index]
        return [e for e in self.edges if cell in e.cells]
    
    def num_edges_at_cell(self, index: int) -> int:
        edge_list = self.get_edges_at_cell(index)
        return sum([1 for e in edge_list if e.status in e.cells])
    
    def get_constraint(self, index: int) -> ConstraintStatus | None:
        constraint = self.cells[index].constraint
        if constraint == None:
            return None
        match sgn(self.num_edges_at_cell(index) - constraint):
            case -1: return ConstraintStatus.LESS
            case  0: return ConstraintStatus.EXACT
            case  1: return ConstraintStatus.MORE
            
    def valid_cell(self, index: int):
        return self.cells[index].status in [None, ConstraintStatus.EXACT]
    
    def update_cell(self, index: int):
        self.cells[index].status = self.get_constraint(index)
    
    
    # Junction
    
    def get_edges_at_junction(self, index: int) -> list[Edge]:
        junction = self.junctions[index]
        return [e for e in self.edges if junction in e.junctions]

    def num_edges_at_junction(self, index: int) -> int:
        edge_list = self.get_edges_at_junction(index)
        return self.num_selected_edges(edge_list)
    
    def valid_junction(self, index: int) -> bool:
        return self.num_edges_at_junction(index) in [0, 2]
    
    def update_junction(self, index: int):
        self.junctions[index].valid = self.valid_junction(index)
                
    

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

    
    @staticmethod
    def parse(arr: list[str]) -> Game:
        return Game()
    
    @staticmethod
    def generate(filename: str) -> Game:
        lines = []
        with open(filename) as file:
            lines = file.readlines()
        return Game.parse(lines)
    
    

def sgn(n: int):
    if n < 0:
        return -1
    elif n == 0:
        return 0
    else:
        return 1    
