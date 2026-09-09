# 🎮 Python Games

A collection of small desktop games written in **Python** using **Pygame**.

The goal of this repository is to keep the games easy to download, easy to run, and easy to understand. Every game is stored as a standalone `.py` file, so you do not need an installer or launcher.

---

## 🕹️ Games included

| Game | File | Description |
|---|---|---|
| 🎯 **Aim Trainer** | `aim_trainer.py` | Practice mouse speed, reaction time and accuracy by hitting targets. |
| 🏎️ **Car Game** | `car_game.py` | Arcade racing game with cars, speed, health, coins, maps and progression. |
| 🧱 **Breakout** | `Breakout.py` | Classic brick-breaking arcade game. |
| 🚦 **Crossy Road** | `crossy_road.py` | Move forward while avoiding traffic and other hazards. |
| 🔴 **Do Not Press** | `donotpress.py` | A chaotic button game where pressing the button keeps making things worse. |
| 🦖 **Dino Hop** | `dyno_hop.py` | Endless runner inspired by the browser dinosaur game. |
| 🐦 **Flappy Bird** | `flappy_bird.py` | Fly through pipes, survive as long as possible and beat your high score. |

---

# ✅ Requirements

You need the following installed on your computer:

- **Windows 10/11** recommended
- **Python 3**
- **pip**
- **Pygame**

You only need to install Pygame **once**. All games in this repository can then use the same installation.

---

# 🐍 Step 1 — Check that Python is installed

Open **PowerShell** and run:

```powershell
py --version
```

You should get something similar to:

```text
Python 3.x.x
```

If `py` is not recognized, try:

```powershell
python --version
```

If neither command works, install Python from the official Python website and make sure Python is added to PATH during installation.

---

# 📦 Step 2 — Download the games

## Option A — Download ZIP

1. Open this repository on GitHub.
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Open the extracted `py-games` folder.

### Open PowerShell directly inside the folder

An easy Windows method:

1. Open the `py-games` folder in File Explorer.
2. Click the address bar at the top.
3. Type:

```text
powershell
```

4. Press **Enter**.

PowerShell will open directly in the correct folder.

---

## Option B — Clone with Git

If Git is installed:

```powershell
git clone https://github.com/kodaniq/py-games.git
cd py-games
```

---

# 📚 Step 3 — Install dependencies

The easiest method is:

```powershell
py -m pip install -r requirements.txt
```

At the moment, this installs:

```text
pygame
```

You can also install Pygame manually:

```powershell
py -m pip install pygame
```

If your PC uses `python` instead of `py`, use:

```powershell
python -m pip install -r requirements.txt
```

or:

```powershell
python -m pip install pygame
```

### Check that Pygame installed correctly

```powershell
py -m pip show pygame
```

Or test it with:

```powershell
py -c "import pygame; print(pygame.version.ver)"
```

If a version number appears, Pygame is ready. ✅

---

# ▶️ Step 4 — Run a game

Make sure PowerShell is inside the `py-games` folder first.

You can check your current files with:

```powershell
dir
```

Then launch any game using one of the commands below.

## 🎯 Aim Trainer

```powershell
py aim_trainer.py
```

## 🏎️ Car Game

```powershell
py car_game.py
```

## 🧱 Breakout

```powershell
py Breakout.py
```

## 🚦 Crossy Road

```powershell
py crossy_road.py
```

## 🔴 Do Not Press

```powershell
py donotpress.py
```

## 🦖 Dino Hop

```powershell
py dyno_hop.py
```

## 🐦 Flappy Bird

```powershell
py flappy_bird.py
```

If your computer uses `python` instead of `py`, simply replace `py` in any command:

```powershell
python car_game.py
```

---

# 🎮 Controls

Controls differ between games and many are also shown inside the game itself.

Common controls used throughout the collection include:

| Input | Typical use |
|---|---|
| `WASD` | Movement |
| Arrow keys | Movement / steering |
| `Space` | Jump / action |
| Mouse | Aim / click / menu interaction |
| `Esc` | Pause / back / exit menus |

If something appears unclear, start the game and check its menu or on-screen instructions.

---

# 💾 Save files and high scores

Some games create local `.json` save files while you play. These may store things such as:

- High scores
- Coins
- Unlocks
- Selected cars or skins
- Settings
- Progress

These save files are generated automatically and are not required to start a fresh game.

They are intentionally ignored by Git using `.gitignore`, so personal progress is not uploaded to the repository by accident.

Deleting a game's save file may reset that game's progress.

---

# 🛠️ Troubleshooting

## `ModuleNotFoundError: No module named 'pygame'`

Pygame is missing from the Python installation you are currently using.

Run:

```powershell
py -m pip install pygame
```

Then try the game again.

---

## `py` is not recognized

Try:

```powershell
python --version
```

If that works, use `python` instead:

```powershell
python flappy_bird.py
```

If neither `py` nor `python` works, Python is probably not installed correctly or is not available in PATH.

---

## PowerShell says it cannot find the game file

You are probably in the wrong directory.

Check where you are:

```powershell
pwd
```

Check which files are there:

```powershell
dir
```

Move into the repository folder, for example:

```powershell
cd "$HOME\Downloads\py-games"
```

Then run the game again.

> Your exact folder path may be different depending on where you extracted or cloned the repository.

---

## Pygame is installed but the game still says it is missing

You may have multiple Python installations.

Check Python:

```powershell
py --version
```

Check pip for that same Python:

```powershell
py -m pip --version
```

Check Pygame:

```powershell
py -m pip show pygame
```

Using `py -m pip` instead of only `pip` helps make sure the package is installed for the same Python version used to run the game.

---

## Update Pygame

```powershell
py -m pip install --upgrade pygame
```

## Update pip

```powershell
py -m pip install --upgrade pip
```

---

# 💻 Running from VS Code

You can also run the games from Visual Studio Code.

1. Open the `py-games` folder in VS Code.
2. Install the **Python** extension from Microsoft if needed.
3. Open the game file you want.
4. Select a Python interpreter.
5. Press the **Run Python File** button.

You can also use VS Code's integrated terminal:

```powershell
py car_game.py
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

---

# 🔄 Updating your local copy

If you cloned the repository using Git, you can download future changes with:

```powershell
git pull
```

If you downloaded the repository as a ZIP, simply download a fresh ZIP when you want the newest version.

---

# 🧪 Quick setup — copy/paste version

If you already have Python and Git installed, this is the fastest setup:

```powershell
git clone https://github.com/kodaniq/py-games.git
cd py-games
py -m pip install -r requirements.txt
py car_game.py
```

Change `car_game.py` to whichever game you want to launch.

---

# 📝 Notes

- These are desktop Python/Pygame projects.
- No external game assets are required for the current versions in this repository.
- Games can be launched individually.
- Internet access is not required to play after dependencies are installed.
- Closing the game window normally exits the program.

---

## ⭐ Have fun

Pick a game, launch it, and try to beat your score. 🎮🔥
