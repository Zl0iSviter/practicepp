import pygame
import random
import time

pygame.init()  # initializes all the pygame sub-modules

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # creating a game window
# set_mode() takes a tuple as an argument

image_background = pygame.image.load('AnimatedStreet.png')
image_player = pygame.image.load('Player.png')
image_enemy = pygame.image.load('Enemy.png')
image_coin = pygame.transform.scale_by(pygame.image.load('Coin.png'), 0.1)

pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound('crash.wav')

font = pygame.font.SysFont("Verdana", 60)
image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

ENEMY_SPEED = 10
SCORE = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5
        # or
        # self.rect.midbottom = (WIDTH // 2, HEIGHT)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = ENEMY_SPEED
        # or
        # self.rect.midbottom = (WIDTH // 2, HEIGHT)

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_coin
        self.rect = self.image.get_rect()
        self.speed = 10
        self.weight = random.choice((1, 3, 5, 10))

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def generate_random_weight(self):
        self.weight = random.choice((1, 3, 5, 10))

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()


class Score():
    def __init__(self):
        super().__init__()
        self.score = SCORE
        self.image = None
        self.rect = None
        self.font = pygame.font.SysFont("Verdana", 18)

    def render_score(self):
        self.image = self.font.render(str(self.score), True, "red")
        self.rect = image_game_over.get_rect(topleft=(10, 10))

    def display_score(self):
        if self.image is not None and self.score == SCORE:
            screen.blit(self.image, self.rect)
        else:
            self.score = SCORE
            self.render_score()


score_text = Score()

running = True

# this object allows us to set the FPS
clock = pygame.time.Clock()
FPS = 60

player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)

while running:  # game loop
    for event in pygame.event.get():  # event loop
        if event.type == pygame.QUIT:
            running = False

    player.move()

    screen.blit(image_background, (0, 0))
    score_text.display_score()

    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, coin_sprites):
        SCORE += coin.weight
        coin.generate_random_rect()
        coin.generate_random_weight()
        ENEMY_SPEED = 10 + SCORE // 5

        for entity in enemy_sprites:
            entity.speed = ENEMY_SPEED

    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        running = False
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()

        time.sleep(3)

    pygame.display.flip()  # updates the screen
    clock.tick(FPS)  # sets the FPS

pygame.quit()