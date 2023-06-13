from __future__ import annotations
import time

from app.shapes import RectangleApp, HexagonApp
from generator.shapes import Rectangle, Hexagon
from generator.generator import Generator


class Game:
    shape: Generator

    def __init__(self, shape: Generator, size: int | tuple[int, int]):
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

    # Setup the grid

    def setup_variables(self):
        t = time.perf_counter()
        for edge in self.shape.edges:
            edge.setup_variables(self.shape.cells, self.shape.junctions)
        print(f"The setup of non-edges took {round(time.perf_counter() - t,3)}s")
        for cell in self.shape.cells:
            cell.setup_variables()
        for junction in self.shape.junctions:
            junction.setup_variables()

    # Update the grid

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

    def play(self, dim, **kwargs):
        match self.shape.__class__.__name__:
            case "Rectangle":
                app = RectangleApp(self, dim)
            case "Hexagon":
                app = HexagonApp(self, dim)
            case _:
                print("Shape not implemented. Defaulting to rectangle")
                app = RectangleApp(self, dim)
        app.run(**kwargs)

    def start(self) -> Game:
        self.setup_variables()
        return self

    @staticmethod
    def generate_random_shape(
        shape: str, size1: int = 0, size2: tuple[int, int] = (0, 0)
    ) -> Game:
        match shape:
            case "square":
                size = size2
                gen = Rectangle.generate(size)
            case "hexagon":
                size = size1
                gen = Hexagon.generate(size)
            case _:
                print("Shape not implemented. Defaulting to rectangle")
                size = size2
                gen = Rectangle.generate(size)

        START = time.perf_counter()
        game = Game(gen, size).start()
        print("Setup completed!")
        SETUP = time.perf_counter()
        print(f"Setup took {round(SETUP - START,3)}s")
        print("Starting algorithm..")
        gen.gen_loop()
        print(f"Shape generation took {round(time.perf_counter() - SETUP,3)}s")
        return game
