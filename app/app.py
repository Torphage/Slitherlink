from abc import ABC, abstractmethod
import math
import pygame

from app.edge_surface import EdgeSurface
from shared.slitherlink import Edge


class App(ABC):
    def __init__(self, game, window_size: tuple[int, int]):
        self.shape = game.shape
        self.size = game.size
        self.window_size = window_size
        self.og_window_size = window_size
        self.running = True
        self.buttons_edges: list[EdgeSurface] = []
        self.padding = (20, 30)
        self.game = game
        self.pressed_button = None

    def run(self, **kwargs):
        self.start(**kwargs)
        drag = False
        select = True
        og_offset = (0, 0)
        moves = (0, 0)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    drag = True
                    og_offset = self.rect.topleft
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    drag = False
                    moves = (0, 0)
                elif event.type == pygame.MOUSEMOTION and drag:
                    mouse_x, mouse_y = event.rel
                    moves = (moves[0] + mouse_x, moves[1] + mouse_y)
                    self.rect.topleft = (
                        og_offset[0] + moves[0],
                        og_offset[1] + moves[1],
                    )
                    select = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not select:
                        select = not select
                    else:
                        pos = pygame.mouse.get_pos()
                        self.handle_collision(pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 or event.button == 5:
                        if (self.zoom_level < 8 and event.button == 4) or (
                            self.zoom_level > 0.5 and event.button == 5
                        ):
                            self.zoom(event.button, event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z or event.key == pygame.K_x:
                        if (self.zoom_level < 8 and event.key == pygame.K_z) or (
                            self.zoom_level > 0.5 and event.key == pygame.K_x
                        ):
                            self.zoom(event.key, pygame.mouse.get_pos())

            self.ratio = math.ceil(self.rect.height / self.og_window_size[1])
            if self.game.solved():
                print("You won!")
                self.running = False

            self.screen.fill((200, 200, 200))

            # TODO Fix showing solved game
            self.draw()

            self.clock.tick(1000)
            self.fps_counter()
            pygame.display.update()

    def handle_collision(self, pos):
        real_pos = (
            pos[0] - self.rect.left,
            pos[1] - self.rect.top,
        )
        pressed = []
        for button in self.buttons_edges:
            if button.hitbox_button.collidepoint(real_pos):
                if button.check_collision(real_pos):
                    pressed.append(button)
        if pressed:
            button = EdgeSurface.get_closest_button(pressed, pos)
            self.pressed_button = button
            self.game.update(button.edge)
            return button.edge
        return None

    def zoom(self, button, pos):
        mx, my = pos

        zoom = 2 if (button == 4 or button == pygame.K_z) else 0.5
        self.zoom_level *= zoom

        left = mx + (self.rect.left - mx) * zoom
        right = mx + (self.rect.right - mx) * zoom
        top = my + (self.rect.top - my) * zoom
        bottom = my + (self.rect.bottom - my) * zoom
        width = right - left
        height = bottom - top

        self.rect = pygame.Rect(left, top, width, height)

        self.window_size = (
            self.rect.size[0] - 2 * self.padding[0],
            self.rect.size[1] - 2 * self.padding[1],
        )
        self.font = pygame.font.SysFont(
            self.font_family,
            math.ceil(self.rect.height / self.og_window_size[1] * self.font_size),
        )
        self.do_zoom = True
        self.setup_variables()

    def start(self, font="helvetica", font_size=30, stretch=False):
        pygame.init()
        self.screen = pygame.display.set_mode(
            self.add_padding(self.add_padding(self.window_size))
        )
        self.font_family = font
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, font_size)
        self.rect = self.screen.get_rect(center=self.screen.get_rect().center)
        self.stretch = stretch
        self.do_zoom = True
        self.zoom_level = 1
        self.setup_variables()
        self.surface = self.screen
        self.clock = pygame.time.Clock()

    def add_padding(self, padding: tuple[float, float]) -> tuple[float, float]:
        return (padding[0] + self.padding[0], padding[1] + self.padding[1])

    @abstractmethod
    def setup_variables(self):
        """Define useful instance variables here that are unique to the shape.
        These can then later be used by the shape in other functions.

        This function is called once, so if you need to update the value of
        these variables, do so outside this functions
        """
        return NotImplemented

    def draw(self):
        sr = self.screen.get_rect()
        r = self.rect

        if r.left > sr.width or r.top > sr.height or r.right < 0 or r.bottom < 0:
            return

        self.surface = self.screen.copy()
        self.draw_cells()
        self.draw_junctions()
        self.draw_edges()
        self.do_zoom = False

        self.screen.blit(
            self.surface,
            (max(r.left, 0), max(r.top, 0)),
        )

    def fps_counter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps, True, pygame.Color("RED"))
        self.screen.blit(fps_t, (0, 0))

    def render(self, source, rect):
        left, top = rect.topleft

        if self.rect.left < 0:
            left += self.rect.left

        if self.rect.top < 0:
            top += self.rect.top

        self.surface.blit(source, (left, top))

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
        rect = pygame.Rect(
            x + self.padding[0] - width, y + self.padding[1] - width, width, width
        )

        self.render(s, rect)
        return (s, rect)

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
