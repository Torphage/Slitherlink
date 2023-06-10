from shared.enums import EdgeStatus
import pygame
import math
from operator import add
from slitherlink import Edge


class EdgeSurface:
    hitbox: pygame.Surface
    visual: pygame.Surface

    def __init__(
        self,
        edge: Edge,
        angle: float,
        x_offset: int,
        y_offset: int,
        length: int,
    ):
        self.edge = edge
        self.angle = angle
        self.x_offset = x_offset
        self.y_offset = y_offset

        pass
        self.pre_update()

        hitbox_dim = (length, self.hitbox_thick)
        self.hitbox = pygame.Surface(hitbox_dim, pygame.SRCALPHA).convert_alpha()
        self.hitbox_hidden = self.hitbox.copy()

        visual_dim = (length, self.thick)
        self.visual = pygame.Surface(visual_dim, pygame.SRCALPHA).convert_alpha()
        self.hitbox.fill((255, 255, 255, 0))
        self.hitbox_hidden.fill((255, 255, 255, 255))
        self.visual.fill(self.color)

    def pre_update(self):
        match self.edge.status:
            case EdgeStatus.MARKED:
                self.color = (0, 0, 0, 15)
                self.thick = 2
            case EdgeStatus.EMPTY:
                self.color = (0, 0, 0, 160)
                self.thick = 2
            case EdgeStatus.SELECTED:
                self.color = (0, 0, 0)
                self.thick = 6
        self.hitbox_thick = 17

    def update(
        self,
        surface: pygame.Surface | None = None,
        angle: float | None = None,
        rotate: float | None = None,
        move_relative: tuple[int, int] | None = None,
        move_absolute: tuple[int, int] | None = None,
    ):
        self.pre_update()

        if angle:
            self.angle = angle
        if rotate:
            self.angle += rotate

        self.rotate(self.angle)

        rad = math.pi * self.angle / 180
        self.hitbox_pos = (
            self.x_offset - sign(math.sin(rad)) * self.hitbox_thick / 2,
            self.y_offset - sign(math.cos(rad)) * self.hitbox_thick / 2,
        )
        self.visual_pos = (
            self.x_offset - sign(math.sin(rad)) * self.thick / 2,
            self.y_offset - sign(math.cos(rad)) * self.thick / 2,
        )
        if move_absolute:
            self.hitbox_pos = move_absolute
            self.visual_pos = move_absolute
        if move_relative:
            self.hitbox_pos = tuple(map(add, self.hitbox_pos, move_relative))
            self.visual_pos = tuple(map(add, self.visual_pos, move_relative))
        if surface:
            self.draw(surface)

    def rotate(self, angle: float):
        self.hitbox = pygame.transform.rotate(self.hitbox, angle)
        self.hitbox_hidden = pygame.transform.rotate(self.hitbox_hidden, angle)
        self.visual = pygame.transform.rotate(self.visual, angle)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.visual, self.visual_pos)
        self.mask = pygame.mask.from_surface(self.hitbox_hidden)
        self.hitbox_button = surface.blit(self.hitbox, self.hitbox_pos)

    def check_collision(self, pos: tuple[int, int]) -> int:
        return self.mask.get_at(
            (pos[0] - self.hitbox_pos[0], pos[1] - self.hitbox_pos[1])
        )

    @staticmethod
    def get_closest_button(pressed: list, pos: tuple[int, int]):
        if len(pressed) == 1:
            return pressed[0]

        distances = []
        for surface, edge in pressed:
            surface_pos = surface.hitbox_button.center
            distances.append(
                math.sqrt((pos[0] - surface_pos[0]) ** 2 + (pos[1] - surface_pos[1]) ** 2),
            )
        min_index = distances.index(min(distances))
        return pressed[min_index]


def sign(x):
    return x if x >= 0 else -x
