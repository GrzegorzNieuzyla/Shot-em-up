import math
from random import choice, randint, uniform

from .animation import Animation
from .pickup import Pickup, PickupType
from .ship import Ship, Barrel
from .timer import Timer


class WaveData:
    @staticmethod
    def readFile(path):
        result = []
        with open(path, 'r') as f:
            wave = []
            for line in filter(lambda st: not st.startswith('#') and st.strip() != '', f.read().splitlines()):
                if line.startswith('---'):
                    if len(wave) > 0:
                        result.append(WaveData(' '.join(wave)))
                        wave.clear()
                else:
                    wave.append(line)
        return result

    def __init__(self, data):
        self.ships = []
        for line in data.split(' '):
            ldata = line.split(':')
            name = ldata[0]
            x = float(ldata[1])
            offset = float(ldata[2])
            speed = float(ldata[3])
            vectors = [self.readBehaviour(x) for x in ldata[4:]]
            self.ships.append((name, x, offset, speed, vectors))

    def readBehaviour(self, string):
        string = string.strip()
        if string[0] != '(' or string[-1] != ')':
            raise ValueError
        values = string[1:-1].split(',')
        return float(values[0]), float(values[1]), float(values[2]), float(values[3])


class AI:
    def __init__(self, level):
        self.display = level.display
        self.players = level.players
        self.resources = level.resources
        self.level = level
        self.mult = 1
        self.count = 0
        self.shipTypes = {}
        self.setupTypes('files/script/shiptypes')
        self.waveInfo = WaveData.readFile('files/script/wavedata')
        self.currentWave = -1
        self.timers = []
        t = Timer(1, True)
        t.onTimeElapsed.append(self.pickups)
        self.timers.append(t)


    def pickups(self):
        if randint(1, 100) < 15:
            field_ch = 30
            health_ch = field_ch + (40 if any(p.hp <= 800 for p in self.players) else 0)
            score_ch = health_ch + 50
            speed_ch = score_ch + 35
            rand = randint(0, speed_ch)
            if rand <= field_ch:
                p = Pickup(0, 0, self.resources.getImage('files/pickup/field_pickup.png'), PickupType.Field, 3, self.resources.getSound('files/sound/pickup.wav'))
            elif rand <= health_ch:
                p = Pickup(0, 0, self.resources.getImage('files/pickup/health.png'), PickupType.Health, 3, self.resources.getSound('files/sound/ammo.wav'))
            elif rand <= score_ch:
                p = Pickup(0, 0, self.resources.getImage('files/pickup/coin.png'), PickupType.Score, 3, self.resources.getSound('files/sound/coin.wav'))
            else:
                p = Pickup(0, 0, self.resources.getImage('files/pickup/speed.png'), PickupType.Speed, 3, self.resources.getSound('files/sound/pickup.wav'))
            p.x = randint(0, self.display.width - p.width)
            self.level.pickups.append(p)
            self.level.addToDrawQueue(p)



    def getBarrel(self, line):
        line = line.strip()
        if line[0] != '(' or line[-1] != ')':
            raise ValueError
        val = line[1:-1].split(',')
        return (self.resources.getImage(val[0]), float(val[1]), float(val[2]), float(val[3]),
                float(val[4]), self.resources.getSound(val[5]), None if val[6] == 'a' else float(val[6]),
                None if val[7] == '-' else self.resources.getAnimation(val[7]), float(val[8]), float(val[9]),
                None if val[10] == '-' else self.resources.getSound(val[10]))

    def setupTypes(self, path):
        with open(path) as f:
            for data in filter(lambda l: not l.startswith('#') and l.strip() != '', f.read().splitlines()):
                spl = data.split(':')
                name = spl[0]
                self.shipTypes[name] = {'sprite': self.resources.getImage(spl[1]), 'value': int(spl[2]),
                                        'hp': int(spl[3]), 'animation': self.resources.getAnimation(spl[4]),
                                        'delay': float(spl[5]), 'sound': self.resources.getSound(spl[6]),
                                        'drop': float(spl[7])}
                self.shipTypes[name]['barrels'] = []
                for barrel in spl[8:]:
                    self.shipTypes[name]['barrels'].append(self.getBarrel(barrel))

    def getOffset(self, ship, target):
        trg = (target[0] * self.display.width - ship.x, target[1] * self.display.height - ship.y)
        if trg[1] == 0:
            trg = (trg[0], 0.1)
        ratio = trg[0] / trg[1]
        signy = 1 if trg[1] >= 0 else -1
        y = signy * target[2] / math.sqrt(1 + ratio ** 2)
        x = y * ratio
        return x, y

    def handleTimers(self):
        toDel = []
        for timer in self.timers:
            timer.update()
            if timer.toDelete:
                toDel.append(timer)
        self.timers = [timer for timer in self.timers if timer not in toDel]

    def moveShip(self, ship):
        if ship.standStill:
            return
        if len(ship.behaviour) == 0:
            ship.move(0, (self.display.getFrameTime() / 100) * ship.speed)
        else:
            offset = self.getOffset(ship, ship.behaviour[0])
            x = offset[0] * self.display.getFrameTime() / 100
            y = offset[1] * self.display.getFrameTime() / 100
            ship.move(x, y)
            pos = (ship.behaviour[0][0] * self.display.width, ship.behaviour[0][1] * self.display.height)
            if ship.x <= pos[0] <= ship.x + ship.width:
                if ship.y * 0.98 <= pos[1] <= (ship.y + ship.height) * 1.02 or ship.y <= pos[1] <= ship.y + ship.height:
                    if ship.behaviour[0][3] > 0:
                        ship.stand(True)
                        t = Timer(ship.behaviour[0][3])
                        t.onTimeElapsed.append(lambda: ship.stand(False))
                        self.timers.append(t)
                    ship.behaviour.pop(0)

    def shoot(self, barrel):
        player = choice(self.players)
        if barrel.direction is not None:
            barrel.shoot(barrel.direction,self.level)
        else:
            barrel.shootAt(player, self.level)

    def handle(self, ships, drawable):
        self.handleTimers()
        if len(ships) <= 0:
            self.initWave(ships, drawable)
        else:
            toDelete = []
            for ship in filter(lambda s: s.hp > 0, ships):
                if ship.y + ship.height < 0:
                    ship.move(0, ship.speed * self.display.getFrameTime() / 100)
                else:
                    self.moveShip(ship)
                if ship.y > self.display.height and len(ship.behaviour) == 0:
                    ship.enabled = False
                    toDelete.append(ship)
            for ship in toDelete:
                ships.remove(ship)
                drawable.remove(ship)

    def initWave(self, ships, drawable):
        self.currentWave += 1
        if self.currentWave >= len(self.waveInfo):
            self.waveInfo = WaveData.readFile('../files/script/wavedata')
            self.currentWave = 0
            self.mult += 0.75
        wave = self.waveInfo[self.currentWave]
        for s in wave.ships:
            t = self.shipTypes[s[0]]
            ship = Ship(t['sprite'], s[1] * self.display.width, 0, t['value'] * self.mult, 2, s[3], s[0], Animation(t['animation']), t['delay'])
            ship.hp = t['hp']
            ship.behaviour = s[4]
            ship.deathSound = t['sound']
            ship.dropchance = t['drop']
            ship.y = -s[2] * ship.height
            for b in t['barrels']:
                ship.barrels.append(Barrel(ship, ship.width * b[1], ship.height * b[2], b[0], b[3]*self.mult, b[4], b[5], b[6], b[7], b[8], b[9], b[10]))
            ships.append(ship)
            drawable.add(ship)
            delta = uniform(0.9, 1.1)
            for barrel in ship.barrels:
                timer = Timer(barrel.firerate * delta, True)
                timer.onTimeElapsed.append(lambda b=barrel: self.shoot(b))
                timer.shouldTimerEnd = lambda sh=ship: sh.hp <= 0 or not sh.enabled
                self.timers.append(timer)
