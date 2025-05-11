import pygame
import math

class ParabolicProjectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, healthy_group):
        super().__init__()
        self.image = pygame.image.load("assets/images/projectiles/cornet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))

        # Position de départ avec les décalages appliqués
        self.start_x, self.start_y = (start_pos[0] + 220, start_pos[1] + 120)
        self.rect = self.image.get_rect(center=(self.start_x, self.start_y))

        self.healthy_group = healthy_group
        self.speed = 5

        # ➤ Ligne d'origine du projectile en tenant compte du décalage
        self.line_index = (self.start_y - 160) // 100

        # ➤ Filtrer les ennemis sur la même ligne (±50 pixels de tolérance)
        self.target = next(
            (enemy for enemy in healthy_group if abs(enemy.rect.centery - (self.start_y + 60)) <= 50 and self.start_x - 100 < enemy.rect.x),
            None
        )

        if not self.target:
            self.kill()
            return

        # Coordonnées de la cible
        self.end_x = self.target.rect.centerx
        self.end_y = self.target.rect.centery

        # Coordonnées du sommet de la parabole
        self.peak_height = -300
        self.control_x = (self.start_x + self.end_x) / 2
        self.control_y = min(self.start_y, self.end_y) + self.peak_height

        self.total_time = 60
        self.timer = 0

    def update(self, *args):
        if not self.target or not self.target.alive():
            self.kill()
            return

        self.timer += 1
        t = self.timer / self.total_time
        if t > 1.0:
            self.kill()
            return

        # Courbe de Bézier quadratique
        x = (1 - t)**2 * self.start_x + 2 * (1 - t) * t * self.control_x + t**2 * self.end_x
        y = (1 - t)**2 * self.start_y + 2 * (1 - t) * t * self.control_y + t**2 * self.end_y
        self.rect.center = (x, y)

        if pygame.sprite.collide_rect(self, self.target):
            self.target.take_damage(100)
            self.kill()


class FriteProjectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, healthy_group):
        super().__init__()
        self.image = pygame.image.load("assets/images/projectiles/frite.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.start_x = start_pos[0] + 200
        self.start_y = start_pos[1] + 150
        self.rect = self.image.get_rect(center=(self.start_x, self.start_y))

        self.x = float(self.rect.x)
        self.speed = 8
        self.healthy_group = healthy_group
        self.damage = 50

        # ➤ Calcul de la ligne d'origine
        self.line_index = (self.start_y - 160) // 100

        # ➤ Vérifie s'il y a un ennemi sur la même ligne
        self.has_target = any(
            abs(enemy.rect.centery - self.rect.centery) <= 50
            for enemy in healthy_group
        )

        if not self.has_target:
            self.kill()  # Tue le projectile dès le départ s’il n’y a personne sur sa ligne

    def update(self, *args):
        if not self.has_target:
            self.kill()

        self.x += self.speed
        self.rect.x = int(self.x)

        if self.rect.left > 1280:
            self.kill()
            

        for enemy in self.healthy_group:
            if abs(enemy.rect.centery - self.rect.centery) <= 50:
                if pygame.sprite.collide_rect(self, enemy):
                    enemy.take_damage(self.damage)
                    self.kill()
                    break