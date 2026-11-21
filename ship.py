import pygame


class Ship:
    """Oyunçu gəmisini idarə edən sinif."""

    def __init__(self, ai_settings, screen, image_path="ship.jpg"):
        """Gəmini, şəklini və başlanğıc mövqeyini təyin edir."""
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()

        raw_image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.smoothscale(raw_image, (64, 64))
        self.rect = self.image.get_rect()

        # Gəmini ekranın aşağı ortasına yerləşdiririk
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 15

        self.center_x = float(self.rect.centerx)

        # Hərəkət bayraqları
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Gəminin üfüqi mövqeyini yeniləyir."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.ai_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center_x -= self.ai_settings.ship_speed

        self.rect.centerx = int(self.center_x)

    def blitme(self):
        """Gəmini ekranda çəkir."""
        self.screen.blit(self.image, self.rect)