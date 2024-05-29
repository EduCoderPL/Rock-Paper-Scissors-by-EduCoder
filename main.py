# Potrzebne importy
import random
import pygame
from pygame.locals import *
from entity import Entity
from constants import *

def writeText(string, coordx, coordy, fontSize):

    font = pygame.font.Font('freesansbold.ttf', fontSize)
    text = font.render(string, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.topleft = (coordx, coordy)
    screen.blit(text, textRect)


PLAYER_ACC = 0.4

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
player = Entity(100, 200, 0)

listOfEntities = []
for i in range(200):
    xRand = random.randint(50, SCREEN_WIDTH - 100)
    yRand = random.randint(50, SCREEN_HEIGHT - 100)
    typeRand = random.randint(0, 2)
    listOfEntities.append(Entity(xRand, yRand, typeRand))

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if keys[K_d]:
        player.xVel += PLAYER_ACC
    if keys[K_a]:
        player.xVel -= PLAYER_ACC
    if keys[K_w]:
        player.yVel -= PLAYER_ACC
    if keys[K_s]:
        player.yVel += PLAYER_ACC

    player.update()

    for entity1 in listOfEntities:
        entity1.update()

        if player.rect.colliderect(entity1.rect):
            entity1.xVel += player.xVel / 2
            entity1.yVel += player.yVel / 2

        entity1.find_closest_entity_to_chase(listOfEntities)

        for entity2 in listOfEntities:
            entity1.check_collision(entity2)

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), Rect(ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT), 3)

    player.draw(screen)

    for entity1 in listOfEntities:
        entity1.draw(screen)

    textWithResults = ""
    for index, value in enumerate(Entity.entityTypeCounter):
        textWithResults = f"{ENTITY_NAMES[index]}: {value}"
        writeText(textWithResults, 10 + 650 * index, 10, 36)

    clock.tick(60)
    pygame.display.flip()


pygame.quit()