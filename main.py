# Potrzebne importy
import random

import pygame
from pygame.locals import *

class Entity:

    def __init__(self, x, y, color):

        self.x = x
        self.y = y

        self.width = 50
        self.height = 50

        self.xVel = 0
        self.yVel = 0

        self.acc = 0.4

        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.color = color

    def update(self):
        self.yVel += 0.1

        self.xVel *= 0.98
        self.yVel *= 0.98

        self.x += self.xVel
        self.y += self.yVel

        if self.x < 0:
            self.x = 0
            self.xVel *= -1

        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.xVel *= -1

        if self.y < 0:
            self.y = 0
            self.yVel = 0

        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.yVel *= -2

        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900


# Inicjalizacja wszystkich mechanizmów pythona (po prostu to jest ważne);
pygame.init()

# Parametry Screena
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Zegar kontrolujący FPS-y
clock = pygame.time.Clock()

player = Entity(100, 200, (255, 0, 0))

listOfEntities = []
for i in range(200):
    xRand = random.randint(50, SCREEN_WIDTH - 100)
    yRand = random.randint(50, SCREEN_HEIGHT - 100)

    randomR = random.randint(0, 150)
    randomG = random.randint(0, 150)
    randomB = random.randint(0, 150)

    listOfEntities.append(Entity(xRand, yRand, (randomR, randomG, randomB)))

# Pętla gry
running = True
while running:

    # Te cztery linijki pozwalają nam normalnie zamknąć program.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if keys[K_d]:
        player.xVel += player.acc
    if keys[K_a]:
        player.xVel -= player.acc
    if keys[K_w]:
        player.yVel -= player.acc
    if keys[K_s]:
        player.yVel += player.acc

    player.update()

    for entity in listOfEntities:
        entity.update()

        if player.rect.colliderect(entity.rect):
            entity.xVel += player.xVel / 2
            entity.yVel += player.yVel / 2


    # Rysowanie grafiki:
    screen.fill((0, 0, 0))
    player.draw()
    for entity in listOfEntities:
        entity.draw()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()