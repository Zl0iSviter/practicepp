
import os
import psycopg2
import psycopg2.extras
DB_AVAILABLE = True

def get_conn():
    # edit this string to match your postgres setup
    dsn = os.environ.get(
        'DATABASE_URL',
        'host=localhost dbname=snake_game user=postgres password=1234'
    )
    return psycopg2.connect(dsn)


def init_db():
    """create tables if they don't exist yet"""
    if not DB_AVAILABLE:
        return
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id       SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id            SERIAL PRIMARY KEY,
                player_id     INTEGER REFERENCES players(id),
                score         INTEGER   NOT NULL,
                level_reached INTEGER   NOT NULL,
                played_at     TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[db] init_db error: {e}")


# ---- player helpers ----

def get_or_create_player(username: str) -> int | None:
    """returns player id, creating a row if needed"""
    if not DB_AVAILABLE:
        return None
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        row = cur.fetchone()
        if row:
            pid = row[0]
        else:
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id",
                (username,)
            )
            pid = cur.fetchone()[0]
            conn.commit()
        cur.close()
        conn.close()
        return pid
    except Exception as e:
        print(f"[db] get_or_create_player error: {e}")
        return None


def save_session(username: str, score: int, level: int):
    """save a completed game session to the database"""
    if not DB_AVAILABLE:
        return
    try:
        pid = get_or_create_player(username)
        if pid is None:
            return
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute(
            """
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s)
            """,
            (pid, score, level)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[db] save_session error: {e}")


def get_personal_best(username: str) -> int:
    """returns the player's all-time high score, or 0 if none"""
    if not DB_AVAILABLE:
        return 0
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(MAX(gs.score), 0)
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            WHERE p.username = %s
            """,
            (username,)
        )
        val = cur.fetchone()[0]
        cur.close()
        conn.close()
        return int(val)
    except Exception as e:
        print(f"[db] get_personal_best error: {e}")
        return 0


def get_leaderboard(limit: int = 10) -> list[dict]:
    """
    returns top `limit` sessions as list of dicts:
    { rank, username, score, level, played_at }
    """
    if not DB_AVAILABLE:
        return []
    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            SELECT p.username,
                   gs.score,
                   gs.level_reached,
                   gs.played_at
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        result = []
        for i, row in enumerate(rows):
            result.append({
                'rank':      i + 1,
                'username':  row['username'],
                'score':     row['score'],
                'level':     row['level_reached'],
                'played_at': row['played_at'].strftime('%Y-%m-%d') if row['played_at'] else '—',
            })
        return result
    except Exception as e:
        print(f"[db] get_leaderboard error: {e}")
        return []
