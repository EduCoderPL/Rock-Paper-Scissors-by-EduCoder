import math
import random

import pygame
from pygame import Rect

from constants import *

WIDTH = 20
HEIGHT = 20
IMG_WIDTH = 64
IMG_HEIGHT = 64

DRAG_COEFFICIENT = 0.9

imgs = {0: "imgs/Scissors.png",
        1: "imgs/Rock.png",
        2: "imgs/Paper.png",
        }

class Entity:

    differentTypeCount = 3

    def __init__(self, x, y, entityType):

        self.x = x
        self.y = y

        self.width = WIDTH
        self.height = HEIGHT

        self.xVel = 0
        self.yVel = 0

        self.rect = Rect(self.x, self.y, self.width, self.height)

        self.type = entityType
        self.color = TYPE_TO_COLOR[entityType]

        self.img = pygame.transform.scale(pygame.image.load(imgs[entityType]), (IMG_WIDTH, IMG_HEIGHT)).convert_alpha()

        self.entityToChase = None
        self.entityToEscape = None

    def update(self):

        self.add_drag()
        self.generate_vector_to_chase_and_escape()
        self.add_random_acceleration()
        self.calculate_position()
        self.check_borders()
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def add_drag(self):
        self.xVel *= DRAG_COEFFICIENT
        self.yVel *= DRAG_COEFFICIENT

    def generate_vector_to_chase_and_escape(self):
        if self.entityToChase:
            vectorToChase = self.get_normalized_vector(self.entityToChase)
            self.xVel += vectorToChase[0] * 0.4
            self.yVel += vectorToChase[1] * 0.4
        if self.entityToEscape:
            vectorToChase = self.get_normalized_vector(self.entityToEscape)
            self.xVel -= vectorToChase[0] * 0.4
            self.yVel -= vectorToChase[1] * 0.4

    def get_normalized_vector(self, target):

        baseVector = (target.x - self.x, target.y - self.y)
        vectorLength = ((baseVector[0] ** 2) + (baseVector[1] ** 2)) ** 0.5
        vectorNormalized = baseVector[0] / vectorLength, baseVector[1] / vectorLength

        return vectorNormalized

    def add_random_acceleration(self):
        self.xVel += random.uniform(-0.5, 0.5)
        self.yVel += random.uniform(-0.5, 0.5)

    def calculate_position(self):
        self.x += self.xVel
        self.y += self.yVel

    def check_borders(self):
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


    def check_collision(self, otherEntity):

        if self.rect.colliderect(otherEntity):

            if self.check_target_to_chase(otherEntity):
                otherEntity.type = self.type

                otherEntity.color = TYPE_TO_COLOR[otherEntity.type]
                otherEntity.img = pygame.transform.scale(pygame.image.load(imgs[otherEntity.type]), (IMG_WIDTH, IMG_HEIGHT)).convert_alpha()
    def find_closest_entity_to_chase(self, entityList):

        self.entityToChase = None
        self.entityToEscape = None

        minDistanceChase = 10000000
        minDistanceEscape = 10000000

        for entity in entityList:

            if self.type == entity.type:
                continue

            dist = math.dist((self.x, self.y), (entity.x, entity.y))

            if self.check_target_to_chase(entity):

                if dist < minDistanceChase or self.entityToChase is None:
                    minDistanceChase = dist
                    self.entityToChase = entity

            if self.check_target_to_escape(entity):

                if dist < minDistanceEscape or self.entityToEscape is None:
                    minDistanceEscape = dist
                    self.entityToEscape = entity

    def check_target_to_chase(self, target):
        return (self.type - 1) % Entity.differentTypeCount == target.type

    def check_target_to_escape(self, target):
        return (self.type + 1) % Entity.differentTypeCount == target.type

    def draw(self, screen):
        # pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.img, (self.x - (IMG_WIDTH - WIDTH) // 2, self.y - (IMG_HEIGHT - HEIGHT) // 2))
