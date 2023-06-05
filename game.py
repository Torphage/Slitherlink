from __future__ import annotations
from generator.shapes import Rectangle
from generator.generate import Generate
from app.shapes import RectangleApp
import time


class Game:
    shape: Generate

    def __init__(self, shape: Generate, size: tuple[int, int]):
        self.shape = shape
        self.size = size

    def populate_numbers(self):
        for cell in self.shape.cells:
            cell.loop_status = self.shape.loop[cell]

        for cell in self.shape.cells:
            cell.set_contraint()
            cell.update()

    def set_puzzle(self):
        pass

    # Check solution

    def solved(self) -> bool:
        return self.solved_cells() and self.valid_junctions()

    def solved_cells(self) -> bool:
        return all([c.is_solved() for c in self.shape.cells])

    def valid_junctions(self) -> bool:
        return all([j.is_valid() for j in self.shape.junctions])

    # Update the grid

    def setup_variables(self):
        t = time.perf_counter()
        for edge in self.shape.edges:
            edge.setup_variables(
                self.shape.cells, self.shape.junctions, self.shape.edges
            )
        print(f"Edges took the following amount to setup {round(time.perf_counter() - t,3)}s")
        for cell in self.shape.cells:
            cell.setup_variables()
        for junction in self.shape.junctions:
            junction.setup_variables()

    def base_update(self):
        for c in self.shape.cells:
            c.update()
        for j in self.shape.junctions:
            j.update()

    def update(self, edge):
        edge.update()
        for c in edge.cells:
            c.update()
        for j in edge.junctions:
            j.update()

    def play(self, dim):
        match self.shape.__class__.__name__:
            case "Rectangle":
                app = RectangleApp(self, dim)
            case _:
                print("Shape not implemented. Defaulting to rectangle")
                app = RectangleApp(self, dim)
        app.run()

    @staticmethod
    def parse(arr: list[str]) -> Game:
        return Game()

    def start(self) -> Game:
        self.setup_variables()
        return self

    @staticmethod
    def generate_random_shape(shape: str, size: tuple[int, int]) -> Game:
        match shape:
            case "square":
                gen = Rectangle.generate(size[0], size[1])
            case "hexagon":
                print("Shape not implemented yet. Defaulting to rectangle")
                gen = Rectangle.generate(size[0], size[1])
            case _:
                print("Shape not implemented. Defaulting to rectangle")
                gen = Rectangle.generate(size[0], size[1])

        START = time.perf_counter()
        game = Game(gen, size).start()
        print("Setup completed!")
        SETUP = time.perf_counter()
        print(f"Setup took {round(SETUP - START,3)}s")
        print("Starting algorithm..")
        gen.gen_loop()
        print(f"Shape generation took {round(time.perf_counter() - SETUP,3)}s")
        return game

    @staticmethod
    def generate_from_file(filename: str) -> Game:
        lines = []
        with open(filename) as file:
            lines = file.readlines()
        return Game.parse(lines)
