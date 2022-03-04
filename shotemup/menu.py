import pygame

from .button import Button
from .events import EventHandler
from .scene import Scene
from .sprite import Sprite


class Menu(Scene):
    def __init__(self, name, display, background):
        super(Menu, self).__init__(name, display)
        self.event = EventHandler()
        self.startButton = None
        self.start2pButton = None
        self.background = None
        self.exitButton = None
        self.resumeButton = None
        self.hiScoresButton = None
        self.optionsButton = None
        self.levelInProgress = None
        self.backgroundPath = background

    def exit(self):
        self.exiting = True

    def startNewGame(self, player2=False):
        scene = Scene.getScene('level_1')
        scene.twoPlayers = player2
        if scene.loaded:
            scene.reset()
        self.switchScene('level_1')

    def suspend(self):
        self.active = False

    def load(self):
        self.background = Sprite(self.resources.getImage(self.backgroundPath),layer=-1)
        self.background.resize(self.display.width, self.display.height)
        self.event.addEventListener(pygame.KEYDOWN, lambda e: self.exit() if e.key == pygame.K_ESCAPE else None)
        self.event.addEventListener(pygame.QUIT, lambda x: self.exit())
        self.resumeButton = Button(
            self.display.width * 0.42, self.display.height * 0.15,
            self.display.width * 0.16, self.display.height * 0.05, "Resume", layer=1,
            sound=self.resources.getSound('files/sound/click.wav'))
        self.startButton = Button(
            self.display.width * 0.42, self.resumeButton.y + self.display.height / 12,
            self.display.width * 0.16, self.display.height * 0.05, "1 Player",layer=1,
            sound=self.resources.getSound('files/sound/click.wav'))
        self.start2pButton = Button(
            self.display.width * 0.42, self.startButton.y + self.display.height / 12,
            self.display.width * 0.16, self.display.height * 0.05, "2 Players", layer=1,
            sound=self.resources.getSound('files/sound/click.wav'))
        self.optionsButton = Button(
            self.display.width * 0.42, self.start2pButton.y + self.display.height / 12,
            self.display.width * 0.16, self.display.height * 0.05, "Options", layer=1,
            sound=self.resources.getSound('files/sound/click.wav'))
        self.hiScoresButton = Button(
            self.display.width * 0.42, self.optionsButton.y + self.display.height / 12,
            self.display.width * 0.16, self.display.height * 0.05, "High Scores", layer=1,
            sound=self.resources.getSound('files/sound/click.wav'))
        self.exitButton = Button(
            self.display.width * 0.42, self.hiScoresButton.y + self.display.height / 12,
            self.display.width * 0.16, self.display.height * 0.05, "Exit", layer=1,
            sound=self.resources.getSound('files/sound/click.wav'))
        self.exitButton.setImage(self.resources.getImage('files/graphic/button.png'),True)
        self.resumeButton.setImage(self.resources.getImage('files/graphic/button.png'),True)
        self.startButton.setImage(self.resources.getImage('files/graphic/button.png'),True)
        self.start2pButton.setImage(self.resources.getImage('files/graphic/button.png'),True)
        self.optionsButton.setImage(self.resources.getImage('files/graphic/button.png'),True)
        self.hiScoresButton.setImage(self.resources.getImage('files/graphic/button.png'),True)
        self.drawable.add(self.startButton)
        self.drawable.add(self.start2pButton)
        self.drawable.add(self.background)
        self.drawable.add(self.resumeButton)
        self.drawable.add(self.optionsButton)
        self.drawable.add(self.hiScoresButton)
        self.drawable.add(self.exitButton)
        self.resumeButton.addEventListener(lambda: self.switchScene('level_1'))
        self.startButton.addEventListener(lambda: self.startNewGame(False))
        self.start2pButton.addEventListener(lambda: self.startNewGame(True))
        self.exitButton.addEventListener(self.exit)
        self.optionsButton.addEventListener(lambda: self.switchScene('options'))
        self.hiScoresButton.addEventListener(lambda: self.switchScene('hiscores'))
        self.event.addEventListener(pygame.MOUSEBUTTONDOWN, lambda e: self.startButton.feedMouseEvent(e))
        self.event.addEventListener(pygame.MOUSEBUTTONDOWN, lambda e: self.start2pButton.feedMouseEvent(e))
        self.event.addEventListener(pygame.MOUSEBUTTONDOWN, lambda e: self.exitButton.feedMouseEvent(e))
        self.event.addEventListener(pygame.MOUSEBUTTONDOWN, lambda e: self.resumeButton.feedMouseEvent(e))
        self.event.addEventListener(pygame.MOUSEBUTTONDOWN, lambda e: self.optionsButton.feedMouseEvent(e))
        self.event.addEventListener(pygame.MOUSEBUTTONDOWN, lambda e: self.hiScoresButton.feedMouseEvent(e))


    def run(self):
        self.display.FPS = 25
        self.resumeButton.enabled =  self.levelInProgress
        self.resumeButton.visible =  self.levelInProgress
        self.active = True
        while self.active and not self.exiting:
            self.event.handle()
            if self.display.fullscreen and self.event.getKeyPressed(pygame.K_TAB) and self.event.getKeyPressed(pygame.K_LALT):
                pygame.display.iconify()
            pygame.event.post(pygame.event.Event(EventHandler.NEXT_FRAME_EVENT))
            self.display.display(self.drawable)

