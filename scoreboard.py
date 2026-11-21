import pygame


class Scoreboard:
    """Xalı, ən yüksək xalı, vaxtı və oyun sonu ekranını idarə edən sinif."""

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        self.score = 0
        self.max_score = 0

        # Rənglər və şriftlər
        self.text_color = (235, 240, 255)
        self.highlight_color = (120, 255, 160)
        self.button_bg = (45, 95, 175)
        self.button_border = (140, 195, 255)

        self.hud_font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 56)
        self.score_font = pygame.font.SysFont(None, 42)
        self.button_font = pygame.font.SysFont(None, 36)

        # "Yenidən başla" düyməsinin ölçüsü və mövqeyi
        self.restart_rect = pygame.Rect(0, 0, 240, 56)
        self.restart_rect.centerx = self.screen_rect.centerx
        self.restart_rect.top = self.screen_rect.centery + 85

    def add_points(self, count):
        """Vurulan yadplanetli sayına görə xalı artırır və max_score-u yeniləyir."""
        self.score += count * self.ai_settings.alien_points
        if self.score > self.max_score:
            self.max_score = self.score

    def reset_for_new_game(self):
        """Yeni raund üçün cari xalı sıfırlayır (max_score saxlanılır)."""
        self.score = 0

    def draw_hud(self, remaining_seconds):
        """Oyun vaxtı yuxarı paneldə xal, max xal və qalan vaxtı göstərir."""
        score_surf = self.hud_font.render(
            f"Score: {self.score}", True, self.text_color
        )
        max_surf = self.hud_font.render(
            f"Max Score: {self.max_score}", True, self.highlight_color
        )
        time_surf = self.hud_font.render(
            f"Time: {max(0, int(remaining_seconds))}s", True, self.text_color
        )

        self.screen.blit(score_surf, (20, 15))
        self.screen.blit(max_surf, (220, 15))
        self.screen.blit(
            time_surf, (self.screen_rect.right - time_surf.get_width() - 20, 15)
        )

    def draw_game_over(self):
        """Vaxt bitəndə Max Score, cari Score və Yenidən başla düyməsini çəkir."""
        over_surf = self.title_font.render("GAME OVER!", True, self.text_color)
        over_rect = over_surf.get_rect(
            center=(self.screen_rect.centerx, self.screen_rect.centery - 75)
        )

        max_surf = self.score_font.render(
            f"Max Score: {self.max_score}", True, self.highlight_color
        )
        max_rect = max_surf.get_rect(
            center=(self.screen_rect.centerx, self.screen_rect.centery - 15)
        )

        current_surf = self.hud_font.render(
            f"THIS ROUND SCORE: {self.score}", True, self.text_color
        )
        current_rect = current_surf.get_rect(
            center=(self.screen_rect.centerx, self.screen_rect.centery + 35)
        )

        self.screen.blit(over_surf, over_rect)
        self.screen.blit(max_surf, max_rect)
        self.screen.blit(current_surf, current_rect)

        # Yenidən başla düyməsi
        pygame.draw.rect(
            self.screen, self.button_bg, self.restart_rect, border_radius=8
        )
        pygame.draw.rect(
            self.screen, self.button_border, self.restart_rect, width=2, border_radius=8
        )

        btn_surf = self.button_font.render("START AGAIN", True, self.text_color)
        btn_rect = btn_surf.get_rect(center=self.restart_rect.center)
        self.screen.blit(btn_surf, btn_rect)