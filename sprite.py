import pygame

from misc import getDistance
from timer import Timer


class Sprite:
    def __init__(self, image, x=0, y=0, layer=0):
        self.image = image
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.x = x
        self.y = y
        self.animation = None
        self.enabled = True
        self.visible = True
        self.layer = layer

    def move(self, x, y):
        x, y = getDistance(x, y)
        self.x += x
        self.y += y




    def setVisible(self, v):
        self.visible = v

    def getCenter(self):
        return self.x + self.width/2, self.y + self.height/2

    def playAnimation(self, animation,  delay) -> Timer:
        self.animation = animation
        self.image = self.animation.nextFrame()
        timer = Timer(delay, True)
        timer.onTimeElapsed.append(lambda: self.setImage(self.animation.nextFrame()))
        timer.shouldTimerEnd = lambda: self.animation.hasEnded()
        return timer

    def setImage(self, img):
        self.image = img

    def resize(self, width, height):
        self.image = pygame.transform.scale(self.image, (int(width), int(height)))
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]

    def draw(self, screen):
        screen.blit(self.image, pygame.Rect(self.x, self.y, self.width, self.height))

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]

    def addRadius(self, radius):
        res = Sprite(self.image, self.x, self.y)
        res.resize(res.width + 2 * radius, res.height + 2 * radius)
        res.x -= radius
        res.y -= radius
        return res

    def crop(self, x, y, width, height):
        img = Sprite(self.image, layer=self.layer)
        img.image = pygame.Surface((width, height))
        img.image.blit(self.image, (0, 0), (x, y, width, height))
        img.width = img.image.get_size()[0]
        img.height = img.image.get_size()[1]
        return img

    def checkCollision(self, sprite) -> bool:
        r1 = pygame.Rect(self.x, self.y, self.image.get_rect().width, self.image.get_rect().height)
        r2 = pygame.Rect(sprite.x, sprite.y, sprite.image.get_rect().width, sprite.image.get_rect().height)
        return r1.colliderect(r2) and self.enabled
