import pygame

from .animation import Animation
from .bullet import Bullet
from .misc import getDistance
from .sprite import Sprite
from .vector import Vector2d


class Weapon:
    def __init__(self, bulletSprite, damage, speed, firerate, radius=0,
                 shootSfx=None, impactSfx=None, animation=None, animDelay=0, offset_cf=1, origin=None):
        self.bulletSprite = bulletSprite
        self.shootSfx = shootSfx
        self.impactSfx = impactSfx
        self.radius = radius
        self.offset_cf = offset_cf
        self.speed = speed
        self.firerate = firerate
        self.animation = animation
        self.animDelay = animDelay
        self.origin = origin
        self.damage = damage



class Player(Sprite):
    def __init__(self, image, display, layer=0, fieldSprite=None):
        super(Player, self).__init__(image, layer=layer)
        self.hp = 1000
        self.field = False
        self.weapons = {}
        self.damageReduction = 0
        self.ammo = {'rocket': 10, 'plasma': 5}
        self.maxSpeed = 0.5
        self.effects = {'field': 0, 'speed': 0}
        self.speed = 0.25
        self.velocity = Vector2d(0, 0)
        self.display = display
        self.changeWeapon = False
        self.currentWeapon = 'default'
        self.shooting = False
        self.fieldSprite = fieldSprite
        self.alarm = False
        self.showField = False

    def setAlarm(self, alarm):
        self.alarm = alarm


    def shoot(self, weapontype, caller):
        if self.enabled:
            weapon = self.weapons[weapontype]
            if weapon.origin:
                srcx = self.x + weapon.origin[0]
                srcy = self.y + weapon.origin[1]
            else:
                srcx, srcy = self.getCenter()

                srcx -= weapon.bulletSprite.get_size()[0] / 2
                srcy -= weapon.bulletSprite.get_size()[1] / 2
            srcy -= weapon.bulletSprite.get_size()[1]
            offset = self.velocity.x * 0.5 * weapon.offset_cf
            bullet = Bullet(srcx, srcy, weapon.bulletSprite, weapon.damage, (-offset, 1), weapon.speed,
                            caller.display, 0, 2, weapon.radius,
                            weapon.shootSfx, weapon.impactSfx, None, weapon.animDelay)
            if weapon.animation:
                bullet.animation = Animation(weapon.animation)
            if bullet.shootSfx:
                bullet.shootSfx.play()
            caller.addToDrawQueue(bullet)
            caller.bullets.append(bullet)
            if self.currentWeapon != 'default':
                self.ammo[self.currentWeapon] -= 1

    def draw(self, screen):
        if self.fieldSprite and self.showField:
            w, h = self.fieldSprite.get_size()
            screen.blit(self.fieldSprite, pygame.Rect(
                self.x - (w-self.width)/2, self.y - (h-self.height)/2, self.width, self.height))
        super(Player, self).draw(screen)

    def movePlayer(self, frametime, diminish=0):
        if self.enabled:
            x, y = getDistance(self.velocity.x * frametime, self.velocity.y * frametime)
            self.x += x
            self.y += y
            xsign = 1 if self.velocity.x > 0 else -1
            ysign = 1 if self.velocity.y > 0 else -1
            self.velocity.x -= diminish * xsign
            self.velocity.y -= diminish * ysign
            if xsign * self.velocity.x < 0:
                self.velocity.x = 0
            if ysign * self.velocity.y < 0:
                self.velocity.y = 0
