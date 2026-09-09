# 🎮 Python Games

A collection of standalone desktop games written in **Python**. Most use **Pygame**; **Do Not Press** uses Python's built-in **Tkinter** GUI.

Each game is a single `.py` file with no external image/audio assets required. Download the repo, install the dependency, and run whichever game you want.

## 📑 Table of contents

- [Games](#-games)
- [Quick start](#-quick-start)
- [Requirements](#-requirements)
- [Installing Python](#-installing-python)
- [Downloading the repository](#-downloading-the-repository)
- [Installing dependencies](#-installing-dependencies)
- [Game guides](#-game-guides)
- [Save files](#-save-files)
- [VS Code](#-running-from-vs-code)
- [Troubleshooting](#️-troubleshooting)
- [Updating](#-updating-your-copy)
- [FAQ](#-faq)

---

# 🕹️ Games

| Game | File | Main idea |
|---|---|---|
| 🎯 **Aim Trainer** | `aim_trainer.py` | Reaction-time and accuracy training with multiple modes. |
| 🏎️ **Car Game** | `car_game.py` | Arcade highway racing with cars, maps, health and coins. |
| 🧱 **Breakout** | `Breakout.py` | Brick breaker with progression, powerups and unlockables. |
| 🚦 **Crossy Road** | `crossy_road.py` | Hop through roads, water and railways while collecting rewards. |
| 🔴 **Do Not Press** | `donotpress.py` | A deliberately chaotic button game that gets worse as you continue. |
| 🦖 **Dino Hop** | `dyno_hop.py` | Endless runner with obstacles, coins, skins and progression. |
| 🐦 **Flappy Bird** | `flappy_bird.py` | Expanded Flappy-style game with modes, worlds, progression and challenges. |

---

# ⚡ Quick start

Already have Python installed? In PowerShell:

```powershell
git clone https://github.com/kodaniq/py-games.git
cd py-games
py -m pip install -r requirements.txt
py car_game.py
```

Replace `car_game.py` with any game filename from the table above.

If you do not have Git, use **Code → Download ZIP** on GitHub instead.

---

# ✅ Requirements

Recommended setup:

- **Windows 10/11**
- **Python 3**
- **pip** (normally included with Python)
- **Pygame** for the Pygame games

`donotpress.py` uses **Tkinter**, which is normally included with the standard Windows Python installation and does not require `pip install pygame` to run.

---

# 🐍 Installing Python

## 1. Check whether Python is already installed

Open **PowerShell** and run:

```powershell
py --version
```

Expected output looks similar to:

```text
Python 3.x.x
```

If `py` is not recognized, also try:

```powershell
python --version
```

## 2. If Python is missing

Download Python from the official website:

👉 **https://www.python.org/downloads/**

On Windows, during installation enable **Add Python to PATH** if the installer shows that option.

After installing:

1. Close PowerShell.
2. Open a new PowerShell window.
3. Run `py --version` again.

## 3. Check pip

```powershell
py -m pip --version
```

If this prints a pip version and a Python path, you're ready for the dependency step.

---

# 📦 Downloading the repository

## Option A — Download ZIP

1. Open the `py-games` repository on GitHub.
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the ZIP.
5. Open the extracted `py-games` folder.

### Open PowerShell in that folder

In File Explorer, open the folder, click the address bar, type:

```text
powershell
```

and press **Enter**.

You can verify that you are in the correct folder with:

```powershell
dir
```

You should see files such as `car_game.py`, `flappy_bird.py` and `requirements.txt`.

## Option B — Clone with Git

```powershell
git clone https://github.com/kodaniq/py-games.git
cd py-games
```

---

# 📚 Installing dependencies

The recommended command is:

```powershell
py -m pip install -r requirements.txt
```

Currently `requirements.txt` installs:

```text
pygame
```

Or install Pygame directly:

```powershell
py -m pip install pygame
```

If your system uses `python` rather than `py`:

```powershell
python -m pip install -r requirements.txt
```

### Verify Pygame

```powershell
py -m pip show pygame
```

or:

```powershell
py -c "import pygame; print(pygame.version.ver)"
```

A Pygame version number means the import works. ✅

---

# 🎮 Game guides

## 🎯 Aim Trainer — `aim_trainer.py`

Run:

```powershell
py aim_trainer.py
```

**What it contains:**

- Classic, Speed, Precision and Chaos modes
- Reaction-time tracking
- Accuracy, combo and score tracking
- Bullseye bonus hits
- Performance ranks
- Best scores for each mode
- Custom crosshair toggle
- Particle and screen-shake settings
- Adjustable game time

**Controls:** the interface is primarily mouse-driven. Use the **left mouse button** to select menus and shoot targets.

**Save file:** `aimtrainer_save.json` stores best scores and settings.

---

## 🏎️ Car Game — `car_game.py`

Run:

```powershell
py car_game.py
```

**Goal:** survive traffic, collect coins and build a high score while controlling your speed and avoiding crashes.

**Features:**

- 4 cars: Starter, Speedster, Tank and Drifter
- Different speed, handling and health stats
- Garage and unlockable cars
- 3 maps: Night City, Desert Highway and Forest Road
- Coins and persistent high score
- Health system and collision damage
- Speedometer
- Crash and coin particles

**Controls:**

| Key | Action |
|---|---|
| `W` | Gas / accelerate |
| `S` | Brake |
| `A` / `D` | Steer left / right |
| `Esc` | Pause |
| `Space` | Play from menu |
| `G` | Garage from menu |
| `L` | Map select from menu |

**Save file:** `racing_save.json` stores high score, coins, owned cars, selected car and selected map.

---

## 🧱 Breakout — `Breakout.py`

Run:

```powershell
py Breakout.py
```

**Features:**

- Easy, Normal and Hard difficulties
- Multi-level brick layouts
- Stronger, gold, explosive and boss bricks
- Powerups including expand, multiball, slow, laser, shield and coins
- Combo scoring
- XP and player levels
- Coins
- Unlockable paddle styles and ball trails
- Achievements and persistent statistics
- Particle and screen-shake effects

**Core movement:** use `A` / `D` or the **Left / Right arrow keys** to move the paddle. Additional actions and menus are shown in-game when relevant.

**Save file:** `breakout_save.json` stores progression, unlocks, difficulty, achievements, stats and settings.

---

## 🚦 Crossy Road — `crossy_road.py`

Run:

```powershell
py crossy_road.py
```

**Features:**

- Smooth tile hopping and camera movement
- Roads with cars and trucks
- Water with moving logs
- Railways and fast trains
- Trees that can block movement
- Coins
- Shield and magnet powerups
- Missions
- XP and levels
- Unlockable skins
- Achievements and run statistics
- Weather, particles and screen shake

**Controls:**

| Key | Action |
|---|---|
| `WASD` | Move |
| Arrow keys | Move |
| `Esc` | Pause |
| `R` | Restart after death |
| `M` | Return to menu |

**Save file:** `crossy_save.json` stores best score, coins, XP, level, skins, achievements, stats and settings.

---

## 🔴 Do Not Press — `donotpress.py`

Run:

```powershell
py donotpress.py
```

This one uses **Tkinter**, not Pygame.

**What happens:** the innocent-looking button progressively turns into a chaos game with moving buttons, fake buttons, gravity/inversion effects, a fake crash screen, countdowns and eventually a boss fight.

**Features:**

- Increasing chaos based on number of presses
- Runaway button
- Clone/fake-button stage
- Gravity and inverted-coordinate chaos
- Fake crash event
- Final boss
- Achievements
- Multiple endings
- Coins and persistent stats
- A hidden secret ending 👀

**Controls:** mostly the **left mouse button**. `Space` starts/restarts from the menu or ending screens, and `Esc` returns to the menu while playing.

**Save file:** `do_not_press_save.json` stores best presses, wins, fails, coins, achievements and endings.

---

## 🦖 Dino Hop — `dyno_hop.py`

Run:

```powershell
py dyno_hop.py
```

**Features:**

- Endless running with increasing speed
- Cacti, double cacti and birds
- Coins
- Near-miss tracking
- Boss-rush sections
- XP and levels
- Unlockable skins
- Achievements and statistics
- Day/night progression
- Particles and screen shake

**Controls:**

| Key | Action |
|---|---|
| `Space` / `↑` / `W` | Jump |
| `↓` / `S` | Duck on ground / fast-fall in air |
| `Esc` | Pause / resume |
| `R` | Restart from pause/death |
| `M` | Menu |

The menu also exposes Shop, Achievements and Settings shortcuts.

**Save file:** `dino_save.json` stores high score, coins, XP, level, skins, achievements, stats and settings.

---

## 🐦 Flappy Bird — `flappy_bird.py`

Run:

```powershell
py flappy_bird.py
```

This is the most feature-heavy game in the collection.

**Features:**

- Classic, Turbo, Tiny Bird, Chaos, Hardcore and Daily Challenge modes
- Easy, Normal and Hard difficulties
- Multiple unlockable worlds
- 6 bird skins
- Unlockable trails
- Coins, XP and levels
- Missions and achievements
- Daily rewards and streaks
- Daily seeded challenge
- Powerups
- Boss sections
- Near-miss tracking
- Local top-10 leaderboard data
- Best-run ghost system
- Player stats and prestige system
- Controller flap support

**Main controls:**

| Key | Action |
|---|---|
| `Space` | Start / flap |
| `↑` | Flap while playing |
| `Esc` | Pause / back |
| `R` | Restart from pause/game over |
| `M` | Menu from pause/game over |

**Menu shortcuts:** `G` Shop, `W` Worlds, `D` Difficulty, `M` Modes, `T` Stats, `A` Achievements, `S` Settings, `P` Profile, `H` Hall and `C` Daily Challenge.

In selection menus, `A/D` or arrow keys browse options and `Enter` selects. In the shop, `Q` switches between skins and trails.

**Controller:** controller button `0` can flap while playing.

**Save file:** `flappy_save.json` stores progression, modes, worlds, cosmetics, stats, achievements, leaderboard/ghost data, daily data and settings.

---

# 💾 Save files

Several games generate JSON files automatically next to the Python scripts. These are **local player data**, not required source files.

| Game | Save file |
|---|---|
| Aim Trainer | `aimtrainer_save.json` |
| Car Game | `racing_save.json` |
| Breakout | `breakout_save.json` |
| Crossy Road | `crossy_save.json` |
| Do Not Press | `do_not_press_save.json` |
| Dino Hop | `dino_save.json` |
| Flappy Bird | `flappy_save.json` |

They may contain high scores, coins, unlocks, settings, achievements and other progression. They are ignored by Git so your personal progress is not accidentally committed.

⚠️ Deleting a save file can reset that game's progress.

---

# 💻 Running from VS Code

1. Open the `py-games` folder in VS Code.
2. Install Microsoft's **Python** extension if needed.
3. Open the `.py` game you want.
4. Select the correct Python interpreter.
5. Press **Run Python File** or use the integrated terminal.

Example:

```powershell
py dyno_hop.py
```

---

# 📁 Repository structure

```text
py-games/
│
├── aim_trainer.py
├── car_game.py
├── Breakout.py
├── crossy_road.py
├── donotpress.py
├── dyno_hop.py
├── flappy_bird.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

The games do not currently require separate image, music or sprite folders.

---

# 🛠️ Troubleshooting

## `ModuleNotFoundError: No module named 'pygame'`

Install Pygame for the same Python you use to launch the game:

```powershell
py -m pip install pygame
```

Then verify:

```powershell
py -m pip show pygame
```

## `py` is not recognized

Try:

```powershell
python --version
```

If that works, replace `py` with `python` in the commands.

If neither command works, install Python from:

👉 **https://www.python.org/downloads/**

## PowerShell cannot find the `.py` file

You are probably in the wrong folder.

```powershell
pwd
dir
```

For a ZIP downloaded to Downloads, the folder may be similar to:

```powershell
cd "$HOME\Downloads\py-games-main"
```

For a Git clone it will normally be:

```powershell
cd "$HOME\Downloads\py-games"
```

Your exact path depends on where you saved the repository.

## Pygame is installed but Python still cannot import it

You may have multiple Python installations. Compare:

```powershell
py --version
py -m pip --version
py -m pip show pygame
```

Using `py -m pip` helps install packages into the Python selected by the Windows launcher.

## Update pip / Pygame

```powershell
py -m pip install --upgrade pip
py -m pip install --upgrade pygame
```

## The window opens and immediately closes

Run the game from PowerShell instead of double-clicking the `.py` file. If Python reports an error, the terminal will remain visible so you can read the traceback.

Example:

```powershell
py flappy_bird.py
```

---

# 🔄 Updating your copy

If you cloned with Git:

```powershell
git pull
```

If you downloaded a ZIP, download a new ZIP to get the latest repository version.

Keep copies of your local save JSON files if you want to preserve progress while replacing folders manually.

---

# ❓ FAQ

### Do I need internet to play?
No. Internet is only needed to download Python, dependencies or the repository. The current games themselves run locally.

### Do I need to install Pygame separately for every game?
No. Install it once into the Python environment you use to run the games.

### Do the games need external assets?
No external game assets are required by the current versions.

### Can I run only one game?
Yes. Each game is a standalone Python file.

### Where is my progress stored?
In the game's local JSON save file, listed in the Save files section above.

### Why should I launch from PowerShell when debugging?
If a game crashes, PowerShell keeps the Python error/traceback visible instead of the window simply disappearing.

### Are Linux and macOS supported?
The projects are primarily intended for Windows. Most Pygame code is cross-platform, but this repository is not claiming full Linux/macOS testing yet.

---

# 🧑‍💻 For developers

Clone and set up:

```powershell
git clone https://github.com/kodaniq/py-games.git
cd py-games
py -m pip install -r requirements.txt
```

Each game is intentionally kept in a standalone source file, making it easy to open, study and modify independently.

When testing a change, run that game's file directly and check the terminal for tracebacks.

---

# 📝 Notes

- These are local desktop Python games.
- Most games use Pygame; Do Not Press uses Tkinter.
- Personal save data is excluded from Git through `.gitignore`.
- Internet access is not required after setup.
- Features and controls can differ significantly between games, so see the individual guide above.

---

## ⭐ Have fun

Pick a game, launch it and try to beat your score. 🎮🔥
