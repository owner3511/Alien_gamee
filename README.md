# Alien_gamee
# Alien Invasion 🚀👾

A classic space arcade game built with Python and the `pygame` library. Control the spaceship at the bottom of the screen to shoot down incoming aliens within 60 seconds and achieve the highest possible score (`Max Score`).

---

## ✨ Features

* **Player Spaceship (`ship.py`):** Smooth left and right movement along the bottom of the screen.
* **Firing System (`bullet.py`):** Fire up to 6 bullets simultaneously using the `SPACE` bar.
* **Dynamic Alien Waves (`alien.py`):** Aliens enter from random positions at the top of the screen individually or in small bursts.
* **Animated Space Background (`space_bg.py`):** A lively cosmic backdrop featuring twinkling and drifting stars, distant planets, and diagonal shooting meteors.
* **60-Second Timer & Scoring System (`scoreboard.py`):**
  * Each destroyed alien awards **+10 points**.
  * Tracks and displays your highest score (`Max Score`) across rounds.
  * When time runs out, displays the final score summary along with a **"Yenidən başla" (Restart)** button (or press `R`) to start a new round.

---

## 📁 Project Structure

```text
alien_invasion/
├── alien_invasion.py   # Main game loop and module integration
├── settings.py         # Screen dimensions, speeds, timer, and scoring settings
├── ship.py             # Player spaceship setup and movement logic
├── bullet.py           # Bullet behavior and rendering
├── alien.py            # Alien spawning and movement logic
├── scoreboard.py       # Score, Max Score, timer, and game-over screen
├── space_bg.py         # Animated space background (stars, planets, meteors)
├── ship.jpg            # Player spaceship sprite image
└── alien1.jpg          # Alien sprite image
