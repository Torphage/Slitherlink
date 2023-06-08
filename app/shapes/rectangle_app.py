import pygame
from app.app import App
from app.edge_surface import EdgeSurface


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

        horizontal_edges = self.shape.edges[: w * (h + 1)]
        vertical_edges = self.shape.edges[w * (h + 1) :]
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

        # # * modifiable values
        # self.line_properties = {

        # }

        # self.num_offset = {"x": 17, "y": 4}

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
                    self.screen.blit(
                        text,
                        self.add_padding(
                            (
                                i * self.cell_size["x"] + offset[0],
                                j * self.cell_size["y"] + offset[1],
                            )
                        ),
                    )

    def draw_junctions(self):
        return []

    def draw_edges(self):
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
                )
                buttons_edges.append((button, edge))

        self.buttons_edges = buttons_edges

    def draw_edge(self, angle, edge, x_offset, y_offset):
        return self.draw_edge_common(angle, edge, x_offset, y_offset)

    def draw_solution(self, angle, edge, x_offset, y_offset):
        if edge.should_be_selected():
            edge.update()
        return self.draw_edge_common(angle, edge, x_offset, y_offset)

    def draw_edge_common(self, angle, edge, x_offset, y_offset):
        surface = EdgeSurface(
            edge=edge,
            angle=angle,
            x_offset=x_offset + self.padding[0],
            y_offset=y_offset + self.padding[1],
            length=self.cell_size["x"],
        )
        surface.update(self.screen)
        return surface


def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    return surf.blit(rotated_image, new_rect)
