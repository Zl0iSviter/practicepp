import pygame
import random
import sys
from persistence import load_settings, add_leaderboard_entry
from ui import (MainMenu, UsernameScreen, SettingsScreen,
                LeaderboardScreen, GameOverScreen)
from racer import (Player, EnemyCar, Coin, Obstacle, PowerUp, NitroStrip,
                   draw_road, draw_hud, WIDTH, HEIGHT)


# ---- difficulty presets ----
DIFF_SETTINGS = {
    'easy':   {'enemy_count': 2, 'obstacle_count': 1, 'coin_count': 4, 'base_scroll': 4},
    'normal': {'enemy_count': 3, 'obstacle_count': 2, 'coin_count': 3, 'base_scroll': 6},
    'hard':   {'enemy_count': 5, 'obstacle_count': 3, 'coin_count': 2, 'base_scroll': 8},
}


def make_fonts():
    # all fonts in one place so its easy to change
    return {
        'big':   pygame.font.SysFont('consolas', 58, bold=True),
        'med':   pygame.font.SysFont('consolas', 36, bold=True),
        'btn':   pygame.font.SysFont('consolas', 20, bold=True),
        'small': pygame.font.SysFont('consolas', 16),
        'tiny':  pygame.font.SysFont('consolas', 13),
    }


def run_game(screen, settings, username, fonts):
    """
    main gameplay loop. returns (score, distance, coins, powerup_bonus)
    when the run ends so the caller can save to leaderboard.
    """
    diff  = DIFF_SETTINGS.get(settings.get('difficulty', 'normal'), DIFF_SETTINGS['normal'])
    clock = pygame.time.Clock()

    # sound setup
    sound_on = settings.get('sound', True)
    # we dont have actual sound files in this build so we just skip loading
    # (original game had crash.wav / background.wav - keep those if you have them)

    # create player
    player = Player(car_color=settings.get('car_color', 'blue'))

    # sprite groups
    all_sprites   = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    coin_sprites  = pygame.sprite.Group()
    obstacle_sprites = pygame.sprite.Group()
    powerup_sprites  = pygame.sprite.Group()
    nitro_sprites    = pygame.sprite.Group()

    all_sprites.add(player)

    # spawn enemies based on difficulty
    for _ in range(diff['enemy_count']):
        e = EnemyCar(speed=diff['base_scroll'] + 1, player_rect=player.rect)
        all_sprites.add(e)
        enemy_sprites.add(e)

    # spawn coins
    for _ in range(diff['coin_count']):
        c = Coin(speed=diff['base_scroll'])
        all_sprites.add(c)
        coin_sprites.add(c)

    # spawn obstacles
    for _ in range(diff['obstacle_count']):
        o = Obstacle(speed=diff['base_scroll'], player_rect=player.rect)
        all_sprites.add(o)
        obstacle_sprites.add(o)

    # spawn one nitro strip
    ns = NitroStrip(speed=diff['base_scroll'])
    all_sprites.add(ns)
    nitro_sprites.add(ns)

    # game state
    score           = 0
    coins_collected = 0
    distance        = 0       # in "meters" (frames / 10)
    powerup_bonus   = 0
    frame_count     = 0
    stripe_offset   = 0       # for road animation
    active_powerup  = None    # name of current active powerup
    powerup_timer   = 0       # countdown for timed powerups

    # how often to spawn a new powerup (frames)
    POWERUP_SPAWN_INTERVAL = 400

    running = True
    while running:

        clock.tick(60)
        frame_count  += 1
        distance      = frame_count // 10
        stripe_offset = (stripe_offset + diff['base_scroll']) % 60

        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # abort run
                    return score, distance, coins_collected, powerup_bonus

        # --- updates ---
        player.move()
        player.update_powerups()

        for sprite in list(enemy_sprites) + list(coin_sprites) + \
                      list(obstacle_sprites) + list(nitro_sprites):
            sprite.move()

        # update powerups and remove expired ones
        for pu in list(powerup_sprites):
            pu.move()
            if pu.is_expired():
                pu.kill()

        # update active powerup timer
        if active_powerup and active_powerup != 'shield':
            powerup_timer -= 1
            if powerup_timer <= 0:
                active_powerup = None

        # spawn powerup periodically
        if frame_count % POWERUP_SPAWN_INTERVAL == 0:
            pu = PowerUp(speed=diff['base_scroll'])
            all_sprites.add(pu)
            powerup_sprites.add(pu)

        # difficulty ramps up over time (every 600 frames ~ 10 seconds)
        if frame_count % 600 == 0:
            for e in enemy_sprites:
                e.speed = min(e.speed + 1, 20)
            for o in obstacle_sprites:
                o.speed = min(o.speed + 1, 18)

        # --- coin collection ---
        for coin in pygame.sprite.spritecollide(player, coin_sprites, False):
            score           += coin.weight * 10
            coins_collected += 1
            coin.respawn()

        # --- powerup collection ---
        for pu in pygame.sprite.spritecollide(player, powerup_sprites, True):
            if pu.kind == 'nitro':
                player.apply_nitro(duration_ticks=240)
                active_powerup = 'nitro'
                powerup_timer  = 240
                powerup_bonus += 50
                score         += 50
            elif pu.kind == 'shield':
                player.apply_shield()
                active_powerup = 'shield'
                powerup_timer  = 0   # shield has no time limit, removed on hit
                powerup_bonus += 30
                score         += 30
            elif pu.kind == 'repair':
                # repair clears one obstacle near the player
                powerup_bonus += 20
                score         += 20
                active_powerup = 'repair'
                powerup_timer  = 60  # brief display
                for obs in list(obstacle_sprites):
                    if abs(obs.rect.centery - player.rect.centery) < 200:
                        obs._spawn_safe(player.rect)
                        break

        # --- nitro strip collection ---
        for ns in pygame.sprite.spritecollide(player, nitro_sprites, True):
            player.apply_nitro(duration_ticks=180)
            # respawn strip somewhere further up
            new_ns = NitroStrip(speed=diff['base_scroll'])
            all_sprites.add(new_ns)
            nitro_sprites.add(new_ns)

        # --- obstacle collision ---
        for obs in pygame.sprite.spritecollide(player, obstacle_sprites, False):
            if obs.kind == 'oil':
                # oil slows player briefly - just nudge spawn
                obs._spawn_safe(player.rect)
                # slow player briefly
                player.speed = max(2, player.speed - 2)
                pygame.time.set_timer(pygame.USEREVENT, 1500)
            elif obs.kind in ('pothole', 'barrier'):
                if not player.absorb_hit():
                    # game over
                    running = False
                    active_powerup = None
                else:
                    obs._spawn_safe(player.rect)
                    if active_powerup == 'shield':
                        active_powerup = None

        # restore speed after oil (listen for user event)
        for event in pygame.event.get(pygame.USEREVENT):
            if not player.nitro_active:
                player.speed = player.base_speed

        # --- enemy collision ---
        if pygame.sprite.spritecollideany(player, enemy_sprites):
            if not player.absorb_hit():
                running = False
            else:
                if active_powerup == 'shield':
                    active_powerup = None

        # --- drawing ---
        draw_road(screen, stripe_offset, player.nitro_active)

        # draw all sprites (player on top)
        for sprite in list(enemy_sprites) + list(obstacle_sprites) + \
                      list(coin_sprites) + list(powerup_sprites) + list(nitro_sprites):
            screen.blit(sprite.image, sprite.rect)
        screen.blit(player.image, player.rect)

        draw_hud(screen, score, distance, coins_collected,
                 player, active_powerup, powerup_timer, fonts)

        pygame.display.flip()

    # brief red flash on crash
    screen.fill((180, 0, 0))
    msg = fonts['med'].render('CRASH!', True, (255, 255, 255))
    screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.delay(800)

    return score, distance, coins_collected, powerup_bonus


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('racer - tsis3')

    fonts    = make_fonts()
    settings = load_settings()

    # screen state machine
    # states: 'menu', 'username', 'game', 'settings', 'leaderboard', 'gameover'
    state    = 'menu'
    username = 'player'
    last_result = None  # (score, distance, coins, powerup_bonus)

    menu_screen  = MainMenu(screen, fonts)
    lb_screen    = LeaderboardScreen(screen, fonts)
    set_screen   = SettingsScreen(screen, fonts)
    go_screen    = GameOverScreen(screen, fonts)
    un_screen    = UsernameScreen(screen, fonts)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ---- menu ----
            if state == 'menu':
                result = menu_screen.handle(event)
                if result == 'play':
                    un_screen = UsernameScreen(screen, fonts)  # fresh instance
                    state = 'username'
                elif result == 'leaderboard':
                    state = 'leaderboard'
                elif result == 'settings':
                    set_screen = SettingsScreen(screen, fonts)
                    state = 'settings'
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()

            # ---- username entry ----
            elif state == 'username':
                name = un_screen.handle(event)
                if name:
                    username = name
                    settings = load_settings()  # reload in case settings changed
                    state = 'game'

            # ---- settings ----
            elif state == 'settings':
                result = set_screen.handle(event)
                if result == 'back':
                    settings = load_settings()
                    state = 'menu'

            # ---- leaderboard ----
            elif state == 'leaderboard':
                result = lb_screen.handle(event)
                if result == 'back':
                    state = 'menu'

            # ---- game over ----
            elif state == 'gameover':
                result = go_screen.handle(event)
                if result == 'retry':
                    settings = load_settings()
                    state = 'game'
                elif result == 'menu':
                    state = 'menu'

        # ---- drawing per state ----
        if state == 'menu':
            menu_screen.draw()

        elif state == 'username':
            un_screen.draw()

        elif state == 'settings':
            set_screen.draw()

        elif state == 'leaderboard':
            lb_screen.draw()

        elif state == 'gameover':
            if last_result:
                go_screen.draw(*last_result)
            else:
                go_screen.draw(0, 0, 0, 0)

        elif state == 'game':
            # run game (blocking - has its own loop)
            result = run_game(screen, settings, username, fonts)
            last_result = result
            score, distance, coins, powerup_bonus = result
            # save to leaderboard
            add_leaderboard_entry(username, score, distance, coins)
            state = 'gameover'

        pygame.display.flip()


main()
