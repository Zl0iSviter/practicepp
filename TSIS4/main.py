import pygame
import sys
from config import *
from db import init_db, save_session, get_personal_best, get_leaderboard, DB_AVAILABLE
from game import (Snake, Food, TimedFood, PoisonFood, PowerUp, Obstacle,
                  spawn_obstacles, draw_grid, draw_hud, draw_overlay)




def make_fonts():
    return {
        'big':   pygame.font.SysFont('consolas', 32, bold=True),
        'med':   pygame.font.SysFont('consolas', 22, bold=True),
        'btn':   pygame.font.SysFont('consolas', 20, bold=True),
        'small': pygame.font.SysFont('consolas', 16),
        'tiny':  pygame.font.SysFont('consolas', 13),
    }


# ---- ui helpers ----

def draw_button(screen, text, rect, fonts, bg=(60, 60, 60), fg=WHITE, hover_bg=None):
    mx, my = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mx, my)
    col = hover_bg if (hovered and hover_bg) else bg
    pygame.draw.rect(screen, col, rect, border_radius=7)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=7)
    lbl = fonts['btn'].render(text, True, fg)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return hovered


def btn_clicked(rect, event):
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and rect.collidepoint(event.pos)




def screen_menu(screen, fonts, settings):
    bw, bh = 200, 50
    cx = WIDTH // 2 - bw // 2
    btns = {
        'play':        pygame.Rect(cx, 230, bw, bh),
        'leaderboard': pygame.Rect(cx, 295, bw, bh),
        'settings':    pygame.Rect(cx, 360, bw, bh),
        'quit':        pygame.Rect(cx, 425, bw, bh),
    }

    stripe_y = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            for name, rect in btns.items():
                if btn_clicked(rect, event):
                    return name

        # draw
        screen.fill(BLACK)
        # moving stripe decoration
        stripe_y = (stripe_y + 1) % 60
        for y in range(-60 + stripe_y, HEIGHT, 60):
            pygame.draw.rect(screen, (20, 20, 20), (0, y, WIDTH, 30))

        title = fonts['big'].render('S N A K E', True, GREEN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

        draw_button(screen, 'PLAY',        btns['play'],        fonts, (30, 140, 50),  BLACK, (50, 200, 80))
        draw_button(screen, 'LEADERBOARD', btns['leaderboard'], fonts, (30, 80,  160), WHITE, (50, 120, 220))
        draw_button(screen, 'SETTINGS',    btns['settings'],    fonts, (70, 70,  70),  WHITE, (110, 110, 110))
        draw_button(screen, 'QUIT',        btns['quit'],        fonts, (140, 30, 30),  WHITE, (220, 50, 50))

        if not DB_AVAILABLE:
            warn = fonts['tiny'].render('db not connected – leaderboard disabled', True, DRED)
            screen.blit(warn, warn.get_rect(center=(WIDTH // 2, HEIGHT - 20)))

        pygame.display.flip()


# ---- username entry ----

def screen_username(screen, fonts, last_name: str = '') -> str:
    name  = last_name
    clock = pygame.time.Clock()
    bw, bh = 160, 46
    btn_ok = pygame.Rect(WIDTH // 2 - bw // 2, 380, bw, bh)

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return last_name or 'player'
                elif len(name) < 16 and event.unicode.isprintable():
                    name += event.unicode
            if btn_clicked(btn_ok, event) and name.strip():
                return name.strip()

        screen.fill(BLACK)
        title  = fonts['med'].render('enter your username', True, CYAN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 200)))

        box = pygame.Rect(WIDTH // 2 - 140, 270, 280, 50)
        pygame.draw.rect(screen, (20, 20, 20), box, border_radius=6)
        pygame.draw.rect(screen, CYAN, box, 2, border_radius=6)
        cursor = '|' if (pygame.time.get_ticks() // 500) % 2 == 0 else ''
        txt = fonts['btn'].render(name + cursor, True, WHITE)
        screen.blit(txt, txt.get_rect(center=box.center))

        draw_button(screen, 'OK', btn_ok, fonts, (30, 140, 50), BLACK, (50, 200, 80))
        pygame.display.flip()


# ---- settings screen ----

def screen_settings(screen, fonts, settings: dict) -> dict:
    """mutates settings dict and saves on back"""
    bw, bh = 200, 46
    cx = WIDTH // 2

    btn_grid  = pygame.Rect(cx + 10, 200, bw, bh)
    btn_sound = pygame.Rect(cx + 10, 265, bw, bh)
    btn_color = pygame.Rect(cx + 10, 330, bw, bh)
    btn_back  = pygame.Rect(cx - 100, 450, 200, 48)

    # cycle through preset colors
    preset_colors = [
        [60, 200, 90],   # green
        [60, 130, 240],  # blue
        [240, 200, 60],  # yellow
        [255, 100, 180], # pink
        [180, 80, 220],  # purple
        [255, 150, 30],  # orange
    ]
    color_names = ['green', 'blue', 'yellow', 'pink', 'purple', 'orange']

    def cur_color_idx():
        c = settings['snake_color']
        for i, p in enumerate(preset_colors):
            if p == c:
                return i
        return 0

    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_clicked(btn_grid, event):
                settings['grid_overlay'] = not settings['grid_overlay']
                save_settings(settings)
            if btn_clicked(btn_sound, event):
                settings['sound'] = not settings['sound']
                save_settings(settings)
            if btn_clicked(btn_color, event):
                idx = (cur_color_idx() + 1) % len(preset_colors)
                settings['snake_color'] = preset_colors[idx]
                save_settings(settings)
            if btn_clicked(btn_back, event):
                return settings
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return settings

        screen.fill(BLACK)
        title = fonts['med'].render('SETTINGS', True, YELLOW)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 110)))

        lx = 50
        for lbl_txt, y in [('grid overlay:', 213), ('sound:', 278), ('snake color:', 343)]:
            lbl = fonts['small'].render(lbl_txt, True, LGRAY)
            screen.blit(lbl, (lx, y + 14))

        g_col  = GREEN if settings['grid_overlay'] else DRED
        s_col  = GREEN if settings['sound']         else DRED
        ci     = cur_color_idx()
        c_col  = tuple(preset_colors[ci])
        c_name = color_names[ci].upper()

        draw_button(screen, 'ON' if settings['grid_overlay'] else 'OFF', btn_grid,  fonts, g_col, BLACK, None)
        draw_button(screen, 'ON' if settings['sound']         else 'OFF', btn_sound, fonts, s_col, BLACK, None)
        draw_button(screen, c_name, btn_color, fonts, c_col, BLACK, None)
        draw_button(screen, 'SAVE & BACK', btn_back, fonts, (70, 70, 70), WHITE, (110, 110, 110))

        hint = fonts['tiny'].render('click to cycle options', True, GRAY)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 405)))
        pygame.display.flip()


# ---- leaderboard screen ----

def screen_leaderboard(screen, fonts):
    clock   = pygame.time.Clock()
    entries = get_leaderboard(10)
    btn_back = pygame.Rect(WIDTH // 2 - 90, HEIGHT - 65, 180, 44)

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_clicked(btn_back, event):
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.fill(BLACK)
        title = fonts['med'].render('TOP 10 LEADERBOARD', True, YELLOW)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 45)))

        # headers
        cols = [20, 55, 185, 285, 365, 475]
        hdrs = ['#', 'name', 'score', 'level', 'date']
        for i, h in enumerate(hdrs):
            lbl = fonts['tiny'].render(h.upper(), True, CYAN)
            screen.blit(lbl, (cols[i], 85))
        pygame.draw.line(screen, GRAY, (15, 103), (WIDTH - 15, 103), 1)

        medal = [YELLOW, (200, 200, 200), (200, 140, 60)]

        if not entries:
            msg = fonts['small'].render('no data – db not connected or no games yet', True, LGRAY)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, 250)))
        else:
            for i, e in enumerate(entries):
                y   = 112 + i * 32
                rc  = medal[i] if i < 3 else WHITE
                row = [str(e['rank']), e['username'][:12], str(e['score']),
                       str(e['level']), e['played_at']]
                for j, val in enumerate(row):
                    lbl = fonts['small'].render(val, True, rc)
                    screen.blit(lbl, (cols[j], y))

        draw_button(screen, 'BACK', btn_back, fonts, (70, 70, 70), WHITE, (110, 110, 110))
        pygame.display.flip()


# ---- game over screen ----

def screen_gameover(screen, fonts, score, level, personal_best, username):
    bw, bh  = 175, 48
    cx      = WIDTH // 2
    btn_retry = pygame.Rect(cx - bw - 10, 440, bw, bh)
    btn_menu  = pygame.Rect(cx + 10,      440, bw, bh)
    clock     = pygame.time.Clock()

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_clicked(btn_retry, event): return 'retry'
            if btn_clicked(btn_menu,  event): return 'menu'

        screen.fill((15, 0, 0))
        title = fonts['big'].render('GAME OVER', True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 110)))

        rows = [
            ('player',        username),
            ('score',         str(score)),
            ('level reached', str(level)),
            ('personal best', str(personal_best)),
        ]
        for i, (lbl, val) in enumerate(rows):
            y  = 190 + i * 50
            ls = fonts['small'].render(lbl + ':', True, LGRAY)
            vs = fonts['med'].render(val, True, YELLOW)
            screen.blit(ls, (80, y))
            screen.blit(vs, (280, y))

        draw_button(screen, 'RETRY',     btn_retry, fonts, (30, 140, 50), BLACK, (50, 200, 80))
        draw_button(screen, 'MAIN MENU', btn_menu,  fonts, (30, 80, 160), WHITE, (50, 120, 220))
        pygame.display.flip()


def run_game(screen, settings: dict, username: str, fonts) -> tuple:
    snake_color = tuple(settings.get('snake_color', [60, 200, 90]))
    show_grid   = settings.get('grid_overlay', True)

    snake = Snake(color=snake_color)
    food  = Food()

    # timed food – second food item that can expire
    timed_food = TimedFood()
    timed_food.generate_random_pos(snake, [])

    poison     = PoisonFood()
    powerup    = PowerUp()
    obstacles: list[Obstacle] = []

    food.generate_random_pos(snake, obstacles)

    score       = 0
    level       = 1
    current_fps = BASE_FPS
    foods_eaten = 0
    level_flash = 0

    # power-up effect tracking
    active_pu_name: str | None = None
    pu_effect_end = 0         # pygame ticks when effect expires
    base_fps_saved = BASE_FPS # saved fps to restore after speed/slow

    # spawn interval for powerup (every 15 foods roughly)
    pu_spawn_counter = 0
    POISON_SPAWN_EVERY = 5  # every N foods, try to spawn poison

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(current_fps)

        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return score, level
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.set_direction(1,  0)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    snake.set_direction(-1, 0)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    snake.set_direction(0,  1)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    snake.set_direction(0, -1)

        # --- update ---
        snake.move()

        if not snake.alive:
            running = False
            break

        # obstacle collision
        for obs in obstacles:
            if snake.head_at(obs.x, obs.y):
                if snake.shield:
                    snake.shield = False
                else:
                    snake.alive = False
                    running = False
                    break

        if not running:
            break

        # check power-up effect expiry
        if active_pu_name in ('speed', 'slow'):
            if pygame.time.get_ticks() >= pu_effect_end:
                current_fps    = base_fps_saved
                active_pu_name = None

        # timed food update
        timed_food.update()
        if timed_food.expired:
            timed_food.generate_random_pos(snake, obstacles)

        # poison update
        poison.update()

        # powerup field update
        powerup.update()

        # --- eating normal food ---
        head = snake.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            score       += food.weight * 10
            foods_eaten += 1
            snake.grow()
            food.generate_random_pos(snake, obstacles)
            pu_spawn_counter += 1

            # level up check
            if foods_eaten >= FOODS_PER_LEVEL:
                level       += 1
                foods_eaten  = 0
                base_fps_saved  = BASE_FPS + (level - 1) * SPEED_INCREMENT
                if active_pu_name not in ('speed', 'slow'):
                    current_fps = base_fps_saved
                level_flash = int(current_fps * 1.5)

                # add obstacles from level 3
                if level >= OBSTACLES_START_LEVEL:
                    new_obs = spawn_obstacles(OBSTACLES_PER_LEVEL, snake, obstacles)
                    obstacles.extend(new_obs)
                    # make sure food/timed_food isn't on new obstacle
                    food.generate_random_pos(snake, obstacles)
                    timed_food.generate_random_pos(snake, obstacles)

            # maybe spawn poison
            if pu_spawn_counter % POISON_SPAWN_EVERY == 0 and not poison.active:
                poison.spawn(snake, obstacles)

            # maybe spawn powerup
            if pu_spawn_counter % 7 == 0 and not powerup.active:
                powerup.spawn(snake, obstacles)

        # --- eating timed food ---
        if not timed_food.expired:
            if head.x == timed_food.pos.x and head.y == timed_food.pos.y:
                score += timed_food.weight * 10
                snake.grow()
                timed_food.generate_random_pos(snake, obstacles)

        # --- eating poison ---
        if poison.active:
            if head.x == poison.pos.x and head.y == poison.pos.y:
                poison.active = False
                if not snake.shorten(2):
                    running = False
                    break

        # --- collecting power-up ---
        if powerup.active:
            if head.x == powerup.pos.x and head.y == powerup.pos.y:
                powerup.active    = False
                active_pu_name    = powerup.kind
                if powerup.kind == 'speed':
                    base_fps_saved = current_fps
                    current_fps    = min(current_fps + 4, 25)
                    pu_effect_end  = pygame.time.get_ticks() + POWERUP_EFFECT_MS
                elif powerup.kind == 'slow':
                    base_fps_saved = current_fps
                    current_fps    = max(current_fps - 3, 2)
                    pu_effect_end  = pygame.time.get_ticks() + POWERUP_EFFECT_MS
                elif powerup.kind == 'shield':
                    snake.shield = True

        if level_flash > 0:
            level_flash -= 1

        # --- draw ---
        screen.fill(BLACK)
        draw_grid(screen, show_grid)

        for obs in obstacles:
            obs.draw(screen)

        food.draw(screen)
        if not timed_food.expired:
            timed_food.draw(screen)
        poison.draw(screen)
        powerup.draw(screen)
        snake.draw(screen)

        pu_end_ms = pu_effect_end if active_pu_name in ('speed', 'slow') else 0
        pb = get_personal_best(username)
        draw_hud(screen, score, level, current_fps, pb,
                 active_pu_name, pu_end_ms)

        if level_flash > 0:
            draw_overlay(screen, [f'LEVEL {level}!', f'Speed x{level}'], ORANGE)

        pygame.display.flip()

    # brief red flash
    screen.fill((120, 0, 0))
    crash = fonts['med'].render('GAME OVER LOX', True, WHITE)
    screen.blit(crash, crash.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.delay(700)

    return score, level


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('snake')

    fonts    = make_fonts()
    settings = load_settings()

    init_db()

    state    = 'menu'
    username = 'player'
    last_score = 0
    last_level = 1

    while True:

        if state == 'menu':
            action = screen_menu(screen, fonts, settings)
            if action == 'play':
                state = 'username'
            elif action == 'leaderboard':
                state = 'leaderboard'
            elif action == 'settings':
                state = 'settings'
            elif action == 'quit':
                pygame.quit(); sys.exit()

        elif state == 'username':
            username = screen_username(screen, fonts, username)
            state = 'game'

        elif state == 'settings':
            settings = screen_settings(screen, fonts, settings)
            state = 'menu'

        elif state == 'leaderboard':
            screen_leaderboard(screen, fonts)
            state = 'menu'

        elif state == 'game':
            last_score, last_level = run_game(screen, settings, username, fonts)
            save_session(username, last_score, last_level)
            state = 'gameover'

        elif state == 'gameover':
            pb     = get_personal_best(username)
            action = screen_gameover(screen, fonts, last_score, last_level, pb, username)
            if action == 'retry':
                state = 'game'
            else:
                state = 'menu'


main()
