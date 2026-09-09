import tkinter as tk
from tkinter import messagebox
import random
import math
import time
import json
import os

# ============================================================
#  — DO NOT PRESS
#  VERSION 999,999,999,999
#
# One-file Tkinter chaos game.
# No external assets needed.
# ============================================================

W, H = 1100, 720
FPS = 16
SAVE_FILE = "do_not_press_save.json"

BG = "#101015"
WHITE = "#f5f5f5"
RED = "#ff3b3b"
DARK_RED = "#a90f0f"
GRAY = "#25252d"
YELLOW = "#ffd84f"
GREEN = "#57e389"
BLUE = "#61a8ff"
PURPLE = "#b16cff"

DEFAULT_SAVE = {
    "best_presses": 0,
    "wins": 0,
    "fails": 0,
    "coins": 0,
    "achievements": [],
    "endings": []
}

ACHIEVEMENTS = [
    ("FIRST BLOOD", "Press the button once"),
    ("TEN IQ", "Press it 10 times"),
    ("FIFTY SHADES OF RED", "Press it 50 times"),
    ("ABSOLUTE MENACE", "Press it 100 times"),
    ("WHY ARE YOU LIKE THIS", "Reach 150 presses"),
    ("BUTTON HUNTER", "Catch the runaway button"),
    ("CLONE WARS", "Survive the clone stage"),
    ("BOSS FIGHT", "Defeat the final boss"),
    ("SECRET GOBLIN", "Find the secret ending"),
]

def load_save():
    data = DEFAULT_SAVE.copy()
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            old = json.load(f)
        data.update(old)
    except Exception:
        pass
    return data

save = load_save()

def save_game():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(save, f, indent=4)
    except Exception:
        pass

def unlock(name):
    if name not in save["achievements"]:
        save["achievements"].append(name)
        save["coins"] += 10
        save_game()
        return True
    return False

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        a = random.uniform(0, math.tau)
        s = random.uniform(2, 7)
        self.vx = math.cos(a) * s
        self.vy = math.sin(a) * s
        self.life = random.randint(20, 50)
        self.r = random.randint(2, 6)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        self.life -= 1

class ChaosButton:
    def __init__(self, game, x, y, w=260, h=100, text="DO NOT PRESS", fake=False):
        self.game = game
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.fake = fake
        self.alive = True
        self.vx = 0
        self.vy = 0
        self.shake = 0

    def contains(self, mx, my):
        return self.alive and self.x <= mx <= self.x+self.w and self.y <= my <= self.y+self.h

    def draw(self):
        if not self.alive:
            return

        shake_x = random.randint(-self.shake, self.shake) if self.shake else 0
        shake_y = random.randint(-self.shake, self.shake) if self.shake else 0

        x1 = self.x + shake_x
        y1 = self.y + shake_y
        x2 = x1 + self.w
        y2 = y1 + self.h

        fill = DARK_RED if self.fake else RED
        self.game.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=fill,
            outline="#ffffff",
            width=4
        )
        self.game.canvas.create_text(
            (x1+x2)/2, (y1+y2)/2,
            text=self.text,
            fill="white",
            font=("Arial", max(12, int(self.h*0.22)), "bold")
        )

class DoNotPressGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DO NOT PRESS — ")
        self.root.geometry(f"{W}x{H}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.canvas = tk.Canvas(
            self.root,
            width=W,
            height=H,
            bg=BG,
            highlightthickness=0
        )
        self.canvas.pack()

        self.state = "menu"
        self.presses = 0
        self.message = ""
        self.message_timer = 0
        self.warning = ""
        self.warning_timer = 0

        self.main_button = ChaosButton(self, W/2-130, H/2-50)
        self.fake_buttons = []
        self.particles = []
        self.stars = [[random.randint(0, W), random.randint(0, H), random.randint(1, 3)] for _ in range(90)]

        self.mouse_x = 0
        self.mouse_y = 0

        self.runaway = False
        self.runaway_timer = 0
        self.clone_mode = False
        self.gravity_mode = False
        self.invert_mode = False
        self.fake_crash = False

        self.countdown = None
        self.countdown_start = 0

        self.boss_active = False
        self.boss_hp = 100
        self.boss_max_hp = 100
        self.boss_x = W/2
        self.boss_y = 160
        self.boss_vx = 4
        self.boss_attack_timer = 0
        self.boss_projectiles = []
        self.player_hp = 100

        self.screen_shake = 0
        self.secret_counter = 0
        self.last_press_time = 0
        self.press_streak = 0
        self.flash = 0

        self.root.bind("<Motion>", self.on_motion)
        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<KeyPress>", self.on_key)

        self.loop()

    def reset_game(self):
        self.state = "game"
        self.presses = 0
        self.message = "Seriously. Don't press it."
        self.message_timer = 180
        self.warning = ""
        self.warning_timer = 0
        self.main_button = ChaosButton(self, W/2-130, H/2-50)
        self.fake_buttons = []
        self.runaway = False
        self.runaway_timer = 0
        self.clone_mode = False
        self.gravity_mode = False
        self.invert_mode = False
        self.fake_crash = False
        self.countdown = None
        self.boss_active = False
        self.boss_projectiles.clear()
        self.player_hp = 100
        self.secret_counter = 0
        self.screen_shake = 0
        self.press_streak = 0

    def on_motion(self, e):
        self.mouse_x = e.x
        self.mouse_y = e.y

    def on_key(self, e):
        if self.state == "menu" and e.keysym == "space":
            self.reset_game()
            return
        if self.state in ("ending", "failed") and e.keysym == "space":
            self.reset_game()
            return

        if self.state == "game":
            if e.keysym.lower() == "s":
                self.secret_counter += 1
                if self.secret_counter >= 7:
                    self.trigger_secret_ending()

            if e.keysym == "Escape":
                self.state = "menu"

    def on_click(self, e):
        if self.state == "menu":
            self.reset_game()
            return

        if self.state in ("ending", "failed"):
            self.reset_game()
            return

        if self.fake_crash:
            self.fake_crash = False
            self.say("...you really clicked the fake crash screen 💀", 150)
            return

        if self.boss_active:
            self.handle_boss_click(e.x, e.y)
            return

        clicked_fake = None
        for b in reversed(self.fake_buttons):
            if b.contains(e.x, e.y):
                clicked_fake = b
                break

        if clicked_fake:
            clicked_fake.alive = False
            self.particle_burst(e.x, e.y, PURPLE, 15)
            self.say(random.choice([
                "WRONG BUTTON 😭",
                "baited",
                "clone got you",
                "skill issue"
            ]), 70)
            if random.random() < 0.35:
                self.presses = max(0, self.presses - 1)
            return

        if self.main_button.contains(e.x, e.y):
            self.press_button()

    def press_button(self):
        now = time.time()
        if now - self.last_press_time < 0.5:
            self.press_streak += 1
        else:
            self.press_streak = 1
        self.last_press_time = now

        self.presses += 1
        save["best_presses"] = max(save["best_presses"], self.presses)
        save["coins"] += 1
        save_game()

        if self.presses == 1:
            unlock("FIRST BLOOD")
        if self.presses >= 10:
            unlock("TEN IQ")
        if self.presses >= 50:
            unlock("FIFTY SHADES OF RED")
        if self.presses >= 100:
            unlock("ABSOLUTE MENACE")
        if self.presses >= 150:
            unlock("WHY ARE YOU LIKE THIS")

        self.flash = 8
        self.screen_shake = min(14, 2 + self.presses//15)
        self.main_button.shake = min(8, self.presses//12)
        self.particle_burst(
            self.main_button.x + self.main_button.w/2,
            self.main_button.y + self.main_button.h/2,
            RED,
            18
        )

        self.advance_chaos()

    def advance_chaos(self):
        p = self.presses

        taunts = {
            1: "I literally said DO NOT PRESS.",
            2: "bro.",
            3: "BRO.",
            5: "Okay this is personal now.",
            7: "Last warning.",
            10: "Fine. You asked for this.",
            15: "Why is your finger like this 💀",
            20: "Catch me then.",
            30: "CLONE WARS.",
            40: "Gravity has entered the chat.",
            50: "Halfway to terrible decisions.",
            60: "System integrity: questionable.",
            75: "You could have stopped ages ago.",
            90: "Something is coming...",
            99: "Do NOT press it one more time.",
            100: "FINAL BOSS."
        }
        if p in taunts:
            self.say(taunts[p], 150)

        if p == 4:
            self.main_button.w = 210
            self.main_button.h = 82

        if p == 6:
            self.main_button.w = 310
            self.main_button.h = 115

        if p == 8:
            self.main_button.text = "SERIOUSLY STOP"

        if p == 11:
            self.main_button.text = "I'M WARNING YOU"

        if p == 14:
            self.teleport_button()

        if p == 20:
            self.runaway = True
            self.runaway_timer = 450

        if p == 30:
            self.start_clone_mode()

        if p == 40:
            self.gravity_mode = True

        if p == 45:
            self.main_button.text = "BAD IDEA"

        if p == 55:
            self.invert_mode = True
            self.say("coordinates.exe has stopped making sense", 150)

        if p == 60:
            self.fake_crash = True

        if p == 70:
            self.countdown = 10
            self.countdown_start = time.time()

        if p == 80:
            self.fake_buttons.extend([
                ChaosButton(
                    self,
                    random.randint(20, W-200),
                    random.randint(120, H-120),
                    180, 70,
                    random.choice(["PRESS ME", "REAL ONE", "TRUST ME", "FREE COINS"]),
                    fake=True
                )
                for _ in range(7)
            ])

        if p == 90:
            self.main_button.w = 140
            self.main_button.h = 55
            self.main_button.text = "NO"

        if p == 95:
            self.runaway = True
            self.runaway_timer = 250

        if p >= 100 and not self.boss_active:
            self.start_boss()

        if p > 12 and p < 100 and random.random() < min(0.55, p/180):
            self.teleport_button()

    def say(self, msg, duration=100):
        self.message = msg
        self.message_timer = duration

    def teleport_button(self):
        self.main_button.x = random.randint(30, W-int(self.main_button.w)-30)
        self.main_button.y = random.randint(130, H-int(self.main_button.h)-50)

    def start_clone_mode(self):
        self.clone_mode = True
        self.fake_buttons = []
        for _ in range(10):
            w = random.randint(150, 250)
            h = random.randint(55, 90)
            self.fake_buttons.append(
                ChaosButton(
                    self,
                    random.randint(20, W-w-20),
                    random.randint(120, H-h-20),
                    w, h,
                    random.choice(["DO NOT PRESS", "REAL BUTTON", "PRESS HERE", "SAFE"]),
                    fake=True
                )
            )
        unlock("CLONE WARS")

    def start_boss(self):
        self.boss_active = True
        self.main_button.alive = False
        self.fake_buttons.clear()
        self.boss_hp = 100
        self.player_hp = 100
        self.boss_attack_timer = 0
        self.say("BUTTON PRIME HAS AWAKENED", 180)

    def handle_boss_click(self, x, y):
        dx = x - self.boss_x
        dy = y - self.boss_y
        if dx*dx + dy*dy <= 80*80:
            dmg = 4 + min(8, self.press_streak//2)
            self.boss_hp -= dmg
            self.particle_burst(x, y, YELLOW, 16)
            self.screen_shake = 10

            if self.boss_hp <= 0:
                unlock("BOSS FIGHT")
                save["wins"] += 1
                save["coins"] += 100
                if "CHAOS ENDING" not in save["endings"]:
                    save["endings"].append("CHAOS ENDING")
                save_game()
                self.state = "ending"
                self.boss_active = False

    def trigger_secret_ending(self):
        save["wins"] += 1
        unlock("SECRET GOBLIN")
        if "SECRET GOBLIN ENDING" not in save["endings"]:
            save["endings"].append("SECRET GOBLIN ENDING")
        save["coins"] += 250
        save_game()
        self.state = "ending"
        self.message = "SECRET GOBLIN ENDING"

    def particle_burst(self, x, y, color, amount):
        for _ in range(amount):
            self.particles.append(Particle(x, y, color))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

        if self.state != "game":
            return

        if self.message_timer > 0:
            self.message_timer -= 1
        if self.warning_timer > 0:
            self.warning_timer -= 1

        if self.runaway and not self.boss_active:
            cx = self.main_button.x + self.main_button.w/2
            cy = self.main_button.y + self.main_button.h/2
            dx = cx - self.mouse_x
            dy = cy - self.mouse_y
            dist = max(1, math.hypot(dx, dy))

            if dist < 230:
                speed = 6.5
                self.main_button.x += dx/dist * speed
                self.main_button.y += dy/dist * speed

            self.main_button.x = max(10, min(W-self.main_button.w-10, self.main_button.x))
            self.main_button.y = max(100, min(H-self.main_button.h-20, self.main_button.y))
            self.runaway_timer -= 1

            if self.runaway_timer <= 0:
                self.runaway = False
                unlock("BUTTON HUNTER")

        if self.gravity_mode and not self.boss_active:
            self.main_button.vy += 0.45
            self.main_button.y += self.main_button.vy
            if self.main_button.y + self.main_button.h >= H-20:
                self.main_button.y = H-20-self.main_button.h
                self.main_button.vy *= -0.78
            if self.main_button.y < 110:
                self.main_button.y = 110
                self.main_button.vy = abs(self.main_button.vy)

        if self.invert_mode and not self.boss_active:
            if random.random() < 0.015:
                self.main_button.x = W - self.main_button.x - self.main_button.w
                self.main_button.y = H - self.main_button.y - self.main_button.h

        if self.countdown is not None:
            elapsed = int(time.time() - self.countdown_start)
            self.countdown = 10 - elapsed
            if self.countdown <= 0:
                self.countdown = None
                self.say("...nothing happened 😭", 180)

        if self.boss_active:
            self.update_boss()

        if self.screen_shake > 0:
            self.screen_shake -= 1
        if self.flash > 0:
            self.flash -= 1

    def update_boss(self):
        self.boss_x += self.boss_vx
        if self.boss_x < 100 or self.boss_x > W-100:
            self.boss_vx *= -1

        self.boss_attack_timer += 1
        if self.boss_attack_timer > 42:
            self.boss_attack_timer = 0
            angle = math.atan2(self.mouse_y-self.boss_y, self.mouse_x-self.boss_x)
            self.boss_projectiles.append([
                self.boss_x,
                self.boss_y,
                math.cos(angle)*6,
                math.sin(angle)*6
            ])

        for b in self.boss_projectiles:
            b[0] += b[2]
            b[1] += b[3]

            if (b[0]-self.mouse_x)**2 + (b[1]-self.mouse_y)**2 < 25**2:
                self.player_hp -= 8
                b[0] = -999
                self.screen_shake = 12

        self.boss_projectiles = [
            b for b in self.boss_projectiles
            if -50 < b[0] < W+50 and -50 < b[1] < H+50
        ]

        if self.player_hp <= 0:
            save["fails"] += 1
            save_game()
            self.state = "failed"
            self.boss_active = False

    def draw_bg(self):
        self.canvas.delete("all")

        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake else 0

        self.canvas.create_rectangle(
            -20+shake_x, -20+shake_y, W+20+shake_x, H+20+shake_y,
            fill="#1b0d12" if self.flash else BG,
            outline=""
        )

        for s in self.stars:
            s[1] += 0.2 + s[2]*0.08
            if s[1] > H:
                s[1] = 0
                s[0] = random.randint(0, W)
            self.canvas.create_oval(
                s[0], s[1], s[0]+s[2], s[1]+s[2],
                fill="#4b4b5c",
                outline=""
            )

    def draw_menu(self):
        self.draw_bg()
        self.canvas.create_text(
            W/2, 135,
            text="DO NOT PRESS",
            fill=RED,
            font=("Arial", 56, "bold")
        )
        self.canvas.create_text(
            W/2, 205,
            text=" VERSION 999,999,999,999",
            fill=WHITE,
            font=("Arial", 20, "bold")
        )
        self.canvas.create_text(
            W/2, 300,
            text="There is one rule.",
            fill="#aaaaaa",
            font=("Arial", 20)
        )
        self.canvas.create_text(
            W/2, 342,
            text="Do not press the button.",
            fill=WHITE,
            font=("Arial", 24, "bold")
        )

        self.canvas.create_rectangle(
            W/2-170, 420, W/2+170, 495,
            fill=RED, outline="white", width=3
        )
        self.canvas.create_text(
            W/2, 457,
            text="START ANYWAY",
            fill="white",
            font=("Arial", 22, "bold")
        )

        self.canvas.create_text(
            W/2, 570,
            text=f"Best presses: {save['best_presses']}    Coins: {save['coins']}    Wins: {save['wins']}",
            fill="#bdbdc8",
            font=("Arial", 16)
        )
        self.canvas.create_text(
            W/2, 620,
            text="Click anywhere or press SPACE",
            fill="#777788",
            font=("Arial", 13)
        )

    def draw_game(self):
        self.draw_bg()

        self.canvas.create_text(
            30, 28,
            anchor="w",
            text=f"PRESSES: {self.presses}",
            fill=WHITE,
            font=("Arial", 19, "bold")
        )
        self.canvas.create_text(
            W-30, 28,
            anchor="e",
            text=f"COINS: {save['coins']}",
            fill=YELLOW,
            font=("Arial", 17, "bold")
        )

        if self.message_timer > 0:
            self.canvas.create_text(
                W/2, 72,
                text=self.message,
                fill=WHITE,
                font=("Arial", 18, "bold")
            )

        if self.countdown is not None:
            self.canvas.create_text(
                W/2, H/2-160,
                text=str(self.countdown),
                fill=RED,
                font=("Arial", 72, "bold")
            )

        if self.fake_crash:
            self.canvas.create_rectangle(0, 0, W, H, fill="#0078d7", outline="")
            self.canvas.create_text(
                90, 110,
                anchor="w",
                text=":(",
                fill="white",
                font=("Arial", 72)
            )
            self.canvas.create_text(
                95, 240,
                anchor="w",
                text="Your PC ran into a problem because someone\npressed a button they were explicitly told not to press.",
                fill="white",
                font=("Arial", 22)
            )
            self.canvas.create_text(
                95, 365,
                anchor="w",
                text="Click anywhere to definitely fix it.",
                fill="white",
                font=("Arial", 16)
            )
            return

        if self.boss_active:
            self.draw_boss()
        else:
            for b in self.fake_buttons:
                b.draw()
            self.main_button.draw()

        for p in self.particles:
            self.canvas.create_oval(
                p.x-p.r, p.y-p.r,
                p.x+p.r, p.y+p.r,
                fill=p.color,
                outline=""
            )

        if self.presses >= 120 and not self.boss_active:
            self.canvas.create_text(
                20, H-24,
                anchor="w",
                text="totally irrelevant hint: S S S S S S S",
                fill="#33333d",
                font=("Arial", 10)
            )

    def draw_boss(self):
        self.canvas.create_text(
            W/2, 58,
            text="BUTTON PRIME",
            fill=RED,
            font=("Arial", 24, "bold")
        )

        self.canvas.create_rectangle(
            250, 88, W-250, 112,
            fill="#33333a",
            outline="white"
        )
        hpw = (W-500) * max(0, self.boss_hp/self.boss_max_hp)
        self.canvas.create_rectangle(
            250, 88, 250+hpw, 112,
            fill=RED,
            outline=""
        )

        r = 80 + math.sin(time.time()*4)*6
        self.canvas.create_oval(
            self.boss_x-r, self.boss_y-r,
            self.boss_x+r, self.boss_y+r,
            fill=DARK_RED,
            outline="white",
            width=5
        )
        self.canvas.create_text(
            self.boss_x, self.boss_y,
            text="PRESS\nME",
            fill="white",
            font=("Arial", 23, "bold")
        )

        for b in self.boss_projectiles:
            self.canvas.create_oval(
                b[0]-9, b[1]-9, b[0]+9, b[1]+9,
                fill=PURPLE,
                outline="white"
            )

        self.canvas.create_text(
            20, H-30,
            anchor="w",
            text=f"YOUR HP: {max(0, self.player_hp)}",
            fill=GREEN if self.player_hp > 35 else RED,
            font=("Arial", 18, "bold")
        )

        self.canvas.create_text(
            W-20, H-30,
            anchor="e",
            text="CLICK THE BOSS • DODGE WITH YOUR MOUSE",
            fill=WHITE,
            font=("Arial", 14, "bold")
        )

    def draw_ending(self):
        self.draw_bg()

        secret = self.message == "SECRET GOBLIN ENDING"
        title = "SECRET GOBLIN ENDING" if secret else "CHAOS ENDING"
        subtitle = (
            "You found the dumbest possible secret. Respect."
            if secret else
            "You defeated BUTTON PRIME. The button has learned fear."
        )

        self.canvas.create_text(
            W/2, 220,
            text=title,
            fill=PURPLE if secret else YELLOW,
            font=("Arial", 42, "bold")
        )
        self.canvas.create_text(
            W/2, 300,
            text=subtitle,
            fill=WHITE,
            font=("Arial", 18, "bold")
        )
        self.canvas.create_text(
            W/2, 380,
            text=f"Presses: {self.presses}   Coins: {save['coins']}",
            fill="#ccccd5",
            font=("Arial", 17)
        )
        self.canvas.create_text(
            W/2, 500,
            text="CLICK / SPACE TO GO AGAIN",
            fill=RED,
            font=("Arial", 19, "bold")
        )

    def draw_failed(self):
        self.draw_bg()
        self.canvas.create_text(
            W/2, 240,
            text="BUTTON PRIME COOKED YOU 💀",
            fill=RED,
            font=("Arial", 40, "bold")
        )
        self.canvas.create_text(
            W/2, 330,
            text="You were warned approximately 100 times.",
            fill=WHITE,
            font=("Arial", 18)
        )
        self.canvas.create_text(
            W/2, 470,
            text="CLICK / SPACE TO REMATCH",
            fill=YELLOW,
            font=("Arial", 20, "bold")
        )

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "game":
            self.draw_game()
        elif self.state == "ending":
            self.draw_ending()
        elif self.state == "failed":
            self.draw_failed()

    def loop(self):
        self.update()
        self.draw()
        self.root.after(FPS, self.loop)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    DoNotPressGame().run()
