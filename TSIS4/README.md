# TSIS3 – Snake Extended

## setup

```bash
pip install pygame psycopg2-binary
```

## database (optional but needed for leaderboard)

create a postgres database and run:

```sql
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
```

then set the `DATABASE_URL` env variable or edit `get_conn()` in `db.py`:

```
DATABASE_URL=host=localhost dbname=snake_game user=postgres password=yourpassword
```

if psycopg2 or the database is unavailable, the game still runs fine –
leaderboard features are just disabled.

## run

```bash
python main.py
```

## controls

arrow keys or WASD to move
ESC to quit current game and go back to menu

## project structure

```
TSIS3/
├── main.py        # entry point, all screens, gameplay loop
├── game.py        # Snake, Food, TimedFood, PoisonFood, PowerUp, Obstacle
├── db.py          # psycopg2 helpers (leaderboard + sessions)
├── config.py      # constants, colors, settings load/save
├── settings.json  # user preferences (auto-created)
└── assets/        # put sounds here if you add them
```
