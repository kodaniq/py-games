
import pygame
import random
import math
import json
import os
import time
from collections import deque

pygame.init()
pygame.mixer.init()

# =========================================================
#  AIM TRAINER 2.0
# Single-file pygame project
# =========================================================

WIDTH, HEIGHT = 1280, 720
FPS = 144
SAVE_FILE = "aimtrainer_save.json"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Aim Trainer 2.0")
clock = pygame.time.Clock()

# ---------------- COLORS ----------------
BG = (13, 15, 22)
BG2 = (19, 22, 31)
PANEL = (26, 29, 40)
PANEL2 = (34, 38, 52)
WHITE = (240, 242, 248)
GRAY = (150, 156, 170)
DARK_GRAY = (85, 92, 108)

RED = (255, 78, 96)
GREEN = (91, 226, 146)
BLUE = (88, 164, 255)
YELLOW = (255, 210, 91)
PURPLE = (178, 117, 255)
CYAN = (79, 228, 232)

# ---------------- FONTS ----------------
FONT_TINY = pygame.font.SysFont("arial", 16)
FONT_SMALL = pygame.font.SysFont("arial", 20)
FONT = pygame.font.SysFont("arial", 28)
FONT_BOLD = pygame.font.SysFont("arial", 28, bold=True)
FONT_BIG = pygame.font.SysFont("arial", 46, bold=True)
FONT_HUGE = pygame.font.SysFont("arial", 72, bold=True)

# =========================================================
# SAVE SYSTEM
# =========================================================

DEFAULT_SAVE = {
    "best_scores": {
        "Classic": 0,
        "Speed": 0,
        "Precision": 0,
        "Chaos": 0
    },
    "settings": {
        "game_time": 30,
        "crosshair": True,
        "particles": True,
        "screen_shake": True
    }
}


def load_save():
    if not os.path.exists(SAVE_FILE):
        return DEFAULT_SAVE.copy()

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Merge missing values safely.
        for mode, value in DEFAULT_SAVE["best_scores"].items():
            data.setdefault("best_scores", {}).setdefault(mode, value)

        for key, value in DEFAULT_SAVE["settings"].items():
            data.setdefault("settings", {}).setdefault(key, value)

        return data
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SAVE.copy()


def save_data():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(save, f, indent=4)


save = load_save()
settings = save["settings"]

# =========================================================
# HELPERS
# =========================================================

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def lerp(a, b, t):
    return a + (b - a) * t


def draw_text(text, font, color, x, y, center=False):
    img = font.render(str(text), True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)
    return rect


def point_in_rect(pos, rect):
    return rect.collidepoint(pos)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def format_ms(seconds):
    if seconds <= 0:
        return "-"
    return f"{seconds * 1000:.0f} ms"


def rank_for(score, accuracy, avg_reaction):
    # Weighted score - deliberately simple and tweakable.
    reaction_score = 0
    if avg_reaction > 0:
        reaction_score = clamp((0.65 - avg_reaction) / 0.45, 0, 1) * 35

    accuracy_score = clamp(accuracy / 100, 0, 1) * 35
    hit_score = clamp(score / 55, 0, 1) * 30
    total = reaction_score + accuracy_score + hit_score

    if total >= 92:
        return "S+", PURPLE
    if total >= 85:
        return "S", PURPLE
    if total >= 76:
        return "A", GREEN
    if total >= 65:
        return "B", BLUE
    if total >= 52:
        return "C", YELLOW
    if total >= 38:
        return "D", RED
    return "F", GRAY


# =========================================================
# UI CLASSES
# =========================================================

class Button:
    def __init__(self, x, y, w, h, text, color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover = 0.0

    def update(self, mouse_pos):
        target = 1.0 if self.rect.collidepoint(mouse_pos) else 0.0
        self.hover = lerp(self.hover, target, 0.18)

    def draw(self):
        grow = int(self.hover * 4)
        rect = self.rect.inflate(grow, grow)
        base = (
            int(lerp(PANEL2[0], self.color[0], self.hover * 0.25)),
            int(lerp(PANEL2[1], self.color[1], self.hover * 0.25)),
            int(lerp(PANEL2[2], self.color[2], self.hover * 0.25)),
        )
        pygame.draw.rect(screen, base, rect, border_radius=14)
        pygame.draw.rect(screen, self.color, rect, 2, border_radius=14)
        draw_text(self.text, FONT_BOLD, WHITE, rect.centerx, rect.centery, center=True)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class Toggle:
    def __init__(self, x, y, label, key):
        self.x = x
        self.y = y
        self.label = label
        self.key = key
        self.rect = pygame.Rect(x + 250, y, 70, 34)

    def draw(self):
        draw_text(self.label, FONT, WHITE, self.x, self.y + 2)

        enabled = bool(settings[self.key])
        color = GREEN if enabled else DARK_GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=17)

        knob_x = self.rect.right - 17 if enabled else self.rect.left + 17
        pygame.draw.circle(screen, WHITE, (knob_x, self.rect.centery), 13)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            settings[self.key] = not settings[self.key]
            save_data()


# =========================================================
# PARTICLES / FX
# =========================================================

class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(100, 330)
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.life = random.uniform(0.25, 0.55)
        self.max_life = self.life
        self.radius = random.uniform(2, 5)
        self.color = color

    def update(self, dt):
        self.pos += self.vel * dt
        self.vel *= 0.96
        self.life -= dt

    def draw(self):
        if self.life <= 0:
            return
        alpha = int(255 * (self.life / self.max_life))
        surf = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (8, 8), int(self.radius))
        screen.blit(surf, (self.pos.x - 8, self.pos.y - 8))


class FloatingText:
    def __init__(self, text, x, y, color):
        self.text = text
        self.pos = pygame.Vector2(x, y)
        self.life = 0.65
        self.max_life = self.life
        self.color = color

    def update(self, dt):
        self.pos.y -= 60 * dt
        self.life -= dt

    def draw(self):
        if self.life <= 0:
            return
        alpha = int(255 * (self.life / self.max_life))
        img = FONT_BOLD.render(self.text, True, self.color)
        img.set_alpha(alpha)
        screen.blit(img, img.get_rect(center=self.pos))


# =========================================================
# TARGET
# =========================================================

class Target:
    def __init__(self, mode, difficulty=1):
        self.mode = mode
        self.difficulty = difficulty
        self.age = 0
        self.scale = 0.0
        self.dead = False
        self.hit = False

        if mode == "Precision":
            self.radius = random.randint(12, 22)
        elif mode == "Speed":
            self.radius = random.randint(22, 32)
        elif mode == "Chaos":
            self.radius = random.randint(18, 30)
        else:
            self.radius = random.randint(26, 38)

        margin = self.radius + 20
        self.pos = pygame.Vector2(
            random.randint(margin, WIDTH - margin),
            random.randint(150 + margin, HEIGHT - margin)
        )

        # Moving targets in Chaos get gentle motion.
        if mode == "Chaos":
            angle = random.uniform(0, math.tau)
            speed = random.uniform(80, 160)
            self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        else:
            self.vel = pygame.Vector2(0, 0)

        if mode == "Speed":
            self.max_age = clamp(1.05 - difficulty * 0.035, 0.38, 1.05)
        elif mode == "Chaos":
            self.max_age = 2.2
        else:
            self.max_age = 999

    def update(self, dt):
        self.age += dt
        self.scale = lerp(self.scale, 1.0, 0.22)

        if self.mode == "Chaos":
            self.pos += self.vel * dt

            if self.pos.x - self.radius < 0:
                self.pos.x = self.radius
                self.vel.x *= -1
            if self.pos.x + self.radius > WIDTH:
                self.pos.x = WIDTH - self.radius
                self.vel.x *= -1
            if self.pos.y - self.radius < 140:
                self.pos.y = 140 + self.radius
                self.vel.y *= -1
            if self.pos.y + self.radius > HEIGHT:
                self.pos.y = HEIGHT - self.radius
                self.vel.y *= -1

        if self.age >= self.max_age:
            self.dead = True

    def contains(self, point):
        return dist(self.pos, point) <= self.radius

    def draw(self):
        r = max(2, int(self.radius * self.scale))

        pulse = math.sin(self.age * 10) * 2
        outer = int(r + 7 + pulse)

        pygame.draw.circle(screen, (65, 25, 35), self.pos, outer)
        pygame.draw.circle(screen, RED, self.pos, r)
        pygame.draw.circle(screen, WHITE, self.pos, r, 3)

        # Bullseye
        pygame.draw.circle(screen, WHITE, self.pos, max(3, int(r * 0.18)))
        pygame.draw.circle(screen, RED, self.pos, max(1, int(r * 0.08)))


# =========================================================
# MAIN GAME
# =========================================================

class AimTrainer:
    def __init__(self):
        self.state = "menu"
        self.mode = "Classic"

        self.menu_buttons = [
            Button(465, 260, 350, 58, "PLAY", GREEN),
            Button(465, 335, 350, 58, "MODES", BLUE),
            Button(465, 410, 350, 58, "SETTINGS", PURPLE),
            Button(465, 485, 350, 58, "QUIT", RED),
        ]

        self.mode_buttons = [
            Button(160, 250, 220, 190, "CLASSIC", GREEN),
            Button(410, 250, 220, 190, "SPEED", YELLOW),
            Button(660, 250, 220, 190, "PRECISION", CYAN),
            Button(910, 250, 220, 190, "CHAOS", PURPLE),
        ]

        self.back_button = Button(40, 630, 180, 50, "BACK", GRAY)
        self.retry_button = Button(440, 580, 190, 55, "RETRY", GREEN)
        self.menu_button = Button(650, 580, 190, 55, "MENU", BLUE)

        self.toggles = [
            Toggle(420, 260, "Custom crosshair", "crosshair"),
            Toggle(420, 325, "Particles", "particles"),
            Toggle(420, 390, "Screen shake", "screen_shake"),
        ]

        self.time_minus = Button(455, 475, 60, 45, "-", RED)
        self.time_plus = Button(765, 475, 60, 45, "+", GREEN)

        self.reset_runtime()

    def reset_runtime(self):
        self.score = 0
        self.misses = 0
        self.combo = 0
        self.best_combo = 0
        self.total_clicks = 0
        self.reaction_times = []
        self.reaction_history = deque(maxlen=40)

        self.targets = []
        self.particles = []
        self.floaters = []

        self.start_ticks = pygame.time.get_ticks()
        self.last_spawn = 0
        self.spawn_interval = 0.7

        self.shake = 0
        self.flash = 0
        self.last_hit_pos = None

    def start_game(self):
        self.reset_runtime()
        self.state = "game"
        self.start_ticks = pygame.time.get_ticks()

        if self.mode == "Chaos":
            for _ in range(3):
                self.spawn_target()
        else:
            self.spawn_target()

    def elapsed(self):
        return (pygame.time.get_ticks() - self.start_ticks) / 1000

    def time_left(self):
        return max(0, settings["game_time"] - self.elapsed())

    def spawn_target(self):
        difficulty = 1 + self.score / 10
        self.targets.append(Target(self.mode, difficulty))

    def add_hit_fx(self, pos, color=YELLOW):
        if settings["particles"]:
            for _ in range(18):
                self.particles.append(Particle(pos[0], pos[1], color))

    def handle_game_click(self, pos):
        self.total_clicks += 1

        # Topmost target gets priority.
        clicked_target = None
        for target in reversed(self.targets):
            if target.contains(pos):
                clicked_target = target
                break

        if clicked_target:
            self.score += 1
            self.combo += 1
            self.best_combo = max(self.best_combo, self.combo)

            rt = clicked_target.age
            self.reaction_times.append(rt)
            self.reaction_history.append(rt)

            bonus = 0
            center_distance = dist(clicked_target.pos, pos)
            if center_distance <= clicked_target.radius * 0.28:
                bonus = 1
                self.score += 1
                self.floaters.append(FloatingText("BULLSEYE +1", pos[0], pos[1] - 20, YELLOW))
            else:
                self.floaters.append(FloatingText("+1", pos[0], pos[1] - 15, GREEN))

            self.add_hit_fx(clicked_target.pos)
            clicked_target.dead = True
            clicked_target.hit = True
            self.last_hit_pos = pos
            self.flash = 0.12

            if settings["screen_shake"]:
                self.shake = 5

            if self.mode != "Chaos":
                self.spawn_target()
            else:
                # Keep Chaos busy.
                self.spawn_target()
                if len([t for t in self.targets if not t.dead]) < 3:
                    self.spawn_target()

        else:
            self.misses += 1
            self.combo = 0
            self.floaters.append(FloatingText("MISS", pos[0], pos[1] - 10, RED))

            if settings["screen_shake"]:
                self.shake = 8

    def accuracy(self):
        if self.total_clicks == 0:
            return 100.0
        return (self.score / max(1, self.total_clicks)) * 100

    def avg_reaction(self):
        if not self.reaction_times:
            return 0
        return sum(self.reaction_times) / len(self.reaction_times)

    def best_reaction(self):
        if not self.reaction_times:
            return 0
        return min(self.reaction_times)

    def finish_game(self):
        self.state = "results"
        if self.score > save["best_scores"][self.mode]:
            save["best_scores"][self.mode] = self.score
            save_data()

    def update(self, dt):
        mouse = pygame.mouse.get_pos()

        if self.state == "menu":
            for b in self.menu_buttons:
                b.update(mouse)

        elif self.state == "modes":
            for b in self.mode_buttons:
                b.update(mouse)
            self.back_button.update(mouse)

        elif self.state == "settings":
            self.back_button.update(mouse)
            self.time_minus.update(mouse)
            self.time_plus.update(mouse)

        elif self.state == "results":
            self.retry_button.update(mouse)
            self.menu_button.update(mouse)

        elif self.state == "game":
            for t in self.targets:
                t.update(dt)

            # Handle targets that timed out.
            for t in self.targets:
                if t.dead and not t.hit and t.mode == "Speed":
                    self.misses += 1
                    self.combo = 0

            self.targets = [t for t in self.targets if not t.dead]

            if self.mode == "Speed" and not self.targets:
                self.spawn_target()

            if self.mode == "Chaos":
                desired = 3 + min(3, self.score // 12)
                while len(self.targets) < desired:
                    self.spawn_target()

            for p in self.particles:
                p.update(dt)
            self.particles = [p for p in self.particles if p.life > 0]

            for f in self.floaters:
                f.update(dt)
            self.floaters = [f for f in self.floaters if f.life > 0]

            if self.flash > 0:
                self.flash -= dt

            if self.shake > 0:
                self.shake = max(0, self.shake - 25 * dt)

            if self.time_left() <= 0:
                self.finish_game()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == "game":
                    self.state = "menu"
                elif self.state in ("modes", "settings", "results"):
                    self.state = "menu"

        if self.state == "menu":
            if self.menu_buttons[0].clicked(event):
                self.start_game()
            elif self.menu_buttons[1].clicked(event):
                self.state = "modes"
            elif self.menu_buttons[2].clicked(event):
                self.state = "settings"
            elif self.menu_buttons[3].clicked(event):
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif self.state == "modes":
            names = ["Classic", "Speed", "Precision", "Chaos"]
            for i, button in enumerate(self.mode_buttons):
                if button.clicked(event):
                    self.mode = names[i]
                    self.start_game()

            if self.back_button.clicked(event):
                self.state = "menu"

        elif self.state == "settings":
            for t in self.toggles:
                t.handle(event)

            if self.time_minus.clicked(event):
                settings["game_time"] = max(10, settings["game_time"] - 5)
                save_data()

            if self.time_plus.clicked(event):
                settings["game_time"] = min(120, settings["game_time"] + 5)
                save_data()

            if self.back_button.clicked(event):
                self.state = "menu"

        elif self.state == "results":
            if self.retry_button.clicked(event):
                self.start_game()

            if self.menu_button.clicked(event):
                self.state = "menu"

        elif self.state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_game_click(event.pos)

    # -----------------------------------------------------
    # DRAW
    # -----------------------------------------------------

    def draw_background(self):
        screen.fill(BG)

        # Soft animated grid.
        offset = int(time.time() * 20) % 40
        for x in range(-40 + offset, WIDTH, 40):
            pygame.draw.line(screen, (20, 23, 32), (x, 0), (x, HEIGHT))
        for y in range(-40 + offset, HEIGHT, 40):
            pygame.draw.line(screen, (20, 23, 32), (0, y), (WIDTH, y))

    def draw_menu(self):
        self.draw_background()

        draw_text(" AIM TRAINER", FONT_HUGE, WHITE, WIDTH // 2, 120, center=True)
        draw_text("2.0", FONT_BIG, PURPLE, WIDTH // 2, 185, center=True)

        draw_text(
            f"Selected mode: {self.mode}",
            FONT_SMALL,
            GRAY,
            WIDTH // 2,
            225,
            center=True
        )

        for b in self.menu_buttons:
            b.draw()

        draw_text(
            "Bullseyes give +1 bonus score • ESC returns to menu",
            FONT_TINY,
            DARK_GRAY,
            WIDTH // 2,
            675,
            center=True
        )

    def draw_modes(self):
        self.draw_background()

        draw_text("CHOOSE MODE", FONT_BIG, WHITE, WIDTH // 2, 95, center=True)

        descriptions = [
            ("Classic", "Static targets", "Balanced size", "Pure flick practice"),
            ("Speed", "Targets disappear", "Reaction focused", "Don't hesitate"),
            ("Precision", "Tiny targets", "Accuracy focused", "Aim carefully"),
            ("Chaos", "Multiple targets", "Moving targets", "Absolute violence"),
        ]

        colors = [GREEN, YELLOW, CYAN, PURPLE]

        for i, button in enumerate(self.mode_buttons):
            card = button.rect
            pygame.draw.rect(screen, PANEL, card, border_radius=18)
            pygame.draw.rect(screen, colors[i], card, 2, border_radius=18)

            name, a, b, c = descriptions[i]
            draw_text(name, FONT_BOLD, colors[i], card.centerx, card.y + 45, center=True)
            draw_text(a, FONT_SMALL, WHITE, card.centerx, card.y + 95, center=True)
            draw_text(b, FONT_SMALL, GRAY, card.centerx, card.y + 125, center=True)
            draw_text(c, FONT_TINY, DARK_GRAY, card.centerx, card.y + 155, center=True)

        self.back_button.draw()

    def draw_settings(self):
        self.draw_background()

        draw_text("SETTINGS", FONT_BIG, WHITE, WIDTH // 2, 110, center=True)

        panel = pygame.Rect(355, 210, 570, 360)
        pygame.draw.rect(screen, PANEL, panel, border_radius=20)
        pygame.draw.rect(screen, PANEL2, panel, 2, border_radius=20)

        for t in self.toggles:
            t.draw()

        draw_text("Round length", FONT, WHITE, 420, 485)
        draw_text(f"{settings['game_time']} sec", FONT_BOLD, YELLOW, WIDTH // 2, 498, center=True)

        self.time_minus.draw()
        self.time_plus.draw()
        self.back_button.draw()

    def draw_hud(self):
        pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, 125))

        draw_text(f"SCORE {self.score}", FONT_BOLD, WHITE, 28, 22)
        draw_text(f"COMBO x{self.combo}", FONT_SMALL, YELLOW, 28, 67)

        draw_text(f"ACC {self.accuracy():.1f}%", FONT_BOLD, WHITE, 245, 22)
        draw_text(f"MISSES {self.misses}", FONT_SMALL, RED, 245, 67)

        draw_text(f"{self.time_left():.1f}", FONT_BIG, WHITE, WIDTH // 2, 55, center=True)

        draw_text(self.mode.upper(), FONT_BOLD, BLUE, WIDTH - 220, 22)
        draw_text(
            f"BEST {save['best_scores'][self.mode]}",
            FONT_SMALL,
            GREEN,
            WIDTH - 220,
            67
        )

        # Time bar
        ratio = self.time_left() / settings["game_time"]
        pygame.draw.rect(screen, PANEL2, (0, 120, WIDTH, 5))
        pygame.draw.rect(screen, BLUE, (0, 120, int(WIDTH * ratio), 5))

    def draw_crosshair(self):
        if not settings["crosshair"]:
            return

        x, y = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)

        pygame.draw.circle(screen, WHITE, (x, y), 10, 1)
        pygame.draw.line(screen, WHITE, (x - 15, y), (x - 5, y), 2)
        pygame.draw.line(screen, WHITE, (x + 5, y), (x + 15, y), 2)
        pygame.draw.line(screen, WHITE, (x, y - 15), (x, y - 5), 2)
        pygame.draw.line(screen, WHITE, (x, y + 5), (x, y + 15), 2)

    def draw_reaction_graph(self, x, y, w, h):
        pygame.draw.rect(screen, PANEL2, (x, y, w, h), border_radius=12)

        if len(self.reaction_history) < 2:
            draw_text("Need more hits for graph", FONT_TINY, DARK_GRAY, x + w // 2, y + h // 2, center=True)
            return

        values = list(self.reaction_history)
        max_v = max(max(values), 0.8)
        min_v = min(values)

        points = []
        for i, value in enumerate(values):
            px = x + 12 + i * ((w - 24) / max(1, len(values) - 1))
            normalized = clamp(value / max_v, 0, 1)
            py = y + h - 12 - normalized * (h - 24)
            points.append((px, py))

        if len(points) >= 2:
            pygame.draw.lines(screen, CYAN, False, points, 2)

        draw_text(f"{min_v * 1000:.0f}ms best", FONT_TINY, GRAY, x + 8, y + 6)

    def draw_game(self):
        self.draw_background()
        self.draw_hud()

        # Draw targets
        for t in self.targets:
            t.draw()

        # FX
        for p in self.particles:
            p.draw()

        for f in self.floaters:
            f.draw()

        # Reaction mini graph
        self.draw_reaction_graph(WIDTH - 250, HEIGHT - 110, 220, 80)

        # Hit flash
        if self.flash > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((80, 255, 130, 22))
            screen.blit(overlay, (0, 0))

        self.draw_crosshair()

    def draw_results(self):
        self.draw_background()
        pygame.mouse.set_visible(True)

        acc = self.accuracy()
        avg = self.avg_reaction()
        rank, rank_color = rank_for(self.score, acc, avg)

        draw_text("RESULTS", FONT_BIG, WHITE, WIDTH // 2, 75, center=True)
        draw_text(rank, FONT_HUGE, rank_color, WIDTH // 2, 160, center=True)

        left = 360
        right = 760

        draw_text("Score", FONT_SMALL, GRAY, left, 245)
        draw_text(str(self.score), FONT_BIG, GREEN, left, 275)

        draw_text("Accuracy", FONT_SMALL, GRAY, right, 245)
        draw_text(f"{acc:.1f}%", FONT_BIG, BLUE, right, 275)

        draw_text("Avg reaction", FONT_SMALL, GRAY, left, 365)
        draw_text(format_ms(avg), FONT_BIG, CYAN, left, 395)

        draw_text("Best reaction", FONT_SMALL, GRAY, right, 365)
        draw_text(format_ms(self.best_reaction()), FONT_BIG, YELLOW, right, 395)

        draw_text("Best combo", FONT_SMALL, GRAY, left, 485)
        draw_text(f"x{self.best_combo}", FONT_BIG, PURPLE, left, 515)

        draw_text("Mode best", FONT_SMALL, GRAY, right, 485)
        draw_text(str(save["best_scores"][self.mode]), FONT_BIG, GREEN, right, 515)

        self.retry_button.draw()
        self.menu_button.draw()

    def draw(self):
        if self.state != "game":
            pygame.mouse.set_visible(True)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "modes":
            self.draw_modes()
        elif self.state == "settings":
            self.draw_settings()
        elif self.state == "game":
            self.draw_game()
        elif self.state == "results":
            self.draw_results()


# =========================================================
# RUN
# =========================================================

game = AimTrainer()
running = True

while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            game.handle_event(event)

    game.update(dt)
    game.draw()

    pygame.display.flip()

pygame.mouse.set_visible(True)
pygame.quit()
