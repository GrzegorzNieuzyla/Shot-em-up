from resources import Resources
from scene import Scene
from sprite import Sprite
from events import EventHandler
from gui import GuiText
import pygame


class Level(Scene):
    LAYER_BACKGROUND = -1
    LAYER_GUI = 10

    def __init__(self, name, display, background):
        super(Level, self).__init__(name, display)
        self.backgroundPath = background
        self.event = None
        self.background = None
        self.backgroundComplement = None
        self.fps = None
        self.reset()


    def fitBackground(self):
        w = self.display.width
        ratio = w / self.background.width
        h = self.background.height * ratio
        self.background.resize(w, h)

    def showFPS(self):
        self.fps.changeText(str(self.display.getFPS()).split('.')[0])


    def addToDrawQueue(self, *args):
        for obj in args:
            self.drawable.add(obj)


    def removeFromDrawQueue(self, obj) -> bool:
        if obj in self.drawable:
            self.drawable.remove(obj)
            return True
        return False

    def reset(self):
        self.drawable = set()
        self.event = EventHandler()
        self.loaded = False
        self.fps = GuiText(10, 10, '', layer=Level.LAYER_GUI)
        self.addToDrawQueue(self.fps)
        self.background = Sprite(self.resources.getImage(self.backgroundPath), layer=Level.LAYER_BACKGROUND)
        self.fitBackground()
        self.backgroundComplement = self.background.crop(
            0, self.background.height - self.display.height, self.background.width, self.display.height)
        self.addToDrawQueue(self.background)
        self.loaded = False


    def moveBackground(self, distance, useComplement=True):
        self.background.y += distance
        if self.background.y > 0:
            if useComplement:
                if (self.backgroundComplement, Level.LAYER_BACKGROUND) not in self.drawable:
                    self.addToDrawQueue(self.backgroundComplement)
                self.backgroundComplement.y = self.background.y - self.backgroundComplement.height
                if self.background.y > self.display.height:
                    self.removeFromDrawQueue(self.backgroundComplement)
                    self.background.y = self.display.height - self.background.height + self.backgroundComplement.y
            else:
                self.background.y = self.display.height - self.background.height + self.background.y


    def exit(self):
        self.exiting = True

    def suspend(self):
        self.active = False

    def run(self):
        raise NotImplementedError("Implement method: run")

    def load(self):
        raise NotImplementedError("Implement method: load")
