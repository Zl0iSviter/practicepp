import json
import os

# --- window / grid ---
WIDTH       = 600
HEIGHT      = 660       # 600 play + 60 hud
CELL        = 30
GRID_COLS   = WIDTH  // CELL    # 20
GRID_ROWS   = HEIGHT // CELL    # 22
PLAY_ROWS   = 20                # rows actually used for gameplay

# --- game tuning ---
BASE_FPS          = 5
SPEED_INCREMENT   = 2
FOODS_PER_LEVEL   = 3
POISON_CHANCE     = 0.25        # probability that extra food is poison
POWERUP_FIELD_TTL = 8000        # ms before a powerup disappears from field
POWERUP_EFFECT_MS = 5000        # ms for speed-boost / slow-motion effect
TIMED_FOOD_TTL    = 7000        # ms before a timed food disappears
OBSTACLES_START_LEVEL = 3       # obstacles appear from this level onward
OBSTACLES_PER_LEVEL   = 3       # how many blocks to add each new level

# --- colors ---
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
GRAY    = (40,  40,  40)
LGRAY   = (120, 120, 120)
RED     = (220, 50,  50)
DRED    = (140, 20,  20)        # poison food
YELLOW  = (240, 200, 60)
GREEN   = (60,  200, 90)
CYAN    = (80,  220, 220)
ORANGE  = (255, 150, 30)
PURPLE  = (180, 80,  220)
BLUE    = (60,  130, 240)
PINK    = (255, 100, 180)

# powerup colors
PU_COLOR = {
    'speed':  (80,  240, 80),
    'slow':   BLUE,
    'shield': PURPLE,
}

# --- settings file ---
SETTINGS_FILE = 'settings.json'

DEFAULT_SETTINGS = {
    'snake_color': [60, 200, 90],   # RGB list (JSON-friendly)
    'grid_overlay': True,
    'sound': False,                  # off by default since we have no wav files
}


def load_settings() -> dict:
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE) as f:
            data = json.load(f)
        # fill missing keys
        for k, v in DEFAULT_SETTINGS.items():
            if k not in data:
                data[k] = v
        return data
    except Exception:
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()


def save_settings(s: dict):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, indent=2)
