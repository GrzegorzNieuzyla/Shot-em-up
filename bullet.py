from animation import Animation
from misc import getDistance
from sprite import Sprite
from events import EventHandler


class Bullet(Sprite):
    def __init__(self, x, y, image, damage, direction, speed, display, owner=0,
                 layer=0, radius=0, shootSfx=None, impactSfx=None, animation=None, animDelay=0):
        super(Bullet, self).__init__(image, x, y, layer)
        self.speed = speed
        self.shootSfx = shootSfx
        self.impactSfx = impactSfx
        self.dir = direction
        self.display = display
        self.damage = damage
        self.animation = animation
        self.toDelete = False
        self.animDelay = animDelay
        self.owner = owner
        self.radius = radius

    def moveBullet(self):
        x, y = getDistance(self.dir[0] * self.display.getFrameTime() * self.speed, self.dir[1] * self.display.getFrameTime() * self.speed)
        self.x -= x
        self.y -= y

    def destroy(self):
        if self.animation:
            self.fitToAnimation(self.animation.width, self.animation.height)
            self.speed = 0
            self.enabled = False
            timer = self.playAnimation(self.animation, self.animDelay)
            timer.onEnd.append(self.setToDelete)
            return timer
        self.toDelete = True
        return None

    def fitToAnimation(self, width, height):
        self.x -= (width - self.width)/2
        self.y -= (height - self.height)/2
        self.y -= self.dir[1] * self.height/2
        self.x -= self.dir[0] * self.width/2

    def setToDelete(self):
        self.toDelete = True


    def addRadius(self):
        res = Bullet(self.x, self.y, self.image, self.speed, self.dir, self.display, self.owner, self.owner)
        res.damage = self.damage
        res.resize(res.width + 2 * self.radius, res.height + 2 * self.radius)
        res.x -= self.radius
        res.y -= self.radius
        return res

    def checkForExit(self):
        if self.x + self.width < 0 or self.x > self.display.width:
            return True
        elif self.y + self.height < 0 or self.y > self.display.height:
            return True
        return False
