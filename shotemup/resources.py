import os

import pygame


class Resources:
    def __init__(self):
        self.animations = {}
        self.images = {}
        self.sounds = {}

    def getSound(self, path):
        if path not in self.sounds:
            self.sounds[path] = self.__loadSound(path)
        return self.sounds[path]

    def getImage(self, path):
        if path not in self.images:
            self.images[path] = self.__loadImage(path)
        return self.images[path]


    def __fitToResolution(self, image):
        width, height = image.get_size()
        w, h = pygame.display.get_surface().get_size()
        if w != 1920 or h != 1080:
            ratioX = w / 1920
            ratioY = h / 1080
            image = pygame.transform.scale(image, (int(width * ratioX), int(height * ratioY)))
        return image

    def __loadImage(self, path):
        return self.__fitToResolution(pygame.image.load(path).convert_alpha())

    def getAnimation(self, path):
        if path not in self.animations:
            self.animations[path] = self.__loadAnimation(path)
        return self.animations[path]


    def __loadAnimation(self, path):
        files = []
        for file in sorted(os.listdir(path)):
            files.append(self.__fitToResolution(pygame.image.load(path + '/' + file).convert_alpha()))
        return files

    def __loadSound(self, path):
        return pygame.mixer.Sound(path)