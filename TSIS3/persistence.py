import json
import os

# --- file paths ---
LEADERBOARD_FILE = 'leaderboard.json'
SETTINGS_FILE = 'settings.json'

# default settings if no file exists yet
DEFAULT_SETTINGS = {
    'sound': True,
    'car_color': 'blue',   # blue, red, green, yellow
    'difficulty': 'normal' # easy, normal, hard
}


# ---- leaderboard stuff ----

def load_leaderboard():
    # loads leaderboard from json file, returns empty list if file doesnt exist
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, KeyError):
        # file is corrupted or something, just start fresh
        return []


def save_leaderboard(entries):
    # saves leaderboard list to json
    # sort by score descending and keep top 10
    entries.sort(key=lambda x: x['score'], reverse=True)
    entries = entries[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(entries, f, indent=2)
    return entries


def add_leaderboard_entry(name, score, distance, coins):
    # adds new entry and saves, returns updated leaderboard
    entries = load_leaderboard()
    entries.append({
        'name': name,
        'score': score,
        'distance': distance,
        'coins': coins
    })
    return save_leaderboard(entries)


# ---- settings stuff ----

def load_settings():
    # loads settings from json, fills in defaults for missing keys
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            # fill in any missing keys with defaults
            for key, val in DEFAULT_SETTINGS.items():
                if key not in data:
                    data[key] = val
            return data
    except (json.JSONDecodeError, KeyError):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)
