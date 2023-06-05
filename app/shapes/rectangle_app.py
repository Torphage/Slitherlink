import pygame
from app.app import App
from shared.enums import EdgeStatus


class RectangleApp(App):
    def __init__(self, game, window_size):
        super().__init__(game, window_size)

    def get_cord(self, pos):
        x = pos[0] // (self.window_size / self.w)
        y = pos[1] // (self.window_size / self.h)
        return (x, y)

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
                    True,
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
                    False,
                    edge,
                    i * self.cell_size["x"],
                    j * self.cell_size["y"],
                )
                buttons_edges.append((button, edge))

        self.buttons_edges = buttons_edges

    def draw_edge(self, is_vertical, edge, x_offset, y_offset):
        if edge.is_selected():
            thick = 5
        else:
            thick = 1
        return self.draw_common_edge(is_vertical, edge, x_offset, y_offset, thick)

    def draw_solution(self, is_vertical, edge, x_offset, y_offset):
        if edge.should_be_selected():
            thick = 5
            edge.update()
        else:
            thick = 1
        return self.draw_common_edge(is_vertical, edge, x_offset, y_offset, thick)

    def draw_common_edge(self, is_vertical, edge, x_offset, y_offset, thick):
        if is_vertical:
            edge_dim = (thick, self.cell_size["y"] + thick)
            hitbox_dim = (11, self.cell_size["y"])
            button_coord = (x_offset - 11 / 2, y_offset)
        else:
            edge_dim = (self.cell_size["x"] + thick, thick)
            hitbox_dim = (self.cell_size["x"], 11)
            button_coord = (x_offset, y_offset - 11 / 2)

        edge_surface = pygame.Surface(edge_dim)
        hitbox = pygame.Surface(hitbox_dim).convert_alpha()

        hitbox.fill((255, 255, 255, 0))
        if edge.status == EdgeStatus.MARKED:
            edge_surface.fill((225, 225, 225))

        button = self.screen.blit(hitbox, self.add_padding(button_coord))
        self.screen.blit(
            edge_surface, self.add_padding((x_offset - thick / 2, y_offset - thick / 2))
        )
        return button
