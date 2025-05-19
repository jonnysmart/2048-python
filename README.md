
# 2048 Game – Python Implementation

A desktop clone of the classic **2048** sliding‑block puzzle, written in Python with the Pygame library.  
Combine identical numbered tiles on a 4×4 grid to reach the elusive **2048** tile before the board fills up.

## Features

- Smooth graphical interface built with Pygame  
- Arrow‑key controls for intuitive play  
- Automatic merging and spawning logic identical to the original game  
- Win / loss detection with on‑screen prompts to **Restart**, **Continue**, or **Quit**  
- Supports unlimited replays in a single session  
- Clean, well‑documented source code

## Requirements

- Python 3.8 or newer  
- [Pygame](https://www.pygame.org/) 2.x


## Installation

```bash
# 1. Clone or download this repository
git clone https://github.com/your‑username/2048‑python.git
cd 2048‑python

# 2. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate 

# 3. Install dependencies
pip install pygame
```

## Usage

```bash
python game_2048.py
```

**Controls**

| Key | Action      |
|-----|-------------|
| ←   | Move left   |
| ↑   | Move up     |
| →   | Move right  |
| ↓   | Move down   |
| R   | Restart (after win/lose) |
| C   | Continue playing (after win) |
| Q   | Quit game   |


## Project Structure

```
├── game_2048.py                    
└── README.md
```


## Screenshot

* *


## Acknowledgements

- Original [2048] game by **Gabriele Cirulli**  
- Pygame community & documentation  

