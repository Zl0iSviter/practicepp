import pygame
from persistence import load_leaderboard, load_settings, save_settings

# colors we use throughout ui
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GRAY    = (80,  80,  80)
DGRAY   = (40,  40,  40)
RED     = (220, 50,  50)
GREEN   = (50,  200, 80)
BLUE    = (50,  120, 220)
YELLOW  = (240, 200, 30)
ORANGE  = (240, 130, 30)
CYAN    = (0,   200, 220)
ROAD_BG = (30,  30,  30)


# --- helper: draw a simple rounded button and return if it was clicked ---
def draw_button(screen, text, rect, font, bg=GRAY, fg=WHITE, hover_bg=None, border=2):
    mx, my = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mx, my)
    color = hover_bg if (hovered and hover_bg) else bg
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, border, border_radius=8)
    label = font.render(text, True, fg)
    screen.blit(label, label.get_rect(center=rect.center))
    return hovered


def check_button_click(rect, event):
    # returns true if mouse clicked inside the rect
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        return rect.collidepoint(event.pos)
    return False


# ---- main menu screen ----
class MainMenu:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.W, self.H = screen.get_size()

        # define button rects
        bw, bh = 220, 52
        cx = self.W // 2 - bw // 2
        self.btn_play       = pygame.Rect(cx, 230, bw, bh)
        self.btn_leaderboard= pygame.Rect(cx, 300, bw, bh)
        self.btn_settings   = pygame.Rect(cx, 370, bw, bh)
        self.btn_quit       = pygame.Rect(cx, 440, bw, bh)

        # simple road stripe animation
        self.stripe_y = 0

    def handle(self, event):
        # returns 'play', 'leaderboard', 'settings', 'quit', or None
        if check_button_click(self.btn_play, event):        return 'play'
        if check_button_click(self.btn_leaderboard, event): return 'leaderboard'
        if check_button_click(self.btn_settings, event):    return 'settings'
        if check_button_click(self.btn_quit, event):        return 'quit'
        return None

    def draw(self):
        self.screen.fill(ROAD_BG)

        # scrolling road stripes for decoration
        self.stripe_y = (self.stripe_y + 2) % 60
        for y in range(-60 + self.stripe_y, self.H, 60):
            pygame.draw.rect(self.screen, (60, 60, 60), (self.W // 2 - 5, y, 10, 35))

        # title
        title = self.fonts['big'].render('RACER', True, YELLOW)
        sub   = self.fonts['med'].render('ARCADE', True, ORANGE)
        self.screen.blit(title, title.get_rect(center=(self.W // 2, 110)))
        self.screen.blit(sub,   sub.get_rect(center=(self.W // 2, 175)))

        # buttons
        draw_button(self.screen, 'PLAY',        self.btn_play,        self.fonts['btn'], GREEN,  BLACK, (80, 220, 100))
        draw_button(self.screen, 'LEADERBOARD', self.btn_leaderboard, self.fonts['btn'], BLUE,   WHITE, (80, 150, 255))
        draw_button(self.screen, 'SETTINGS',    self.btn_settings,    self.fonts['btn'], GRAY,   WHITE, (110, 110, 110))
        draw_button(self.screen, 'QUIT',        self.btn_quit,        self.fonts['btn'], RED,    WHITE, (255, 80,  80))


# ---- username entry screen ----
class UsernameScreen:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts  = fonts
        self.W, self.H = screen.get_size()
        self.name   = ''
        self.active = True
        bw, bh = 180, 48
        self.btn_ok = pygame.Rect(self.W // 2 - bw // 2, 340, bw, bh)

    def handle(self, event):
        # returns the entered name when done, or None to keep going
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.name.strip():
                return self.name.strip()
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif len(self.name) < 16 and event.unicode.isprintable():
                self.name += event.unicode
        if check_button_click(self.btn_ok, event) and self.name.strip():
            return self.name.strip()
        return None

    def draw(self):
        self.screen.fill(ROAD_BG)
        prompt = self.fonts['med'].render('enter your name', True, WHITE)
        self.screen.blit(prompt, prompt.get_rect(center=(self.W // 2, 200)))

        # text input box
        box = pygame.Rect(self.W // 2 - 130, 265, 260, 48)
        pygame.draw.rect(self.screen, DGRAY, box, border_radius=6)
        pygame.draw.rect(self.screen, CYAN,  box, 2, border_radius=6)
        txt = self.fonts['btn'].render(self.name + ('|' if (pygame.time.get_ticks() // 500) % 2 == 0 else ''), True, WHITE)
        self.screen.blit(txt, txt.get_rect(center=box.center))

        draw_button(self.screen, 'START', self.btn_ok, self.fonts['btn'], GREEN, BLACK, (80, 220, 100))


# ---- settings screen ----
class SettingsScreen:
    def __init__(self, screen, fonts):
        self.screen   = screen
        self.fonts    = fonts
        self.W, self.H = screen.get_size()
        self.settings = load_settings()

        bw, bh = 180, 44
        cx = self.W // 2
        self.btn_sound  = pygame.Rect(cx + 20,  200, bw, bh)
        self.btn_color  = pygame.Rect(cx + 20,  265, bw, bh)
        self.btn_diff   = pygame.Rect(cx + 20,  330, bw, bh)
        self.btn_back   = pygame.Rect(cx - 90,  430, 180, 48)

        self.car_colors = ['blue', 'red', 'green', 'yellow']
        self.diffs      = ['easy', 'normal', 'hard']

    def handle(self, event):
        # returns 'back' or None, and modifies settings in place
        if check_button_click(self.btn_sound, event):
            self.settings['sound'] = not self.settings['sound']
            save_settings(self.settings)

        if check_button_click(self.btn_color, event):
            idx = self.car_colors.index(self.settings['car_color'])
            self.settings['car_color'] = self.car_colors[(idx + 1) % len(self.car_colors)]
            save_settings(self.settings)

        if check_button_click(self.btn_diff, event):
            idx = self.diffs.index(self.settings['difficulty'])
            self.settings['difficulty'] = self.diffs[(idx + 1) % len(self.diffs)]
            save_settings(self.settings)

        if check_button_click(self.btn_back, event):
            return 'back'
        return None

    def draw(self):
        self.screen.fill(ROAD_BG)
        title = self.fonts['med'].render('SETTINGS', True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(self.W // 2, 120)))

        lx = 50
        # sound label
        s_lbl = self.fonts['small'].render('sound:', True, WHITE)
        self.screen.blit(s_lbl, (lx, 213))
        s_val = 'ON' if self.settings['sound'] else 'OFF'
        s_col = GREEN if self.settings['sound'] else RED
        draw_button(self.screen, s_val, self.btn_sound, self.fonts['btn'], s_col, BLACK, None)

        # car color label
        c_lbl = self.fonts['small'].render('car color:', True, WHITE)
        self.screen.blit(c_lbl, (lx, 278))
        cc = self.settings['car_color']
        cc_map = {'blue': BLUE, 'red': RED, 'green': GREEN, 'yellow': YELLOW}
        draw_button(self.screen, cc.upper(), self.btn_color, self.fonts['btn'], cc_map.get(cc, GRAY), BLACK, None)

        # difficulty label
        d_lbl = self.fonts['small'].render('difficulty:', True, WHITE)
        self.screen.blit(d_lbl, (lx, 343))
        diff = self.settings['difficulty']
        dc = GREEN if diff == 'easy' else (ORANGE if diff == 'normal' else RED)
        draw_button(self.screen, diff.upper(), self.btn_diff, self.fonts['btn'], dc, BLACK, None)

        draw_button(self.screen, 'BACK', self.btn_back, self.fonts['btn'], GRAY, WHITE, (110, 110, 110))

        hint = self.fonts['tiny'].render('click buttons to cycle options', True, (130, 130, 130))
        self.screen.blit(hint, hint.get_rect(center=(self.W // 2, 400)))


# ---- leaderboard screen ----
class LeaderboardScreen:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts  = fonts
        self.W, self.H = screen.get_size()
        self.btn_back = pygame.Rect(self.W // 2 - 90, self.H - 70, 180, 46)

    def handle(self, event):
        if check_button_click(self.btn_back, event):
            return 'back'
        return None

    def draw(self):
        self.screen.fill(ROAD_BG)
        title = self.fonts['med'].render('LEADERBOARD', True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(self.W // 2, 55)))

        # column headers
        headers = ['#', 'name', 'score', 'dist', 'coins']
        col_x   = [20, 55, 175, 265, 330]
        for i, h in enumerate(headers):
            lbl = self.fonts['tiny'].render(h.upper(), True, CYAN)
            self.screen.blit(lbl, (col_x[i], 100))
        pygame.draw.line(self.screen, GRAY, (15, 118), (self.W - 15, 118), 1)

        entries = load_leaderboard()
        rank_colors = [YELLOW, (200, 200, 200), (200, 140, 60)]  # gold/silver/bronze

        for i, entry in enumerate(entries[:10]):
            y = 130 + i * 35
            rc = rank_colors[i] if i < 3 else WHITE
            rank  = self.fonts['small'].render(f'{i+1}', True, rc)
            name  = self.fonts['small'].render(entry.get('name', '?')[:12], True, rc)
            score = self.fonts['small'].render(str(entry.get('score', 0)), True, rc)
            dist  = self.fonts['small'].render(f"{entry.get('distance', 0)}m", True, rc)
            coins = self.fonts['small'].render(str(entry.get('coins', 0)), True, rc)
            for surf, x in zip([rank, name, score, dist, coins], col_x):
                self.screen.blit(surf, (x, y))

        if not entries:
            empty = self.fonts['small'].render('no scores yet — go race!', True, GRAY)
            self.screen.blit(empty, empty.get_rect(center=(self.W // 2, 260)))

        draw_button(self.screen, 'BACK', self.btn_back, self.fonts['btn'], GRAY, WHITE, (110, 110, 110))


# ---- game over screen ----
class GameOverScreen:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts  = fonts
        self.W, self.H = screen.get_size()
        bw, bh = 180, 48
        cx = self.W // 2
        self.btn_retry = pygame.Rect(cx - bw - 10, 420, bw, bh)
        self.btn_menu  = pygame.Rect(cx + 10,       420, bw, bh)

    def handle(self, event):
        if check_button_click(self.btn_retry, event): return 'retry'
        if check_button_click(self.btn_menu,  event): return 'menu'
        return None

    def draw(self, score, distance, coins, powerup_bonus):
        self.screen.fill((20, 0, 0))
        title = self.fonts['big'].render('GAME OVER', True, RED)
        self.screen.blit(title, title.get_rect(center=(self.W // 2, 110)))

        # stats
        rows = [
            ('score',        str(score)),
            ('distance',     f'{distance} m'),
            ('coins',        str(coins)),
            ('powerup bonus',str(powerup_bonus)),
        ]
        for i, (label, val) in enumerate(rows):
            y = 210 + i * 45
            l_surf = self.fonts['small'].render(label + ':', True, (180, 180, 180))
            v_surf = self.fonts['btn'].render(val, True, YELLOW)
            self.screen.blit(l_surf, (80, y))
            self.screen.blit(v_surf, (260, y))

        draw_button(self.screen, 'RETRY',     self.btn_retry, self.fonts['btn'], GREEN, BLACK, (80, 220, 100))
        draw_button(self.screen, 'MAIN MENU', self.btn_menu,  self.fonts['btn'], BLUE,  WHITE, (80, 150, 255))
