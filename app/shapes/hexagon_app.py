import pygame
from app.app import App
from shared.enums import EdgeStatus


class HexagonApp(App):
    def __init__(self, game, window_size):
        super().__init__(game, window_size)

    def get_cord(self, pos):
        pass

    def setup_variables(self):
        pass

    def draw_cells(self):
        return super().draw_cells()

    def draw_junctions(self):
        return super().draw_junctions()

    def draw_edges(self):
        return super().draw_edges()

    def draw_solution(self):
        return super().draw_solution()
