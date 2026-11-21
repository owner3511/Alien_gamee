import math
import random
import pygame


class SpaceBackground:
    """Arxa fonda ulduzlar, planetlər və meteorlardan ibarət canlı kosmos animasiyası."""

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width = ai_settings.screen_width
        self.height = ai_settings.screen_height
        self.bg_color = ai_settings.bg_color

        # 1. Müxtəlif dərinlikdə ulduzlar
        self.stars = []
        for _ in range(95):
            layer = random.choice(["far", "mid", "near"])
            if layer == "far":
                speed = random.uniform(0.08, 0.18)
                radius = 1
                base_alpha = random.randint(90, 145)
            elif layer == "mid":
                speed = random.uniform(0.20, 0.35)
                radius = random.choice([1, 2])
                base_alpha = random.randint(150, 205)
            else:
                speed = random.uniform(0.40, 0.65)
                radius = 2
                base_alpha = random.randint(205, 255)

            tint = random.choice([
                (225, 235, 255),
                (255, 248, 225),
                (180, 215, 255),
            ])

            self.stars.append({
                "x": random.uniform(0, self.width),
                "y": random.uniform(0, self.height),
                "speed": speed,
                "radius": radius,
                "base_alpha": base_alpha,
                "tint": tint,
                "twinkle_phase": random.uniform(0, math.pi * 2),
                "twinkle_speed": random.uniform(0.02, 0.05),
            })

        # 2. Uzaq planetlər
        self.planets = [
            {
                "x": self.width * 0.16,
                "y": self.height * 0.22,
                "radius": 28,
                "speed_y": 0.04,
                "body_color": (48, 66, 112),
                "shade_color": (28, 38, 72),
                "ring_color": (110, 145, 205),
                "has_ring": True,
            },
            {
                "x": self.width * 0.84,
                "y": self.height * 0.58,
                "radius": 19,
                "speed_y": 0.06,
                "body_color": (108, 56, 78),
                "shade_color": (62, 30, 48),
                "ring_color": None,
                "has_ring": False,
            },
        ]

        # 3. Meteorlar
        self.meteors = []
        self.next_meteor_time = pygame.time.get_ticks() + random.randint(1500, 3200)

    def _spawn_meteor(self):
        """Ekranın yuxarı/sağ hissəsindən diaqonal uçan yeni meteor yaradır."""
        start_x = random.uniform(self.width * 0.15, self.width * 1.05)
        start_y = random.uniform(-40, self.height * 0.25)

        angle = random.uniform(math.radians(115), math.radians(145))
        speed = random.uniform(3.2, 5.2)
        length = random.randint(35, 65)

        self.meteors.append({
            "x": start_x,
            "y": start_y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "length": length,
            "life": 255,
        })

    def update(self, now_ms):
        """Ulduzları, planetləri və meteorları yeniləyir."""
        for star in self.stars:
            star["y"] += star["speed"]
            star["twinkle_phase"] += star["twinkle_speed"]
            if star["y"] > self.height + 4:
                star["y"] = -4
                star["x"] = random.uniform(0, self.width)

        for planet in self.planets:
            planet["y"] += planet["speed_y"]
            if planet["y"] - planet["radius"] - 25 > self.height:
                planet["y"] = -planet["radius"] - 25
                planet["x"] = random.uniform(self.width * 0.12, self.width * 0.88)

        if now_ms >= self.next_meteor_time:
            if len(self.meteors) < 3:
                self._spawn_meteor()
            self.next_meteor_time = now_ms + random.randint(2200, 4500)

        for meteor in self.meteors[:]:
            meteor["x"] += meteor["vx"]
            meteor["y"] += meteor["vy"]
            meteor["life"] -= 2

            if (
                meteor["life"] <= 0
                or meteor["x"] < -100
                or meteor["y"] > self.height + 100
            ):
                self.meteors.remove(meteor)

    def _draw_planet(self, planet):
        """Tək bir planeti və varsa halqasını çəkir."""
        cx = int(planet["x"])
        cy = int(planet["y"])
        r = planet["radius"]

        if planet["has_ring"] and planet["ring_color"]:
            ring_rect = pygame.Rect(
                cx - int(r * 1.75), cy - int(r * 0.42), int(r * 3.5), int(r * 0.84)
            )
            pygame.draw.ellipse(self.screen, planet["ring_color"], ring_rect, width=2)

        pygame.draw.circle(self.screen, planet["body_color"], (cx, cy), r)

        shade_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(shade_surf, (*planet["shade_color"], 130), (r, r), r)
        pygame.draw.circle(
            shade_surf, (0, 0, 0, 0), (int(r * 0.75), int(r * 0.75)), int(r * 0.85)
        )
        self.screen.blit(shade_surf, (cx - r, cy - r))

        if planet["has_ring"] and planet["ring_color"]:
            front_rect = pygame.Rect(
                cx - int(r * 1.75), cy - int(r * 0.1), int(r * 3.5), int(r * 0.52)
            )
            pygame.draw.ellipse(self.screen, planet["ring_color"], front_rect, width=2)

    def draw(self):
        """Kosmos fonunu, ulduzları, planetləri və meteorları ekrana çəkir."""
        self.screen.fill(self.bg_color)

        for star in self.stars:
            twinkle = 0.75 + 0.25 * math.sin(star["twinkle_phase"])
            alpha = max(30, min(255, int(star["base_alpha"] * twinkle)))

            star_surf = pygame.Surface(
                (star["radius"] * 2 + 2, star["radius"] * 2 + 2), pygame.SRCALPHA
            )
            color_with_alpha = (*star["tint"], alpha)
            center = star["radius"] + 1
            pygame.draw.circle(
                star_surf, color_with_alpha, (center, center), star["radius"]
            )
            self.screen.blit(
                star_surf, (int(star["x"]) - center, int(star["y"]) - center)
            )

        for planet in self.planets:
            self._draw_planet(planet)

        for meteor in self.meteors:
            head_x = meteor["x"]
            head_y = meteor["y"]

            norm = math.hypot(meteor["vx"], meteor["vy"]) or 1.0
            dir_x = meteor["vx"] / norm
            dir_y = meteor["vy"] / norm

            tail_x = head_x - dir_x * meteor["length"]
            tail_y = head_y - dir_y * meteor["length"]

            alpha = max(0, min(255, meteor["life"]))
            meteor_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.line(
                meteor_surf,
                (170, 215, 255, int(alpha * 0.55)),
                (tail_x, tail_y),
                (head_x, head_y),
                width=2,
            )
            pygame.draw.circle(
                meteor_surf,
                (255, 245, 210, alpha),
                (int(head_x), int(head_y)),
                3,
            )
            self.screen.blit(meteor_surf, (0, 0))