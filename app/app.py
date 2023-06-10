from abc import ABC, abstractmethod
import pygame
from .edge_surface import EdgeSurface


class App(ABC):
    def __init__(self, game, window_size):
        self.shape = game.shape
        self.size = game.size
        self.window_size = window_size
        self.running = True
        self.buttons_edges: list[tuple] = []
        self.padding = (20, 30)
        self.game = game

    def run(self, **kwargs):
        self.start(**kwargs)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    pressed = []
                    for surface, edge in self.buttons_edges:
                        if surface.hitbox_button.collidepoint(pos):
                            if surface.check_collision(pos):
                                pressed.append((surface, edge))
                    if pressed:
                        (button, edge) = EdgeSurface.get_closest_button(pressed, pos)
                        self.game.update(edge)

            # TODO Fix below
            # * the line below is needed when using draw_solution
            # * since the cells only update around the edge that
            # * you actually click.
            # self.game.base_update()
            if self.game.solved():
                print("You won!")
                self.running = False

            self.screen.fill((255, 255, 255))
            self.draw()
            pygame.display.update()

    def start(self, font="helvetica", font_size=30):
        pygame.init()
        self.screen = pygame.display.set_mode(
            self.add_padding(self.add_padding(self.window_size))
        )
        self.font = pygame.font.SysFont(font, font_size)
        self.setup_variables()

    def add_padding(self, padding: tuple):
        return (padding[0] + self.padding[0], padding[1] + self.padding[1])

    @abstractmethod
    def setup_variables(self):
        """Define useful instance variables here that are unique to the shape.
        These can then later be used by the shape in other functions.

        This function is called once, so if you need to update the value of these variables,
        do so outside this functions
        """
        return NotImplemented

    def draw(self):
        self.draw_cells()
        self.draw_junctions()
        self.draw_edges()

    def draw_point(self, x, y):
        pygame.draw.circle(
            self.screen,
            (0, 0, 0),
            (x + self.padding[0], y + self.padding[1]),
            7,
        )

    @abstractmethod
    def draw_cells(self):
        return NotImplemented

    @abstractmethod
    def draw_junctions(self):
        return NotImplemented

    @abstractmethod
    def draw_edges(self):
        return NotImplemented

    @abstractmethod
    def draw_solution(self):
        return NotImplemented
