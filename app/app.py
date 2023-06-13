from abc import ABC, abstractmethod
import math
import pygame

from app.edge_surface import EdgeSurface


class App(ABC):
    def __init__(self, game, window_size: tuple[int, int]):
        self.shape = game.shape
        self.size = game.size
        self.window_size = window_size
        self.windowsize = window_size
        self.running = True
        self.buttons_edges: list[tuple] = []
        self.padding = (20, 30)
        self.game = game

    def run(self, **kwargs):
        self.start(**kwargs)
        drag = False
        offset_x, offset_y = 0, 0
        select = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    drag = True
                    mouse_x, mouse_y = event.pos
                    offset_x = self.rect.x - mouse_x
                    offset_y = self.rect.y - mouse_y
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    drag = False
                elif event.type == pygame.MOUSEMOTION and drag:
                    mouse_x, mouse_y = event.pos
                    self.rect.x = mouse_x + offset_x
                    self.rect.y = mouse_y + offset_y
                    select = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not select:
                        select = not select
                        continue
                    pos = pygame.mouse.get_pos()
                    real_pos = [pos[0] - self.rect.left, pos[1] - self.rect.top]
                    pressed = []
                    for surface, edge in self.buttons_edges:
                        if surface.hitbox_button.collidepoint(real_pos):
                            if surface.check_collision(real_pos):
                                pressed.append((surface, edge))
                    if pressed:
                        edge = EdgeSurface.get_closest_button(pressed, pos)
                        self.game.update(edge)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 or event.button == 5:
                        zoom = 1.1 if event.button == 4 else 0.9
                        mx, my = event.pos
                        left = mx + (self.rect.left - mx) * zoom
                        right = mx + (self.rect.right - mx) * zoom
                        top = my + (self.rect.top - my) * zoom
                        bottom = my + (self.rect.bottom - my) * zoom
                        self.rect = pygame.Rect(left, top, right - left, bottom - top)
                        self.window_size = (
                            self.rect.size[0] - 2 * self.padding[0],
                            self.rect.size[1] - 2 * self.padding[1],
                        )
                        self.zoom(stretch=self.stretch)

            # TODO Fix showing solved game
            # * the line below is needed when using draw_solution
            # * since the cells only update around the edge that
            # * you actually click.
            self.ratio = math.ceil(self.rect.height / self.windowsize[1])
            if self.game.solved():
                print("You won!")
                self.running = False

            self.screen.fill((200, 200, 200))
            self.draw()
            pygame.display.update()

    def zoom(self, **kwargs):
        self.font = pygame.font.SysFont(
            self.font_family,
            math.ceil(self.rect.height / self.windowsize[1] * self.font_size),
        )
        self.setup_variables(**kwargs)

    def start(self, font="helvetica", font_size=30, **kwargs):
        pygame.init()
        self.screen = pygame.display.set_mode(
            self.add_padding(self.add_padding(self.window_size))
        )
        self.font_family = font
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, font_size)
        self.rect = self.screen.get_rect(center=self.screen.get_rect().center)
        self.setup_variables(**kwargs)

    def add_padding(self, padding: tuple):
        return (padding[0] + self.padding[0], padding[1] + self.padding[1])

    def setup_variables(self, stretch=False):
        """Define useful instance variables here that are unique to the shape.
        These can then later be used by the shape in other functions.

        This function is called once, so if you need to update the value of
        these variables, do so outside this functions
        """
        self.stretch = stretch

    def draw(self):
        self.surface = pygame.transform.smoothscale(self.screen, self.rect.size)
        self.draw_cells()
        self.draw_junctions()
        self.draw_edges()
        # TODO Game slows down (a lot) when zooming in
        self.screen.blit(self.surface, self.rect)

    def draw_point(self, x, y, width=1):
        width = self.ratio + width
        s = pygame.Surface((2 * width, 2 * width))
        s.set_colorkey((0, 0, 0))
        s.set_alpha(255)
        pygame.draw.circle(
            s,
            (1, 1, 1, 255),
            (width, width),
            width,
        )
        self.surface.blit(s, (x + self.padding[0] - width, y + self.padding[1] - width))

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
