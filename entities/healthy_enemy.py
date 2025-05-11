# entities/healthy_enemy.py

import pygame
import random
from config import WIDTH, LANES

class Healthy(pygame.sprite.Sprite):
    def __init__(self, image, health=100):
        super().__init__()
        self.image = pygame.transform.scale(image, (64 * 1.5, 64 * 1.5))
        self.rect = self.image.get_rect()
        self.health = health
        lane = random.randint(0, LANES - 1)
        self.rect.x = WIDTH
        self.rect.y = 160 + lane * 100
        self.speed = 1
        self.damage = 20  # dégâts infligés par frame
        self.attack_delay = 500  # délai entre les attaques en ms
        self.last_attack_time = pygame.time.get_ticks()

    def update(self, grid):
        col = (self.rect.centerx - grid.x_offset) // grid.cell_size
        row = (self.rect.centery - grid.y_offset) // grid.cell_size

        if 0 <= row < grid.rows and 0 <= col < grid.columns:
            unit = grid.get_unit(row, col)
            if unit:
                # Attaque s’il y a une unité McDo
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= self.attack_delay:
                    unit.take_damage(self.damage)
                    self.last_attack_time = current_time

                    if unit.health <= 0:
                        grid.grid[row][col] = None  # Suppression dans la grille
                        unit.kill()  # Suppression du groupe de sprites

            else:
                self.rect.x -= self.speed  # Continue d’avancer s’il n’y a pas d’unité
        else:
            self.rect.x -= self.speed  # Continue d’avancer si en dehors de la grille
        if self.rect.right < 200:
            self.kill() 
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()