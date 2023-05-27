from __future__ import annotations
from generator.shapes import Rectangle
from generator.generate import Generate


class Game:
    shape: Generate

    def __init__(self, shape: Generate):
        self.shape = shape

    def populate_numbers(self):
        for cell in self.shape.cells:
            cell.loop_status = self.shape.loop[cell]

        for cell in self.shape.cells:
            cell.set_contraint()

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
        for edge in self.shape.edges:
            edge.setup_variables(
                self.shape.cells, self.shape.junctions, self.shape.edges
            )
        for cell in self.shape.cells:
            cell.setup_variables(self.shape.cells, self.shape.junctions)
        for junction in self.shape.junctions:
            junction.setup_variables(self.shape.cells)

    def update(self, index: int):
        edge = self.shape.edges[index]
        edge.update()
        for c in edge.cells:
            c.update()
        for j in edge.junctions:
            j.update()

    @staticmethod
    def parse(arr: list[str]) -> Game:
        return Game()

    def start(self) -> Game:
        [c.update() for c in self.shape.cells]
        [j.update() for j in self.shape.junctions]
        self.setup_variables()
        return self

    @staticmethod
    def generate_random_shape(shape: str, size: tuple[int, int]) -> Game:
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
