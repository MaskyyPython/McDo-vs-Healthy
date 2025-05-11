# core/grid.py

import pygame
from config import CELL_SIZE, COLUMNS, LANES, HEIGHT, WIDTH
from entities.mcdo_unit import Fontaine, Nugget

class Grid:
    def __init__(self):
        self.columns = COLUMNS
        self.rows = LANES
        self.cell_size = CELL_SIZE

        # Calcul du décalage vertical pour centrer la grille
        self.y_offset = (HEIGHT - (self.rows * self.cell_size)) // 2 + 50
        self.x_offset = (WIDTH - (self.columns * self.cell_size)) // 2 + 50

        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.columns):
                x = self.x_offset + col * self.cell_size
                y = self.y_offset + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                # pygame.draw.rect(screen, (50, 50, 50), rect, 1) # Pour dessiner la grille

                unit = self.grid[row][col]
                if unit:
                    screen.blit(unit.image, (x, y))

    def get_cell_from_pos(self, pos):
        x, y = pos
        col = (x - self.x_offset) // self.cell_size
        row = (y - self.y_offset) // self.cell_size
        if 0 <= col < self.columns and 0 <= row < self.rows:
            return int(row), int(col)
        return None

    def place_unit(self, row, col, unit_instance):
        if self.grid[row][col] is None:
            self.grid[row][col] = unit_instance
            return True
        return False
    def get_unit(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return self.grid[row][col]
        return None