import pygame
import random
import json
import os
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 700
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" BREAKOUT - MAXXED OUT")
CLOCK = pygame.time.Clock()

# ------------------------------------------------------------
# COLORS
# ------------------------------------------------------------
WHITE = (245, 245, 245)
BLACK = (15, 15, 20)
DARK = (28, 28, 38)
GRAY = (120, 120, 135)
LIGHT_GRAY = (200, 200, 210)
RED = (235, 70, 70)
ORANGE = (255, 145, 45)
YELLOW = (255, 220, 70)
GREEN = (80, 210, 110)
CYAN = (70, 220, 245)
BLUE = (70, 130, 245)
PURPLE = (160, 85, 235)
PINK = (255, 100, 180)
GOLD = (255, 205, 50)

FONT_BIG = pygame.font.Font(None, 68)
FONT_MEDIUM = pygame.font.Font(None, 40)
FONT_SMALL = pygame.font.Font(None, 28)
FONT_TINY = pygame.font.Font(None, 22)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "breakout_save.json")

# ------------------------------------------------------------
# GAME CONTENT
# ------------------------------------------------------------

DIFFICULTIES = {
    "easy": {"name": "Easy", "ball_speed": 5.2, "reward": 0.8},
    "normal": {"name": "Normal", "ball_speed": 6.2, "reward": 1.0},
    "hard": {"name": "Hard", "ball_speed": 7.3, "reward": 1.3},
}

PADDLES = {
    "classic": {"name": "Classic", "price": 0, "color": WHITE},
    "neon": {"name": "Neon", "price": 80, "color": CYAN},
    "gold": {"name": "Gold", "price": 160, "color": GOLD},
    "void": {"name": "Void", "price": 260, "color": PURPLE},
}
PADDLE_ORDER = list(PADDLES.keys())

TRAILS = {
    "none": {"name": "None", "price": 0},
    "spark": {"name": "Spark", "price": 60},
    "fire": {"name": "Fire", "price": 120},
    "rainbow": {"name": "Rainbow", "price": 220},
}
TRAIL_ORDER = list(TRAILS.keys())

ACHIEVEMENTS = {
    "first_level": {"name": "Warmup", "desc": "Clear level 1", "reward": 25},
    "combo_10": {"name": "Combo Machine", "desc": "Reach 10 combo", "reward": 30},
    "boss_1": {"name": "Boss Breaker", "desc": "Beat a boss level", "reward": 60},
    "coins_500": {"name": "Brick Banker", "desc": "Own 500 coins", "reward": 100},
    "level_10": {"name": "Brick Legend", "desc": "Reach level 10", "reward": 120},
}

POWERUP_TYPES = ["expand", "multi", "slow", "laser", "shield", "coin"]

# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

def default_save():
    return {
        "high_score": 0,
        "coins": 0,
        "xp": 0,
        "player_level": 1,
        "owned_paddles": ["classic"],
        "selected_paddle": "classic",
        "owned_trails": ["none"],
        "selected_trail": "none",
        "difficulty": "normal",
        "achievements": [],
        "stats": {
            "runs": 0,
            "levels_cleared": 0,
            "bosses_beaten": 0,
            "bricks_broken": 0,
            "best_combo": 0,
            "total_score": 0,
        },
        "settings": {
            "particles": True,
            "screen_shake": True,
        },
    }

def load_save():
    data = default_save()
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            old = json.load(f)
        for k, v in old.items():
            if k in ("stats", "settings") and isinstance(v, dict):
                data[k].update(v)
            else:
                data[k] = v
    except Exception:
        pass
    if data["selected_paddle"] not in PADDLES:
        data["selected_paddle"] = "classic"
    if data["selected_trail"] not in TRAILS:
        data["selected_trail"] = "none"
    if data["difficulty"] not in DIFFICULTIES:
        data["difficulty"] = "normal"
    return data

save = load_save()

def save_game():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(save, f, indent=4)
    except OSError:
        pass

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

particles = []
floating_text = []
screen_shake = 0
message_text = ""
message_timer = 0

def add_message(text, frames=100):
    global message_text, message_timer
    message_text = text
    message_timer = frames

def xp_needed(level):
    return 120 + (level - 1) * 60

def grant_xp(amount):
    save["xp"] += amount
    while save["xp"] >= xp_needed(save["player_level"]):
        need = xp_needed(save["player_level"])
        save["xp"] -= need
        save["player_level"] += 1
        save["coins"] += 30
        add_message(f"LEVEL UP! LVL {save['player_level']} +30 coins")
    save_game()

def achievement(key):
    if key not in save["achievements"]:
        save["achievements"].append(key)
        reward = ACHIEVEMENTS[key]["reward"]
        save["coins"] += reward
        add_message(f"Achievement: {ACHIEVEMENTS[key]['name']} +{reward}")
        save_game()

def check_achievements(level_num, combo):
    if level_num >= 2:
        achievement("first_level")
    if combo >= 10:
        achievement("combo_10")
    if save["stats"]["bosses_beaten"] >= 1:
        achievement("boss_1")
    if save["coins"] >= 500:
        achievement("coins_500")
    if level_num >= 10:
        achievement("level_10")

def spawn_particles(x, y, colors, count=10, speed=3):
    if not save["settings"]["particles"]:
        return
    for _ in range(count):
        ang = random.uniform(0, math.tau)
        s = random.uniform(0.5, speed)
        particles.append({
            "x": x,
            "y": y,
            "vx": math.cos(ang) * s,
            "vy": math.sin(ang) * s,
            "life": random.randint(18, 36),
            "color": random.choice(colors),
            "size": random.randint(2, 5),
        })

def update_particles():
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.04
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

def draw_particles(surface):
    for p in particles:
        pygame.draw.circle(surface, p["color"], (int(p["x"]), int(p["y"])), p["size"])

def add_floating(text, x, y, color=WHITE):
    floating_text.append({"text": text, "x": x, "y": y, "life": 60, "color": color})

def update_floating():
    for f in floating_text[:]:
        f["y"] -= 0.5
        f["life"] -= 1
        if f["life"] <= 0:
            floating_text.remove(f)

def draw_floating(surface):
    for f in floating_text:
        t = FONT_TINY.render(f["text"], True, f["color"])
        surface.blit(t, (int(f["x"]), int(f["y"])))

# ------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------

class Paddle:
    def __init__(self):
        self.base_width = 130
        self.width = self.base_width
        self.height = 18
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 55
        self.speed = 8
        self.laser = False
        self.laser_cooldown = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), self.height)

    def update(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
        self.x = max(0, min(WIDTH - self.width, self.x))
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

    def draw(self, surface):
        color = PADDLES[save["selected_paddle"]]["color"]
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
        if self.laser:
            pygame.draw.rect(surface, RED, (self.x + 8, self.y - 8, 8, 10))
            pygame.draw.rect(surface, RED, (self.x + self.width - 16, self.y - 8, 8, 10))

class Ball:
    def __init__(self, x, y, vx=None, vy=None):
        speed = DIFFICULTIES[save["difficulty"]]["ball_speed"]
        self.x = float(x)
        self.y = float(y)
        self.radius = 9
        if vx is None:
            angle = random.uniform(-0.9, 0.9)
            self.vx = math.sin(angle) * speed
            self.vy = -abs(math.cos(angle) * speed)
        else:
            self.vx = vx
            self.vy = vy
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def update(self, game):
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -abs(self.vx)

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = abs(self.vy)

        if self.y - self.radius > HEIGHT:
            if game.shield > 0:
                game.shield -= 1
                self.y = HEIGHT - 100
                self.vy = -abs(self.vy)
                add_message("SHIELD SAVED A BALL!")
            else:
                self.alive = False

        if self.rect.colliderect(game.paddle.rect) and self.vy > 0:
            hit = (self.x - game.paddle.rect.centerx) / max(1, game.paddle.width / 2)
            speed = min(10.5, math.hypot(self.vx, self.vy) + 0.12)
            self.vx = hit * speed * 0.95
            self.vy = -abs(math.sqrt(max(1, speed * speed - self.vx * self.vx)))
            self.y = game.paddle.y - self.radius - 1
            spawn_particles(self.x, self.y, [WHITE, CYAN], 6, 2)

        for brick in game.bricks[:]:
            if not brick.alive:
                continue
            if self.rect.colliderect(brick.rect):
                overlap_left = self.rect.right - brick.rect.left
                overlap_right = brick.rect.right - self.rect.left
                overlap_top = self.rect.bottom - brick.rect.top
                overlap_bottom = brick.rect.bottom - self.rect.top
                m = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                if m in (overlap_left, overlap_right):
                    self.vx *= -1
                else:
                    self.vy *= -1

                brick.hit(game)
                break

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, CYAN, (int(self.x), int(self.y)), self.radius, 2)

class Brick:
    def __init__(self, x, y, w, h, hp=1, kind="normal"):
        self.rect = pygame.Rect(x, y, w, h)
        self.hp = hp
        self.max_hp = hp
        self.kind = kind
        self.alive = True

    def hit(self, game, laser=False):
        global screen_shake
        self.hp -= 1
        spawn_particles(self.rect.centerx, self.rect.centery, [YELLOW, ORANGE, WHITE], 8, 3)
        if save["settings"]["screen_shake"]:
            screen_shake = max(screen_shake, 4)

        if self.hp <= 0:
            self.alive = False
            game.score += 100 * game.combo
            game.combo += 1
            game.max_combo = max(game.max_combo, game.combo)
            save["stats"]["bricks_broken"] += 1
            game.run_xp += 2
            add_floating(f"+{100 * max(1, game.combo - 1)}", self.rect.x, self.rect.y, GOLD)

            drop_chance = 0.16
            if self.kind == "gold":
                game.coins_run += 3
                save["coins"] += 3
                add_floating("+3 coins", self.rect.x, self.rect.y + 14, GOLD)
                drop_chance = 0.4

            if self.kind == "explosive":
                for b in game.bricks:
                    if b.alive and b is not self and abs(b.rect.centerx - self.rect.centerx) < 110 and abs(b.rect.centery - self.rect.centery) < 70:
                        b.hp = 0
                        b.alive = False
                        game.score += 80
                        save["stats"]["bricks_broken"] += 1
                        spawn_particles(b.rect.centerx, b.rect.centery, [RED, ORANGE, YELLOW], 10, 4)

            if random.random() < drop_chance:
                game.powerups.append(PowerUp(self.rect.centerx, self.rect.centery, random.choice(POWERUP_TYPES)))

    def draw(self, surface):
        if not self.alive:
            return
        if self.kind == "gold":
            color = GOLD
        elif self.kind == "explosive":
            color = RED
        elif self.kind == "boss":
            color = PURPLE
        elif self.hp >= 3:
            color = BLUE
        elif self.hp == 2:
            color = ORANGE
        else:
            color = GREEN
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)

        if self.max_hp > 1:
            hpw = int((self.hp / self.max_hp) * (self.rect.width - 6))
            pygame.draw.rect(surface, DARK, (self.rect.x + 3, self.rect.bottom - 6, self.rect.width - 6, 3))
            pygame.draw.rect(surface, WHITE, (self.rect.x + 3, self.rect.bottom - 6, hpw, 3))

class PowerUp:
    COLORS = {
        "expand": CYAN,
        "multi": PURPLE,
        "slow": BLUE,
        "laser": RED,
        "shield": GREEN,
        "coin": GOLD,
    }
    LABELS = {
        "expand": "E",
        "multi": "M",
        "slow": "S",
        "laser": "L",
        "shield": "H",
        "coin": "$",
    }

    def __init__(self, x, y, kind):
        self.x = float(x)
        self.y = float(y)
        self.kind = kind
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x - 14), int(self.y - 14), 28, 28)

    def update(self, game):
        self.y += 3.0
        if self.rect.colliderect(game.paddle.rect):
            self.apply(game)
            self.alive = False
        elif self.y > HEIGHT:
            self.alive = False

    def apply(self, game):
        if self.kind == "expand":
            game.paddle.width = min(220, game.paddle.width + 45)
            add_message("PADDLE EXPANDED!")
        elif self.kind == "multi":
            if game.balls:
                base = random.choice(game.balls)
                game.balls.append(Ball(base.x, base.y, -base.vx, base.vy))
                game.balls.append(Ball(base.x, base.y, base.vx * 0.6, base.vy))
            add_message("MULTIBALL!")
        elif self.kind == "slow":
            for b in game.balls:
                b.vx *= 0.78
                b.vy *= 0.78
            add_message("SLOW BALL!")
        elif self.kind == "laser":
            game.paddle.laser = True
            game.laser_timer = 600
            add_message("LASER MODE!")
        elif self.kind == "shield":
            game.shield += 1
            add_message("SHIELD +1!")
        elif self.kind == "coin":
            gain = 10
            save["coins"] += gain
            game.coins_run += gain
            add_message("+10 COINS!")
        spawn_particles(self.x, self.y, [self.COLORS[self.kind], WHITE], 16, 4)

    def draw(self, surface):
        c = self.COLORS[self.kind]
        pygame.draw.circle(surface, c, (int(self.x), int(self.y)), 15)
        t = FONT_TINY.render(self.LABELS[self.kind], True, BLACK)
        surface.blit(t, t.get_rect(center=(int(self.x), int(self.y))))

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.rect = pygame.Rect(x - 3, y, 6, 18)

    def update(self, game):
        self.y -= 12
        self.rect.y = int(self.y)
        if self.y < -30:
            self.alive = False
            return
        for brick in game.bricks:
            if brick.alive and self.rect.colliderect(brick.rect):
                brick.hit(game, laser=True)
                self.alive = False
                break

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

# ------------------------------------------------------------
# GAME
# ------------------------------------------------------------

class Game:
    def __init__(self):
        self.state = "menu"
        self.paddle = Paddle()
        self.balls = []
        self.bricks = []
        self.powerups = []
        self.lasers = []
        self.score = 0
        self.level = 1
        self.lives = 3
        self.combo = 1
        self.max_combo = 1
        self.coins_run = 0
        self.run_xp = 0
        self.shield = 0
        self.laser_timer = 0
        self.shop_tab = "paddles"
        self.shop_index = 0
        self.diff_index = list(DIFFICULTIES).index(save["difficulty"])
        self.reset_level(first=True)

    def reset_run(self):
        save["stats"]["runs"] += 1
        self.score = 0
        self.level = 1
        self.lives = 3
        self.combo = 1
        self.max_combo = 1
        self.coins_run = 0
        self.run_xp = 0
        self.shield = 0
        self.paddle = Paddle()
        self.reset_level(first=True)
        self.state = "playing"

    def reset_ball(self):
        self.balls = [Ball(self.paddle.rect.centerx, self.paddle.y - 18)]

    def reset_level(self, first=False):
        self.paddle.width = self.paddle.base_width
        self.paddle.x = WIDTH // 2 - self.paddle.width // 2
        self.powerups.clear()
        self.lasers.clear()
        self.combo = 1
        self.generate_level()
        self.reset_ball()
        if not first:
            add_message(f"LEVEL {self.level}")

    def generate_level(self):
        self.bricks = []
        cols = 10
        rows = min(7, 4 + self.level // 2)
        gap = 7
        margin = 45
        brick_w = (WIDTH - margin * 2 - gap * (cols - 1)) // cols
        brick_h = 26
        start_y = 95

        boss = self.level % 5 == 0

        if boss:
            bx = WIDTH // 2 - 180
            by = 130
            self.bricks.append(Brick(bx, by, 360, 55, hp=8 + self.level // 2, kind="boss"))
            for i in range(6):
                x = 120 + i * 110
                self.bricks.append(Brick(x, 240, 90, 26, hp=2, kind="normal"))
        else:
            for r in range(rows):
                for c in range(cols):
                    x = margin + c * (brick_w + gap)
                    y = start_y + r * (brick_h + gap)
                    hp = 1
                    kind = "normal"

                    roll = random.random()
                    if roll < 0.06:
                        kind = "gold"
                    elif roll < 0.12:
                        kind = "explosive"

                    if self.level >= 3 and random.random() < min(0.35, self.level * 0.03):
                        hp = 2
                    if self.level >= 7 and random.random() < 0.14:
                        hp = 3

                    self.bricks.append(Brick(x, y, brick_w, brick_h, hp=hp, kind=kind))

    def level_clear(self):
        if any(b.alive for b in self.bricks):
            return False

        if self.level % 5 == 0:
            save["stats"]["bosses_beaten"] += 1
            self.coins_run += 25
            save["coins"] += 25
            add_message("BOSS CLEARED! +25 coins")

        save["stats"]["levels_cleared"] += 1
        self.level += 1
        self.lives = min(5, self.lives + 1)
        level_reward = int((8 + self.level * 2) * DIFFICULTIES[save["difficulty"]]["reward"])
        save["coins"] += level_reward
        self.coins_run += level_reward
        self.run_xp += 20
        check_achievements(self.level, self.max_combo)
        self.reset_level()
        save_game()
        return True

    def shoot(self):
        if self.paddle.laser and self.paddle.laser_cooldown <= 0:
            self.lasers.append(Laser(int(self.paddle.x + 12), int(self.paddle.y)))
            self.lasers.append(Laser(int(self.paddle.x + self.paddle.width - 12), int(self.paddle.y)))
            self.paddle.laser_cooldown = 18

    def update(self):
        global screen_shake

        keys = pygame.key.get_pressed()
        self.paddle.update(keys)

        if self.laser_timer > 0:
            self.laser_timer -= 1
            if self.laser_timer <= 0:
                self.paddle.laser = False

        for ball in self.balls:
            ball.update(self)
        self.balls = [b for b in self.balls if b.alive]

        if not self.balls:
            self.lives -= 1
            self.combo = 1
            if self.lives <= 0:
                self.game_over()
                return
            self.reset_ball()

        for p in self.powerups:
            p.update(self)
        self.powerups = [p for p in self.powerups if p.alive]

        for l in self.lasers:
            l.update(self)
        self.lasers = [l for l in self.lasers if l.alive]

        self.level_clear()

        save["high_score"] = max(save["high_score"], self.score)
        save["stats"]["best_combo"] = max(save["stats"]["best_combo"], self.max_combo)

        update_particles()
        update_floating()

        if screen_shake > 0:
            screen_shake -= 1

    def game_over(self):
        save["high_score"] = max(save["high_score"], self.score)
        save["stats"]["total_score"] += self.score
        grant_xp(self.run_xp + self.level * 10)
        save_game()
        self.state = "gameover"

    def draw_background(self, surface):
        surface.fill((18, 20, 35))
        for i in range(35):
            x = (i * 97 + pygame.time.get_ticks() // 25) % WIDTH
            y = (i * 53) % HEIGHT
            pygame.draw.circle(surface, (50, 55, 85), (x, y), 2)

    def draw_game(self):
        surf = pygame.Surface((WIDTH, HEIGHT))
        self.draw_background(surf)

        for brick in self.bricks:
            brick.draw(surf)
        for p in self.powerups:
            p.draw(surf)
        for l in self.lasers:
            l.draw(surf)
        for ball in self.balls:
            ball.draw(surf)
        self.paddle.draw(surf)

        draw_particles(surf)
        draw_floating(surf)

        hud = [
            f"Score: {self.score}",
            f"Lives: {self.lives}",
            f"Level: {self.level}",
            f"Combo: x{self.combo}",
            f"Coins: {save['coins']}",
        ]
        x = 15
        for text in hud:
            t = FONT_TINY.render(text, True, WHITE)
            surf.blit(t, (x, 15))
            x += t.get_width() + 22

        if self.shield:
            t = FONT_TINY.render(f"Shield x{self.shield}", True, GREEN)
            surf.blit(t, (WIDTH - t.get_width() - 15, 42))

        if self.paddle.laser:
            t = FONT_TINY.render("LASER", True, RED)
            surf.blit(t, (WIDTH - t.get_width() - 15, 65))

        if message_timer > 0 and message_text:
            t = FONT_SMALL.render(message_text, True, GOLD)
            surf.blit(t, (WIDTH // 2 - t.get_width() // 2, 50))

        sx = sy = 0
        if screen_shake > 0 and save["settings"]["screen_shake"]:
            sx = random.randint(-5, 5)
            sy = random.randint(-5, 5)

        SCREEN.fill(BLACK)
        SCREEN.blit(surf, (sx, sy))

    def draw_menu(self):
        self.draw_background(SCREEN)
        title = FONT_BIG.render(" BREAKOUT", True, WHITE)
        sub = FONT_SMALL.render("MAXXED OUT EDITION", True, GOLD)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        SCREEN.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 145))

        preview = pygame.Rect(WIDTH // 2 - 75, 235, 150, 20)
        pygame.draw.rect(SCREEN, PADDLES[save["selected_paddle"]]["color"], preview, border_radius=10)

        lines = [
            "SPACE = PLAY",
            "G = SHOP",
            "D = DIFFICULTY",
            "T = STATS",
            "A = ACHIEVEMENTS",
            "S = SETTINGS",
            "ESC = QUIT",
        ]
        y = 340
        for i, line in enumerate(lines):
            t = FONT_MEDIUM.render(line, True, CYAN if i == 0 else WHITE)
            SCREEN.blit(t, (WIDTH // 2 - t.get_width() // 2, y))
            y += 45

        info = FONT_SMALL.render(
            f"Best {save['high_score']}   Coins {save['coins']}   Player LVL {save['player_level']}",
            True,
            GOLD,
        )
        SCREEN.blit(info, (WIDTH // 2 - info.get_width() // 2, 650))

    def draw_shop(self):
        SCREEN.fill(DARK)
        title = FONT_BIG.render("SHOP", True, WHITE)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 45))
        tab = FONT_SMALL.render(f"Q = SWITCH TAB   [{self.shop_tab.upper()}]", True, CYAN)
        SCREEN.blit(tab, (WIDTH // 2 - tab.get_width() // 2, 110))

        if self.shop_tab == "paddles":
            item_id = PADDLE_ORDER[self.shop_index % len(PADDLE_ORDER)]
            item = PADDLES[item_id]
            owned = item_id in save["owned_paddles"]
            selected = item_id == save["selected_paddle"]

            pygame.draw.rect(SCREEN, item["color"], (WIDTH // 2 - 100, 250, 200, 24), border_radius=12)
            name = FONT_MEDIUM.render(item["name"], True, item["color"])
        else:
            item_id = TRAIL_ORDER[self.shop_index % len(TRAIL_ORDER)]
            item = TRAILS[item_id]
            owned = item_id in save["owned_trails"]
            selected = item_id == save["selected_trail"]
            name = FONT_MEDIUM.render(item["name"], True, GOLD)

        SCREEN.blit(name, (WIDTH // 2 - name.get_width() // 2, 320))

        if selected:
            status = "SELECTED"
        elif owned:
            status = "ENTER = SELECT"
        else:
            status = f"ENTER = BUY ({item['price']} coins)"

        st = FONT_SMALL.render(status, True, GREEN if selected else GOLD)
        SCREEN.blit(st, (WIDTH // 2 - st.get_width() // 2, 390))

        nav = FONT_SMALL.render("A / D = browse   ESC = back", True, WHITE)
        SCREEN.blit(nav, (WIDTH // 2 - nav.get_width() // 2, 500))
        coins = FONT_SMALL.render(f"Coins: {save['coins']}", True, GOLD)
        SCREEN.blit(coins, (WIDTH // 2 - coins.get_width() // 2, 550))

    def shop_action(self):
        if self.shop_tab == "paddles":
            item_id = PADDLE_ORDER[self.shop_index % len(PADDLE_ORDER)]
            item = PADDLES[item_id]
            owned_key = "owned_paddles"
            selected_key = "selected_paddle"
        else:
            item_id = TRAIL_ORDER[self.shop_index % len(TRAIL_ORDER)]
            item = TRAILS[item_id]
            owned_key = "owned_trails"
            selected_key = "selected_trail"

        if item_id in save[owned_key]:
            save[selected_key] = item_id
        elif save["coins"] >= item["price"]:
            save["coins"] -= item["price"]
            save[owned_key].append(item_id)
            save[selected_key] = item_id
        save_game()

    def draw_difficulty(self):
        SCREEN.fill(DARK)
        title = FONT_BIG.render("DIFFICULTY", True, WHITE)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        key = list(DIFFICULTIES)[self.diff_index % len(DIFFICULTIES)]
        diff = DIFFICULTIES[key]
        t = FONT_MEDIUM.render(diff["name"], True, GOLD)
        SCREEN.blit(t, (WIDTH // 2 - t.get_width() // 2, 260))
        n = FONT_SMALL.render("A / D = browse   ENTER = select   ESC = back", True, WHITE)
        SCREEN.blit(n, (WIDTH // 2 - n.get_width() // 2, 350))

    def draw_stats(self):
        SCREEN.fill(DARK)
        title = FONT_BIG.render("STATS", True, WHITE)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 45))
        s = save["stats"]
        lines = [
            f"High score: {save['high_score']}",
            f"Player level: {save['player_level']}",
            f"XP: {save['xp']} / {xp_needed(save['player_level'])}",
            f"Coins: {save['coins']}",
            f"Runs: {s['runs']}",
            f"Levels cleared: {s['levels_cleared']}",
            f"Bosses beaten: {s['bosses_beaten']}",
            f"Bricks broken: {s['bricks_broken']}",
            f"Best combo: {s['best_combo']}",
            f"Total score: {s['total_score']}",
        ]
        y = 130
        for line in lines:
            t = FONT_SMALL.render(line, True, WHITE)
            SCREEN.blit(t, (200, y))
            y += 46
        b = FONT_SMALL.render("ESC = back", True, GRAY)
        SCREEN.blit(b, (WIDTH // 2 - b.get_width() // 2, 640))

    def draw_achievements(self):
        SCREEN.fill(DARK)
        title = FONT_BIG.render("ACHIEVEMENTS", True, WHITE)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 45))
        y = 135
        for key, a in ACHIEVEMENTS.items():
            done = key in save["achievements"]
            mark = "[X]" if done else "[ ]"
            col = GREEN if done else GRAY
            t = FONT_SMALL.render(f"{mark} {a['name']} - {a['desc']} (+{a['reward']})", True, col)
            SCREEN.blit(t, (95, y))
            y += 70
        b = FONT_SMALL.render("ESC = back", True, WHITE)
        SCREEN.blit(b, (WIDTH // 2 - b.get_width() // 2, 640))

    def draw_settings(self):
        SCREEN.fill(DARK)
        title = FONT_BIG.render("SETTINGS", True, WHITE)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        p = "ON" if save["settings"]["particles"] else "OFF"
        s = "ON" if save["settings"]["screen_shake"] else "OFF"
        lines = [
            f"1 = Particles: {p}",
            f"2 = Screen shake: {s}",
            "ESC = back",
        ]
        y = 250
        for line in lines:
            t = FONT_MEDIUM.render(line, True, WHITE)
            SCREEN.blit(t, (WIDTH // 2 - t.get_width() // 2, y))
            y += 75

    def draw_gameover(self):
        self.draw_game()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        SCREEN.blit(overlay, (0, 0))

        title = FONT_BIG.render("GAME OVER", True, RED)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))

        lines = [
            f"Score: {self.score}",
            f"Best: {save['high_score']}",
            f"Level reached: {self.level}",
            f"Coins this run: {self.coins_run}",
            f"Max combo: {self.max_combo}",
            "R = restart",
            "M = menu",
        ]
        y = 270
        for i, line in enumerate(lines):
            t = FONT_SMALL.render(line, True, CYAN if i >= 5 else WHITE)
            SCREEN.blit(t, (WIDTH // 2 - t.get_width() // 2, y))
            y += 42

game = Game()

# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

running = True
while running:
    CLOCK.tick(FPS)

    if message_timer > 0:
        message_timer -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game.state == "menu":
                if event.key == pygame.K_SPACE:
                    game.reset_run()
                elif event.key == pygame.K_g:
                    game.shop_tab = "paddles"
                    game.shop_index = 0
                    game.state = "shop"
                elif event.key == pygame.K_d:
                    game.diff_index = list(DIFFICULTIES).index(save["difficulty"])
                    game.state = "difficulty"
                elif event.key == pygame.K_t:
                    game.state = "stats"
                elif event.key == pygame.K_a:
                    game.state = "achievements"
                elif event.key == pygame.K_s:
                    game.state = "settings"
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif game.state == "playing":
                if event.key == pygame.K_ESCAPE:
                    game.state = "paused"
                elif event.key == pygame.K_SPACE:
                    game.shoot()

            elif game.state == "paused":
                if event.key == pygame.K_ESCAPE:
                    game.state = "playing"
                elif event.key == pygame.K_r:
                    game.reset_run()
                elif event.key == pygame.K_m:
                    game.state = "menu"

            elif game.state == "gameover":
                if event.key == pygame.K_r:
                    game.reset_run()
                elif event.key == pygame.K_m:
                    game.state = "menu"

            elif game.state == "shop":
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    game.shop_index -= 1
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    game.shop_index += 1
                elif event.key == pygame.K_q:
                    game.shop_tab = "trails" if game.shop_tab == "paddles" else "paddles"
                    game.shop_index = 0
                elif event.key == pygame.K_RETURN:
                    game.shop_action()
                elif event.key == pygame.K_ESCAPE:
                    game.state = "menu"

            elif game.state == "difficulty":
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    game.diff_index -= 1
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    game.diff_index += 1
                elif event.key == pygame.K_RETURN:
                    key = list(DIFFICULTIES)[game.diff_index % len(DIFFICULTIES)]
                    save["difficulty"] = key
                    save_game()
                elif event.key == pygame.K_ESCAPE:
                    game.state = "menu"

            elif game.state in ("stats", "achievements"):
                if event.key == pygame.K_ESCAPE:
                    game.state = "menu"

            elif game.state == "settings":
                if event.key == pygame.K_1:
                    save["settings"]["particles"] = not save["settings"]["particles"]
                    save_game()
                elif event.key == pygame.K_2:
                    save["settings"]["screen_shake"] = not save["settings"]["screen_shake"]
                    save_game()
                elif event.key == pygame.K_ESCAPE:
                    game.state = "menu"

    if game.state == "playing":
        game.update()
    else:
        update_particles()
        update_floating()

    if game.state == "menu":
        game.draw_menu()
    elif game.state == "playing":
        game.draw_game()
    elif game.state == "paused":
        game.draw_game()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        SCREEN.blit(overlay, (0, 0))
        t = FONT_BIG.render("PAUSED", True, WHITE)
        SCREEN.blit(t, (WIDTH // 2 - t.get_width() // 2, 260))
        p = FONT_SMALL.render("ESC = resume   R = restart   M = menu", True, WHITE)
        SCREEN.blit(p, (WIDTH // 2 - p.get_width() // 2, 350))
    elif game.state == "gameover":
        game.draw_gameover()
    elif game.state == "shop":
        game.draw_shop()
    elif game.state == "difficulty":
        game.draw_difficulty()
    elif game.state == "stats":
        game.draw_stats()
    elif game.state == "achievements":
        game.draw_achievements()
    elif game.state == "settings":
        game.draw_settings()

    pygame.display.flip()

save_game()
pygame.quit()
sys.exit()
