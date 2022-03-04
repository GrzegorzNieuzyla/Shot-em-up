from enum import Enum

from .sprite import Sprite
from .timer import Timer


class PickupType(Enum):
    Health = 0
    Speed = 1
    Field = 2
    Score = 3
    RocketAmmo = 4
    PlasmaAmmo = 5



class Pickup(Sprite):
    def __init__(self, x, y, image, ptype, layer=0, pickupSfx=None):
        super(Pickup, self).__init__(image, x, y, layer)
        self.type = ptype
        self.pickupSfx = pickupSfx

    def atPickup(self, player, caller):
        if self.type == PickupType.Health:
            player.hp += 200
        elif self.type == PickupType.Speed:
            if player.effects['speed'] == 0:
                player.speed *= 1.5
                player.maxSpeed *= 1.5
            player.effects['speed'] += 1
            t = Timer(10)
            t.onTimeElapsed.append(lambda: self.__turnSpeedOff(player))
            caller.timers.add(t)
        elif self.type == PickupType.Field:
            player.effects['field'] += 1
            player.field = True
            player.showField = True
            player.damageReduction = 0.8
            t = Timer(10)
            t.onTimeElapsed.append(lambda: self.__blinkField(caller, player))
            caller.timers.add(t)
        elif self.type == PickupType.Score:
            caller.score += 2000
        elif self.type == PickupType.RocketAmmo:
            player.ammo['rocket'] += 20
        elif self.type == PickupType.PlasmaAmmo:
            player.ammo['plasma'] += 20

    def __turnSpeedOff(self, player):
        player.effects['speed'] -= 1
        if player.effects['speed'] == 0:
            player.speed /= 1.5
            player.maxSpeed /= 1.5


    def __blinkField(self, caller, player):
        player.effects['field'] -= 1
        if player.effects['field'] == 0:
            t = Timer(0.3, True)
            t.shouldTimerEnd = lambda: t.count > 8 or player.effects['field'] > 0
            t.onTimeElapsed.append(lambda: self.__toggleField(player))
            t.onEnd.append(lambda: self.__turnFieldOff(player))
            caller.timersQueue.append(t)

    def __turnFieldOff(self, player):
        if player.effects['field'] == 0:
            player.showField = False
            player.field = False
            player.damageReduction = 0

    def __toggleField(self, player):
        player.showField = not player.showField
