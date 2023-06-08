from app.app import App
from app.edge_surface import EdgeSurface
import math


class HexagonApp(App):
    size: int

    def __init__(self, game, window_size):
        super().__init__(game, window_size)

    def setup_variables(self):
        self.cell_widths = [
            self.size + s
            for s in list(range(self.size)) + list(range(self.size - 1))[::-1]
        ]
        self.junction_widths = [
            self.size + s
            for s in list(range(self.size)) + [a + 1 for a in list(range(self.size))[::-1]]
        ]

        self.cell_size = {
            "x": (self.window_size[0] - self.padding[0]) / (2 * self.size - 1),
            "y": (self.window_size[1] - self.padding[1]) / (2 * self.size - 1),
        }
        self.offset = {
            "x": self.cell_size["x"],
            "y": self.cell_size["y"] * math.sqrt(3) / 2,
        }

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
                if con is not None:
                    num_offset = self.num_offset(str(con))
                    text = self.font.render(str(con), True, (0, 0, 0))
                    self.screen.blit(
                        text,
                        self.add_padding(
                            (
                                x * self.offset["x"] + num_offset[0] + left_padding,
                                y * self.offset["y"] + num_offset[1],
                            )
                        ),
                    )

                index += 1

    def draw_junctions(self):
        return super().draw_junctions()

    def draw_edges(self):
        buttons_edges = []
        edges = []

        index = 0
        indexes = []
        for width, y in zip(self.junction_widths, list(range(2 * self.size))):
            left_padding = (self.window_size[0] - width * self.cell_size["x"]) / 2

            for x in range(width):
                junction = self.game.shape.junctions[index]
                indexes.append(index)

                x_coord = x * self.offset["x"] + self.padding[0] + left_padding
                y_coord = y * self.offset["y"] + self.padding[1]

                done = [False, False, False]
                for edge in junction.edges:
                    if edge in edges:
                        continue
                    if y != 0 and not done[0]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=90,
                            x_offset=x_coord + self.cell_size["x"] / 2,
                            y_offset=y_coord - self.cell_size["y"] * math.tan(math.pi / 6),
                            length=self.cell_size["y"] * math.sqrt(3) / 3,
                        )
                        done[0] = True
                    elif (y < self.size or x != 0) and not done[2]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=30,
                            x_offset=x_coord,
                            y_offset=y_coord,
                            length=self.cell_size["y"] * math.sqrt(3) / 3,
                        )
                        done[2] = True
                    elif (y < self.size or x != width - 1) and not done[1]:
                        button = EdgeSurface(
                            edge=edge,
                            angle=-30,
                            x_offset=x_coord + self.cell_size["x"] / 2,
                            y_offset=y_coord,
                            length=self.cell_size["y"] * math.sqrt(3) / 3,
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

    # def draw_edge_common()

    def draw_solution(self):
        return super().draw_solution()
