# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
SPEED = 2
SCORE = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render('Game Over', True, BLACK)

background = pygame.image.load("Background.png")

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((360, 640))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Flappy Bird")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        x = random.randint(-30, 200)
        y = random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT + 30)
        a = random.choice([x, y])
        self.rect.center = (SCREEN_WIDTH, a)

    def move(self):
        global SCORE
        self.rect.move_ip(-SPEED, 0)
        if (self.rect.right < 0):
            SCORE += 1
            self.rect.top = 0
            x = random.randint(-30, 200)
            y = random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT + 30)
            a = random.choice([x, y])
            self.rect.center = (SCREEN_WIDTH, a)
            self.move()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (100, 300)
        self.fall()

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -15)
        self.fall()

    def fall(self):
        #while True and self.rect.bottom < SCREEN_HEIGHT:
        for i in range(4):
            if self.rect.bottom < SCREEN_HEIGHT:
                self.rect.move_ip(0, 1)


# Setting up Sprites
P1 = Player()
E1 = Enemy()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:

    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies) or P1.rect.top < 0 or P1.rect.bottom > SCREEN_HEIGHT-1:
        pygame.display.update()
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        score = font_small.render("Score: " + str(SCORE), True, BLACK)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (10, 250))
        DISPLAYSURF.blit(score, (130, 350))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)