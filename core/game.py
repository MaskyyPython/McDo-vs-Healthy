# core/game.py
import pygame
import random
from core.grid import Grid
from entities.mcdo_unit import *
from entities.happymeal import HappyMeal
from entities.healthy_enemy import Healthy  # Ajoute d'autres unités ici

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.grid = Grid()
        self.happymeal_points = 200
        self.happy_meal_group = pygame.sprite.Group()
        self.mcdo_unit_group = pygame.sprite.Group()  # déjà ajouté
        self.healthy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.last_sky_spawn_time = pygame.time.get_ticks()
        self.sky_spawn_interval = 5000  # 10 sec
        self.happy_meal_image = pygame.image.load("assets/images/meal.png").convert_alpha()

        # Dictionnaire des unités disponibles et leurs coûts
        """
        self.mcdo_units = {
            "Fontaine": {"class": Fontaine, "cost": 25},
            "Nugget": {"class": Nugget, "cost": 50},
            # Ajoute d'autres unités ici…
        }
        """
        self.mcdo_units = {}

        for cls in McDoUnit.__subclasses__():
            instance = cls(0, 0)
            self.mcdo_units[instance.unit_name] = {"class" : cls, "cost": instance.cost}

    def try_place_unit(self, row, col, unit_type):
        if unit_type in self.mcdo_units:
            unit_info = self.mcdo_units[unit_type]
            if self.happymeal_points >= unit_info["cost"]:
                unit_instance = unit_info["class"](row, col)
                placed = self.grid.place_unit(row, col, unit_instance)
                if placed:
                    self.happymeal_points -= unit_info["cost"]
                    self.mcdo_unit_group.add(unit_instance)
                    print(self.mcdo_unit_group)
                    print(f"{unit_type} placé. Points restants : {self.happymeal_points}")
                    return True
        return False

    def update(self):
        current_time = pygame.time.get_ticks()

        # Apparition des happy meals du ciel
        if current_time - self.last_sky_spawn_time > self.sky_spawn_interval:
            x = random.randint(self.grid.x_offset, self.grid.x_offset + self.grid.columns * self.grid.cell_size - 64)
            happy_meal = HappyMeal(self.happy_meal_image, (x, 0))
            self.happy_meal_group.add(happy_meal)
            self.last_sky_spawn_time = current_time

        # Mise à jour des unités
        for row in self.grid.grid:
            for unit in row:
                if isinstance(unit, Fontaine):
                    unit.update(self.happy_meal_group, self.happy_meal_image)
                if isinstance(unit, LanceurCornet):
                    unit.update(self.projectile_group, self.healthy_group)
                if isinstance(unit, LanceurFrite):
                    unit.update(self.projectile_group, self.healthy_group)
    
    def spawn_healthy(self, image):
        new_healthy = Healthy(image)
        self.healthy_group.add(new_healthy)

    def draw(self, bg):
        self.screen.blit(bg, (120, 00)) 
        #self.screen.fill((0, 0, 0))
        self.grid.draw(self.screen)
        self.happy_meal_group.draw(self.screen)
        
