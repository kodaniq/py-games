# Python Games

A collection of small Python games made with Python and Pygame.

## Games

- **Aim Trainer** — practice speed and accuracy by clicking targets.
- **Automäng** — a simple car/racing game.
- **Breakout** — classic brick-breaking arcade game.
- **Crossy Road** — cross roads, avoid traffic, and keep moving forward.
- **Do Not Press** — a chaotic button game with surprises.
- **Dino** — endless runner inspired by the classic browser dinosaur game.
- **Flappy Bird** — fly through pipes and try to beat your high score.

## Requirements

You need:

- **Python 3**
- **pip**
- **Pygame**

All current games in this repository use Pygame, so you only need to install it once.

### Install everything at once

Open **PowerShell** inside the downloaded/cloned `py-games` folder and run:

```powershell
py -m pip install -r requirements.txt
```

Or install Pygame directly:

```powershell
py -m pip install pygame
```

You do **not** need to install Pygame again for every game. Once it is installed for your Python installation, all of these games can use it.

## Download the repository

### Option 1 — GitHub ZIP

Click **Code → Download ZIP**, extract the ZIP, then open PowerShell inside the extracted folder.

### Option 2 — Git

```powershell
git clone https://github.com/kodaniq/py-games.git
cd py-games
py -m pip install -r requirements.txt
```

## Running the games

If you are already inside the `py-games` folder in PowerShell, use these commands:

### Aim Trainer

```powershell
py aim_trainer.py
```

### Automäng

```powershell
py automang.py
```

### Breakout

```powershell
py Breakout.py
```

### Crossy Road

```powershell
py crossy_road.py
```

### Do Not Press

```powershell
py donotpress.py
```

### Dino

```powershell
py dyno.py
```

### Flappy Bird

```powershell
py flappy_bird.py
```

## If `py` does not work

Some systems use `python` instead of `py`. For example:

```powershell
python -m pip install pygame
python flappy_bird.py
```

## Common problems

### `ModuleNotFoundError: No module named 'pygame'`

Install Pygame:

```powershell
py -m pip install pygame
```

### PowerShell cannot find the `.py` file

Make sure you are inside the correct folder first:

```powershell
cd path\to\py-games
```

Then run the game again.

You can also type `dir` to see the files in your current folder:

```powershell
dir
```

### Multiple Python versions installed

Check which Python you are using:

```powershell
py --version
```

Check whether Pygame is installed for that Python:

```powershell
py -m pip show pygame
```

## Save files

Some games may create local save/high-score files when you play. These are ignored by Git and are not required to download or run the games.

## Controls

Controls vary by game. Most games show their controls inside the game itself. Typical controls include:

- **Arrow keys / WASD** — movement
- **Space** — jump/action
- **Mouse** — aiming/clicking
- **Esc** — pause/back

## Tested setup

These projects are primarily intended for desktop Python on Windows and can be launched directly from PowerShell, VS Code, or another Python-capable terminal.

---

Have fun 🎮
