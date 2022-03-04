from pathlib import Path

import pygame

from .button import Button
from .events import EventHandler
from .gui import GuiText
from .scene import Scene
from .sprite import Sprite


class HiScoresScene(Scene):
    def __init__(self, name, display, background, path):
        super(HiScoresScene, self).__init__(name, display)
        self.path = path
        self.background = background
        self.event = None
        self.scoreTexts = None
        self.exitButton = None

    def getScores(self):
        scores = []
        if Path(self.path).exists():
            with open(self.path, 'r') as f:
                for line in f.readlines():
                    if ':' in line:
                        parts = line.split(':', 1)
                        scores.append((parts[0], parts[1][:-1]))
        scores.sort(key=lambda x: int(float(x[1])), reverse=True)
        if len(scores) > 10:
            scores = scores[0:10]
        elif len(scores) < 10:
            scores += [('', 0)] * (10-len(scores))
        return scores


    def exit(self):
        self.exiting = True

    def run(self):
        self.active = True
        self.update()
        while self.active and not self.exiting:
            self.event.handle()
            self.display.display(self.drawable)

    def update(self):
        scores = self.getScores()
        i = 0
        for st in self.scoreTexts:
            st.changeText('{}:  {} Points'.format(scores[i][0], scores[i][1]))
            self.recenter(st)
            i += 1

    def recenter(self, box):
        w = box.getSize()[0]
        box.x = (self.display.width - w) / 2

    def suspend(self):
        self.active = False

    def load(self):
        self.scoreTexts = []
        self.event = EventHandler()
        self.event.addEventListener(pygame.QUIT, lambda x: self.exit())
        self.exitButton = Button(0, 0, self.display.width / 8, self.display.height / 12, 'Exit', 70,
                                 sound=self.resources.getSound('files/sound/click.wav'))
        self.exitButton.x = self.display.width - self.exitButton.width - self.exitButton.height / 2
        self.exitButton.y = self.display.height - self.exitButton.height * 1.5
        self.exitButton.setImage(self.resources.getImage('files/graphic/button.png'), True)
        self.drawable.add(self.exitButton)
        self.event.addEventListener(pygame.MOUSEBUTTONDOWN , self.exitButton.feedMouseEvent)
        self.exitButton.addEventListener(lambda: self.switchScene('menu'))
        spacing = (self.display.height * 0.7) / 10
        for i in range(10):
            text = GuiText(0, 0.15 * self.display.height + i * spacing, '', 50)
            self.recenter(text)
            self.drawable.add(text)
            self.scoreTexts.append(text)

        self.event.addEventListener(pygame.KEYDOWN, lambda e: self.switchScene('menu') if e.key == pygame.K_ESCAPE else None)
        bgr = Sprite(pygame.image.load(self.background), layer=-5)
        bgr.resize(self.display.width, self.display.height)
        self.drawable.add(bgr)
