import pygame

class PauseMenu:
    def __init__(self, screen, fullscreen=False):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)

        # Boutons
        self.resume_button_rect = pygame.Rect(200, 380, 200, 50)
        self.quit_button_rect = pygame.Rect(200, 450, 200, 50)

        # Slider volume
        self.slider_rect = pygame.Rect(200, 200, 200, 5)
        self.slider_knob_rect = pygame.Rect(200 + 100 - 10, 190, 20, 20)
        self.dragging_slider = False
        self.volume = 0.5  # entre 0.0 et 1.0

        # Checkbox plein écran
        self.checkbox_rect = pygame.Rect(200, 260, 20, 20)
        self.fullscreen = fullscreen

    def draw(self):
        # Fond du menu pause
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Titre
        title = self.font.render("Menu Pause", True, (255, 255, 255))
        self.screen.blit(title, (200, 120))

        # Slider de volume
        pygame.draw.rect(self.screen, (255, 255, 255), self.slider_rect)
        pygame.draw.rect(self.screen, (100, 100, 255), self.slider_knob_rect)
        vol_text = self.font.render(f"Volume : {int(self.volume * 100)}%", True, (255, 255, 255))
        self.screen.blit(vol_text, (self.slider_rect.x, self.slider_rect.y - 30))

        # Checkbox plein écran
        pygame.draw.rect(self.screen, (255, 255, 255), self.checkbox_rect, 2)
        if self.fullscreen:
            pygame.draw.line(self.screen, (255, 0, 0), self.checkbox_rect.topleft, self.checkbox_rect.bottomright, 2)
            pygame.draw.line(self.screen, (255, 0, 0), self.checkbox_rect.topright, self.checkbox_rect.bottomleft, 2)
        fs_text = self.font.render("Plein écran", True, (255, 255, 255))
        self.screen.blit(fs_text, (self.checkbox_rect.right + 10, self.checkbox_rect.y - 5))

        # Bouton Reprendre
        pygame.draw.rect(self.screen, (0, 180, 0), self.resume_button_rect)
        resume_text = self.font.render("Reprendre", True, (255, 255, 255))
        self.screen.blit(resume_text, (self.resume_button_rect.x + 30, self.resume_button_rect.y + 10))

        # Bouton Quitter
        pygame.draw.rect(self.screen, (180, 0, 0), self.quit_button_rect)
        quit_text = self.font.render("Quitter", True, (255, 255, 255))
        self.screen.blit(quit_text, (self.quit_button_rect.x + 50, self.quit_button_rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.resume_button_rect.collidepoint(event.pos):
                return "resume"

            if self.quit_button_rect.collidepoint(event.pos):
                return "quit"

            if self.slider_knob_rect.collidepoint(event.pos):
                self.dragging_slider = True

            if self.checkbox_rect.collidepoint(event.pos):
                self.fullscreen = not self.fullscreen
                return "toggle_fullscreen"

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_slider = False

        elif event.type == pygame.MOUSEMOTION and self.dragging_slider:
            x = max(self.slider_rect.left, min(event.pos[0], self.slider_rect.right))
            self.slider_knob_rect.centerx = x
            self.volume = (x - self.slider_rect.left) / self.slider_rect.width
            return "volume_changed"

        return None

    def get_volume(self):
        return self.volume

    def is_fullscreen(self):
        return self.fullscreen
