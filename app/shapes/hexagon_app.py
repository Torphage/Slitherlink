import math

from app.app import App
from app.edge_surface import EdgeSurface


class HexagonApp(App):
    size: int

    def __init__(self, game, window_size):
        super().__init__(game, window_size)

    def setup_variables(self, **kwargs):
        super().setup_variables(**kwargs)
        self.cell_counts = [
            self.size + s
            for s in list(range(self.size)) + list(range(self.size - 1))[::-1]
        ]
        self.junction_counts = [
            self.size + s
            for s in list(range(self.size)) + list(range(1, self.size + 1))[::-1]
        ]

        game_size = self.game_size()

        self.cell_width = (1 * game_size[0]) / (2 * self.size - 1)
        self.calc_angle()

        self.edge_length = self.cell_width / (2 * math.cos(self.rad))
        self.angled_height = self.edge_length * math.sin(self.rad)

        self.total_height = 2 * self.size * self.angled_height + self.edge_length * (
            2 * self.size - 1
        )

        self.upper_padding = (game_size[1] - self.total_height) / 2

        self.offset = {
            "x": self.cell_width,
            "y": self.cell_width * math.tan(self.rad) / 2 + self.edge_length,
        }

    def game_size(self):
        if self.stretch:
            return self.window_size

        if self.window_size[0] > self.window_size[1]:
            return (self.window_size[1], self.window_size[1])
        else:
            return (self.window_size[0], self.window_size[0])

    def calc_angle(self):
        if self.stretch:
            c, m, s = self.cell_width, self.window_size[1], self.size
            # https://www.wolframalpha.com/input?i=m+%3D+%282*s+-+1%29+%28c%2F2%29+*+sec%28a%29+%2B+%282*s%29+%28c%2F2%29+*+tan%28a%29%2C+a%3D%3F
            self.rad = 2 * math.atan(
                (math.sqrt((c**2) * (4 * s - 1) + 4 * (m**2)) - 2 * c * s)
                / (c * (2 * s - 1) + 2 * m)
            )
            self.angle = self.rad * 180 / math.pi
        else:
            self.rad = math.pi / 6
            self.angle = 30

    def num_offset(self, text):
        w, h = self.font.size(text)
        return (
            (self.cell_width - w) / 2,
            (self.cell_width * math.tan(self.rad) + self.edge_length - h) / 2,
        )

    def draw_cells(self):
        index = 0
        for width, y in zip(self.cell_counts, range(2 * self.size - 1)):
            left_padding = (self.window_size[0] - width * self.cell_width) / 2
            for x in range(width):
                con = self.game.shape.cells[index].constraint
                index += 1
                if con is None:
                    continue

                num_offset = self.num_offset(str(con))
                text = self.font.render(str(con), True, (0, 0, 0))
                self.surface.blit(
                    text,
                    self.add_padding(
                        (
                            x * self.offset["x"] + num_offset[0] + left_padding,
                            y * self.offset["y"] + num_offset[1] + self.upper_padding,
                        )
                    ),
                )

    def draw_junctions(self):
        for width, y in zip(self.junction_counts, list(range(2 * self.size))):
            left_padding = (self.window_size[0] - width * self.cell_width) / 2

            for x in range(width):
                x_coord = x * self.offset["x"] + left_padding
                y_coord = y * self.offset["y"] + self.upper_padding

                x2_coord = (width - x) * self.offset["x"] + left_padding
                y2_coord = (2 * self.size - 1 - y) * self.offset[
                    "y"
                ] + self.upper_padding

                self.draw_point(
                    x_coord + self.cell_width / 2,
                    y_coord,
                )

                self.draw_point(
                    x2_coord - self.cell_width / 2, y2_coord + self.angled_height
                )

                # if y != 0:
                #     self.draw_point(
                #         x_coord + self.cell_width / 2,
                #         y_coord - self.edge_length,
                #     )
                # if x != 0 and y == 2 * self.size - 1:
                #     self.draw_point(
                #         x_coord,
                #         y_coord + self.angled_height,
                #     )

    def draw_edges(self):
        # if self.buttons_edges:
        #     for button, _ in self.buttons_edges:
        #         button.draw(self.surface)
        #     return self.buttons_edges
        buttons_edges = []
        edges = []

        if self.angle < 0:
            opposite = self.angled_height
        else:
            opposite = 0

        index = 0
        for width, y in zip(self.junction_counts, list(range(2 * self.size))):
            left_padding = (self.window_size[0] - width * self.cell_width) / 2

            for x in range(width):
                junction = self.game.shape.junctions[index]

                x_pos = x * self.offset["x"] + left_padding
                y_pos = y * self.offset["y"] + self.upper_padding

                done = [False, False, False]
                for edge in junction.edges:
                    if edge in edges:
                        continue
                    if y != 0 and not done[0]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=90,
                            x_offset=x_pos + self.cell_width / 2,
                            y_offset=y_pos - self.edge_length,
                            length=self.edge_length,
                            padding=self.padding,
                            ratio=self.ratio,
                        )
                        done[0] = True
                    elif (y < self.size or x != 0) and not done[1]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=self.angle,
                            x_offset=x_pos,
                            y_offset=y_pos + opposite,
                            length=self.edge_length,
                            padding=self.padding,
                            ratio=self.ratio,
                        )
                        done[1] = True
                    elif (y < self.size or x != width - 1) and not done[2]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=-self.angle,
                            x_offset=x_pos + self.cell_width / 2,
                            y_offset=y_pos + opposite,
                            length=self.edge_length,
                            padding=self.padding,
                            ratio=self.ratio,
                        )
                        done[2] = True
                    else:
                        raise Exception("Invalid edge found")
                    edges.append(edge)
                    button.update(self.surface)
                    buttons_edges.append((button, edge))

                index += 1
            if y < self.size:
                index += width + 1
            else:
                index += width - 1

        self.buttons_edges = buttons_edges

    def draw_solution(self):
        return super().draw_solution()
