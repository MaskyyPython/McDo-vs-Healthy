import pygame

class HUD:
    def __init__(self, unit_buttons, width, height, font):
        self.unit_buttons = unit_buttons  # Liste d'objets UnitButton
        self.width = width
        self.height = height
        self.bg_color = (63, 33, 7)
        self.font = font  # Ajout du paramètre font pour le texte global

    def draw(self, screen, happymeal_points):
        # Dessin du fond du HUD
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, self.width + 20, self.height))
        pygame.draw.rect(screen, self.bg_color, (10, 0, self.width, self.height))

        happy_meal_image = pygame.image.load("assets/images/meal.png").convert_alpha()
        happy_meal_image = pygame.transform.scale(happy_meal_image, (50, 50))

        # Affichage des Happy Meal Points
        points = self.font.render(str(happymeal_points), True, (255, 255, 255))
        screen.blit(happy_meal_image, (20, self.height - 60))
        screen.blit(points, (40, self.height - 20))

        # Dessin des boutons d'unités
        for button in self.unit_buttons:
            button.draw(screen)

    def handle_click(self, pos):
        clicked_unit = None
        for button in self.unit_buttons:
            if button.rect.collidepoint(pos):
                current_time = pygame.time.get_ticks()
                if current_time - button.last_placed_time >= button.cooldown_time:
                    clicked_unit = button.unit_name
                    button.selected = True
                else:
                    print("Unité en recharge, clique ignoré.")
            else:
                button.selected = False
        return clicked_unit


class UnitButton:
    def __init__(self, unit_name, image, x, y, cost, font):
        self.unit_name = unit_name
        self.image_original = pygame.transform.scale(image, (64, 64))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cost = cost
        self.font = font

        self.cooldown_time = 5000  # sera mis à jour dynamiquement
        self.last_placed_time = -self.cooldown_time
        self.selected = False

    def set_cooldown(self, remaining, total):
        self.cooldown_time = total
        current_time = pygame.time.get_ticks()
        self.last_placed_time = current_time - (total - remaining)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # Overlay de cooldown progressif
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_placed_time
        if elapsed < self.cooldown_time:
            remaining_ratio = 1 - (elapsed / self.cooldown_time)
            overlay_height = int(64 * remaining_ratio)
            overlay = pygame.Surface((64, overlay_height), pygame.SRCALPHA)
            overlay.fill((100, 100, 100, 180))  # gris semi-transparent
            screen.blit(overlay, (self.rect.x, self.rect.y))

        # Affichage du coût
        cost_text = self.font.render(str(self.cost), True, (255, 255, 0))
        cost_rect = cost_text.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 5))
        screen.blit(cost_text, cost_rect)

        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 5)


class Button:
    def __init__(self, name, image, x, y):
        self.name = name
        self.image = pygame.transform.scale(image, (80, 80))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, is_selected=False):
        screen.blit(self.image, self.rect)
        if is_selected:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 3)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
"""
class VolumeSlider:
    def __init__(self, x, y, width=100, height=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x + width - 10, y - 5, 10, height + 10)
        self.dragging = False
        self.volume = 1.0  # Volume initial (max)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_x = min(max(event.pos[0], self.rect.x), self.rect.x + self.rect.width - self.handle_rect.width)
                self.handle_rect.x = new_x
                self.volume = (new_x - self.rect.x) / (self.rect.width - self.handle_rect.width)
                pygame.mixer.music.set_volume(self.volume)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)  # Barre de fond
        pygame.draw.rect(screen, (255, 215, 0), self.handle_rect)  # Curseur
"""