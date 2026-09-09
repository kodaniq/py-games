# 🎮 Python Games

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-powered-green)
![Windows 11](https://img.shields.io/badge/Windows%2011-tested-success?logo=windows11)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A collection of standalone desktop games written in **Python**. Most use **Pygame**; **Do Not Press** uses Python's built-in **Tkinter** GUI.

Each game is a single `.py` file with no external image/audio assets required. Download the repository, install the dependency, and run whichever game you want.

> ✅ **Tested on Windows 11**

---

# 📸 Screenshots

![Python Games screenshots](assets/screenshots.jpg)

The image above shows all seven games currently included in the repository: **Car Game, Aim Trainer, Breakout, Crossy Road, Do Not Press, Dino Hop and Flappy Bird**.

---

## 📑 Table of contents

- [Screenshots](#-screenshots)
- [Games](#-games)
- [Quick start](#-quick-start)
- [Requirements](#-requirements)
- [Compatibility](#-compatibility)
- [Installing Python](#-installing-python)
- [Downloading the repository](#-downloading-the-repository)
- [Installing dependencies](#-installing-dependencies)
- [Game guides](#-game-guides)
- [Save files](#-save-files)
- [Running from VS Code](#-running-from-vs-code)
- [Troubleshooting](#️-troubleshooting)
- [Updating your copy](#-updating-your-copy)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [Feature requests](#-feature-requests)
- [License](#-license)
- [Bug reports & contact](#-bug-reports--contact)

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

Already have Python and Git installed? Open **PowerShell** and run:

```powershell
git clone https://github.com/kodaniq/py-games.git
cd py-games
py -m pip install -r requirements.txt
py car_game.py
```

Replace `car_game.py` with any filename from the games table above.

If you do not have Git, use **Code → Download ZIP** on GitHub instead.

---

# ✅ Requirements

- **Windows 11** — tested
- **Python 3**
- **pip** — normally included with Python
- **Pygame** for the Pygame games

`donotpress.py` uses **Tkinter**, which is normally included with the standard Windows Python installation and does not require Pygame to run.

---

# 🪟 Compatibility

| Platform | Status |
|---|---|
| **Windows 11** | ✅ Tested |
| Windows 10 | ⚪ Not officially tested |
| Linux | ⚪ Not officially tested |
| macOS | ⚪ Not officially tested |

Most of the Pygame code is cross-platform, so other operating systems may work, but **Windows 11 is currently the confirmed test platform**.

---

# 🐍 Installing Python

## 1. Check whether Python is installed

Open PowerShell and run:

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

On Windows, enable **Add Python to PATH** if the installer shows that option.

After installation, close and reopen PowerShell, then run `py --version` again.

## 3. Check pip

```powershell
py -m pip --version
```

If this prints a pip version and Python path, you're ready.

---

# 📦 Downloading the repository

## Option A — Download ZIP

1. Open this repository on GitHub.
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Extract the ZIP.
5. Open the extracted folder.

To open PowerShell directly inside that folder, open the folder in File Explorer, click the address bar, type `powershell`, and press **Enter**.

Check that you are in the right place with:

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

Install everything listed in `requirements.txt`:

```powershell
py -m pip install -r requirements.txt
```

Currently this installs `pygame`.

You can also install Pygame directly:

```powershell
py -m pip install pygame
```

If your PC uses `python` instead of `py`:

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

If a version number appears, Pygame is working. ✅

---

# 🎮 Game guides

## 🎯 Aim Trainer — `aim_trainer.py`

```powershell
py aim_trainer.py
```

**Features:** Classic, Speed, Precision and Chaos modes, reaction-time tracking, accuracy and combo tracking, bullseye bonuses, ranks, best scores, custom crosshair, particles, screen shake and adjustable game time.

**Controls:** mainly the **left mouse button** for menus and targets.

**Save file:** `aimtrainer_save.json`

---

## 🏎️ Car Game — `car_game.py`

```powershell
py car_game.py
```

**Goal:** survive traffic, collect coins and build a high score while controlling speed and avoiding crashes.

**Features:** 4 cars, different speed/handling/health stats, garage, unlockable cars, Night City / Desert Highway / Forest Road maps, coins, high score, health system, speedometer and effects.

| Key | Action |
|---|---|
| `W` | Accelerate |
| `S` | Brake |
| `A` / `D` | Steer |
| `Esc` | Pause |
| `Space` | Play from menu |
| `G` | Garage |
| `L` | Map selection |

**Save file:** `racing_save.json`

---

## 🧱 Breakout — `Breakout.py`

```powershell
py Breakout.py
```

**Features:** Easy/Normal/Hard difficulties, multiple levels, stronger/gold/explosive/boss bricks, expand/multiball/slow/laser/shield/coin powerups, combos, XP, player levels, coins, paddle styles, trails, achievements and statistics.

**Controls:** `A` / `D` or **Left / Right arrows** move the paddle. Other controls are displayed in-game when relevant.

**Save file:** `breakout_save.json`

---

## 🚦 Crossy Road — `crossy_road.py`

```powershell
py crossy_road.py
```

**Features:** smooth hopping, roads with cars/trucks, water/logs, railways/trains, trees, coins, shield and magnet powerups, missions, XP, levels, skins, achievements, weather, particles and screen shake.

| Key | Action |
|---|---|
| `WASD` | Move |
| Arrow keys | Move |
| `Esc` | Pause |
| `R` | Restart after death |
| `M` | Menu |

**Save file:** `crossy_save.json`

---

## 🔴 Do Not Press — `donotpress.py`

```powershell
py donotpress.py
```

This game uses **Tkinter**, not Pygame.

**Features:** moving button, fake buttons, clone stage, gravity/inversion chaos, fake crash event, countdowns, final boss, achievements, multiple endings, coins and persistent stats.

**Controls:** mainly the **left mouse button**. `Space` starts/restarts and `Esc` returns to the menu while playing.

**Save file:** `do_not_press_save.json`

---

## 🦖 Dino Hop — `dyno_hop.py`

```powershell
py dyno_hop.py
```

**Features:** endless running, increasing speed, cacti, birds, coins, near misses, boss rush sections, XP, levels, skins, achievements, statistics, day/night progression, particles and screen shake.

| Key | Action |
|---|---|
| `Space` / `↑` / `W` | Jump |
| `↓` / `S` | Duck / fast-fall |
| `Esc` | Pause / resume |
| `R` | Restart |
| `M` | Menu |

**Save file:** `dino_save.json`

---

## 🐦 Flappy Bird — `flappy_bird.py`

```powershell
py flappy_bird.py
```

This is the most feature-heavy game in the collection.

**Features:** Classic, Turbo, Tiny Bird, Chaos, Hardcore and Daily Challenge modes; Easy/Normal/Hard difficulty; multiple worlds; skins; trails; coins; XP; levels; missions; achievements; daily rewards; powerups; boss sections; near misses; local leaderboard; ghost system; stats; prestige and controller flap support.

| Key | Action |
|---|---|
| `Space` | Start / flap |
| `↑` | Flap |
| `Esc` | Pause / back |
| `R` | Restart |
| `M` | Menu from pause/game over |

**Menu shortcuts:** `G` Shop, `W` Worlds, `D` Difficulty, `M` Modes, `T` Stats, `A` Achievements, `S` Settings, `P` Profile, `H` Hall and `C` Daily Challenge.

**Save file:** `flappy_save.json`

---

# 💾 Save files

Several games create local JSON save files automatically.

| Game | Save file |
|---|---|
| Aim Trainer | `aimtrainer_save.json` |
| Car Game | `racing_save.json` |
| Breakout | `breakout_save.json` |
| Crossy Road | `crossy_save.json` |
| Do Not Press | `do_not_press_save.json` |
| Dino Hop | `dino_save.json` |
| Flappy Bird | `flappy_save.json` |

These can contain high scores, coins, unlocks, settings, achievements and progression. They are ignored by Git so personal progress is not accidentally uploaded.

⚠️ Deleting a save file can reset that game's progress.

---

# 💻 Running from VS Code

1. Open the `py-games` folder in VS Code.
2. Install Microsoft's **Python** extension if needed.
3. Open the `.py` file you want to run.
4. Select the correct Python interpreter.
5. Press **Run Python File** or use the terminal.

Example:

```powershell
py dyno_hop.py
```

---

# 📁 Repository structure

```text
py-games/
│
├── assets/
│   └── screenshots.jpg
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
├── LICENSE
└── README.md
```

---

# 🛠️ Troubleshooting

## `ModuleNotFoundError: No module named 'pygame'`

```powershell
py -m pip install pygame
```

Then verify:

```powershell
py -m pip show pygame
```

## `py` is not recognized

Try `python --version`. If that works, replace `py` with `python` in the commands.

If neither command works, install Python from:

👉 **https://www.python.org/downloads/**

## PowerShell cannot find the `.py` file

Check your current folder and files:

```powershell
pwd
dir
```

Then `cd` into the folder containing the repository.

## Pygame is installed but Python cannot import it

You may have multiple Python installations. Check:

```powershell
py --version
py -m pip --version
py -m pip show pygame
```

## Update pip / Pygame

```powershell
py -m pip install --upgrade pip
py -m pip install --upgrade pygame
```

## Game window opens and immediately closes

Run the game from PowerShell instead of double-clicking the `.py` file. The terminal will keep the error message visible.

---

# 🔄 Updating your copy

If you cloned with Git:

```powershell
git pull
```

If you downloaded a ZIP, download a fresh ZIP for the newest version.

Keep a backup of your local save JSON files if you want to preserve progress while replacing folders manually.

---

# ❓ FAQ

### Do I need internet to play?
No. Internet is only needed to download Python, dependencies or the repository.

### Do I need to install Pygame separately for every game?
No. Install it once for the Python environment you use.

### Do the games need external assets?
No external image/audio assets are currently required.

### Can I run only one game?
Yes. Every game is a standalone Python file.

### Where is my progress stored?
In the local JSON save files listed above.

### Are Linux and macOS supported?
They may work, but the repository is currently **tested on Windows 11**. Linux/macOS are not officially tested yet.

---

# 🤝 Contributing

Contributions are welcome. If you want to fix a bug, improve a game or clean up code:

1. Fork the repository.
2. Create a new branch for your change.
3. Make and test your changes.
4. Keep unrelated changes out of the same commit when possible.
5. Open a Pull Request and explain what you changed.

Please test game changes before submitting them. If a change adds a new dependency, also update `requirements.txt`.

---

# 💡 Feature requests

Ideas for new features, game modes, quality-of-life improvements or new games are welcome.

When suggesting something, include **which game** the idea is for, **what you would like added**, and a short explanation of **how it should work**. GitHub Issues are a good place for public suggestions.

---

# 🧑‍💻 For developers

Clone and set up:

```powershell
git clone https://github.com/kodaniq/py-games.git
cd py-games
py -m pip install -r requirements.txt
```

Each game is intentionally kept mostly self-contained so it is easy to open, study and modify independently.

---

# 📄 License

This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for the full license text.

---

# 🐛 Bug reports & contact

Found a bug, crash, broken feature or something that behaves strangely?

You can report it through **GitHub Issues** or contact:

📧 **kodaniq@outlook.com**

If possible, include:

- which game you were playing
- what you were doing when the bug happened
- steps that make the bug happen again
- the error/traceback from PowerShell, if there is one
- your Windows version
- your Python and Pygame versions

Please do **not** include passwords, API keys, tokens or other private information in bug reports.

Feedback, bug reports and improvement ideas are appreciated. ❤️

---

## ⭐ Have fun

Pick a game, launch it and try to beat your score. If you enjoy the project, feel free to ⭐ the repository.
