import pygame
import random
import sys
import os
import json
import math

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 700
HEIGHT = 850
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" RACING V4")

CLOCK = pygame.time.Clock()


# =========================================================
# COLORS
# =========================================================

BLACK = (15, 15, 18)
DARK = (25, 25, 30)
DARKER = (10, 10, 14)

WHITE = (240, 240, 245)
GRAY = (120, 120, 130)
LIGHT_GRAY = (180, 180, 190)

BLUE = (45, 125, 245)
LIGHT_BLUE = (90, 190, 255)

RED = (220, 50, 55)
GREEN = (55, 200, 95)
YELLOW = (250, 210, 55)
ORANGE = (245, 130, 45)
PURPLE = (155, 80, 230)

GOLD = (255, 205, 40)


# =========================================================
# FONTS
# =========================================================

FONT_HUGE = pygame.font.Font(None, 90)
FONT_BIG = pygame.font.Font(None, 70)
FONT_MEDIUM = pygame.font.Font(None, 42)
FONT_SMALL = pygame.font.Font(None, 28)
FONT_TINY = pygame.font.Font(None, 22)


# =========================================================
# SAVE FILE
# =========================================================

FOLDER = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(FOLDER, "racing_save.json")


# =========================================================
# CARS
# =========================================================

CARS = {
    "starter": {
        "name": "STARTER",
        "price": 0,
        "color": BLUE,
        "max_speed": 17,
        "handling": 1.0,
        "health": 100
    },

    "speedster": {
        "name": "SPEEDSTER",
        "price": 40,
        "color": RED,
        "max_speed": 22,
        "handling": 0.90,
        "health": 75
    },

    "tank": {
        "name": "TANK",
        "price": 65,
        "color": GREEN,
        "max_speed": 14,
        "handling": 0.75,
        "health": 170
    },

    "drifter": {
        "name": "DRIFTER",
        "price": 90,
        "color": PURPLE,
        "max_speed": 19,
        "handling": 1.45,
        "health": 90
    }
}

CAR_ORDER = [
    "starter",
    "speedster",
    "tank",
    "drifter"
]


# =========================================================
# MAPS
# =========================================================

MAPS = {
    "night_city": {
        "name": "NIGHT CITY",

        "road": (42, 42, 52),
        "road_edge": (80, 160, 255),
        "ground": (12, 12, 25),

        "line": (210, 220, 255),

        "accent": LIGHT_BLUE,

        "description": "Neon lights & city streets"
    },

    "desert": {
        "name": "DESERT HIGHWAY",

        "road": (70, 65, 60),
        "road_edge": (240, 210, 120),
        "ground": (190, 145, 70),

        "line": (245, 230, 190),

        "accent": ORANGE,

        "description": "Hot sand & endless highway"
    },

    "forest": {
        "name": "FOREST ROAD",

        "road": (48, 50, 48),
        "road_edge": (210, 220, 210),
        "ground": (25, 80, 35),

        "line": (235, 235, 220),

        "accent": GREEN,

        "description": "Trees, grass & speed"
    }
}

MAP_ORDER = [
    "night_city",
    "desert",
    "forest"
]


# =========================================================
# LOAD SAVE
# =========================================================

def load_save():

    default = {
        "high_score": 0,
        "coins": 0,
        "owned_cars": ["starter"],
        "selected_car": "starter",
        "selected_map": "night_city"
    }

    try:

        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            default["high_score"] = data.get(
                "high_score",
                0
            )

            default["coins"] = data.get(
                "coins",
                0
            )

            default["owned_cars"] = data.get(
                "owned_cars",
                ["starter"]
            )

            default["selected_car"] = data.get(
                "selected_car",
                "starter"
            )

            default["selected_map"] = data.get(
                "selected_map",
                "night_city"
            )

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError
    ):
        pass

    if "starter" not in default["owned_cars"]:
        default["owned_cars"].append("starter")

    if default["selected_car"] not in CARS:
        default["selected_car"] = "starter"

    if default["selected_car"] not in default["owned_cars"]:
        default["selected_car"] = "starter"

    if default["selected_map"] not in MAPS:
        default["selected_map"] = "night_city"

    return default


save_data = load_save()

high_score = save_data["high_score"]
coins = save_data["coins"]

owned_cars = save_data["owned_cars"]

selected_car = save_data["selected_car"]
selected_map = save_data["selected_map"]


def save_game():

    try:

        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {
                    "high_score": high_score,
                    "coins": coins,
                    "owned_cars": owned_cars,
                    "selected_car": selected_car,
                    "selected_map": selected_map
                },
                file,
                indent=4
            )

    except OSError:
        pass


# =========================================================
# ROAD
# =========================================================

ROAD_X = 110
ROAD_WIDTH = 480

LANES = 3

LINE_HEIGHT = 80
LINE_GAP = 55
LINE_WIDTH = 8

road_offset = 0
scenery_offset = 0


def lane_center(lane):

    lane_width = ROAD_WIDTH / LANES

    return (
        ROAD_X
        + lane_width * lane
        + lane_width / 2
    )


# =========================================================
# PLAYER
# =========================================================

CAR_WIDTH = 58
CAR_HEIGHT = 105

player_x = WIDTH / 2 - CAR_WIDTH / 2
player_y = HEIGHT - 160

horizontal_speed = 0

BASE_X_ACCELERATION = 0.75
FRICTION_X = 0.84
BASE_MAX_X_SPEED = 9


# =========================================================
# SPEED
# =========================================================

speed = 3

MIN_SPEED = 3

ACCELERATION = 0.12
BRAKE_POWER = 0.22
NATURAL_SLOWDOWN = 0.025


def current_car():
    return CARS[selected_car]


def current_map():
    return MAPS[selected_map]


def get_max_speed():
    return current_car()["max_speed"]


def get_kmh():
    return int(speed * 14)


# =========================================================
# STATE
# =========================================================

screen_state = "menu"

score = 0
health = current_car()["health"]

enemies = []
coin_pickups = []
particles = []

spawn_timer = 0
coin_spawn_timer = 0

spawn_delay = 90
coin_spawn_delay = 150

invincible_timer = 0

shake_timer = 0
shake_strength = 0

flash_timer = 0

run_coins = 0

garage_index = CAR_ORDER.index(selected_car)
map_index = MAP_ORDER.index(selected_map)


# =========================================================
# PARTICLES
# =========================================================

def create_particles(x, y, colors, amount):

    for _ in range(amount):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        particle_speed = random.uniform(
            1.5,
            8
        )

        particles.append(
            {
                "x": x,
                "y": y,

                "vx": math.cos(angle) * particle_speed,
                "vy": math.sin(angle) * particle_speed,

                "life": random.randint(18, 45),

                "size": random.randint(2, 8),

                "color": random.choice(colors)
            }
        )


def create_crash_particles(x, y):

    create_particles(
        x,
        y,
        [
            ORANGE,
            YELLOW,
            RED,
            WHITE
        ],
        28
    )


def create_coin_particles(x, y):

    create_particles(
        x,
        y,
        [
            GOLD,
            YELLOW,
            WHITE
        ],
        14
    )


def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["vx"] *= 0.96
        particle["vy"] *= 0.96

        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(particle)


def draw_particles(surface):

    for particle in particles:

        pygame.draw.circle(
            surface,
            particle["color"],
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            particle["size"]
        )


# =========================================================
# CAR DRAWING
# =========================================================

def draw_car(
    surface,
    x,
    y,
    body_color,
    player=False,
    scale=1.0
):

    width = int(CAR_WIDTH * scale)
    height = int(CAR_HEIGHT * scale)

    x = int(x)
    y = int(y)

    pygame.draw.ellipse(
        surface,
        (15, 15, 18),
        (
            x - 5,
            y + 10,
            width + 10,
            height
        )
    )

    wheel_width = max(
        5,
        int(8 * scale)
    )

    wheel_height = max(
        12,
        int(24 * scale)
    )

    wheel_positions = [
        (
            x - 4,
            y + int(18 * scale)
        ),

        (
            x + width - wheel_width + 4,
            y + int(18 * scale)
        ),

        (
            x - 4,
            y + int(70 * scale)
        ),

        (
            x + width - wheel_width + 4,
            y + int(70 * scale)
        )
    ]

    for wx, wy in wheel_positions:

        pygame.draw.rect(
            surface,
            BLACK,
            (
                wx,
                wy,
                wheel_width,
                wheel_height
            ),
            border_radius=3
        )

    pygame.draw.rect(
        surface,
        body_color,
        (
            x,
            y,
            width,
            height
        ),
        border_radius=max(
            5,
            int(13 * scale)
        )
    )

    pygame.draw.rect(
        surface,
        DARK,
        (
            x + int(10 * scale),
            y + int(30 * scale),
            width - int(20 * scale),
            int(48 * scale)
        ),
        border_radius=max(
            4,
            int(9 * scale)
        )
    )

    pygame.draw.rect(
        surface,
        LIGHT_BLUE,
        (
            x + int(13 * scale),
            y + int(33 * scale),
            width - int(26 * scale),
            int(18 * scale)
        ),
        border_radius=4
    )

    pygame.draw.rect(
        surface,
        (55, 105, 145),
        (
            x + int(13 * scale),
            y + int(57 * scale),
            width - int(26 * scale),
            int(15 * scale)
        ),
        border_radius=4
    )

    pygame.draw.circle(
        surface,
        YELLOW,
        (
            x + int(12 * scale),
            y + int(8 * scale)
        ),
        max(
            3,
            int(5 * scale)
        )
    )

    pygame.draw.circle(
        surface,
        YELLOW,
        (
            x + width - int(12 * scale),
            y + int(8 * scale)
        ),
        max(
            3,
            int(5 * scale)
        )
    )

    if player:

        pygame.draw.rect(
            surface,
            WHITE,
            (
                x + width // 2 - 3,
                y + 3,
                6,
                height - 6
            ),
            border_radius=3
        )


# =========================================================
# SCENERY - NIGHT CITY
# =========================================================

def draw_night_city(surface):

    block_height = 130
    offset = int(scenery_offset % block_height)

    for y in range(
        -block_height + offset,
        HEIGHT + block_height,
        block_height
    ):

        # Left building
        pygame.draw.rect(
            surface,
            (20, 22, 38),
            (
                10,
                y,
                75,
                105
            ),
            border_radius=4
        )

        # Right building
        pygame.draw.rect(
            surface,
            (25, 20, 38),
            (
                WIDTH - 85,
                y,
                75,
                105
            ),
            border_radius=4
        )

        # Windows
        for wx in [25, 50]:

            for wy in range(
                y + 15,
                y + 90,
                25
            ):

                pygame.draw.rect(
                    surface,
                    random.choice(
                        [
                            (70, 180, 255),
                            (255, 90, 190),
                            (255, 210, 80)
                        ]
                    ),
                    (
                        wx,
                        wy,
                        10,
                        12
                    )
                )

        for wx in [
            WIDTH - 70,
            WIDTH - 45
        ]:

            for wy in range(
                y + 15,
                y + 90,
                25
            ):

                pygame.draw.rect(
                    surface,
                    random.choice(
                        [
                            (70, 180, 255),
                            (255, 90, 190),
                            (255, 210, 80)
                        ]
                    ),
                    (
                        wx,
                        wy,
                        10,
                        12
                    )
                )

        # Street lights
        pygame.draw.circle(
            surface,
            LIGHT_BLUE,
            (
                ROAD_X - 18,
                y + 115
            ),
            6
        )

        pygame.draw.circle(
            surface,
            LIGHT_BLUE,
            (
                ROAD_X + ROAD_WIDTH + 18,
                y + 115
            ),
            6
        )


# =========================================================
# SCENERY - DESERT
# =========================================================

def draw_cactus(surface, x, y):

    cactus_color = (
        35,
        115,
        55
    )

    pygame.draw.rect(
        surface,
        cactus_color,
        (
            x - 6,
            y - 35,
            12,
            45
        ),
        border_radius=5
    )

    pygame.draw.rect(
        surface,
        cactus_color,
        (
            x - 18,
            y - 22,
            14,
            8
        ),
        border_radius=4
    )

    pygame.draw.rect(
        surface,
        cactus_color,
        (
            x - 18,
            y - 30,
            8,
            16
        ),
        border_radius=4
    )

    pygame.draw.rect(
        surface,
        cactus_color,
        (
            x + 4,
            y - 14,
            17,
            8
        ),
        border_radius=4
    )

    pygame.draw.rect(
        surface,
        cactus_color,
        (
            x + 13,
            y - 25,
            8,
            18
        ),
        border_radius=4
    )


def draw_desert(surface):

    gap = 170
    offset = int(
        scenery_offset % gap
    )

    for y in range(
        -gap + offset,
        HEIGHT + gap,
        gap
    ):

        draw_cactus(
            surface,
            55,
            y + 80
        )

        draw_cactus(
            surface,
            WIDTH - 55,
            y
        )

        pygame.draw.circle(
            surface,
            (140, 105, 65),
            (
                85,
                y + 25
            ),
            10
        )

        pygame.draw.circle(
            surface,
            (140, 105, 65),
            (
                WIDTH - 90,
                y + 100
            ),
            13
        )


# =========================================================
# SCENERY - FOREST
# =========================================================

def draw_tree(surface, x, y):

    pygame.draw.rect(
        surface,
        (90, 55, 30),
        (
            x - 5,
            y,
            10,
            35
        )
    )

    pygame.draw.circle(
        surface,
        (25, 115, 45),
        (
            x,
            y - 12
        ),
        25
    )

    pygame.draw.circle(
        surface,
        (35, 145, 55),
        (
            x - 12,
            y - 3
        ),
        18
    )

    pygame.draw.circle(
        surface,
        (20, 95, 35),
        (
            x + 14,
            y - 2
        ),
        19
    )


def draw_forest(surface):

    gap = 120
    offset = int(
        scenery_offset % gap
    )

    for y in range(
        -gap + offset,
        HEIGHT + gap,
        gap
    ):

        draw_tree(
            surface,
            55,
            y + 40
        )

        draw_tree(
            surface,
            WIDTH - 55,
            y
        )


# =========================================================
# ROAD
# =========================================================

def draw_road(surface):

    map_data = current_map()

    surface.fill(
        map_data["ground"]
    )

    if selected_map == "night_city":
        draw_night_city(surface)

    elif selected_map == "desert":
        draw_desert(surface)

    elif selected_map == "forest":
        draw_forest(surface)

    pygame.draw.rect(
        surface,
        map_data["road"],
        (
            ROAD_X,
            0,
            ROAD_WIDTH,
            HEIGHT
        )
    )

    pygame.draw.rect(
        surface,
        map_data["road_edge"],
        (
            ROAD_X,
            0,
            8,
            HEIGHT
        )
    )

    pygame.draw.rect(
        surface,
        map_data["road_edge"],
        (
            ROAD_X + ROAD_WIDTH - 8,
            0,
            8,
            HEIGHT
        )
    )

    lane_width = ROAD_WIDTH / LANES

    for lane in range(
        1,
        LANES
    ):

        x = int(
            ROAD_X
            + lane_width * lane
        )

        y = (
            -LINE_HEIGHT
            + road_offset
        )

        while y < HEIGHT:

            pygame.draw.rect(
                surface,
                map_data["line"],
                (
                    x - LINE_WIDTH // 2,
                    int(y),
                    LINE_WIDTH,
                    LINE_HEIGHT
                )
            )

            y += (
                LINE_HEIGHT
                + LINE_GAP
            )


# =========================================================
# ENEMIES
# =========================================================

def create_enemy():

    lane = random.randint(
        0,
        LANES - 1
    )

    x = (
        lane_center(lane)
        - CAR_WIDTH / 2
    )

    enemy = {
        "lane": lane,

        "x": x,
        "y": -CAR_HEIGHT - 20,

        "color": random.choice(
            [
                RED,
                ORANGE,
                YELLOW,
                GREEN,
                PURPLE,
                LIGHT_GRAY
            ]
        ),

        "speed_modifier": random.uniform(
            0.65,
            1.15
        )
    }

    enemies.append(enemy)


# =========================================================
# COINS
# =========================================================

def create_coin():

    lane = random.randint(
        0,
        LANES - 1
    )

    coin_pickups.append(
        {
            "x": lane_center(lane),
            "y": -30,
            "rotation": 0
        }
    )


def draw_coin(
    surface,
    coin
):

    x = int(
        coin["x"]
    )

    y = int(
        coin["y"]
    )

    pulse = abs(
        math.sin(
            coin["rotation"]
        )
    )

    width = max(
        5,
        int(
            18 * pulse
        )
    )

    pygame.draw.ellipse(
        surface,
        GOLD,
        (
            x - width // 2,
            y - 14,
            width,
            28
        )
    )

    if width > 10:

        pygame.draw.ellipse(
            surface,
            YELLOW,
            (
                x - width // 4,
                y - 9,
                max(
                    3,
                    width // 2
                ),
                18
            ),
            2
        )


# =========================================================
# HITBOX
# =========================================================

def player_hitbox():

    return pygame.Rect(
        int(player_x + 8),
        int(player_y + 7),
        CAR_WIDTH - 16,
        CAR_HEIGHT - 14
    )


def enemy_hitbox(enemy):

    return pygame.Rect(
        int(enemy["x"] + 8),
        int(enemy["y"] + 7),
        CAR_WIDTH - 16,
        CAR_HEIGHT - 14
    )


# =========================================================
# SCORE
# =========================================================

def update_high_score():

    global high_score

    if score > high_score:

        high_score = score

        save_game()


# =========================================================
# COIN COLLECTION
# =========================================================

def collect_coin(coin):

    global coins
    global run_coins

    coins += 1
    run_coins += 1

    create_coin_particles(
        coin["x"],
        coin["y"]
    )

    if coin in coin_pickups:
        coin_pickups.remove(coin)

    save_game()


# =========================================================
# COLLISIONS
# =========================================================

def check_collisions():

    global health
    global speed

    global invincible_timer

    global shake_timer
    global shake_strength

    global flash_timer

    global screen_state

    p_rect = player_hitbox()

    if invincible_timer <= 0:

        for enemy in enemies[:]:

            if p_rect.colliderect(
                enemy_hitbox(enemy)
            ):

                health -= 34

                health = max(
                    0,
                    health
                )

                speed *= 0.55

                invincible_timer = 80

                shake_timer = 20
                shake_strength = 10

                flash_timer = 10

                create_crash_particles(
                    player_x + CAR_WIDTH / 2,
                    player_y + CAR_HEIGHT / 2
                )

                enemies.remove(enemy)

                if health <= 0:

                    update_high_score()
                    save_game()

                    screen_state = "gameover"

                break

    coin_size = 30

    for coin in coin_pickups[:]:

        coin_rect = pygame.Rect(
            int(
                coin["x"]
                - coin_size / 2
            ),
            int(
                coin["y"]
                - coin_size / 2
            ),
            coin_size,
            coin_size
        )

        if p_rect.colliderect(
            coin_rect
        ):

            collect_coin(
                coin
            )


# =========================================================
# HUD
# =========================================================

def draw_hud(surface):

    car = current_car()
    map_data = current_map()

    pygame.draw.rect(
        surface,
        DARKER,
        (
            15,
            15,
            190,
            145
        ),
        border_radius=12
    )

    score_text = FONT_SMALL.render(
        f"SCORE  {score}",
        True,
        WHITE
    )

    best_text = FONT_TINY.render(
        f"BEST  {high_score}",
        True,
        YELLOW
    )

    coin_text = FONT_TINY.render(
        f"COINS  {coins}",
        True,
        GOLD
    )

    map_text = FONT_TINY.render(
        map_data["name"],
        True,
        map_data["accent"]
    )

    surface.blit(
        score_text,
        (30, 28)
    )

    surface.blit(
        best_text,
        (30, 62)
    )

    surface.blit(
        coin_text,
        (30, 88)
    )

    surface.blit(
        map_text,
        (30, 115)
    )

    health_percent = (
        health
        / car["health"]
    )

    pygame.draw.rect(
        surface,
        (60, 60, 65),
        (
            30,
            140,
            150,
            10
        ),
        border_radius=5
    )

    if health_percent > 0.6:
        health_color = GREEN

    elif health_percent > 0.3:
        health_color = YELLOW

    else:
        health_color = RED

    pygame.draw.rect(
        surface,
        health_color,
        (
            30,
            140,
            int(
                150
                * health_percent
            ),
            10
        ),
        border_radius=5
    )

    # Speedometer
    pygame.draw.rect(
        surface,
        DARKER,
        (
            WIDTH - 200,
            15,
            185,
            135
        ),
        border_radius=12
    )

    speed_text = FONT_MEDIUM.render(
        str(get_kmh()),
        True,
        WHITE
    )

    kmh = FONT_TINY.render(
        "KM/H",
        True,
        GRAY
    )

    car_text = FONT_TINY.render(
        car["name"],
        True,
        car["color"]
    )

    surface.blit(
        speed_text,
        (
            WIDTH - 185,
            30
        )
    )

    surface.blit(
        kmh,
        (
            WIDTH - 90,
            52
        )
    )

    surface.blit(
        car_text,
        (
            WIDTH - 185,
            92
        )
    )

    pygame.draw.rect(
        surface,
        (60, 60, 65),
        (
            WIDTH - 185,
            120,
            150,
            13
        ),
        border_radius=6
    )

    speed_percent = (
        speed
        / get_max_speed()
    )

    pygame.draw.rect(
        surface,
        car["color"],
        (
            WIDTH - 185,
            120,
            int(
                150
                * speed_percent
            ),
            13
        ),
        border_radius=6
    )


# =========================================================
# MENU
# =========================================================

def draw_menu():

    SCREEN.fill(
        BLACK
    )

    title = FONT_BIG.render(
        " RACING",
        True,
        YELLOW
    )

    version = FONT_SMALL.render(
        "V4 - WORLD UPDATE",
        True,
        GRAY
    )

    car = current_car()
    map_data = current_map()

    SCREEN.blit(
        title,
        (
            WIDTH // 2
            - title.get_width() // 2,
            100
        )
    )

    SCREEN.blit(
        version,
        (
            WIDTH // 2
            - version.get_width() // 2,
            175
        )
    )

    preview_scale = 1.5

    preview_width = int(
        CAR_WIDTH
        * preview_scale
    )

    draw_car(
        SCREEN,
        WIDTH // 2
        - preview_width // 2,
        235,
        car["color"],
        True,
        preview_scale
    )

    selected_text = FONT_SMALL.render(
        f"{car['name']}  |  {map_data['name']}",
        True,
        map_data["accent"]
    )

    SCREEN.blit(
        selected_text,
        (
            WIDTH // 2
            - selected_text.get_width() // 2,
            405
        )
    )

    menu_lines = [
        (
            "SPACE = PLAY",
            WHITE
        ),

        (
            "G = GARAGE",
            LIGHT_BLUE
        ),

        (
            "L = MAP SELECT",
            map_data["accent"]
        )
    ]

    for i, (
        text,
        text_color
    ) in enumerate(menu_lines):

        rendered = FONT_MEDIUM.render(
            text,
            True,
            text_color
        )

        SCREEN.blit(
            rendered,
            (
                WIDTH // 2
                - rendered.get_width() // 2,
                485 + i * 58
            )
        )

    info = FONT_SMALL.render(
        f"COINS: {coins}     BEST: {high_score}",
        True,
        GOLD
    )

    controls = FONT_TINY.render(
        "W/S = GAS/BRAKE    A/D = STEER    ESC = PAUSE",
        True,
        GRAY
    )

    SCREEN.blit(
        info,
        (
            WIDTH // 2
            - info.get_width() // 2,
            690
        )
    )

    SCREEN.blit(
        controls,
        (
            WIDTH // 2
            - controls.get_width() // 2,
            760
        )
    )


# =========================================================
# STAT BAR
# =========================================================

def draw_stat_bar(
    surface,
    name,
    value,
    maximum,
    y,
    bar_color
):

    text = FONT_TINY.render(
        name,
        True,
        WHITE
    )

    surface.blit(
        text,
        (
            190,
            y
        )
    )

    pygame.draw.rect(
        surface,
        (60, 60, 68),
        (
            310,
            y + 2,
            200,
            16
        ),
        border_radius=8
    )

    pygame.draw.rect(
        surface,
        bar_color,
        (
            310,
            y + 2,
            int(
                200
                * min(
                    1,
                    value / maximum
                )
            ),
            16
        ),
        border_radius=8
    )


# =========================================================
# GARAGE
# =========================================================

def draw_garage():

    SCREEN.fill(
        DARKER
    )

    car_id = CAR_ORDER[
        garage_index
    ]

    car = CARS[
        car_id
    ]

    title = FONT_BIG.render(
        "GARAGE",
        True,
        WHITE
    )

    money = FONT_SMALL.render(
        f"COINS: {coins}",
        True,
        GOLD
    )

    car_name = FONT_MEDIUM.render(
        car["name"],
        True,
        car["color"]
    )

    SCREEN.blit(
        title,
        (
            WIDTH // 2
            - title.get_width() // 2,
            55
        )
    )

    SCREEN.blit(
        money,
        (
            WIDTH // 2
            - money.get_width() // 2,
            130
        )
    )

    SCREEN.blit(
        car_name,
        (
            WIDTH // 2
            - car_name.get_width() // 2,
            190
        )
    )

    preview_scale = 2.1

    preview_width = int(
        CAR_WIDTH
        * preview_scale
    )

    draw_car(
        SCREEN,
        WIDTH // 2
        - preview_width // 2,
        260,
        car["color"],
        True,
        preview_scale
    )

    draw_stat_bar(
        SCREEN,
        "SPEED",
        car["max_speed"],
        22,
        510,
        RED
    )

    draw_stat_bar(
        SCREEN,
        "HANDLING",
        car["handling"],
        1.45,
        550,
        BLUE
    )

    draw_stat_bar(
        SCREEN,
        "HEALTH",
        car["health"],
        170,
        590,
        GREEN
    )

    if car_id == selected_car:

        status_text = "SELECTED"
        status_color = GREEN

    elif car_id in owned_cars:

        status_text = "ENTER = SELECT"
        status_color = LIGHT_BLUE

    elif coins >= car["price"]:

        status_text = (
            f"ENTER = BUY ({car['price']})"
        )

        status_color = GOLD

    else:

        status_text = (
            f"LOCKED - {car['price']} COINS"
        )

        status_color = RED

    status = FONT_MEDIUM.render(
        status_text,
        True,
        status_color
    )

    arrows = FONT_SMALL.render(
        "<  A / D  >",
        True,
        WHITE
    )

    back = FONT_SMALL.render(
        "ESC = BACK",
        True,
        GRAY
    )

    SCREEN.blit(
        status,
        (
            WIDTH // 2
            - status.get_width() // 2,
            650
        )
    )

    SCREEN.blit(
        arrows,
        (
            WIDTH // 2
            - arrows.get_width() // 2,
            720
        )
    )

    SCREEN.blit(
        back,
        (
            WIDTH // 2
            - back.get_width() // 2,
            765
        )
    )


def garage_select():

    global selected_car
    global coins

    car_id = CAR_ORDER[
        garage_index
    ]

    car = CARS[
        car_id
    ]

    if car_id in owned_cars:

        selected_car = car_id
        save_game()

    elif coins >= car["price"]:

        coins -= car["price"]

        owned_cars.append(
            car_id
        )

        selected_car = car_id

        save_game()


# =========================================================
# MAP SELECT
# =========================================================

def draw_map_select():

    map_id = MAP_ORDER[
        map_index
    ]

    map_data = MAPS[
        map_id
    ]

    SCREEN.fill(
        map_data["ground"]
    )

    title = FONT_BIG.render(
        "SELECT MAP",
        True,
        WHITE
    )

    name = FONT_MEDIUM.render(
        map_data["name"],
        True,
        map_data["accent"]
    )

    description = FONT_SMALL.render(
        map_data["description"],
        True,
        LIGHT_GRAY
    )

    SCREEN.blit(
        title,
        (
            WIDTH // 2
            - title.get_width() // 2,
            70
        )
    )

    SCREEN.blit(
        name,
        (
            WIDTH // 2
            - name.get_width() // 2,
            170
        )
    )

    # Map preview
    preview = pygame.Surface(
        (
            460,
            360
        )
    )

    preview.fill(
        map_data["ground"]
    )

    pygame.draw.rect(
        preview,
        map_data["road"],
        (
            100,
            0,
            260,
            360
        )
    )

    pygame.draw.rect(
        preview,
        map_data["road_edge"],
        (
            100,
            0,
            7,
            360
        )
    )

    pygame.draw.rect(
        preview,
        map_data["road_edge"],
        (
            353,
            0,
            7,
            360
        )
    )

    pygame.draw.line(
        preview,
        map_data["line"],
        (
            187,
            0
        ),
        (
            187,
            360
        ),
        5
    )

    pygame.draw.line(
        preview,
        map_data["line"],
        (
            273,
            0
        ),
        (
            273,
            360
        ),
        5
    )

    if map_id == "night_city":

        for y in range(
            20,
            350,
            80
        ):

            pygame.draw.rect(
                preview,
                (25, 25, 45),
                (
                    10,
                    y,
                    65,
                    60
                )
            )

            pygame.draw.rect(
                preview,
                (25, 25, 45),
                (
                    385,
                    y,
                    65,
                    60
                )
            )

            pygame.draw.circle(
                preview,
                LIGHT_BLUE,
                (
                    85,
                    y + 30
                ),
                5
            )

            pygame.draw.circle(
                preview,
                LIGHT_BLUE,
                (
                    375,
                    y + 30
                ),
                5
            )

    elif map_id == "desert":

        for y in range(
            50,
            350,
            100
        ):

            pygame.draw.circle(
                preview,
                (35, 115, 55),
                (
                    55,
                    y
                ),
                14
            )

            pygame.draw.circle(
                preview,
                (35, 115, 55),
                (
                    405,
                    y + 35
                ),
                14
            )

    elif map_id == "forest":

        for y in range(
            30,
            350,
            80
        ):

            pygame.draw.circle(
                preview,
                (25, 125, 45),
                (
                    50,
                    y
                ),
                22
            )

            pygame.draw.circle(
                preview,
                (25, 125, 45),
                (
                    410,
                    y + 30
                ),
                22
            )

    SCREEN.blit(
        preview,
        (
            WIDTH // 2 - 230,
            245
        )
    )

    SCREEN.blit(
        description,
        (
            WIDTH // 2
            - description.get_width() // 2,
            630
        )
    )

    if map_id == selected_map:

        status_text = "SELECTED"
        status_color = GREEN

    else:

        status_text = "ENTER = SELECT"
        status_color = map_data["accent"]

    status = FONT_MEDIUM.render(
        status_text,
        True,
        status_color
    )

    arrows = FONT_SMALL.render(
        "<  A / D  >",
        True,
        WHITE
    )

    back = FONT_SMALL.render(
        "ESC = BACK",
        True,
        GRAY
    )

    SCREEN.blit(
        status,
        (
            WIDTH // 2
            - status.get_width() // 2,
            690
        )
    )

    SCREEN.blit(
        arrows,
        (
            WIDTH // 2
            - arrows.get_width() // 2,
            750
        )
    )

    SCREEN.blit(
        back,
        (
            WIDTH // 2
            - back.get_width() // 2,
            790
        )
    )


# =========================================================
# PAUSE
# =========================================================

def draw_pause():

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            10,
            10,
            15,
            215
        )
    )

    SCREEN.blit(
        overlay,
        (
            0,
            0
        )
    )

    title = FONT_BIG.render(
        "PAUSED",
        True,
        WHITE
    )

    SCREEN.blit(
        title,
        (
            WIDTH // 2
            - title.get_width() // 2,
            270
        )
    )

    options = [
        "ESC = RESUME",
        "R = RESTART",
        "M = MAIN MENU"
    ]

    for i, text in enumerate(
        options
    ):

        rendered = FONT_SMALL.render(
            text,
            True,
            LIGHT_BLUE
            if i == 0
            else WHITE
        )

        SCREEN.blit(
            rendered,
            (
                WIDTH // 2
                - rendered.get_width() // 2,
                410 + i * 50
            )
        )


# =========================================================
# GAME OVER
# =========================================================

def draw_game_over():

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            10,
            10,
            15,
            225
        )
    )

    SCREEN.blit(
        overlay,
        (
            0,
            0
        )
    )

    title = FONT_BIG.render(
        "WRECKED!",
        True,
        RED
    )

    score_text = FONT_MEDIUM.render(
        f"SCORE: {score}",
        True,
        WHITE
    )

    coins_text = FONT_SMALL.render(
        f"COINS COLLECTED: {run_coins}",
        True,
        GOLD
    )

    best = FONT_SMALL.render(
        f"BEST: {high_score}",
        True,
        YELLOW
    )

    restart = FONT_SMALL.render(
        "R = RESTART",
        True,
        LIGHT_BLUE
    )

    menu = FONT_SMALL.render(
        "M = MAIN MENU",
        True,
        WHITE
    )

    items = [
        (
            title,
            230
        ),

        (
            score_text,
            350
        ),

        (
            coins_text,
            410
        ),

        (
            best,
            450
        ),

        (
            restart,
            530
        ),

        (
            menu,
            575
        )
    ]

    for item, y in items:

        SCREEN.blit(
            item,
            (
                WIDTH // 2
                - item.get_width() // 2,
                y
            )
        )


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global player_x
    global horizontal_speed

    global speed
    global score
    global health

    global enemies
    global coin_pickups
    global particles

    global spawn_timer
    global coin_spawn_timer

    global invincible_timer

    global shake_timer
    global flash_timer

    global road_offset
    global scenery_offset

    global run_coins
    global screen_state

    player_x = (
        WIDTH / 2
        - CAR_WIDTH / 2
    )

    horizontal_speed = 0

    speed = MIN_SPEED

    score = 0

    health = current_car()[
        "health"
    ]

    enemies = []
    coin_pickups = []
    particles = []

    spawn_timer = 0
    coin_spawn_timer = 0

    invincible_timer = 0

    shake_timer = 0
    flash_timer = 0

    road_offset = 0
    scenery_offset = 0

    run_coins = 0

    screen_state = "game"


# =========================================================
# UPDATE GAME
# =========================================================

def update_game():

    global player_x
    global horizontal_speed

    global speed

    global road_offset
    global scenery_offset

    global spawn_timer
    global coin_spawn_timer

    global score

    global invincible_timer
    global shake_timer
    global flash_timer

    keys = pygame.key.get_pressed()

    car = current_car()

    max_speed = car[
        "max_speed"
    ]

    handling = car[
        "handling"
    ]

    # GAS
    if (
        keys[pygame.K_w]
        or
        keys[pygame.K_UP]
    ):

        speed += ACCELERATION

    else:

        speed -= NATURAL_SLOWDOWN

    # BRAKE
    if (
        keys[pygame.K_s]
        or
        keys[pygame.K_DOWN]
    ):

        speed -= BRAKE_POWER

    speed = max(
        MIN_SPEED,
        min(
            max_speed,
            speed
        )
    )

    # STEERING
    x_acceleration = (
        BASE_X_ACCELERATION
        * handling
    )

    max_x_speed = (
        BASE_MAX_X_SPEED
        * handling
    )

    if (
        keys[pygame.K_a]
        or
        keys[pygame.K_LEFT]
    ):

        horizontal_speed -= (
            x_acceleration
        )

    if (
        keys[pygame.K_d]
        or
        keys[pygame.K_RIGHT]
    ):

        horizontal_speed += (
            x_acceleration
        )

    horizontal_speed *= (
        FRICTION_X
    )

    horizontal_speed = max(
        -max_x_speed,
        min(
            max_x_speed,
            horizontal_speed
        )
    )

    player_x += (
        horizontal_speed
    )

    # Road bounds
    left_limit = (
        ROAD_X + 12
    )

    right_limit = (
        ROAD_X
        + ROAD_WIDTH
        - CAR_WIDTH
        - 12
    )

    if player_x < left_limit:

        player_x = left_limit
        horizontal_speed *= -0.2

    if player_x > right_limit:

        player_x = right_limit
        horizontal_speed *= -0.2

    # Scroll
    road_offset += speed
    scenery_offset += speed * 0.75

    total_line = (
        LINE_HEIGHT
        + LINE_GAP
    )

    if road_offset >= total_line:
        road_offset -= total_line

    # Enemies
    spawn_timer += 1

    current_spawn_delay = max(
        38,
        int(
            spawn_delay
            - speed * 2
        )
    )

    if spawn_timer >= current_spawn_delay:

        create_enemy()

        spawn_timer = 0

    # Coins
    coin_spawn_timer += 1

    if coin_spawn_timer >= coin_spawn_delay:

        create_coin()

        coin_spawn_timer = random.randint(
            -40,
            20
        )

    # Enemy movement
    for enemy in enemies[:]:

        enemy["y"] += (
            speed
            * enemy["speed_modifier"]
        )

        if enemy["y"] > HEIGHT:

            enemies.remove(
                enemy
            )

            score += 1

            update_high_score()

    # Coin movement
    for coin in coin_pickups[:]:

        coin["y"] += speed

        coin["rotation"] += 0.12

        if coin["y"] > HEIGHT + 30:

            coin_pickups.remove(
                coin
            )

    check_collisions()

    if invincible_timer > 0:
        invincible_timer -= 1

    if shake_timer > 0:
        shake_timer -= 1

    if flash_timer > 0:
        flash_timer -= 1

    update_particles()


# =========================================================
# DRAW GAME
# =========================================================

def draw_game():

    game_surface = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        )
    )

    draw_road(
        game_surface
    )

    for coin in coin_pickups:

        draw_coin(
            game_surface,
            coin
        )

    for enemy in enemies:

        draw_car(
            game_surface,
            enemy["x"],
            enemy["y"],
            enemy["color"]
        )

    show_player = True

    if invincible_timer > 0:

        if (
            invincible_timer // 5
        ) % 2 == 0:

            show_player = False

    if show_player:

        draw_car(
            game_surface,
            player_x,
            player_y,
            current_car()["color"],
            True
        )

    draw_particles(
        game_surface
    )

    draw_hud(
        game_surface
    )

    shake_x = 0
    shake_y = 0

    if shake_timer > 0:

        shake_x = random.randint(
            -shake_strength,
            shake_strength
        )

        shake_y = random.randint(
            -shake_strength,
            shake_strength
        )

    SCREEN.fill(
        BLACK
    )

    SCREEN.blit(
        game_surface,
        (
            shake_x,
            shake_y
        )
    )

    if flash_timer > 0:

        flash = pygame.Surface(
            (
                WIDTH,
                HEIGHT
            ),
            pygame.SRCALPHA
        )

        flash.fill(
            (
                255,
                40,
                40,
                80
            )
        )

        SCREEN.blit(
            flash,
            (
                0,
                0
            )
        )


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    CLOCK.tick(
        FPS
    )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # =================================================
            # MENU
            # =================================================

            if screen_state == "menu":

                if event.key == pygame.K_SPACE:

                    reset_game()

                elif event.key == pygame.K_g:

                    garage_index = CAR_ORDER.index(
                        selected_car
                    )

                    screen_state = "garage"

                elif event.key == pygame.K_l:

                    map_index = MAP_ORDER.index(
                        selected_map
                    )

                    screen_state = "maps"

                elif event.key == pygame.K_ESCAPE:

                    running = False

            # =================================================
            # GARAGE
            # =================================================

            elif screen_state == "garage":

                if (
                    event.key == pygame.K_a
                    or
                    event.key == pygame.K_LEFT
                ):

                    garage_index -= 1

                    if garage_index < 0:

                        garage_index = (
                            len(CAR_ORDER)
                            - 1
                        )

                elif (
                    event.key == pygame.K_d
                    or
                    event.key == pygame.K_RIGHT
                ):

                    garage_index += 1

                    if garage_index >= len(
                        CAR_ORDER
                    ):

                        garage_index = 0

                elif event.key == pygame.K_RETURN:

                    garage_select()

                elif event.key == pygame.K_ESCAPE:

                    screen_state = "menu"

            # =================================================
            # MAP SELECT
            # =================================================

            elif screen_state == "maps":

                if (
                    event.key == pygame.K_a
                    or
                    event.key == pygame.K_LEFT
                ):

                    map_index -= 1

                    if map_index < 0:

                        map_index = (
                            len(MAP_ORDER)
                            - 1
                        )

                elif (
                    event.key == pygame.K_d
                    or
                    event.key == pygame.K_RIGHT
                ):

                    map_index += 1

                    if map_index >= len(
                        MAP_ORDER
                    ):

                        map_index = 0

                elif event.key == pygame.K_RETURN:

                    selected_map = MAP_ORDER[
                        map_index
                    ]

                    save_game()

                elif event.key == pygame.K_ESCAPE:

                    screen_state = "menu"

            # =================================================
            # GAME
            # =================================================

            elif screen_state == "game":

                if event.key == pygame.K_ESCAPE:

                    screen_state = "pause"

            # =================================================
            # PAUSE
            # =================================================

            elif screen_state == "pause":

                if event.key == pygame.K_ESCAPE:

                    screen_state = "game"

                elif event.key == pygame.K_r:

                    reset_game()

                elif event.key == pygame.K_m:

                    update_high_score()
                    save_game()

                    screen_state = "menu"

            # =================================================
            # GAME OVER
            # =================================================

            elif screen_state == "gameover":

                if event.key == pygame.K_r:

                    reset_game()

                elif event.key == pygame.K_m:

                    screen_state = "menu"

    # =====================================================
    # UPDATE
    # =====================================================

    if screen_state == "game":

        update_game()

    # =====================================================
    # DRAW
    # =====================================================

    if screen_state == "menu":

        draw_menu()

    elif screen_state == "garage":

        draw_garage()

    elif screen_state == "maps":

        draw_map_select()

    elif screen_state == "game":

        draw_game()

    elif screen_state == "pause":

        draw_game()
        draw_pause()

    elif screen_state == "gameover":

        draw_game()
        draw_game_over()

    pygame.display.flip()


# =========================================================
# EXIT
# =========================================================

update_high_score()
save_game()

pygame.quit()
sys.exit()