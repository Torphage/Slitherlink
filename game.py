from __future__ import annotations
from generator.shapes import Rectangle
from generator.generate import Generate
import time
import pygame
from shared.enums import EdgeStatus


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

    def play(self):
        pygame.font.init()
        self.screen = pygame.display.set_mode((500, 600))
        self.base_update()
        run = True
        dic = {}
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ## if mouse is pressed get position of cursor ##
                    pos = pygame.mouse.get_pos()
                    ## check if cursor is on button ##
                    for b in dic:
                        if b[0].collidepoint(pos):
                            ## exit ##
                            self.update(b[1])
                            # b[1].update()
            if self.solved():
                print("You won!")
                return
                            
            self.screen.fill((255, 255, 255))
            dic = self.draw_solution()
            pygame.display.update()

    def get_cord(self, pos):
        dif = 500 / 9
        x = pos[0] // dif
        y = pos[1] // dif
        return (x, y)

    def draw_solution(self):
        cell_size = 500 / 9
        font1 = pygame.font.SysFont("helvetica", 40)
        n = self.shape.h
        horizontal_edges = self.shape.edges[:self.shape.w * (self.shape.h + 1)]
        vertical_edges = self.shape.edges[self.shape.w * (self.shape.h + 1):]
        grid = [self.shape.cells[i:i + n] for i in range(0, len(self.shape.cells), self.shape.w)]
        horizontal_edges = [horizontal_edges[i:i + n] for i in range(0, len(horizontal_edges), self.shape.w)]
        vertical_edges = [vertical_edges[i:i + n + 1] for i in range(0, len(vertical_edges), self.shape.w + 1)]
        # grid2 = [self.shape.edges[i:i + n + 1] for i in range(0, len(self.shape.edges), n+1)]
        
        grid = list(map(list, zip(*grid)))
        for i in range(self.shape.w):
            for j in range(self.shape.h):
                if grid[i][j].constraint != -1 and grid[i][j].constraint is not None:

                    # Fill grid with default numbers specified
                    text1 = font1.render(str(grid[i][j].constraint), True, (0, 0, 0))
                    self.screen.blit(text1, (i * cell_size + 17, j * cell_size + 4))
        # Draw the horizontal edges
        dic = []
        for i in range(self.shape.w):
            for j in range(self.shape.h + 1):

                # if grid[i][j].
                if horizontal_edges[j][i].is_selected():
                    thick = 5
                else:
                    thick = 1
                hitbox = pygame.Surface((cell_size, 11)).convert_alpha()
                hitbox.fill((255, 255, 255, 0))
                edge = pygame.Surface((cell_size + thick, thick))
                if horizontal_edges[j][i].status == EdgeStatus.MARKED:
                    edge.fill((225,225,225))
                b = self.screen.blit(hitbox, (i * cell_size, j * cell_size - 11 / 2))
                self.screen.blit(edge, (i * cell_size - thick / 2, j * cell_size - thick / 2))
                dic.append((b, horizontal_edges[j][i]))

        # draw the vertical edges
        for i in range(self.shape.w + 1):
            for j in range(self.shape.h):
                # if grid[i][j].
                if vertical_edges[j][i].is_selected():
                    thick = 5
                else:
                    thick = 1
                # if 
                hitbox = pygame.Surface((11, cell_size)).convert_alpha()
                hitbox.fill((255, 255, 255, 0))
                edge = pygame.Surface((thick, cell_size + thick))
                if vertical_edges[j][i].status == EdgeStatus.MARKED:
                    edge.fill((225,225,225))
                b = self.screen.blit(hitbox, (i * cell_size - 11 / 2, j * cell_size))
                self.screen.blit(edge, (i * cell_size - thick / 2, j * cell_size - thick / 2))
                dic.append((b, vertical_edges[j][i]))
        return dic

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
                print("Shape not implemented yet. Defaulting to rectangle")
                gen = Rectangle.generate(size[0], size[1])
            case _:
                print("Shape not implemented. Defaulting to rectangle")
                gen = Rectangle.generate(size[0], size[1])

        START = time.perf_counter()
        game = Game(gen).start()
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
