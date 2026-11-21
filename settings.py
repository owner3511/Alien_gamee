class Settings:
    """Oyunun bütün əsas parametrlərini saxlayan sinif."""
    def __init__(self):
        """Oyunun başlanğıc parametrlərini təyin edir."""
        # Ekran ölçüləri (en, hündürlük)
        self.screen_width = 1000
        self.screen_height = 700

        # Fon rəngi (şəkillərin tünd fonuna uyğun tünd göy-qara)
        self.bg_color = (25, 30, 50)

        # Gəmi sürəti
        self.ship_speed = 0.8

        # Güllə parametrləri
        self.bullet_speed = 2.0
        self.bullet_width = 5
        self.bullet_height = 16
        self.bullet_color = (255, 220, 70)
        self.bullets_allowed = 6

        # Yadplanetli parametrləri (yuxarıdan axın və enmə)
        self.alien_speed_y = 0.35
        self.alien_sway_speed = 0.25
        self.spawn_delay_ms = 900
        self.burst_chance = 0.30

        # Vaxt və xal parametrləri
        self.game_duration_sec = 60
        self.alien_points = 10
