from gui import GuiText
from level import Level
from player import Player, Weapon
from events import EventHandler
from bullet import Bullet
import pygame
import math
from random import randint, uniform, random
from ship import Ship
from timer import Timer
from pickup import PickupType, Pickup
from animation import Animation
from misc import getAngle, getDistance
from scene import Scene
from ai import AI
from sprite import Sprite

class Level1(Level):
    def __init__(self, name, display, background):
        super(Level1, self).__init__(name, display, background)
        self.timers = None
        self.players = None
        self.twoPlayers = False
        self.running = False
        self.ships = None
        self.bullets = None
        self.pickups = None
        self.dir = None
        self.hpBar = None
        self.hpBar2 = None
        self.HP = None
        self.timersQueue = None
        self.score = None
        self.scoreText = None
        self.rocketAmmo = None
        self.plasmaAmmo = None
        self.plasmaAmmo2 = None
        self.rocketAmmo2 = None
        self.AI = None




    def load(self):
        self.event = EventHandler()
        self.timers = set()
        self.ships = []
        self.bullets = []
        self.pickups = []
        self.timersQueue = []
        self.score = 0
        self.dir = 1
        self.event.addEventListener(pygame.KEYDOWN,lambda x: self.switchScene('menu') if x.key == pygame.K_ESCAPE else None)
        self.event.addEventListener(pygame.QUIT, lambda x: self.exit())
        self.event.addEventListener(pygame.KEYDOWN, self.checkInput)
        self.background.y = self.display.height - self.background.height
        self.setupPlayer()
        self.AI = AI(self)
        if self.twoPlayers:
            self.hpBar2 = GuiText(self.display.width-150, self.display.height-40, '', fontsize=30, layer=5)
            self.rocketAmmo2 = GuiText(self.display.width-150, self.display.height - 110, '', fontsize=30, layer=5)
            self.plasmaAmmo2 = GuiText(self.display.width-150, self.display.height - 75, '', fontsize=30, layer=5)
            self.addToDrawQueue(self.hpBar2, self.rocketAmmo2, self.plasmaAmmo2)
        self.rocketAmmo = GuiText(20, self.display.height-110, '', fontsize=30, layer=5)
        self.plasmaAmmo = GuiText(20, self.display.height-75, '', fontsize=30, layer=5)
        self.hpBar = GuiText(20, self.display.height-40, '', fontsize=30, layer=5)
        self.addToDrawQueue(self.hpBar, self.plasmaAmmo,self.rocketAmmo)
        #t = Timer(0.5, True)
        #t.onTimeElapsed.append(lambda: self.showFPS())
        #self.timers.add(t)
        self.setupWeapons()
        self.scoreText = GuiText(self.display.width-200, 30,'',fontsize=35,layer=5)
        self.addToDrawQueue(self.scoreText)



    def setupWeapons(self):
        for player in self.players:
            player.weapons['default'] = Weapon(self.resources.getImage('files/bullets/laser.png'),
                                                    30, 1.5, 0.1, 0,self.resources.getSound('files/sound/laser.aiff'),
                                                    self.resources.getSound('files/sound/laserhit.wav'))
            player.weapons['rocket'] = Weapon(self.resources.getImage('files/bullets/missile.png'),
                                                   125, 1, 0.2, 50, self.resources.getSound('files/sound/missile.wav'),
                                                   self.resources.getSound('files/sound/explosion.wav'),
                                                   self.resources.getAnimation('files/animation/explosion'), 0.02)
            player.weapons['plasma'] = Weapon(self.resources.getImage('files/bullets/plasma.png'),
                                              250, 0.5, 0.3, 20, self.resources.getSound('files/sound/plasma.wav'),
                                              self.resources.getSound('files/sound/explosion.wav'),
                                              self.resources.getAnimation('files/animation/plasma'), 0.02)


    def setupPlayer(self):
        self.players = []
        player = Player(self.resources.getImage('files/ships/player.png'),
                             self.display,fieldSprite=self.resources.getImage('files/pickup/field.png'))
        player.x = (self.display.width - player.width)/2
        player.y = self.display.height - player.height
        self.addToDrawQueue(player)
        self.players.append(player)
        if self.twoPlayers:
            player2 = Player(self.resources.getImage('files/ships/player2.png'),
                            self.display, fieldSprite=self.resources.getImage('files/pickup/field.png'))
            player2.x = (self.display.width - player2.width)/3
            player2.y = self.display.height - player2.height
            self.addToDrawQueue(player2)
            self.players.append(player2)

    def shoot(self, player):
        self.updateTimers()
        if not player.shooting and not player.changeWeapon:
            player.shooting = True
            t = Timer(player.weapons[player.currentWeapon].firerate,True)
            t.onTimeElapsed.append(lambda: player.shoot(player.currentWeapon, self))
            t.shouldTimerEnd = lambda: (not self.event.getKeyPressed(int(self.getOptions()['KEY_SHOOT_P1'])) or player.changeWeapon)
            t.onEnd.append(lambda: self.stopShooting(player))
            self.timers.add(t)
            player.shoot(player.currentWeapon, self)

    def stopShooting(self, player):
        player.shooting = False
        player.changeWeapon = False

    def checkInput(self, event=None):
        options = self.getOptions()
        if event:
            if event.key == int(options['KEY_WEAPON1_P1']):
                self.players[0].currentWeapon = 'default'
                if self.players[0].shooting:
                    self.players[0].shooting = False
                    self.players[0].changeWeapon = True
            if event.key == int(options['KEY_WEAPON2_P1']) and self.players[0].ammo['rocket'] > 0:
                self.players[0].currentWeapon = 'rocket'
                if self.players[0].shooting:
                    self.players[0].shooting = False
                    self.players[0].changeWeapon = True
            if event.key == int(options['KEY_WEAPON3_P1'])and self.players[0].ammo['plasma'] > 0:
                self.players[0].currentWeapon = 'plasma'
                if self.players[0].shooting:
                    self.players[0].shooting = False
                    self.players[0].changeWeapon = True
            if len(self.players) > 1:
                if event.key == int(options['KEY_WEAPON1_P2']):
                    self.players[1].currentWeapon = 'default'
                    if self.players[1].shooting:
                        self.players[1].shooting = False
                        self.players[1].changeWeapon = True
                if event.key == int(options['KEY_WEAPON2_P2'])and self.players[1].ammo['rocket'] > 0:
                    self.players[1].currentWeapon = 'rocket'
                    if self.players[1].shooting:
                        self.players[1].shooting = False
                        self.players[1].changeWeapon = True
                if event.key == int(options['KEY_WEAPON3_P2']) and self.players[1].ammo['plasma'] > 0:
                    self.players[1].currentWeapon = 'plasma'
                    if self.players[0].shooting:
                        self.players[0].shooting = False
                        self.players[0].changeWeapon = True
        else:
            if self.event.getKeyPressed(int(options['KEY_SHOOT_P1'])):
                self.shoot(self.players[0])
            if self.event.getKeyPressed(int(options['KEY_M_LEFT_P1'])):
                self.players[0].velocity.x -= self.players[0].speed
            if self.event.getKeyPressed(int(options['KEY_M_RIGHT_P1'])):
                self.players[0].velocity.x += self.players[0].speed
            if self.event.getKeyPressed(int(options['KEY_M_UP_P1'])):
                self.players[0].velocity.y -= self.players[0].speed
            if self.event.getKeyPressed(int(options['KEY_M_DOWN_P1'])):
                self.players[0].velocity.y += self.players[0].speed
            if len(self.players) > 1:
                if self.event.getKeyPressed(int(options['KEY_SHOOT_P2'])):
                    self.shoot(self.players[1])
                if self.event.getKeyPressed(int(options['KEY_M_LEFT_P2'])):
                    self.players[1].velocity.x -= self.players[1].speed
                if self.event.getKeyPressed(int(options['KEY_M_RIGHT_P2'])):
                    self.players[1].velocity.x += self.players[1].speed
                if self.event.getKeyPressed(int(options['KEY_M_UP_P2'])):
                    self.players[1].velocity.y -= self.players[1].speed
                if self.event.getKeyPressed(int(options['KEY_M_DOWN_P2'])):
                    self.players[1].velocity.y += self.players[1].speed
            for player in filter(lambda p: p.enabled, self.players):
                if player.velocity.x > player.maxSpeed:
                    player.velocity.x = player.maxSpeed
                if player.velocity.x < -player.maxSpeed:
                    player.velocity.x = -player.maxSpeed
                if player.velocity.y > player.maxSpeed:
                    player.velocity.y = player.maxSpeed
                if player.velocity.y < -player.maxSpeed:
                    player.velocity.y = -player.maxSpeed

    def processPickups(self):
        toDelete = []
        for pick in self.pickups:
            if pick.y > self.display.height:
                toDelete.append(self.pickups.index(pick))
                self.removeFromDrawQueue(pick)
                continue
            pick.move(*getDistance(0, 0.35 *self.display.getFrameTime()))
            for player in filter(lambda p: p.enabled, self.players):
                if player.checkCollision(pick):
                    pick.atPickup(player, self)
                    toDelete.append(self.pickups.index(pick))
                    self.removeFromDrawQueue(pick)
                    if pick.pickupSfx:
                        pick.pickupSfx.play()
                    break
        for id in sorted(toDelete, reverse=True):
            self.pickups.pop(id)



    def processBullets(self):
        for b in self.bullets:
            b.moveBullet()
        for b in filter(lambda b: b.checkForExit(), self.bullets):
            self.removeFromDrawQueue(b)
            b.toDelete = True

        for i in range(len(self.bullets)-1,-1,-1):
            if self.bullets[i].toDelete:
                self.removeFromDrawQueue(self.bullets[i])
                self.bullets.pop(i)

        for b in self.bullets:
            if b.owner == 1:
                for player in filter(lambda p: p.enabled, self.players):
                    if b.checkCollision(player):
                        if player.field:
                            b.owner = 0
                            b.rotate(180)
                            b.dir = (-b.dir[0], -b.dir[1])
                            continue
                        player.hp -= b.damage * (1 - player.damageReduction)
                        if b.impactSfx:
                            b.impactSfx.play()
                        timer = b.destroy()
                        if timer:
                            self.timers.add(timer)
            else:
                radius = None
                hit = None
                for s in filter(lambda s: s.enabled, self.ships):
                    if b.checkCollision(s):
                        if b.impactSfx:
                            b.impactSfx.play()
                        if b.radius > 0 and not radius:
                            radius = b.addRadius()
                            hit = s
                        s.hp -= b.damage
                        if s.hp <= 0:
                            self.destroyShip(s)
                        b.enabled = False
                        timer = b.destroy()
                        if timer:
                            self.timers.add(timer)
                if radius:
                    for s in self.ships:
                        if s.enabled and radius.checkCollision(s) and hit is not s:
                            s.hp -= radius.damage
                            if s.hp <= 0:
                                self.destroyShip(s)

        for i in range(len(self.bullets)-1,-1,-1):
            if self.bullets[i].toDelete:
                self.removeFromDrawQueue(self.bullets[i])
                self.bullets.pop(i)


    def destroyShip(self, ship):
        if random() < ship.dropchance:
            if random() < 0.7:
                p = Pickup(0,0,self.resources.getImage('files/pickup/rocket.png'), PickupType.RocketAmmo,3, self.resources.getSound('files/sound/ammo.wav'))
            else:
                p = Pickup(0,0,self.resources.getImage('files/pickup/plasma.png'), PickupType.PlasmaAmmo,3, self.resources.getSound('files/sound/ammo.wav'))
            p.x = ship.x + ship.width/2 - p.width/2
            p.y = ship.y + ship.height/2 - p.height/2
            self.addToDrawQueue(p)
            self.pickups.append(p)
        self.score += int(ship.scoreValue)
        ship.enabled = False
        if ship.deathSound:
            ship.deathSound.play()
        timer = ship.playDeathAnimation()
        timer.onEnd.append(lambda: self.removeShip(ship))
        self.timers.add(timer)

    def removeShip(self, ship):
        self.removeFromDrawQueue(ship)
        if ship in self.ships:
            self.ships.remove(ship)

    def process(self):
        self.checkInput()
        for player in filter(lambda p: p.enabled, self.players):
            player.movePlayer(self.display.getFrameTime(), self.display.getFrameTime()/350)
            if player.x < 0:
               player.x = 0
            if player.x > self.display.width - player.width:
                player.x = self.display.width - player.width
            if player.y < 0:
                player.y = 0
            if player.y > self.display.height - player.height:
                player.y = self.display.height - player.height
        self.processBullets()
        self.processPickups()
        for ship in filter(lambda s: s.enabled, self.ships):
            for player in filter(lambda p: p.enabled, self.players):
                if player.checkCollision(ship):
                    if player.field:
                        ship.hp -= self.display.getFrameTime()/5
                        if ship.hp <= 0:
                            self.destroyShip(ship)
                    else:
                        player.hp -= self.display.getFrameTime()/2
                        if not player.alarm:
                            self.resources.getSound('files/sound/alarm.wav').play()
                            player.alarm = True
                            t = Timer(1.5)
                            t.onTimeElapsed.append(lambda: player.setAlarm(False))
                            self.timers.add(t)
        for player in self.players:
            player.hp = max(0, player.hp)
        for player in filter(lambda p: p.enabled, self.players):
            if player.currentWeapon != 'default':
                if player.ammo[player.currentWeapon] <= 0:
                    player.ammo[player.currentWeapon] = 0
                    player.currentWeapon = 'default'
                    if player.shooting:
                        player.shooting = False
                        player.changeWeapon = True
            if player.hp <= 0:
                self.death(player)





    def run(self):
        self.display.FPS = 200
        Scene.getScene('menu').levelInProgress = True
        self.event.recheck()
        self.running = True
        self.active = True
        while self.active and not self.exiting:
            self.event.handle()
            self.updateTimers()
            self.AI.handle(self.ships, self.drawable)
            self.process()
            self.render()
            self.display.display(self.drawable)


    def render(self):
        self.moveBackground(self.display.getFrameTime() * 0.2)
        if self.twoPlayers:
            self.hpBar2.changeText('{:4} HP'.format(str(int(self.players[1].hp))))
            self.plasmaAmmo2.changeText('Plasma: ' + str(self.players[1].ammo['plasma']))
            self.rocketAmmo2.changeText('Rockets: ' + str(self.players[1].ammo['rocket']))
        self.hpBar.changeText('{:4} HP'.format(str(int(self.players[0].hp))))
        self.plasmaAmmo.changeText('Plasma: ' + str(self.players[0].ammo['plasma']))
        self.rocketAmmo.changeText('Rockets: ' + str(self.players[0].ammo['rocket']))
        self.scoreText.changeText("Score: " + str(self.score))

    def updateTimers(self):
        toDel = []
        for timer in self.timers:
            timer.update()
            if timer.toDelete:
                toDel.append(timer)
        for t in toDel:
            self.timers.remove(t)
        for tim in self.timersQueue:
            self.timers.add(tim)
        self.timersQueue = []

    def death(self, player):
        player.enabled = False
        an = Animation(self.resources.getAnimation('files/animation/destruction'))
        self.resources.getSound('files/sound/destruction.wav').play()
        timer = player.playAnimation(an, 0.01)
        timer.onEnd.append(lambda p=player: p.setVisible(False))
        timer.onEnd.append(self.gameOver)
        self.timers.add(timer)

    def gameOver(self):
        if all(not p.enabled for p in self.players):
            self.suspend()
            self.reset()
            self.switchScene('gameover')
            Scene.getScene('gameover').score = self.score
            Scene.getScene('menu').levelInProgress = False
