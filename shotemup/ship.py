from .animation import Animation
from .bullet import Bullet
from .misc import getAngle, getAngleValue, getVectorFromAngle
from .sprite import Sprite


class Barrel:
    def __init__(self, ship, posX, posY, bulletSprite, damage, speed, sound=None, direction=None, animation=None,
                 animDelay=0, firerate=0.5, shootSound=None):
        self.posX = posX
        self.posY = posY
        self.ship = ship
        self.direction = direction
        self.bulletSprite = bulletSprite
        self.shootSound = shootSound
        self.animDelay = animDelay
        self.animation = animation
        self.firerate = firerate
        self.sound = sound
        self.damage = damage
        self.speed = speed



    def shoot(self, direction, caller):
        while direction > 180:
            direction -= 360
        while direction < -180:
            direction += 360
        srcX = self.ship.x + self.posX
        srcY = self.ship.y + self.posY
        bullet = Bullet(0, 0, self.bulletSprite, self.damage, 0, self.speed, caller.display, 1, 2,
                        impactSfx=self.sound, animation=Animation(self.animation) if self.animation else None, animDelay=self.animDelay)
        bullet.rotate(-direction+90)
        dirx, diry = getVectorFromAngle(direction)
        if 180 >= direction > 90:
            srcY -= bullet.image.get_size()[1]
        if 0 >= direction > -90:
            srcX -= bullet.image.get_size()[0]
        if 90 >= direction > 0:
            srcX -= bullet.image.get_size()[0]
            srcY -= bullet.image.get_size()[1]

        bullet.x = srcX
        bullet.y = srcY
        bullet.dir = (dirx, diry)
        caller.addToDrawQueue(bullet)
        caller.bullets.append(bullet)
        if self.shootSound:
            self.shootSound.play()


    def shootAt(self, target, caller):
        destx, desty = target.getCenter()
        destx += self.bulletSprite.get_size()[0] / 2
        desty += self.bulletSprite.get_size()[1] / 2
        srcX = self.ship.x + self.posX
        srcY = self.ship.y + self.posY
        bullet = Bullet(0, 0, self.bulletSprite, self.damage, 0, self.speed, caller.display, 1, 2,
                        impactSfx=self.sound, animation=Animation(self.animation) if self.animation else None, animDelay=self.animDelay)
        angle = -getAngleValue(srcX, srcY, destx, desty) - 90
        if target.x >= srcX and target.y <= srcY:
            srcY -= bullet.image.get_size()[1]
        if target.x <= srcX and target.y > srcY:
            srcX -= bullet.image.get_size()[0]
            angle -= 180
        if target.x <= srcX and target.y <= srcY:
            srcX -= bullet.image.get_size()[0]
            srcY -= bullet.image.get_size()[1]
            angle -= 180

        bullet.rotate(angle)
        bullet.x = srcX
        bullet.y = srcY
        dirx, diry = getAngle(srcX, srcY, destx, desty)
        bullet.dir = (dirx, diry)
        caller.addToDrawQueue(bullet)
        caller.bullets.append(bullet)
        if self.shootSound:
            self.shootSound.play()



class Ship(Sprite):
    def __init__(self, image, x, y, scoreValue=10, layer=0, speed=0, shipType='regular', animation=None, animationSpeed=None):
        super(Ship, self).__init__(image, x, y, layer)
        self.hp = 1
        self.animation = animation
        self.animationSpeed = animationSpeed
        self.barrels = []
        self.shipType = shipType
        self.speed = speed
        self.dropchance = 0
        self.damage = 10
        self.deathSound = None
        self.scoreValue = scoreValue
        self.behaviour = []
        self.standStill = False

    def draw(self, screen):
        super(Ship, self).draw(screen)


    def playDeathAnimation(self):
        self.x -= (self.animation.width - self.width)/2
        self.y -= (self.animation.height - self.height)/2
        return self.playAnimation(self.animation, self.animationSpeed)

    def stand(self, stand):
        self.standStill = stand
