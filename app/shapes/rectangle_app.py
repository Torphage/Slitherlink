import pygame
import time

from app.app import App
from app.edge_surface import EdgeSurface
from shared.slitherlink import Edge


class RectangleApp(App):
    size: tuple[int, int]

    def __init__(self, game, window_size):
        super().__init__(game, window_size)

    def setup_variables(self):
        w, h = self.w, self.h = self.size[0], self.size[1]

        cell_grid = [
            self.shape.cells[i : i + h] for i in range(0, len(self.shape.cells), w)
        ]
        self.cell_grid = list(map(list, zip(*cell_grid)))

        horizontal_edges = self.shape.edges_arr[: w * (h + 1)]
        vertical_edges = self.shape.edges_arr[w * (h + 1) :]
        self.horizontal_edges = [
            horizontal_edges[i : i + h] for i in range(0, len(horizontal_edges), w)
        ]
        self.vertical_edges = [
            vertical_edges[i : i + w + 1] for i in range(0, len(vertical_edges), w + 1)
        ]

        self.cell_size = {
            "x": self.window_size[0] / w,
            "y": self.window_size[1] / h,
        }

    def num_offset(self, text):
        w, h = self.font.size(text)
        return (
            (self.cell_size["x"] - w) / 2,
            (self.cell_size["y"] - h) / 2,
        )

    def draw_cells(self):
        for i in range(self.w):
            for j in range(self.h):
                con = self.cell_grid[i][j].constraint
                if con is not None:
                    offset = self.num_offset(str(con))
                    text = self.font.render(str(con), True, (0, 0, 0))
                    rect = pygame.Rect(
                        self.add_padding(
                            (
                                i * self.cell_size["x"] + offset[0],
                                j * self.cell_size["y"] + offset[1],
                            )
                        ),
                        text.get_size(),
                    )
                    self.render(text, rect)

    def draw_junctions(self):
        for i in range(self.w + 1):
            for j in range(self.h + 1):
                self.draw_point(
                    i * self.cell_size["x"],
                    j * self.cell_size["y"],
                )

    def draw_edges(self):
        if self.buttons_edges and self.pressed_button:
            self.pressed_button.update(edge=self.pressed_button.edge)

            for button, _ in self.buttons_edges:
                self.render(button.visual, button.visual_rect)
            self.pressed_button = None
            return

        if self.buttons_edges and not self.do_zoom:
            for button, _ in self.buttons_edges:
                self.render(button.visual, button.visual_rect)
            return

        buttons_edges = []

        # vertical edges
        for i in range(self.w + 1):
            for j in range(self.h):
                edge = self.vertical_edges[j][i]
                button = self.draw_edge(
                    90,
                    edge,
                    i * self.cell_size["x"],
                    j * self.cell_size["y"],
                    self.cell_size["y"],
                )
                buttons_edges.append((button, edge))

        # horizontal edges
        for i in range(self.w):
            for j in range(self.h + 1):
                edge = self.horizontal_edges[j][i]
                button = self.draw_edge(
                    0,
                    edge,
                    i * self.cell_size["x"],
                    j * self.cell_size["y"],
                    self.cell_size["x"],
                )
                buttons_edges.append((button, edge))

        self.buttons_edges = buttons_edges

    def draw_edge(self, angle, edge, x_offset, y_offset, length):
        return self.draw_edge_common(angle, edge, x_offset, y_offset, length)

    def draw_solution(self, angle, edge, x_offset, y_offset, length):
        if edge.should_be_selected():
            edge.update()
        return self.draw_edge_common(angle, edge, x_offset, y_offset, length)

    def draw_edge_common(self, angle, edge, x_offset, y_offset, length):
        surface = EdgeSurface(
            edge=edge,
            angle=angle,
            x_offset=x_offset + self.padding[0],
            y_offset=y_offset + self.padding[1],
            length=length,
        )
        (v, vr) = surface.update()
        self.render(v, vr)

        return surface
