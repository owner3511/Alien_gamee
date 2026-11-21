import random
import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard
from space_bg import SpaceBackground


def spawn_aliens(ai_settings, screen, aliens, alien_images):
    """Yuxarıdan tək və ya eyni anda bir neçə yadplanetli yaradır."""
    count = random.randint(2, 3) if random.random() < ai_settings.burst_chance else 1
    for _ in range(count):
        chosen_image = random.choice(alien_images)
        new_alien = Alien(ai_settings, screen, chosen_image)
        aliens.add(new_alien)


def reset_ship_position(ship):
    """Gəmini ekranın aşağı ortasına qaytarır."""
    ship.rect.centerx = ship.screen_rect.centerx
    ship.center_x = float(ship.rect.centerx)
    ship.moving_right = False
    ship.moving_left = False


def start_new_round(ai_settings, screen, ship, bullets, aliens, scoreboard, alien_images):
    """Yeni 1 dəqiqəlik raundu başladır."""
    scoreboard.reset_for_new_game()
    bullets.empty()
    aliens.empty()
    reset_ship_position(ship)

    start_ticks = pygame.time.get_ticks()
    last_spawn_ticks = start_ticks
    spawn_aliens(ai_settings, screen, aliens, alien_images)
    return start_ticks, last_spawn_ticks, True


def run_game():
    """Oyunu başladır və əsas dövrəni işə salır."""
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings, screen, "ship.jpg")
    bullets = Group()
    aliens = Group()
    alien_images = ["alien1.jpg"]
    sb = Scoreboard(ai_settings, screen)
    space_bg = SpaceBackground(ai_settings, screen)

    start_ticks, last_spawn_ticks, game_active = start_new_round(
        ai_settings, screen, ship, bullets, aliens, sb, alien_images
    )

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_active:
                if sb.restart_rect.collidepoint(event.pos):
                    start_ticks, last_spawn_ticks, game_active = start_new_round(
                        ai_settings, screen, ship, bullets, aliens, sb, alien_images
                    )
            elif event.type == pygame.KEYDOWN:
                if game_active:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        ship.moving_right = True
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        ship.moving_left = True
                    elif event.key == pygame.K_SPACE:
                        if len(bullets) < ai_settings.bullets_allowed:
                            new_bullet = Bullet(ai_settings, screen, ship)
                            bullets.add(new_bullet)
                else:
                    if event.key == pygame.K_r:
                        start_ticks, last_spawn_ticks, game_active = start_new_round(
                            ai_settings, screen, ship, bullets, aliens, sb, alien_images
                        )
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    ship.moving_right = False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    ship.moving_left = False

        space_bg.update(now)

        elapsed_seconds = (now - start_ticks) / 1000.0
        remaining_seconds = ai_settings.game_duration_sec - elapsed_seconds

        if game_active and remaining_seconds <= 0:
            remaining_seconds = 0
            game_active = False

        if game_active:
            if now - last_spawn_ticks >= ai_settings.spawn_delay_ms:
                spawn_aliens(ai_settings, screen, aliens, alien_images)
                last_spawn_ticks = now

            ship.update()

            bullets.update()
            for bullet in bullets.copy():
                if bullet.rect.bottom <= 0:
                    bullets.remove(bullet)

            collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
            if collisions:
                hit_count = sum(len(hit_aliens) for hit_aliens in collisions.values())
                sb.add_points(hit_count)

            aliens.update()
            for alien in aliens.copy():
                if alien.rect.top > ai_settings.screen_height:
                    aliens.remove(alien)

        space_bg.draw()

        if game_active:
            for bullet in bullets.sprites():
                bullet.draw_bullet()
            ship.blitme()
            for alien in aliens.sprites():
                alien.blitme()
            sb.draw_hud(remaining_seconds)
        else:
            sb.draw_game_over()

        pygame.display.flip()
run_game()
