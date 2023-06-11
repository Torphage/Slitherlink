import math

from app.app import App
from app.edge_surface import EdgeSurface


class HexagonApp(App):
    size: int

    def __init__(self, game, window_size):
        super().__init__(game, window_size)

    def setup_variables(self, **kwargs):
        super().setup_variables(**kwargs)
        self.cell_widths = [
            self.size + s
            for s in list(range(self.size)) + list(range(self.size - 1))[::-1]
        ]
        self.junction_widths = [
            self.size + s
            for s in list(range(self.size)) + list(range(1, self.size + 1))[::-1]
        ]

        if self.stretch:
            x, y = 0, 1
            self.angle = "something"  # TODO calculate angle
        elif self.window_size[0] > self.window_size[1]:
            x, y = 1, 1
        else:
            x, y = 0, 0

        self.cell_size = {
            "x": (self.window_size[x] - self.padding[x]) / (2 * self.size - 1),
            "y": (self.window_size[y] - self.padding[y]) / (2 * self.size - 1),
        }

        self.offset = {
            "x": self.cell_size["x"],
            "y": self.cell_size["y"] * math.sqrt(3) / 2,
        }

        self.total_height = self.cell_size["y"] * (
            3 * math.tan(math.pi / 6) * (2 * self.size - 1) / 2 + math.tan(math.pi / 6)
        )
        self.upper_padding = (self.window_size[1] - self.total_height) / 2
        self.edge_length = self.cell_size["y"] * math.sqrt(3) / 3

    def num_offset(self, text):
        w, h = self.font.size(text)
        return (
            (self.cell_size["x"] - w) / 2,
            (self.cell_size["y"] - h) / 2,
        )

    def draw_cells(self):
        index = 0
        for width, y in zip(self.cell_widths, range(2 * self.size - 1)):
            left_padding = (self.window_size[0] - width * self.cell_size["x"]) / 2
            for x in range(width):
                con = self.game.shape.cells[index].constraint
                index += 1
                if con is None:
                    continue

                num_offset = self.num_offset(str(con))
                text = self.font.render(str(con), True, (0, 0, 0))
                self.screen.blit(
                    text,
                    self.add_padding(
                        (
                            x * self.offset["x"] + num_offset[0] + left_padding,
                            y * self.offset["y"] + num_offset[1] + self.upper_padding,
                        )
                    ),
                )

    def draw_junctions(self):
        for width, y in zip(self.junction_widths, list(range(2 * self.size))):
            left_padding = (self.window_size[0] - width * self.cell_size["x"]) / 2

            for x in range(width):
                x_coord = x * self.offset["x"] + left_padding
                y_coord = y * self.offset["y"] + self.upper_padding

                self.draw_point(
                    x_coord + self.cell_size["x"] / 2,
                    y_coord,
                )
                self.draw_point(
                    self.window_size[0] - x_coord - self.cell_size["x"] / 2,
                    self.window_size[1] - y_coord - self.edge_length / 2,
                )

    def draw_edges(self):
        buttons_edges = []
        edges = []

        index = 0
        for width, y in zip(self.junction_widths, list(range(2 * self.size))):
            left_padding = (self.window_size[0] - width * self.cell_size["x"]) / 2

            for x in range(width):
                junction = self.game.shape.junctions[index]

                x_pos = x * self.offset["x"] + self.padding[0] + left_padding
                y_pos = y * self.offset["y"] + self.padding[1] + self.upper_padding

                done = [False, False, False]
                for edge in junction.edges:
                    if edge in edges:
                        continue
                    if y != 0 and not done[0]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=90,
                            x_offset=x_pos + self.cell_size["x"] / 2,
                            y_offset=y_pos - self.edge_length,
                            length=self.edge_length,
                        )
                        done[0] = True
                    elif (y < self.size or x != 0) and not done[2]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=30,
                            x_offset=x_pos,
                            y_offset=y_pos,
                            length=self.edge_length,
                        )
                        done[2] = True
                    elif (y < self.size or x != width - 1) and not done[1]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=-30,
                            x_offset=x_pos + self.cell_size["x"] / 2,
                            y_offset=y_pos,
                            length=self.edge_length,
                        )
                        done[1] = True
                    else:
                        continue
                    edges.append(edge)
                    button.update(self.screen)
                    buttons_edges.append((button, edge))

                index += 1
            if y < self.size:
                index += width + 1
            else:
                index += width - 1

        self.buttons_edges = buttons_edges

        return super().draw_edges()

    def draw_solution(self):
        return super().draw_solution()
