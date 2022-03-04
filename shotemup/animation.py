import pygame


class Animation:
    def __init__(self, frames):
        self.frames = frames
        self.index = -1
        self.endOfAnimation = False
        self.width, self.height = self.frames[0].get_size()

    def nextFrame(self) -> pygame.image:
        self.index += 1
        if self.index >= len(self.frames):
            self.endOfAnimation = True
            return self.frames[len(self.frames)-1]
        img = self.frames[self.index]
        return img

    def hasEnded(self):
        return self.endOfAnimation
