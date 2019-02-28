import pygame

from button import Button
from events import EventHandler
from gui import GuiText
from levels import Level1
from resources import Resources
from scene import Scene
from sprite import Sprite


class GameOverScene(Scene):
    def __init__(self, name, display,background, path, score=0):
        super(GameOverScene, self).__init__(name, display)
        self.scoreText = None
        self.path = path
        self.events = None
        self.background = background
        self.score = score
        self.textname = None
        self.exitButton = None
        self.tryAgainButton = None
        self.text = None
        self.saved = None

    def saveScore(self, path):
        self.saved = True
        self.drawable.remove(self.text)
        with open(path, 'a') as file:
            file.write("{}:{}\n".format(self.textname.text, self.score))
        self.textname.changeText('')
        width = self.display.width / 10
        height = self.display.height / 16
        self.exitButton = Button((self.display.width / 2) - 1.25 * width, (self.display.height - height) / 2,
                                 width, height, 'Exit', sound=self.resources.getSound('files/sound/click.wav'))
        self.tryAgainButton = Button((self.display.width / 2) + 0.25 * width, (self.display.height - height) / 2,
                                     width, height, 'Try Again', sound=self.resources.getSound('files/sound/click.wav'))
        self.exitButton.addEventListener(lambda: self.exitToMenu())
        self.tryAgainButton.addEventListener(self.reset)
        self.exitButton.setImage(self.resources.getImage('files/graphic/button.png'), True)
        self.tryAgainButton.setImage(self.resources.getImage('files/graphic/button.png'), True)
        self.drawable.add(self.exitButton)
        self.drawable.add(self.tryAgainButton)
        self.events.addEventListener(pygame.MOUSEBUTTONDOWN, self.exitButton.feedMouseEvent)
        self.events.addEventListener(pygame.MOUSEBUTTONDOWN, self.tryAgainButton.feedMouseEvent)

    def suspend(self):
        self.active = False

    def reset(self):
        self.score = 0
        self.saved = False
        self.loaded = False
        self.switchScene('level_1')

    def processEvents(self, event):
        if event.key == pygame.K_ESCAPE:
            self.exitToMenu()
        if not self.saved:
            if event.key == pygame.K_BACKSPACE:
                self.textname.changeText(self.textname.text[:-1])
            elif event.key == pygame.K_SPACE:
                self.textname.changeText(self.textname.text + ' ')
            elif event.key == pygame.K_RETURN:
                self.saveScore(self.path)
            elif len(self.textname.text) < 12:
                if 122 >= event.key >= 97:
                    key = event.key - 32 if self.events.getKeyPressed(pygame.K_LSHIFT) or self.events.getKeyPressed(
                        pygame.K_RSHIFT) else event.key
                    self.textname.changeText(self.textname.text + chr(key))
                elif 48 <= event.key <= 57:
                    self.textname.changeText(self.textname.text + chr(event.key))
            self.recenter(self.textname)


    def exitToMenu(self):
        self.score = 0
        self.loaded = False
        self.switchScene('menu')


    def run(self):
        self.active = True
        while self.active and not self.exiting:
            self.events.handle()
            self.display.display(self.drawable)



    def recenter(self, box):
        w = box.getSize()[0]
        box.x = (self.display.width - w) / 2


    def load(self):
        self.drawable.clear()
        self.events = EventHandler()
        self.events.addEventListener(pygame.KEYDOWN, self.processEvents)
        self.textname = GuiText(self.display.width/2, self.display.height / 2, '', 50)
        self.drawable.add(self.textname)
        self.scoreText = GuiText(self.display.width / 2, self.display.height/5,
                                 'Score: {}'.format(self.score), 120)
        self.text = GuiText(0, self.display.height/2.5, 'Enter name:', 75)
        self.recenter(self.text)
        self.recenter(self.scoreText)
        self.drawable.add(self.scoreText)
        self.drawable.add(self.text)
        bgr = Sprite(pygame.image.load(self.background), 0, 0, -5)
        bgr.resize(self.display.width, self.display.height)
        self.drawable.add(bgr)
        self.saved = False

    def exit(self):
        self.exiting = True
