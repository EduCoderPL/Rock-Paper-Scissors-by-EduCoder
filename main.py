# Potrzebne importy
import math
import random

import pygame
from pygame.locals import *

class Entity:

    differentTypeCount = 3

    def __init__(self, x, y, entityType):

        self.x = x
        self.y = y

        self.width = 20
        self.height = 20

        self.xVel = 0
        self.yVel = 0

        self.acc = 0.4

        self.rect = Rect(self.x, self.y, self.width, self.height)

        self.type = entityType
        self.color = TYPE_TO_COLOR[entityType]

        self.entityToChase = None
        self.entityToEscape = None

    def update(self):

        self.xVel *= 0.9
        self.yVel *= 0.9

        if self.entityToChase:
            vectorToChase = self.getVectorToTarget(self.entityToChase)
            self.xVel += vectorToChase[0] * 0.4
            self.yVel += vectorToChase[1] * 0.4

        if self.entityToEscape:
            vectorToChase = self.getVectorToTarget(self.entityToEscape)
            self.xVel -= vectorToChase[0] * 0.4
            self.yVel -= vectorToChase[1] * 0.4

        self.xVel += random.uniform(-0.5, 0.5)
        self.yVel += random.uniform(-0.5, 0.5)

        self.x += self.xVel
        self.y += self.yVel

        if self.x < 0:
            self.x = 0
            self.xVel *= -1.4

        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.xVel *= -1.4

        if self.y < 0:
            self.y = 0
            self.yVel *= -1.4

        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.yVel *= -1.4

        self.rect = Rect(self.x, self.y, self.width, self.height)


    def getVectorToTarget(self, target):

        vectorToTargetToChase = (target.x - self.x, target.y - self.y)
        vectorLength = ((vectorToTargetToChase[0] ** 2) + (vectorToTargetToChase[1] ** 2)) ** 0.5

        vectorNormalized = vectorToTargetToChase[0] / vectorLength, vectorToTargetToChase[1] / vectorLength

        vectorWithVelocity = vectorNormalized[0], vectorNormalized[1]

        return vectorWithVelocity

    def checkCollision(self, otherEntity):

        if self.rect.colliderect(otherEntity):

            if (self.type - 1) % Entity.differentTypeCount == otherEntity.type:
                otherEntity.type = self.type

                otherEntity.color = TYPE_TO_COLOR[otherEntity.type]

    def checkClosestEntityToChase(self, entityList):

        self.entityToChase = None
        self.entityToEscape = None

        minDistanceChase = 10000000
        minDistanceEscape = 10000000

        for entity in entityList:

            if self.type == entity.type:
                continue

            dist = math.dist((self.x, self.y), (entity.x, entity.y))
            if (self.type - 1) % Entity.differentTypeCount == entity.type:

                if dist < minDistanceChase or self.entityToChase is None:
                    minDistanceChase = dist
                    self.entityToChase = entity

            if (self.type + 1) % Entity.differentTypeCount == entity.type:

                if dist < minDistanceEscape or self.entityToEscape is None:
                    minDistanceEscape = dist
                    self.entityToEscape = entity


    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

TYPE_TO_COLOR = {
    0: (200, 0, 0),
    1: (0, 200, 0),
    2: (0, 0, 200),
}

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900


# Inicjalizacja wszystkich mechanizmów pythona (po prostu to jest ważne);
pygame.init()

# Parametry Screena
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Zegar kontrolujący FPS-y
clock = pygame.time.Clock()

player = Entity(100, 200, 0)

listOfEntities = []
for i in range(300):
    xRand = random.randint(50, SCREEN_WIDTH - 100)
    yRand = random.randint(50, SCREEN_HEIGHT - 100)

    typeRand = random.randint(0, 2)

    listOfEntities.append(Entity(xRand, yRand, typeRand))

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

    for entity1 in listOfEntities:
        entity1.update()

        if player.rect.colliderect(entity1.rect):
            entity1.xVel += player.xVel / 2
            entity1.yVel += player.yVel / 2

        entity1.checkClosestEntityToChase(listOfEntities)

        for entity2 in listOfEntities:
            entity1.checkCollision(entity2)



    # Rysowanie grafiki:
    screen.fill((0, 0, 0))
    player.draw()
    for entity1 in listOfEntities:
        entity1.draw()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()