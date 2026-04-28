import pygame
import random
from config import *


class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def copy(self):
        return Point(self.x, self.y)


# ---- snake ----

class Snake:
    def __init__(self, color: tuple = GREEN):
        mid = PLAY_ROWS // 2
        self.body: list[Point] = [
            Point(10, mid),
            Point(9,  mid),
            Point(8,  mid),
        ]
        self.dx       = 1
        self.dy       = 0
        self.alive    = True
        self.color    = color
        self.shield   = False   # True when shield power-up is active

    def set_direction(self, dx: int, dy: int):
        # prevent reversing direction
        if dx == -self.dx and dy == -self.dy:
            return
        self.dx = dx
        self.dy = dy

    def move(self):
        # shift body segments
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # move head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        head = self.body[0]

        # wall collision
        if not (0 <= head.x < GRID_COLS and 0 <= head.y < PLAY_ROWS):
            if self.shield:
                # wrap back to opposite wall
                head.x = head.x % GRID_COLS
                head.y = head.y % PLAY_ROWS
                self.shield = False  # shield used up
            else:
                self.alive = False
                return

        # self collision
        for seg in self.body[1:]:
            if head.x == seg.x and head.y == seg.y:
                if self.shield:
                    self.shield = False
                else:
                    self.alive = False
                    return

    def grow(self):
        self.body.append(self.body[-1].copy())

    def shorten(self, by: int = 2):
        """remove `by` tail segments; returns False if snake too short"""
        for _ in range(by):
            if len(self.body) <= 1:
                self.alive = False
                return False
            self.body.pop()
        return True

    def occupies(self, x: int, y: int) -> bool:
        return any(s.x == x and s.y == y for s in self.body)

    def head_at(self, x: int, y: int) -> bool:
        return self.body[0].x == x and self.body[0].y == y

    def draw(self, screen):
        head = self.body[0]
        # head is brighter / outlined
        hx = head.x * CELL + 1
        hy = head.y * CELL + 1
        pygame.draw.rect(screen, RED, (hx, hy, CELL - 2, CELL - 2))
        # body segments
        for seg in self.body[1:]:
            pygame.draw.rect(
                screen, self.color,
                (seg.x * CELL + 2, seg.y * CELL + 2, CELL - 4, CELL - 4)
            )

        # shield glow
        if self.shield:
            hx2 = head.x * CELL
            hy2 = head.y * CELL
            pygame.draw.rect(screen, PURPLE, (hx2, hy2, CELL, CELL), 3)


# ---- food base ----

class Food:
    """Normal food – weighted score value."""
    WEIGHTS = {1: GREEN, 3: YELLOW, 5: ORANGE}

    def __init__(self):
        self.pos    = Point(15, 10)
        self.weight = 1
        self.color  = GREEN

    def _pick_weight(self):
        self.weight = random.choice(list(self.WEIGHTS.keys()))
        self.color  = self.WEIGHTS[self.weight]

    def generate_random_pos(self, snake: Snake, obstacles: list):
        """place food avoiding snake body and obstacle blocks"""
        blocked = {(o.x, o.y) for o in obstacles}
        while True:
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, PLAY_ROWS - 1)
            if not snake.occupies(x, y) and (x, y) not in blocked:
                self.pos.x = x
                self.pos.y = y
                self._pick_weight()
                return

    def draw(self, screen):
        px = self.pos.x * CELL + 2
        py = self.pos.y * CELL + 2
        pygame.draw.rect(screen, self.color, (px, py, CELL - 4, CELL - 4))
        # small weight number
        lbl = pygame.font.SysFont('consolas', 11).render(str(self.weight), True, BLACK)
        screen.blit(lbl, (px + 3, py + 3))


# ---- timed food ----

class TimedFood(Food):
    """Disappears from the field if not eaten within TIMED_FOOD_TTL ms."""

    def __init__(self):
        super().__init__()
        self.spawn_time = pygame.time.get_ticks()
        self.expired    = False

    def generate_random_pos(self, snake: Snake, obstacles: list):
        super().generate_random_pos(snake, obstacles)
        self.spawn_time = pygame.time.get_ticks()
        self.expired    = False

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > TIMED_FOOD_TTL:
            self.expired = True

    def draw(self, screen):
        if self.expired:
            return
        # show a shrinking alpha bar to hint at remaining time
        px = self.pos.x * CELL + 2
        py = self.pos.y * CELL + 2
        pygame.draw.rect(screen, CYAN, (px, py, CELL - 4, CELL - 4))
        elapsed = pygame.time.get_ticks() - self.spawn_time
        ratio   = max(0, 1 - elapsed / TIMED_FOOD_TTL)
        bar_w   = int((CELL - 6) * ratio)
        pygame.draw.rect(screen, WHITE, (px + 1, py + CELL - 10, bar_w, 4))
        lbl = pygame.font.SysFont('consolas', 11).render(str(self.weight), True, BLACK)
        screen.blit(lbl, (px + 3, py + 3))


# ---- poison food ----

class PoisonFood:
    """Eating this shortens the snake by 2 segments."""

    def __init__(self):
        self.pos     = Point(5, 5)
        self.active  = False   # only shown when spawned
        self.spawn_time = 0

    def spawn(self, snake: Snake, obstacles: list):
        blocked = {(o.x, o.y) for o in obstacles}
        for _ in range(100):
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, PLAY_ROWS - 1)
            if not snake.occupies(x, y) and (x, y) not in blocked:
                self.pos.x  = x
                self.pos.y  = y
                self.active = True
                self.spawn_time = pygame.time.get_ticks()
                return

    def update(self):
        # disappears after TIMED_FOOD_TTL ms as well
        if self.active:
            if pygame.time.get_ticks() - self.spawn_time > TIMED_FOOD_TTL:
                self.active = False

    def draw(self, screen):
        if not self.active:
            return
        px = self.pos.x * CELL + 2
        py = self.pos.y * CELL + 2
        pygame.draw.rect(screen, DRED, (px, py, CELL - 4, CELL - 4))
        # skull symbol (just an X)
        pygame.draw.line(screen, WHITE, (px + 2, py + 2), (px + CELL - 7, py + CELL - 7), 2)
        pygame.draw.line(screen, WHITE, (px + CELL - 7, py + 2), (px + 2, py + CELL - 7), 2)


# ---- power-up ----

class PowerUp:
    """
    kind: 'speed' | 'slow' | 'shield'
    spawned on the field for POWERUP_FIELD_TTL ms, then disappears.
    """

    def __init__(self):
        self.pos        = Point(0, 0)
        self.kind       = 'speed'
        self.active     = False   # True = visible on field
        self.spawn_time = 0
        self._font      = pygame.font.SysFont('consolas', 14, bold=True)

    def spawn(self, snake: Snake, obstacles: list):
        self.kind = random.choice(['speed', 'slow', 'shield'])
        blocked   = {(o.x, o.y) for o in obstacles}
        for _ in range(100):
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, PLAY_ROWS - 1)
            if not snake.occupies(x, y) and (x, y) not in blocked:
                self.pos.x      = x
                self.pos.y      = y
                self.active     = True
                self.spawn_time = pygame.time.get_ticks()
                return

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.spawn_time > POWERUP_FIELD_TTL:
                self.active = False

    def draw(self, screen):
        if not self.active:
            return
        px  = self.pos.x * CELL
        py  = self.pos.y * CELL
        col = PU_COLOR.get(self.kind, WHITE)
        pygame.draw.rect(screen, col, (px + 2, py + 2, CELL - 4, CELL - 4), border_radius=5)
        pygame.draw.rect(screen, WHITE, (px + 2, py + 2, CELL - 4, CELL - 4), 2, border_radius=5)
        labels = {'speed': '»', 'slow': '«', 'shield': '✦'}
        lbl = self._font.render(labels.get(self.kind, '?'), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(px + CELL // 2, py + CELL // 2)))


# ---- obstacle ----

class Obstacle:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, screen):
        px = self.x * CELL
        py = self.y * CELL
        pygame.draw.rect(screen, LGRAY, (px, py, CELL, CELL))
        pygame.draw.rect(screen, GRAY,  (px, py, CELL, CELL), 2)
        # brick lines
        pygame.draw.line(screen, GRAY, (px, py + CELL // 2), (px + CELL, py + CELL // 2), 1)
        pygame.draw.line(screen, GRAY, (px + CELL // 2, py), (px + CELL // 2, py + CELL // 2), 1)


def spawn_obstacles(count: int, snake: Snake, existing: list) -> list:
    """
    add `count` new obstacle blocks, ensuring:
    - not on snake body
    - not adjacent to snake head (so the snake isn't immediately trapped)
    - not duplicating existing obstacles
    """
    taken = {(o.x, o.y) for o in existing}
    # buffer cells around snake head
    hx, hy = snake.body[0].x, snake.body[0].y
    buffer = {(hx + dx, hy + dy) for dx in range(-2, 3) for dy in range(-2, 3)}
    new_obs = []
    attempts = 0
    while len(new_obs) < count and attempts < 500:
        attempts += 1
        x = random.randint(1, GRID_COLS - 2)
        y = random.randint(1, PLAY_ROWS - 2)
        if snake.occupies(x, y):
            continue
        if (x, y) in taken or (x, y) in buffer:
            continue
        taken.add((x, y))
        new_obs.append(Obstacle(x, y))
    return new_obs


# ---- drawing helpers ----

_grid_font = None
_hud_big   = None
_hud_small = None


def _init_fonts():
    global _grid_font, _hud_big, _hud_small
    if _hud_big is None:
        _grid_font = pygame.font.SysFont('consolas', 13)
        _hud_big   = pygame.font.SysFont('consolas', 26, bold=True)
        _hud_small = pygame.font.SysFont('consolas', 17)


def draw_grid(screen, show: bool):
    if not show:
        return
    for row in range(PLAY_ROWS):
        for col in range(GRID_COLS):
            pygame.draw.rect(screen, GRAY, (col * CELL, row * CELL, CELL, CELL), 1)


def draw_hud(screen, score, level, fps, personal_best,
             active_pu_name: str | None, pu_end_ms: int):
    _init_fonts()
    hud_y = PLAY_ROWS * CELL

    pygame.draw.rect(screen, (15, 15, 15), (0, hud_y, WIDTH, HEIGHT - hud_y))
    pygame.draw.line(screen, CYAN, (0, hud_y), (WIDTH, hud_y), 2)

    score_s = _hud_big.render(f'SCORE {score}', True, CYAN)
    level_s = _hud_big.render(f'LVL {level}', True, ORANGE)
    speed_s = _hud_small.render(f'{fps}fps', True, LGRAY)
    pb_s    = _hud_small.render(f'PB:{personal_best}', True, YELLOW)

    screen.blit(score_s, (8,   hud_y + 6))
    screen.blit(level_s, (220, hud_y + 6))
    screen.blit(speed_s, (430, hud_y + 6))
    screen.blit(pb_s,    (430, hud_y + 28))

    # active power-up countdown
    if active_pu_name:
        remaining = max(0, (pu_end_ms - pygame.time.get_ticks()) // 1000)
        col = PU_COLOR.get(active_pu_name, WHITE)
        pu_s = _hud_small.render(f'{active_pu_name.upper()} {remaining}s', True, col)
        screen.blit(pu_s, (8, hud_y + 36))


def draw_overlay(screen, lines: list, color=WHITE):
    _init_fonts()
    overlay = pygame.Surface((WIDTH, PLAY_ROWS * CELL), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))

    total_h  = len(lines) * 46
    start_y  = (PLAY_ROWS * CELL - total_h) // 2

    for i, line in enumerate(lines):
        surf = _hud_big.render(line, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, start_y + i * 46))
        screen.blit(surf, rect)
