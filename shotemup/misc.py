import math

import pygame


def getAngle(x1, y1, x2, y2):
    x = x1 - x2
    y = y1 - y2
    if x == 0 or y == 0:
        return tuple((x, y))
    angle = math.atan(y / x)
    sx = 1 if x > 0 else -1
    return tuple((sx * math.cos(angle), sx * math.sin(angle)))


def getVectorFromAngle(angle):
    return math.cos(math.radians(angle)), math.sin(math.radians(angle))


def getAngleValue(x1, y1, x2, y2):
    x = x1 - x2
    y = y1 - y2
    if x == 0 or y == 0:
        return 0
    return math.degrees(math.atan(y / x))



def getDistance(x, y):
    width, height = pygame.display.get_surface().get_size()
    if width != 1920:
        ratio = width / 1920
        x *= ratio
    if height != 1080:
        ratio = height / 1080
        y *= ratio
    return x, y