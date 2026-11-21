import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Gəmidən atılan gülləni idarə edən sinif."""

    def __init__(self, ai_settings, screen, ship):
        """Gəminin mövqeyində yeni güllə obyekti yaradır."""
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

    def update(self):
        """Gülləni yuxarı doğru hərəkət etdirir."""
        self.y -= self.speed
        self.rect.y = int(self.y)
    def draw_bullet(self):
        """Gülləni ekranda çəkir."""
        pygame.draw.rect(self.screen, self.color, self.rect)
