# entities/happymeal.py

import pygame
import random
from config import WIDTH, HEIGHT

class HappyMeal(pygame.sprite.Sprite):
    def __init__(self, image, pos, stop=HEIGHT):
        super().__init__()
        self.image = pygame.transform.scale(image, (60, 60))
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 2  # vitesse de descente (si flottant)
        self.collected = False
        self.stop = stop

    def update(self):
        if not self.collected:
            if self.stop == HEIGHT:
                if self.rect.y <= self.stop-80:
                    self.rect.y += self.speed  # descend doucement (optionnel)
            else:
                if self.rect.y <= self.stop+200:
                    self.rect.y += self.speed

    def collect(self):
        self.collected = True
        
        # Tu peux ajouter une animation ou un son ici si tu veux
