# entities/mcdo_unit.py

import pygame
from entities.happymeal import HappyMeal
from entities.projectile import *
class McDoUnit(pygame.sprite.Sprite):
    def __init__(self, unit_name, image, cost, row, col, health=100, cooldown=5000):
        super().__init__()
        self.unit_name = unit_name
        self.health = health
        self.cooldown = cooldown
        self.image = image
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.cost = cost
        self.row = row
        self.col = col
        self.rect = self.image.get_rect()
        self.x = col * 100  # à ajuster si besoin
        self.y = row * 100

    def update(self):
        # Cette méthode peut être utilisée pour mettre à jour les unités (mouvement, animations, etc.)
        pass
    def take_damage(self, amount):
        self.health -= amount
        print(self.health)
        if self.health <= 0:
            self.kill()  # Retire du sprite group si utilisé

class Fontaine(McDoUnit):
    def __init__(self, row, col):
        image = pygame.image.load("assets/images/mcdo/foutain.png").convert_alpha()
        
        super().__init__("Fontaine", image, cost=50, row=row, col=col)
        self.last_produce_time = pygame.time.get_ticks()
        self.produce_interval = 10000  # 5 sec
    def update(self, happy_meal_group, img):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_produce_time >= self.produce_interval:
            happy_meal = HappyMeal(img, (self.x+250, self.y+100), stop=self.row*100)  # léger décalage
            happy_meal_group.add(happy_meal)
            self.last_produce_time = current_time

class Nugget(McDoUnit):
    def __init__(self, row, col):
        image = pygame.image.load("assets/images/mcdo/nugget.jpg").convert_alpha()
        super().__init__("Nugget", image, cost=100, row=row, col=col, health=500, cooldown=10000)

class LanceurCornet(McDoUnit):
    def __init__(self, row, col):
        image = pygame.image.load("assets/images/mcdo/lanceur.jpg").convert_alpha()
        super().__init__("LanceurCornet", image, cost=125, row=row, col=col, health=200, cooldown=7000)
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_interval = 3000

    def update(self, projectile_group, healthy_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            projectile = ParabolicProjectile((self.x + 60, self.y + 30), healthy_group)
            projectile_group.add(projectile)
            self.last_shot_time = now

class LanceurFrite(McDoUnit):
    def __init__(self, row, col):
        image = pygame.image.load("assets/images/mcdo/lanceur_frite.png").convert_alpha()
        super().__init__("LanceurFrite", image, cost=75, row=row, col=col, health=250, cooldown=6000)
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_interval = 1500

    def update(self, projectile_group, healthy_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            projectile = FriteProjectile((self.x + 100, self.y + 50), healthy_group)
            projectile_group.add(projectile)
            self.last_shot_time = now
