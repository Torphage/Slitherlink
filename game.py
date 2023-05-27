from __future__ import annotations
from slitherlink import Cell, Edge, Junction, Data
from generator.generate import Generate


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

    def generate_random(self, shape: str, size: tuple[int, int]) -> Game:
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
