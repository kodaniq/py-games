import pygame
import random
import sys
import os
import json
import math
from datetime import date

pygame.init()

WIDTH, HEIGHT = 520, 760
FPS = 60
GROUND_HEIGHT = 80

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" FLAPPY MEGABUILD - ULTIMATE EDITION")
CLOCK = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (20, 20, 24)
DARKER = (12, 12, 18)
GRAY = (120, 120, 130)
LIGHT_GRAY = (195, 195, 205)
GREEN = (55, 190, 80)
DARK_GREEN = (35, 140, 60)
YELLOW = (255, 220, 60)
ORANGE = (255, 145, 40)
RED = (230, 65, 65)
BLUE = (65, 140, 250)
CYAN = (80, 220, 240)
PURPLE = (155, 80, 230)
PINK = (255, 105, 180)
GOLD = (255, 205, 40)
GROUND_DARK = (170, 140, 70)

FONT_BIG = pygame.font.Font(None, 64)
FONT_MEDIUM = pygame.font.Font(None, 38)
FONT_SMALL = pygame.font.Font(None, 28)
FONT_TINY = pygame.font.Font(None, 22)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "flappy_save.json")

SKINS = {
    "classic": {"name": "Classic", "price": 0, "rarity": "Common", "body": YELLOW, "wing": ORANGE},
    "blue": {"name": "Bluebird", "price": 25, "rarity": "Common", "body": BLUE, "wing": CYAN},
    "pink": {"name": "Pinky", "price": 50, "rarity": "Rare", "body": PINK, "wing": PURPLE},
    "void": {"name": "Void Bird", "price": 100, "rarity": "Epic", "body": (65, 45, 100), "wing": PURPLE},
    "gold": {"name": "Golden", "price": 175, "rarity": "Legendary", "body": GOLD, "wing": YELLOW},
    "toxic": {"name": "Toxic", "price": 240, "rarity": "Mythic", "body": (110, 255, 90), "wing": (40, 150, 60)},
}
SKIN_ORDER = list(SKINS.keys())

TRAILS = {
    "none": {"name": "None", "price": 0},
    "spark": {"name": "Spark", "price": 40},
    "fire": {"name": "Fire", "price": 90},
    "void": {"name": "Void", "price": 140},
}
TRAIL_ORDER = list(TRAILS.keys())

WORLDS = {
    "meadow": {"name": "Sunny Meadow", "unlock": 0},
    "sunset": {"name": "Sunset City", "unlock": 8},
    "night": {"name": "Night Sky", "unlock": 16},
    "storm": {"name": "Storm Zone", "unlock": 24},
}
WORLD_ORDER = list(WORLDS.keys())

DIFFICULTIES = {
    "easy": {"name": "Easy", "gap_bonus": 28, "speed_bonus": -0.7, "coin_mult": 0.8},
    "normal": {"name": "Normal", "gap_bonus": 0, "speed_bonus": 0.0, "coin_mult": 1.0},
    "hard": {"name": "Hard", "gap_bonus": -22, "speed_bonus": 0.8, "coin_mult": 1.35},
}
DIFFICULTY_ORDER = list(DIFFICULTIES.keys())

GAME_MODES = {
    "classic": {"name": "Classic", "unlock": 0, "desc": "The full  Flappy experience."},
    "turbo": {"name": "Turbo", "unlock": 6, "desc": "Faster pipes, tighter timing, bigger rewards."},
    "tiny": {"name": "Tiny Bird", "unlock": 12, "desc": "Smaller hitbox, faster gravity."},
    "chaos": {"name": "Chaos", "unlock": 18, "desc": "More moving/golden pipes and random madness."},
    "hardcore": {"name": "Hardcore", "unlock": 25, "desc": "No shield saves. Maximum rewards."},
    "daily": {"name": "Daily Challenge", "unlock": 0, "desc": "Same seeded challenge for the whole day."},
}
MODE_ORDER = list(GAME_MODES.keys())

ACHIEVEMENTS = {
    "first_pipe": {"name": "First Flight", "desc": "Pass 1 pipe", "reward": 10},
    "score_10": {"name": "Getting Good", "desc": "Reach score 10", "reward": 20},
    "score_25": {"name": "Sky Grinder", "desc": "Reach score 25", "reward": 40},
    "score_50": {"name": "Bird Legend", "desc": "Reach score 50", "reward": 80},
    "coin_100": {"name": "Coin Goblin", "desc": "Own 100 coins", "reward": 25},
    "combo_10": {"name": "Combo Beast", "desc": "Reach 10 combo", "reward": 30},
    "boss_clear": {"name": "Boss Breaker", "desc": "Clear a boss section", "reward": 60},
}

MISSION_POOL = [
    {"type": "score", "target": 8, "text": "Reach score 8", "reward": 20},
    {"type": "coins", "target": 5, "text": "Collect 5 coins in one run", "reward": 20},
    {"type": "combo", "target": 6, "text": "Reach combo 6", "reward": 25},
    {"type": "score", "target": 15, "text": "Reach score 15", "reward": 35},
]

def default_save():
    return {
        "high_score": 0,
        "coins": 0,
        "xp": 0,
        "level": 1,
        "owned_skins": ["classic"],
        "selected_skin": "classic",
        "owned_trails": ["none"],
        "selected_trail": "none",
        "selected_world": "meadow",
        "difficulty": "normal",
        "selected_mode": "classic",
        "prestige": 0,
        "daily_last": "",
        "daily_streak": 0,
        "best_mode_scores": {},
        "leaderboard": [],
        "best_ghost": [],
        "daily_best": {},
        "achievements": [],
        "stats": {
            "runs": 0,
            "deaths": 0,
            "total_score": 0,
            "total_coins_collected": 0,
            "best_combo": 0,
            "bosses_cleared": 0,
            "powerups_collected": 0,
            "near_misses": 0,
            "play_seconds": 0,
        },
        "settings": {
            "screen_shake": True,
            "particles": True,
            "ghost": True,
        },
        "mission": random.choice(MISSION_POOL),
    }

def load_save():
    data = default_save()
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)
        for k, v in saved.items():
            if k in ("stats", "settings") and isinstance(v, dict):
                data[k].update(v)
            else:
                data[k] = v
    except Exception:
        pass

    if data["selected_skin"] not in SKINS:
        data["selected_skin"] = "classic"
    if data["selected_trail"] not in TRAILS:
        data["selected_trail"] = "none"
    if data["selected_world"] not in WORLDS:
        data["selected_world"] = "meadow"
    if data["difficulty"] not in DIFFICULTIES:
        data["difficulty"] = "normal"
    if data.get("selected_mode") not in GAME_MODES:
        data["selected_mode"] = "classic"
    return data

save = load_save()

def claim_daily_reward():
    today = date.today().isoformat()
    if save.get("daily_last", "") == today:
        return
    old = save.get("daily_last", "")
    if old:
        try:
            previous = date.fromisoformat(old)
            if (date.today() - previous).days == 1:
                save["daily_streak"] = min(30, save.get("daily_streak", 0) + 1)
            else:
                save["daily_streak"] = 1
        except ValueError:
            save["daily_streak"] = 1
    else:
        save["daily_streak"] = 1
    reward = 15 + save["daily_streak"] * 5 + save.get("prestige", 0) * 3
    save["coins"] += reward
    save["daily_last"] = today
    save["daily_reward_pending"] = reward

def player_title():
    p = save.get("prestige", 0)
    lvl = save.get("level", 1)
    if p >= 5: return "FLAPPY DEITY"
    if p >= 2: return "SKY EMPEROR"
    if p >= 1: return "ASCENDED BIRD"
    if lvl >= 30: return "LEGEND"
    if lvl >= 20: return "ACE PILOT"
    if lvl >= 10: return "PIPE HUNTER"
    if lvl >= 5: return "FLAPPER"
    return "ROOKIE"

def prestige_multiplier():
    return 1.0 + save.get("prestige", 0) * 0.08

def save_game():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(save, f, indent=4)
    except OSError:
        pass

claim_daily_reward()
save_game()

game_state = "menu"
bird_x = 125
bird_y = HEIGHT // 2
bird_vel = 0.0
GRAVITY = 0.46
FLAP = -8.6

pipes = []
particles = []
clouds = []
powerups = []

score = 0
combo = 0
run_coins = 0
run_xp = 0
spawn_timer = 0
screen_shake = 0
flash_timer = 0
ground_offset = 0
boss_mode = False
boss_timer = 0
boss_target = 0
shield = 0
magnet_timer = 0
slow_timer = 0
double_timer = 0
invuln_timer = 0
near_misses = 0
ghost_recording = []
ghost_playback = save.get("best_ghost", [])
ghost_tick = 0
fever_bonus_claimed = 0

shop_tab = "skins"
shop_index = 0
world_index = 0
difficulty_index = 1
mode_index = MODE_ORDER.index(save.get("selected_mode", "classic"))
profile_index = 0
play_frame_counter = 0
message_text = ""
message_timer = 0

for _ in range(7):
    clouds.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(50, 320),
        "speed": random.uniform(0.2, 0.8),
        "size": random.randint(18, 38),
    })

def daily_seed():
    return int(date.today().strftime("%Y%m%d"))

def daily_target():
    return 12 + (daily_seed() % 9)

def daily_modifier():
    mods = ["FAST PIPES", "TIGHT GAPS", "MOVING MADNESS", "GOLD RUSH"]
    return mods[daily_seed() % len(mods)]

def add_leaderboard_entry(final_score):
    entry = {
        "score": int(final_score),
        "mode": save.get("selected_mode", "classic"),
        "world": save.get("selected_world", "meadow"),
        "difficulty": save.get("difficulty", "normal"),
    }
    board = save.setdefault("leaderboard", [])
    board.append(entry)
    board.sort(key=lambda x: x.get("score", 0), reverse=True)
    del board[10:]

def add_message(text, frames=120):
    global message_text, message_timer
    message_text = text
    message_timer = frames

def xp_needed(level):
    return 100 + (level - 1) * 55

def grant_xp(amount):
    save["xp"] += amount
    while save["xp"] >= xp_needed(save["level"]):
        need = xp_needed(save["level"])
        save["xp"] -= need
        save["level"] += 1
        save["coins"] += 25
        add_message(f"LEVEL UP! LVL {save['level']} +25 coins")
    save_game()

def unlock_achievement(key):
    if key not in save["achievements"]:
        save["achievements"].append(key)
        reward = ACHIEVEMENTS[key]["reward"]
        save["coins"] += reward
        add_message(f"Achievement: {ACHIEVEMENTS[key]['name']} +{reward}")
        save_game()

def check_achievements():
    if score >= 1: unlock_achievement("first_pipe")
    if score >= 10: unlock_achievement("score_10")
    if score >= 25: unlock_achievement("score_25")
    if score >= 50: unlock_achievement("score_50")
    if save["coins"] >= 100: unlock_achievement("coin_100")
    if combo >= 10: unlock_achievement("combo_10")

def mission_progress():
    m = save["mission"]
    if m["type"] == "score": return score
    if m["type"] == "coins": return run_coins
    if m["type"] == "combo": return combo
    return 0

def check_mission():
    m = save["mission"]
    if mission_progress() >= m["target"]:
        save["coins"] += m["reward"]
        grant_xp(35)
        add_message(f"Mission complete! +{m['reward']} coins")
        save["mission"] = random.choice(MISSION_POOL)
        save_game()

def get_world_colors():
    world = save["selected_world"]
    if world == "meadow":
        return (120, 200, 255), (215, 185, 100), (245, 245, 250)
    if world == "sunset":
        return (235, 125, 120), (180, 125, 90), (255, 200, 190)
    if world == "night":
        return (25, 30, 70), (80, 75, 95), (180, 180, 220)
    return (70, 75, 90), (90, 95, 105), (180, 185, 200)

def get_pipe_gap():
    base = 188 - min(score, 45) * 1.25
    base += DIFFICULTIES[save["difficulty"]]["gap_bonus"]
    mode = save.get("selected_mode", "classic")
    if mode == "turbo": base -= 14
    if mode == "tiny": base -= 8
    if mode == "chaos": base -= random.randint(0, 10)
    if mode == "hardcore": base -= 18
    if boss_mode:
        base -= 20
    return max(112, int(base))

def get_pipe_speed():
    base = 4.0 + min(score, 50) * 0.07
    base += DIFFICULTIES[save["difficulty"]]["speed_bonus"]
    mode = save.get("selected_mode", "classic")
    if mode == "turbo": base += 1.35
    if mode == "chaos": base += 0.45
    if mode == "hardcore": base += 0.9
    if boss_mode:
        base += 1.0
    if save.get("selected_mode") == "daily" and daily_modifier() == "FAST PIPES":
        base += 0.9
    if slow_timer > 0:
        base *= 0.62
    return min(9.2, base)

def get_spawn_delay():
    delay = 96 - min(score, 50) * 0.35
    if boss_mode:
        delay -= 12
    return max(68, int(delay))

def bird_rect():
    if save.get("selected_mode") == "tiny":
        return pygame.Rect(bird_x - 10, int(bird_y) - 10, 20, 20)
    return pygame.Rect(bird_x - 14, int(bird_y) - 14, 28, 28)

def spawn_particles(x, y, colors, amount=8, speed=3):
    if not save["settings"]["particles"]:
        return
    for _ in range(amount):
        a = random.uniform(0, math.tau)
        s = random.uniform(0.4, speed)
        particles.append({
            "x": x, "y": y,
            "vx": math.cos(a) * s,
            "vy": math.sin(a) * s,
            "life": random.randint(18, 34),
            "size": random.randint(2, 5),
            "color": random.choice(colors),
        })

def create_pipe():
    gap = get_pipe_gap()
    min_y = 110 + gap // 2
    max_y = HEIGHT - GROUND_HEIGHT - 110 - gap // 2
    gap_y = random.randint(min_y, max_y)

    pipes.append({
        "x": WIDTH + 20,
        "gap_y": gap_y,
        "base_gap_y": gap_y,
        "move_phase": random.uniform(0, math.tau),
        "moving": random.random() < (0.38 if save.get("selected_mode") == "chaos" else min(0.22, score * 0.006)),
        "golden": random.random() < (0.16 if save.get("selected_mode") == "chaos" else 0.08),
        "coin": random.random() < 0.7,
        "coin_collected": False,
        "scored": False,
        "near_checked": False,
    })

def spawn_powerup(x, y):
    kinds = ["shield", "magnet", "slow", "double"]
    powerups.append({"x": x, "y": y, "kind": random.choice(kinds)})

def reset_run():
    global bird_y, bird_vel, pipes, particles, powerups, score, combo
    global run_coins, run_xp, spawn_timer, screen_shake, flash_timer
    global ground_offset, boss_mode, boss_timer, boss_target
    global shield, magnet_timer, slow_timer, double_timer, invuln_timer
    global near_misses, game_state, ghost_recording, ghost_playback, ghost_tick, fever_bonus_claimed

    bird_y = HEIGHT // 2
    bird_vel = 0
    pipes = []
    particles = []
    powerups = []
    score = 0
    combo = 0
    run_coins = 0
    run_xp = 0
    spawn_timer = 0
    screen_shake = 0
    flash_timer = 0
    ground_offset = 0
    boss_mode = False
    boss_timer = 0
    boss_target = 0
    shield = 0
    magnet_timer = 0
    slow_timer = 0
    double_timer = 0
    invuln_timer = 0
    near_misses = 0
    ghost_recording = []
    ghost_playback = save.get("best_ghost", [])[:] if save.get("settings", {}).get("ghost", True) else []
    ghost_tick = 0
    fever_bonus_claimed = 0
    if save.get("selected_mode") == "daily":
        random.seed(daily_seed())
    else:
        random.seed()
    save["stats"]["runs"] += 1
    game_state = "playing"

def game_over():
    global game_state, screen_shake, flash_timer
    game_state = "gameover"
    save["stats"]["deaths"] += 1
    save["stats"]["total_score"] += score
    save["stats"]["total_coins_collected"] += run_coins
    save["stats"]["best_combo"] = max(save["stats"]["best_combo"], combo)
    old_best = save.get("high_score", 0)
    save["high_score"] = max(old_best, score)
    mode = save.get("selected_mode", "classic")
    save.setdefault("best_mode_scores", {})[mode] = max(save.get("best_mode_scores", {}).get(mode, 0), score)
    add_leaderboard_entry(score)
    if score > old_best and ghost_recording:
        save["best_ghost"] = ghost_recording[:2400]
    if mode == "daily":
        today = date.today().isoformat()
        old_daily = save.setdefault("daily_best", {}).get(today, 0)
        save["daily_best"][today] = max(old_daily, score)
        target = daily_target()
        if score >= target and old_daily < target:
            reward = 75 + save.get("prestige", 0) * 10
            save["coins"] += reward
            add_message(f"DAILY CLEARED! +{reward} coins")
    grant_xp(run_xp)
    spawn_particles(bird_x, bird_y, [RED, WHITE, SKINS[save["selected_skin"]]["body"]], 28, 6)
    screen_shake = 14 if save["settings"]["screen_shake"] else 0
    flash_timer = 10
    save_game()

def update_clouds():
    for c in clouds:
        c["x"] -= c["speed"]
        if c["x"] < -100:
            c["x"] = WIDTH + random.randint(40, 160)
            c["y"] = random.randint(50, 320)

def update_particles():
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.04
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

def check_powerups():
    global shield, magnet_timer, slow_timer, double_timer
    br = bird_rect()
    for p in powerups[:]:
        pr = pygame.Rect(int(p["x"] - 14), int(p["y"] - 14), 28, 28)
        if br.colliderect(pr):
            if p["kind"] == "shield":
                shield = 1
                add_message("SHIELD!")
            elif p["kind"] == "magnet":
                magnet_timer = 420
                add_message("MAGNET!")
            elif p["kind"] == "slow":
                slow_timer = 360
                add_message("SLOW-MO!")
            elif p["kind"] == "double":
                double_timer = 420
                add_message("x2 COINS!")
            save["stats"]["powerups_collected"] = save["stats"].get("powerups_collected", 0) + 1
            spawn_particles(p["x"], p["y"], [CYAN, GOLD, WHITE], 16, 4)
            powerups.remove(p)

def update_game():
    global bird_y, bird_vel, spawn_timer, score, combo, run_coins, run_xp
    global ground_offset, boss_mode, boss_timer, boss_target
    global shield, magnet_timer, slow_timer, double_timer, invuln_timer
    global screen_shake, flash_timer, near_misses, ghost_tick, fever_bonus_claimed

    gravity_now = GRAVITY * (1.12 if save.get("selected_mode") == "tiny" else 1.0)
    bird_vel += gravity_now
    bird_y += bird_vel

    if magnet_timer > 0: magnet_timer -= 1
    if slow_timer > 0: slow_timer -= 1
    if double_timer > 0: double_timer -= 1
    if invuln_timer > 0: invuln_timer -= 1
    if screen_shake > 0: screen_shake -= 1
    if flash_timer > 0: flash_timer -= 1

    speed = get_pipe_speed()
    ground_offset = (ground_offset + speed) % 40

    spawn_timer += 1
    if spawn_timer >= get_spawn_delay():
        create_pipe()
        spawn_timer = 0

    if not boss_mode and score > 0 and score % 20 == 0 and boss_target != score:
        boss_mode = True
        boss_timer = 480
        boss_target = score
        add_message("BOSS SECTION!")

    if boss_mode:
        boss_timer -= 1
        if boss_timer <= 0:
            boss_mode = False
            save["stats"]["bosses_cleared"] += 1
            save["coins"] += 25
            run_coins += 25
            unlock_achievement("boss_clear")
            add_message("BOSS CLEARED! +25 coins")

    gap = get_pipe_gap()

    for pipe in pipes[:]:
        pipe["x"] -= speed

        if pipe["moving"]:
            pipe["move_phase"] += 0.035
            pipe["gap_y"] = pipe["base_gap_y"] + math.sin(pipe["move_phase"]) * 42

        if pipe["coin"] and not pipe["coin_collected"]:
            coin_x = pipe["x"] + 37
            coin_y = pipe["gap_y"]
            cr = pygame.Rect(int(coin_x - 13), int(coin_y - 13), 26, 26)

            if magnet_timer > 0 and math.hypot(bird_x - coin_x, bird_y - coin_y) < 170:
                cr.center = (bird_x, int(bird_y))

            if bird_rect().colliderect(cr):
                pipe["coin_collected"] = True
                gain = 2 if double_timer > 0 else 1
                gain = max(1, int(round(gain * DIFFICULTIES[save["difficulty"]]["coin_mult"])))
                save["coins"] += gain
                run_coins += gain
                run_xp += 3
                spawn_particles(coin_x, coin_y, [GOLD, YELLOW, WHITE], 14, 4)

        if not pipe["scored"] and pipe["x"] + 75 < bird_x:
            pipe["scored"] = True
            score += 1
            combo += 1

            # Reward multiplier must be defined BEFORE the fever bonus uses it.
            # Daily mode is included too, otherwise selecting Daily Challenge
            # would raise KeyError: 'daily' after passing a pipe.
            mode = save.get("selected_mode", "classic")
            mode_bonus = {
                "classic": 1.0,
                "turbo": 1.2,
                "tiny": 1.15,
                "chaos": 1.35,
                "hardcore": 1.6,
                "daily": 1.25,
            }.get(mode, 1.0)
            reward_mult = mode_bonus * prestige_multiplier()

            if combo >= 12 and score // 5 > fever_bonus_claimed:
                fever_bonus_claimed = score // 5
                fever_gain = max(1, int(3 * reward_mult))
                save["coins"] += fever_gain
                run_coins += fever_gain
                add_message(f"FEVER BONUS +{fever_gain}", 55)

            run_xp += max(1, int((5 + combo // 4) * mode_bonus * prestige_multiplier()))
            if score % 5 == 0:
                bonus_coin = max(1, int(mode_bonus * prestige_multiplier()))
                save["coins"] += bonus_coin
                run_coins += bonus_coin

            if pipe["golden"]:
                bonus = 4 if double_timer > 0 else 2
                save["coins"] += bonus
                run_coins += bonus
                add_message(f"GOLDEN PIPE +{bonus}")

            if random.random() < 0.12:
                spawn_powerup(pipe["x"] + 110, pipe["gap_y"])

            check_achievements()
            check_mission()

        if not pipe["near_checked"] and abs((pipe["x"] + 75) - bird_x) < 10:
            pipe["near_checked"] = True
            top = pipe["gap_y"] - gap / 2
            bottom = pipe["gap_y"] + gap / 2
            margin = min(abs((bird_y + 14) - bottom), abs((bird_y - 14) - top))
            if margin < 14:
                near_misses += 1
                save["stats"]["near_misses"] = save["stats"].get("near_misses", 0) + 1
                run_xp += 2
                add_message("NEAR MISS +2 XP", 50)

        if pipe["x"] + 75 < -20:
            pipes.remove(pipe)

    for p in powerups[:]:
        p["x"] -= speed
        if p["x"] < -40:
            powerups.remove(p)

    check_powerups()

    br = bird_rect()
    collided = br.top <= 0 or br.bottom >= HEIGHT - GROUND_HEIGHT

    if not collided:
        for pipe in pipes:
            x = int(pipe["x"])
            top_h = int(pipe["gap_y"] - gap / 2)
            bottom_y = int(pipe["gap_y"] + gap / 2)
            top_rect = pygame.Rect(x, 0, 75, max(0, top_h))
            bottom_rect = pygame.Rect(x, bottom_y, 75, HEIGHT - GROUND_HEIGHT - bottom_y)
            if br.colliderect(top_rect) or br.colliderect(bottom_rect):
                collided = True
                break

    if collided and invuln_timer <= 0:
        if shield > 0 and save.get("selected_mode") != "hardcore":
            shield = 0
            invuln_timer = 90
            bird_vel = FLAP * 0.7
            spawn_particles(bird_x, bird_y, [CYAN, WHITE], 20, 5)
            add_message("SHIELD SAVED YOU!")
        else:
            game_over()
            return

    update_particles()
    update_clouds()
    save["high_score"] = max(save["high_score"], score)

def draw_clouds(surface):
    _, _, cloud_color = get_world_colors()
    for c in clouds:
        x, y, s = int(c["x"]), int(c["y"]), c["size"]
        pygame.draw.circle(surface, cloud_color, (x, y), s)
        pygame.draw.circle(surface, cloud_color, (x + s, y + 6), int(s * 0.75))
        pygame.draw.circle(surface, cloud_color, (x - s, y + 7), int(s * 0.68))

def draw_parallax(surface):
    world = save.get("selected_world", "meadow")
    t = pygame.time.get_ticks() / 1000.0
    if world in ("sunset", "night", "storm"):
        far_col = (90, 90, 125) if world != "sunset" else (150, 90, 110)
        near_col = (55, 60, 85) if world != "sunset" else (105, 70, 90)
        for layer, (col, speed, base_y, step) in enumerate([
            (far_col, 10, HEIGHT-GROUND_HEIGHT-125, 58),
            (near_col, 22, HEIGHT-GROUND_HEIGHT-82, 44),
        ]):
            offset = int(t * speed) % step
            for x in range(-step, WIDTH + step, step):
                h = 35 + ((x // step + layer * 3) % 5) * 13
                pygame.draw.rect(surface, col, (x-offset, base_y-h, step-7, h))
                if world == "night":
                    for wy in range(base_y-h+10, base_y-8, 15):
                        pygame.draw.rect(surface, (210,190,100), (x-offset+10, wy, 4, 5))
    else:
        offset = int(t * 12) % 120
        for x in range(-120, WIDTH+120, 120):
            pygame.draw.circle(surface, (90,170,105), (x-offset, HEIGHT-GROUND_HEIGHT-25), 70)

def draw_ghost(surface):
    if not ghost_playback or not save.get("settings", {}).get("ghost", True):
        return
    frame = ghost_tick // 4
    if 0 <= frame < len(ghost_playback):
        gy = ghost_playback[frame]
        ghost = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(ghost, (255,255,255,75), (20,20), 13)
        pygame.draw.circle(ghost, (80,220,240,80), (20,20), 17, 2)
        surface.blit(ghost, ghost.get_rect(center=(bird_x, int(gy))))

def draw_background(surface):
    sky, _, _ = get_world_colors()
    surface.fill(sky)
    world = save["selected_world"]

    if world == "night":
        for pos in [(30,60),(90,110),(170,70),(260,130),(350,50),(430,120),(480,70)]:
            pygame.draw.circle(surface, WHITE, pos, 2)
        pygame.draw.circle(surface, (245,245,215), (430, 80), 28)
    elif world == "storm":
        for i in range(18):
            x = (i * 47 + pygame.time.get_ticks() // 8) % WIDTH
            y = (i * 83 + pygame.time.get_ticks() // 5) % (HEIGHT - GROUND_HEIGHT)
            pygame.draw.line(surface, (170,190,220), (x, y), (x - 8, y + 16), 2)
    else:
        pygame.draw.circle(surface, YELLOW, (430, 80), 30)

    draw_clouds(surface)
    draw_parallax(surface)

def draw_ground(surface):
    _, ground_col, _ = get_world_colors()
    pygame.draw.rect(surface, ground_col, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(surface, GROUND_DARK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, 10))
    for x in range(-40, WIDTH + 40, 40):
        pygame.draw.rect(surface, (235, 205, 115),
                         (int(x - ground_offset), HEIGHT - GROUND_HEIGHT + 18, 22, 7))

def draw_bird(surface, x=None, y=None, angle=None):
    if x is None: x = bird_x
    if y is None: y = bird_y

    skin = SKINS[save["selected_skin"]]
    bird = pygame.Surface((64, 64), pygame.SRCALPHA)
    wing_offset = int(math.sin(pygame.time.get_ticks() * 0.025) * 4)

    pygame.draw.circle(bird, skin["body"], (28, 32), 17)
    pygame.draw.ellipse(bird, skin["wing"], (8, 31 + wing_offset, 22, 13))
    pygame.draw.circle(bird, WHITE, (37, 25), 7)
    pygame.draw.circle(bird, BLACK, (40, 25), 3)
    pygame.draw.polygon(bird, ORANGE, [(45,29),(60,34),(45,39)])

    if shield > 0:
        pygame.draw.circle(bird, CYAN, (28,32), 24, 2)

    if angle is None:
        angle = max(-70, min(28, -bird_vel * 5))

    bird = pygame.transform.rotate(bird, angle)
    surface.blit(bird, bird.get_rect(center=(int(x), int(y))))

    trail = save["selected_trail"]
    if trail != "none" and save["settings"]["particles"] and random.random() < 0.35:
        colors = {
            "spark": [GOLD, WHITE],
            "fire": [RED, ORANGE, YELLOW],
            "void": [PURPLE, PINK, CYAN],
        }[trail]
        spawn_particles(x - 18, y + 5, colors, 1, 1.5)

def draw_pipes(surface):
    gap = get_pipe_gap()
    for pipe in pipes:
        x = int(pipe["x"])
        gy = int(pipe["gap_y"])
        top_h = int(gy - gap / 2)
        bottom_y = int(gy + gap / 2)

        col = GOLD if pipe["golden"] else GREEN
        dark = ORANGE if pipe["golden"] else DARK_GREEN

        pygame.draw.rect(surface, col, (x, 0, 75, max(0, top_h)))
        pygame.draw.rect(surface, col, (x, bottom_y, 75, HEIGHT - GROUND_HEIGHT - bottom_y))
        pygame.draw.rect(surface, dark, (x - 5, max(0, top_h - 28), 85, 28))
        pygame.draw.rect(surface, dark, (x - 5, bottom_y, 85, 28))

        if pipe["moving"]:
            pygame.draw.circle(surface, CYAN, (x + 37, gy), 4)

        if pipe["coin"] and not pipe["coin_collected"]:
            w = max(5, int(22 * abs(math.sin(pygame.time.get_ticks() * 0.01))))
            pygame.draw.ellipse(surface, GOLD, (x + 37 - w//2, gy - 14, w, 28))

def draw_powerups(surface):
    icons = {"shield":"S", "magnet":"M", "slow":"T", "double":"2X"}
    colors = {"shield":CYAN, "magnet":PURPLE, "slow":BLUE, "double":GOLD}
    for p in powerups:
        pygame.draw.circle(surface, colors[p["kind"]], (int(p["x"]), int(p["y"])), 15)
        txt = FONT_TINY.render(icons[p["kind"]], True, BLACK)
        surface.blit(txt, txt.get_rect(center=(int(p["x"]), int(p["y"]))))

def draw_particles(surface):
    for p in particles:
        pygame.draw.circle(surface, p["color"], (int(p["x"]), int(p["y"])), p["size"])

def draw_hud(surface):
    score_t = FONT_BIG.render(str(score), True, WHITE)
    surface.blit(score_t, (WIDTH//2 - score_t.get_width()//2, 28))

    lines = [
        f"Coins: {save['coins']}",
        f"Best: {save['high_score']}",
        f"Combo: x{combo}",
        f"LVL: {save['level']}",
    ]
    for i, line in enumerate(lines):
        t = FONT_TINY.render(line, True, GOLD if i == 0 else WHITE)
        surface.blit(t, (18, 15 + i*19))

    buffs = []
    if shield: buffs.append("SHIELD")
    if magnet_timer: buffs.append("MAGNET")
    if slow_timer: buffs.append("SLOW")
    if double_timer: buffs.append("x2")
    if boss_mode: buffs.append("BOSS")
    if combo >= 12: buffs.append("FEVER")
    if save.get("selected_mode") == "daily": buffs.append("DAILY")
    if buffs:
        t = FONT_TINY.render(" | ".join(buffs), True, CYAN)
        surface.blit(t, (WIDTH - t.get_width() - 12, 15))

    m = save["mission"]
    prog = min(mission_progress(), m["target"])
    mt = FONT_TINY.render(f"Mission: {m['text']} [{prog}/{m['target']}]", True, WHITE)
    surface.blit(mt, (WIDTH//2 - mt.get_width()//2, HEIGHT - GROUND_HEIGHT - 28))

def draw_message(surface):
    if message_timer > 0 and message_text:
        t = FONT_SMALL.render(message_text, True, WHITE)
        x = WIDTH//2 - t.get_width()//2
        surface.blit(t, (x, 112))

def draw_game():
    surf = pygame.Surface((WIDTH, HEIGHT))
    draw_background(surf)
    draw_pipes(surf)
    draw_powerups(surf)
    draw_particles(surf)
    draw_ghost(surf)
    draw_bird(surf)
    draw_ground(surf)
    draw_hud(surf)
    draw_message(surf)

    sx = sy = 0
    if screen_shake > 0 and save["settings"]["screen_shake"]:
        sx = random.randint(-5,5)
        sy = random.randint(-5,5)

    SCREEN.fill(BLACK)
    SCREEN.blit(surf, (sx, sy))

def draw_menu():
    draw_background(SCREEN)
    draw_ground(SCREEN)

    title = FONT_BIG.render(" FLAPPY", True, WHITE)
    sub = FONT_SMALL.render("MEGABUILD - ULTIMATE EDITION", True, GOLD)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 90))
    SCREEN.blit(sub, (WIDTH//2-sub.get_width()//2, 150))
    if save.get("daily_reward_pending", 0):
        daily = FONT_TINY.render(f"DAILY REWARD +{save['daily_reward_pending']} COINS | Streak {save.get('daily_streak',1)}", True, GOLD)
        SCREEN.blit(daily, (WIDTH//2-daily.get_width()//2, 185))

    bob = math.sin(pygame.time.get_ticks()*0.004)*9
    draw_bird(SCREEN, WIDTH//2, 255+bob, 0)

    items = [
        ("SPACE", "PLAY"),
        ("G", "SHOP"),
        ("W", "WORLD"),
        ("D", "DIFFICULTY"),
        ("T", "STATS"),
        ("A", "ACHIEVEMENTS"),
        ("S", "SETTINGS"),
        ("M", "GAME MODE"),
        ("P", "PROFILE / PRESTIGE"),
        ("H", "HALL OF FAME"),
        ("C", "DAILY CHALLENGE"),
    ]
    y = 360
    for key, label in items:
        t = FONT_MEDIUM.render(f"{key} = {label}", True, WHITE if key != "SPACE" else CYAN)
        SCREEN.blit(t, (WIDTH//2-t.get_width()//2, y))
        y += 30

    info = FONT_TINY.render(
        f"{player_title()} | Best {save['high_score']} | Coins {save['coins']} | LVL {save['level']} | P{save.get('prestige',0)}",
        True, GOLD)
    SCREEN.blit(info, (WIDTH//2-info.get_width()//2, 690))

def draw_shop():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("SHOP", True, WHITE)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 50))

    tab = FONT_SMALL.render(f"TAB: {shop_tab.upper()}   Q = switch", True, CYAN)
    SCREEN.blit(tab, (WIDTH//2-tab.get_width()//2, 110))

    if shop_tab == "skins":
        ids = SKIN_ORDER
        item_id = ids[shop_index % len(ids)]
        item = SKINS[item_id]
        owned = item_id in save["owned_skins"]
        selected = item_id == save["selected_skin"]

        pygame.draw.circle(SCREEN, item["body"], (WIDTH//2, 260), 60)
        name = FONT_MEDIUM.render(f"{item['name']} [{item['rarity']}]", True, item["body"])
        SCREEN.blit(name, (WIDTH//2-name.get_width()//2, 350))

        if selected:
            status = "SELECTED"
        elif owned:
            status = "ENTER = SELECT"
        else:
            status = f"ENTER = BUY ({item['price']} coins)"
    else:
        ids = TRAIL_ORDER
        item_id = ids[shop_index % len(ids)]
        item = TRAILS[item_id]
        owned = item_id in save["owned_trails"]
        selected = item_id == save["selected_trail"]

        name = FONT_MEDIUM.render(item["name"], True, GOLD)
        SCREEN.blit(name, (WIDTH//2-name.get_width()//2, 300))
        if selected:
            status = "SELECTED"
        elif owned:
            status = "ENTER = SELECT"
        else:
            status = f"ENTER = BUY ({item['price']} coins)"

    st = FONT_SMALL.render(status, True, GOLD if not selected else GREEN)
    SCREEN.blit(st, (WIDTH//2-st.get_width()//2, 430))

    nav = FONT_SMALL.render("A / D = browse    ESC = back", True, WHITE)
    SCREEN.blit(nav, (WIDTH//2-nav.get_width()//2, 520))
    coins = FONT_SMALL.render(f"Coins: {save['coins']}", True, GOLD)
    SCREEN.blit(coins, (WIDTH//2-coins.get_width()//2, 570))

def draw_worlds():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("WORLDS", True, WHITE)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 60))
    wid = WORLD_ORDER[world_index % len(WORLD_ORDER)]
    world = WORLDS[wid]
    unlocked = save["level"] >= world["unlock"]
    name = FONT_MEDIUM.render(world["name"], True, CYAN if unlocked else RED)
    SCREEN.blit(name, (WIDTH//2-name.get_width()//2, 230))
    info = "ENTER = SELECT" if unlocked else f"Unlock at LVL {world['unlock']}"
    t = FONT_SMALL.render(info, True, WHITE)
    SCREEN.blit(t, (WIDTH//2-t.get_width()//2, 300))
    nav = FONT_SMALL.render("A / D = browse    ESC = back", True, WHITE)
    SCREEN.blit(nav, (WIDTH//2-nav.get_width()//2, 500))

def draw_difficulty():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("DIFFICULTY", True, WHITE)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 60))
    did = DIFFICULTY_ORDER[difficulty_index % len(DIFFICULTY_ORDER)]
    d = DIFFICULTIES[did]
    name = FONT_MEDIUM.render(d["name"], True, GOLD)
    SCREEN.blit(name, (WIDTH//2-name.get_width()//2, 250))
    info = FONT_SMALL.render("ENTER = SELECT    A/D = browse", True, WHITE)
    SCREEN.blit(info, (WIDTH//2-info.get_width()//2, 340))

def draw_modes():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("GAME MODES", True, WHITE)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 55))
    mid = MODE_ORDER[mode_index % len(MODE_ORDER)]
    mode = GAME_MODES[mid]
    unlocked = save["level"] >= mode["unlock"] or save.get("prestige", 0) > 0
    col = CYAN if unlocked else RED
    name = FONT_MEDIUM.render(mode["name"], True, col)
    SCREEN.blit(name, (WIDTH//2-name.get_width()//2, 210))
    desc = FONT_SMALL.render(mode["desc"], True, WHITE)
    SCREEN.blit(desc, (WIDTH//2-desc.get_width()//2, 270))
    best = save.get("best_mode_scores", {}).get(mid, 0)
    bt = FONT_SMALL.render(f"Best: {best}", True, GOLD)
    SCREEN.blit(bt, (WIDTH//2-bt.get_width()//2, 320))
    state = "ENTER = SELECT" if unlocked else f"Unlock at LVL {mode['unlock']}"
    st = FONT_SMALL.render(state, True, col)
    SCREEN.blit(st, (WIDTH//2-st.get_width()//2, 390))
    nav = FONT_SMALL.render("A/D = browse   ESC = back", True, WHITE)
    SCREEN.blit(nav, (WIDTH//2-nav.get_width()//2, 520))

def draw_hall():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("HALL OF FAME", True, GOLD)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 45))
    board = save.get("leaderboard", [])
    if not board:
        t = FONT_SMALL.render("No legendary runs yet.", True, GRAY)
        SCREEN.blit(t, (WIDTH//2-t.get_width()//2, 180))
    y = 135
    for i, e in enumerate(board[:10], 1):
        line = f"#{i}  {e.get('score',0)}  | {e.get('mode','classic')} | {e.get('world','meadow')}"
        col = GOLD if i == 1 else WHITE
        t = FONT_SMALL.render(line, True, col)
        SCREEN.blit(t, (55, y))
        y += 45
    back = FONT_SMALL.render("ESC = back", True, GRAY)
    SCREEN.blit(back, (WIDTH//2-back.get_width()//2, 700))

def draw_daily():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("DAILY CHALLENGE", True, CYAN)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 55))
    today = date.today().isoformat()
    best = save.get("daily_best", {}).get(today, 0)
    target = daily_target()
    lines = [
        f"Date: {today}",
        f"Modifier: {daily_modifier()}",
        f"Target score: {target}",
        f"Today's best: {best}",
        "ENTER = select Daily mode",
        "Same seed all day. No excuses gng.",
    ]
    y = 180
    for i, line in enumerate(lines):
        t = FONT_SMALL.render(line, True, GOLD if i == 2 else WHITE)
        SCREEN.blit(t, (WIDTH//2-t.get_width()//2, y))
        y += 55
    back = FONT_SMALL.render("ESC = back", True, GRAY)
    SCREEN.blit(back, (WIDTH//2-back.get_width()//2, 680))

def draw_profile():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("PROFILE", True, WHITE)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 50))
    lines = [
        f"Title: {player_title()}",
        f"Level: {save['level']}",
        f"XP: {save['xp']}/{xp_needed(save['level'])}",
        f"Prestige: {save.get('prestige',0)}",
        f"Permanent bonus: +{int((prestige_multiplier()-1)*100)}% XP/reward",
        f"Daily streak: {save.get('daily_streak',0)}",
        f"Mode: {GAME_MODES[save.get('selected_mode','classic')]['name']}",
    ]
    y = 160
    for line in lines:
        t = FONT_SMALL.render(line, True, GOLD if "Title" in line else WHITE)
        SCREEN.blit(t, (70, y))
        y += 45
    can = save["level"] >= 30
    msg = "R = PRESTIGE (reset LVL, gain permanent bonus)" if can else "Prestige unlocks at LVL 30"
    mt = FONT_SMALL.render(msg, True, CYAN if can else GRAY)
    SCREEN.blit(mt, (WIDTH//2-mt.get_width()//2, 540))
    back = FONT_SMALL.render("ESC = back", True, WHITE)
    SCREEN.blit(back, (WIDTH//2-back.get_width()//2, 620))

def do_prestige():
    if save["level"] < 30:
        return
    save["prestige"] = save.get("prestige", 0) + 1
    save["level"] = 1
    save["xp"] = 0
    save["coins"] += 100 + save["prestige"] * 25
    save_game()
    add_message("PRESTIGE COMPLETE!")

def draw_stats():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("STATS", True, WHITE)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 45))
    stats = save["stats"]
    lines = [
        f"High score: {save['high_score']}",
        f"Level: {save['level']}   XP: {save['xp']}/{xp_needed(save['level'])}",
        f"Coins: {save['coins']}",
        f"Runs: {stats['runs']}",
        f"Deaths: {stats['deaths']}",
        f"Total score: {stats['total_score']}",
        f"Total coins collected: {stats['total_coins_collected']}",
        f"Best combo: {stats['best_combo']}",
        f"Bosses cleared: {stats['bosses_cleared']}",
        f"Powerups collected: {stats.get('powerups_collected',0)}",
        f"Near misses: {stats.get('near_misses',0)}",
        f"Prestige: {save.get('prestige',0)}",
    ]
    y = 150
    for line in lines:
        t = FONT_SMALL.render(line, True, WHITE)
        SCREEN.blit(t, (80, y))
        y += 45
    back = FONT_SMALL.render("ESC = back", True, GRAY)
    SCREEN.blit(back, (WIDTH//2-back.get_width()//2, 680))

def draw_achievements():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("ACHIEVEMENTS", True, WHITE)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 35))
    y = 115
    for key, ach in ACHIEVEMENTS.items():
        unlocked = key in save["achievements"]
        mark = "[X]" if unlocked else "[ ]"
        col = GREEN if unlocked else GRAY
        t = FONT_TINY.render(f"{mark} {ach['name']} - {ach['desc']} (+{ach['reward']})", True, col)
        SCREEN.blit(t, (35, y))
        y += 54
    back = FONT_SMALL.render("ESC = back", True, WHITE)
    SCREEN.blit(back, (WIDTH//2-back.get_width()//2, 700))

def draw_settings():
    SCREEN.fill(DARKER)
    title = FONT_BIG.render("SETTINGS", True, WHITE)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 60))
    shake = "ON" if save["settings"]["screen_shake"] else "OFF"
    parts = "ON" if save["settings"]["particles"] else "OFF"
    ghost = "ON" if save["settings"].get("ghost", True) else "OFF"
    lines = [
        f"1 = Screen shake: {shake}",
        f"2 = Particles: {parts}",
        f"3 = Best-run ghost: {ghost}",
        "ESC = back",
    ]
    y = 230
    for line in lines:
        t = FONT_MEDIUM.render(line, True, WHITE)
        SCREEN.blit(t, (WIDTH//2-t.get_width()//2, y))
        y += 70

def draw_pause():
    o = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    o.fill((0,0,0,175))
    SCREEN.blit(o,(0,0))
    t = FONT_BIG.render("PAUSED", True, WHITE)
    SCREEN.blit(t, (WIDTH//2-t.get_width()//2, 240))
    for i, line in enumerate(["ESC = resume", "R = restart", "M = menu"]):
        s = FONT_SMALL.render(line, True, WHITE)
        SCREEN.blit(s, (WIDTH//2-s.get_width()//2, 350+i*45))

def draw_gameover():
    o = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    o.fill((0,0,0,185))
    SCREEN.blit(o,(0,0))
    title = FONT_BIG.render("GAME OVER", True, RED)
    SCREEN.blit(title, (WIDTH//2-title.get_width()//2, 150))

    medal = "NONE"
    col = GRAY
    if score >= 40: medal, col = "DIAMOND", CYAN
    elif score >= 25: medal, col = "GOLD", GOLD
    elif score >= 15: medal, col = "SILVER", LIGHT_GRAY
    elif score >= 5: medal, col = "BRONZE", ORANGE

    lines = [
        f"Score: {score}",
        f"Best: {save['high_score']}",
        f"Coins this run: {run_coins}",
        f"XP this run: {run_xp}",
        f"Near misses: {near_misses}",
        f"Medal: {medal}",
    ]
    y = 260
    for i, line in enumerate(lines):
        t = FONT_SMALL.render(line, True, col if i == 5 else WHITE)
        SCREEN.blit(t, (WIDTH//2-t.get_width()//2, y))
        y += 42

    for i, line in enumerate(["R = restart", "M = menu"]):
        t = FONT_SMALL.render(line, True, CYAN if i == 0 else WHITE)
        SCREEN.blit(t, (WIDTH//2-t.get_width()//2, 580+i*38))

def shop_action():
    if shop_tab == "skins":
        item_id = SKIN_ORDER[shop_index % len(SKIN_ORDER)]
        item = SKINS[item_id]
        if item_id in save["owned_skins"]:
            save["selected_skin"] = item_id
        elif save["coins"] >= item["price"]:
            save["coins"] -= item["price"]
            save["owned_skins"].append(item_id)
            save["selected_skin"] = item_id
    else:
        item_id = TRAIL_ORDER[shop_index % len(TRAIL_ORDER)]
        item = TRAILS[item_id]
        if item_id in save["owned_trails"]:
            save["selected_trail"] = item_id
        elif save["coins"] >= item["price"]:
            save["coins"] -= item["price"]
            save["owned_trails"].append(item_id)
            save["selected_trail"] = item_id
    save_game()

for j in range(pygame.joystick.get_count()):
    try:
        pygame.joystick.Joystick(j).init()
    except pygame.error:
        pass

running = True
while running:
    CLOCK.tick(FPS)

    if message_timer > 0:
        message_timer -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_SPACE:
                    save["daily_reward_pending"] = 0
                    save_game()
                    reset_run()
                    bird_vel = FLAP
                elif event.key == pygame.K_g:
                    shop_tab = "skins"
                    shop_index = 0
                    game_state = "shop"
                elif event.key == pygame.K_w:
                    world_index = WORLD_ORDER.index(save["selected_world"])
                    game_state = "worlds"
                elif event.key == pygame.K_d:
                    difficulty_index = DIFFICULTY_ORDER.index(save["difficulty"])
                    game_state = "difficulty"
                elif event.key == pygame.K_t:
                    game_state = "stats"
                elif event.key == pygame.K_a:
                    game_state = "achievements"
                elif event.key == pygame.K_s:
                    game_state = "settings"
                elif event.key == pygame.K_m:
                    mode_index = MODE_ORDER.index(save.get("selected_mode", "classic"))
                    game_state = "modes"
                elif event.key == pygame.K_p:
                    game_state = "profile"
                elif event.key == pygame.K_h:
                    game_state = "hall"
                elif event.key == pygame.K_c:
                    game_state = "daily"
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == "playing":
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    bird_vel = FLAP
                    spawn_particles(bird_x-15, bird_y+8, [WHITE, SKINS[save["selected_skin"]]["wing"]], 5, 2)
                elif event.key == pygame.K_ESCAPE:
                    game_state = "paused"

            elif game_state == "paused":
                if event.key == pygame.K_ESCAPE:
                    game_state = "playing"
                elif event.key == pygame.K_r:
                    reset_run()
                elif event.key == pygame.K_m:
                    game_state = "menu"

            elif game_state == "gameover":
                if event.key == pygame.K_r:
                    reset_run()
                elif event.key == pygame.K_m:
                    game_state = "menu"

            elif game_state == "shop":
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    shop_index -= 1
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    shop_index += 1
                elif event.key == pygame.K_q:
                    shop_tab = "trails" if shop_tab == "skins" else "skins"
                    shop_index = 0
                elif event.key == pygame.K_RETURN:
                    shop_action()
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "worlds":
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    world_index -= 1
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    world_index += 1
                elif event.key == pygame.K_RETURN:
                    wid = WORLD_ORDER[world_index % len(WORLD_ORDER)]
                    if save["level"] >= WORLDS[wid]["unlock"]:
                        save["selected_world"] = wid
                        save_game()
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "difficulty":
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    difficulty_index -= 1
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    difficulty_index += 1
                elif event.key == pygame.K_RETURN:
                    did = DIFFICULTY_ORDER[difficulty_index % len(DIFFICULTY_ORDER)]
                    save["difficulty"] = did
                    save_game()
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "modes":
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    mode_index -= 1
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    mode_index += 1
                elif event.key == pygame.K_RETURN:
                    mid = MODE_ORDER[mode_index % len(MODE_ORDER)]
                    if save["level"] >= GAME_MODES[mid]["unlock"] or save.get("prestige",0) > 0:
                        save["selected_mode"] = mid
                        save_game()
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "profile":
                if event.key == pygame.K_r:
                    do_prestige()
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "hall":
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "daily":
                if event.key == pygame.K_RETURN:
                    save["selected_mode"] = "daily"
                    save_game()
                    game_state = "menu"
                    add_message("Daily Challenge selected")
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state in ("stats", "achievements"):
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            elif game_state == "settings":
                if event.key == pygame.K_1:
                    save["settings"]["screen_shake"] = not save["settings"]["screen_shake"]
                    save_game()
                elif event.key == pygame.K_2:
                    save["settings"]["particles"] = not save["settings"]["particles"]
                    save_game()
                elif event.key == pygame.K_3:
                    save["settings"]["ghost"] = not save["settings"].get("ghost", True)
                    save_game()
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"

        if event.type == pygame.JOYBUTTONDOWN and game_state == "playing":
            if event.button == 0:
                bird_vel = FLAP

    if game_state == "playing":
        play_frame_counter += 1
        if play_frame_counter >= FPS:
            save["stats"]["play_seconds"] = save["stats"].get("play_seconds", 0) + 1
            play_frame_counter = 0
        update_game()
    elif game_state == "menu":
        update_clouds()
        update_particles()

    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "paused":
        draw_game()
        draw_pause()
    elif game_state == "gameover":
        draw_game()
        draw_gameover()
    elif game_state == "shop":
        draw_shop()
    elif game_state == "worlds":
        draw_worlds()
    elif game_state == "difficulty":
        draw_difficulty()
    elif game_state == "modes":
        draw_modes()
    elif game_state == "profile":
        draw_profile()
    elif game_state == "hall":
        draw_hall()
    elif game_state == "daily":
        draw_daily()
    elif game_state == "stats":
        draw_stats()
    elif game_state == "achievements":
        draw_achievements()
    elif game_state == "settings":
        draw_settings()

    pygame.display.flip()

save_game()
pygame.quit()
sys.exit()
