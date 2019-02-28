import pygame

from button import Button
from events import EventHandler
from gui import GuiText
from scene import Scene
from sprite import Sprite


class Control:
    def __init__(self, posX, posY, key, text, image, sound, caller):
        self.posX = posX
        self.posY = posY
        self.key = key
        self.text = text
        self.image = image
        self.sound = sound
        self.caller = caller
        self.await_ = False
        self.button = Button(self.caller.display.width/10 + posX * self.caller.display.width/3,
                             self.caller.display.height/10 + posY * self.caller.display.height/10,
                             self.caller.display.width/5, self.caller.display.height/12, self.text + ': ' + self.getKeyName(caller.getOptions()[self.key]),
                             sound=self.sound)
        self.button.setImage(self.image, True)
        self.caller.drawable.add(self.button)
        self.button.addEventListener(self.onClick)
        self.caller.events.addEventListener(pygame.MOUSEBUTTONDOWN, self.button.feedMouseEvent)

    def getKeyName(self, key):
        name = pygame.key.name(int(key))
        if name.startswith('['):
            name = name.replace('[', 'Numpad ')
            name = name.replace(']', '')
        return name.title()

    def feedKey(self, key):
        if self.await__:
            self.await_ = False
            opt = self.caller.getOptions()
            opt[self.key] = str(key)
            Scene.saveOptions(opt)
            self.button.changeText(self.text + ': ' + self.getKeyName(self.caller.getOptions()[self.key]))

    def cancel(self):
        self.button.changeText(self.text + ': ' + self.getKeyName(self.caller.getOptions()[self.key]))
        self.await_ = False

    def onClick(self):
        self.await_ = True
        self.button.changeText('Enter key:')

    def draw(self, screen):
        self.button.draw(screen)





class OptionsScene(Scene):
    def __init__(self, name, display, background):
        super(OptionsScene, self).__init__(name, display)
        self.events = None
        self.backgroundPath = background
        self.exitButton = None
        self.buttons = []
        self.toggle = None
        self.background = None
        self.label1 = None
        self.label2 = None

    def suspend(self):
        self.active = False
        for button in self.buttons:
            button.cancel()

    def load(self):
        self.drawable.clear()
        self.events = EventHandler()
        self.background = self.resources.getImage(self.backgroundPath)
        bkg = Sprite(self.background, layer=-5)
        bkg.resize(self.display.width, self.display.height)
        self.drawable.add(bkg)
        self.exitButton = Button(0, 0, self.display.width/8, self.display.height/12, 'Exit', 70, sound=self.resources.getSound('files/sound/click.wav'))
        self.exitButton.x = self.display.width - self.exitButton.width - self.exitButton.height/2
        self.exitButton.y = self.display.height - self.exitButton.height * 1.5
        self.drawable.add(self.exitButton)
        self.events.addEventListener(pygame.QUIT, lambda x: self.exit())
        self.exitButton.addEventListener(lambda: self.switchScene('menu'))
        self.exitButton.setImage(self.resources.getImage('files/graphic/button.png'), True)
        self.events.addEventListener(pygame.KEYDOWN, lambda x: self.switchScene('menu') if x.key == pygame.K_ESCAPE else None)
        self.events.addEventListener(pygame.MOUSEBUTTONDOWN, self.exitButton.feedMouseEvent)
        self.setupKeys()


    def toggleFullscreen(self):
        pygame.display.toggle_fullscreen()
        self.display.fullscreen = not self.display.fullscreen
        opt = self.getOptions()
        opt['FULLSCREEN'] = str(int(self.display.fullscreen))
        Scene.saveOptions(opt)


    def setupKeys(self):
        buttonImg = self.resources.getImage('files/graphic/button.png')
        sound = self.resources.getSound('files/sound/click.wav')
        self.label1 = GuiText(self.display.width/10, self.display.height/20, 'Player 1',50)
        self.label2 = GuiText(self.display.width/10 + self.display.width/3, self.display.height/20, 'Player 2', 50)
        self.drawable.add(self.label1)
        self.drawable.add(self.label2)
        self.toggle = Button(self.display.width/10 + self.display.width/1.5, self.display.height/10, self.display.width/5, self.display.height/12, 'Toggle Fullscreen',sound=sound)
        self.toggle.setImage(buttonImg, True)
        self.toggle.addEventListener(self.toggleFullscreen)
        self.events.addEventListener(pygame.MOUSEBUTTONDOWN, self.toggle.feedMouseEvent)
        self.drawable.add(self.toggle)
        self.buttons.append(Control(0, 0, 'KEY_SHOOT_P1', 'Shoot', buttonImg, sound, self))
        self.buttons.append(Control(0, 1, 'KEY_M_UP_P1', 'Up', buttonImg, sound, self))
        self.buttons.append(Control(0, 2, 'KEY_M_DOWN_P1', 'Down', buttonImg, sound, self))
        self.buttons.append(Control(0, 3, 'KEY_M_LEFT_P1', 'Left', buttonImg, sound, self))
        self.buttons.append(Control(0, 4, 'KEY_M_RIGHT_P1', 'Right', buttonImg, sound, self))
        self.buttons.append(Control(0, 5, 'KEY_WEAPON1_P1', 'Laser', buttonImg, sound, self))
        self.buttons.append(Control(0, 6, 'KEY_WEAPON2_P1', 'Rockets', buttonImg, sound, self))
        self.buttons.append(Control(0, 7, 'KEY_WEAPON3_P1', 'Plasma', buttonImg, sound, self))

        self.buttons.append(Control(1, 0, 'KEY_SHOOT_P2', 'Shoot', buttonImg, sound, self))
        self.buttons.append(Control(1, 1, 'KEY_M_UP_P2', 'Up', buttonImg, sound, self))
        self.buttons.append(Control(1, 2, 'KEY_M_DOWN_P2', 'Down', buttonImg, sound, self))
        self.buttons.append(Control(1, 3, 'KEY_M_LEFT_P2', 'Left', buttonImg, sound, self))
        self.buttons.append(Control(1, 4, 'KEY_M_RIGHT_P2', 'Right', buttonImg, sound, self))
        self.buttons.append(Control(1, 5, 'KEY_WEAPON1_P2', 'Laser', buttonImg, sound, self))
        self.buttons.append(Control(1, 6, 'KEY_WEAPON2_P2', 'Rockets', buttonImg, sound, self))
        self.buttons.append(Control(1, 7, 'KEY_WEAPON3_P2', 'Plasma', buttonImg, sound, self))

    def exit(self):
        self.exiting = True

    def run(self):
        self.active = True
        while self.active and not self.exiting:
            self.events.handle()
            if len([x for x in self.buttons if x.await_]) > 1:
                for control in self.buttons:
                    control.cancel()
            else:
                for control in self.buttons:
                    if control.await_:
                        key = self.events.getAnyKey()
                        if key:
                            control.feedKey(key)
                        break
            self.display.display(self.drawable)


