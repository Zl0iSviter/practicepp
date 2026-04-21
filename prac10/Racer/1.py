import pygame
import sys
from pygame.locals import *
import random , time

pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()

SCORE = 0
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over" , True, BLACK)


background = pygame.image.load("AnimatedStreet.png")

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5


DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill((255,255,255))

pygame.display.set_caption("Brbrmashinki")

class coin(pygame.sprite.Sprite):
    RADIUS = 20
    OUTLINE = (230, 230, 0)
    def __init__(self):
        super().__init__()

        # 1. Создаем поверхность
        side = self.RADIUS * 2
        self.image = pygame.Surface((side, side), pygame.SRCALPHA)  # SRCALPHA для прозрачности

        # 2. Рисуем монету на её собственной поверхности
        pygame.draw.circle(self.image, self.OUTLINE, (self.RADIUS, self.RADIUS), self.RADIUS)
        pygame.draw.circle(self.image, YELLOW, (self.RADIUS, self.RADIUS), self.RADIUS - 2)

        # 3. Создаем rect для позиционирования
        x = random.randint(40, 360)
        y = 540
        self.rect = self.image.get_rect(center=(x, y))
    def move(self):
        pass
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0)

      def move(self):
        self.rect.move_ip(0,SPEED )
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

      def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

P1 = Player()
E1 = Enemy()


enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
def create_coin():
    new_coin = coin()
    coins.add(new_coin)
    all_sprites.add(new_coin)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

COIN_SPAWN = pygame.USEREVENT + 2
pygame.time.set_timer(COIN_SPAWN, random.randint(1000, 5000))


while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == COIN_SPAWN:
            pygame.time.set_timer(COIN_SPAWN, random.randint(1000, 5000))
            for entity in coins:
                entity.kill()
            create_coin()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (370, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    if pygame.sprite.spritecollideany(P1,enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        DISPLAYSURF.blit(font.render("Score:"+ str(SCORE) , True, BLACK), (30 , 300))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(4)
        pygame.quit()
        sys.exit()

    if pygame.sprite.spritecollideany(P1, coins):
        pygame.mixer.Sound('coin.mp3').play()
        for entity in coins:
            entity.kill()
        SCORE += 1
    pygame.display.update()
    FramePerSec.tick(FPS)