from __future__ import annotations
from slitherlink import Cell, Edge, Junction, Data
from generator.shapes import Rectangle
from generator.generate import Generate
from shared.enums import LoopStatus


class Game:
    data: Data
    loop: dict[Cell, LoopStatus]
    shape: Generate

    def __init__(self, shape: Generate):
        self.shape = shape
        self.data = {
            "cells": shape.cells,
            "junctions": shape.junctions,
            "edges": shape.edges,
        }
        self.loop = shape.loop

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

    def start(self) -> Game:
        [c.update() for c in self.data["cells"]]
        [j.update() for j in self.data["junctions"]]
        self.setup_variables()
        return self

    @staticmethod
    def generate_random(shape: str, size: tuple[int, int]) -> Game:
        match shape:
            case "square":
                gen = Rectangle.generate(size[0], size[1])
            case "hexagon":
                pass
            case _:
                pass

        game = Game(gen).start()
        gen.gen_loop()
        return game

    @staticmethod
    def generate_from_file(filename: str) -> Game:
        lines = []
        with open(filename) as file:
            lines = file.readlines()
        return Game.parse(lines)
