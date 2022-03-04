from pathlib import Path

import pygame

from .resources import Resources


class Scene:
    options = {}
    scenes = []
    optionsPath = 'files/script/options'
    next = None

    @staticmethod
    def getScene(name):
        for scene in Scene.scenes:
            if scene.name == name:
                return scene
        return None


    @staticmethod
    def loadOptions():
        if Path(Scene.optionsPath).exists():
            for line in open(Scene.optionsPath,'r').read().splitlines():
                key, value = line.split(':', 2)
                Scene.options[key] = value
        else:
            Scene.options['KEY_WEAPON1_P1'] = str(pygame.K_1)
            Scene.options['KEY_WEAPON2_P1'] = str(pygame.K_2)
            Scene.options['KEY_WEAPON3_P1'] = str(pygame.K_3)
            Scene.options['KEY_WEAPON1_P2'] = str(pygame.K_KP1)
            Scene.options['KEY_WEAPON2_P2'] = str(pygame.K_KP2)
            Scene.options['KEY_WEAPON3_P2'] = str(pygame.K_KP3)
            Scene.options['KEY_M_LEFT_P1'] = str(pygame.K_a)
            Scene.options['KEY_M_RIGHT_P1'] = str(pygame.K_d)
            Scene.options['KEY_M_UP_P1'] = str(pygame.K_w)
            Scene.options['KEY_M_DOWN_P1'] = str(pygame.K_s)
            Scene.options['KEY_M_LEFT_P2'] = str(pygame.K_LEFT)
            Scene.options['KEY_M_RIGHT_P2'] = str(pygame.K_RIGHT)
            Scene.options['KEY_M_UP_P2'] = str(pygame.K_UP)
            Scene.options['KEY_M_DOWN_P2'] = str(pygame.K_DOWN)
            Scene.options['KEY_SHOOT_P1'] = str(pygame.K_SPACE)
            Scene.options['KEY_SHOOT_P2'] = str(pygame.K_RSHIFT)
            Scene.options['FULLSCREEN'] = '1'
            Scene.saveOptions(Scene.options)

    @staticmethod
    def saveOptions(options):
        with open(Scene.optionsPath, 'w') as file:
            for key in options.keys():
                file.write(key)
                file.write(':')
                file.write(str(options[key]))
                file.write('\n')
        Scene.options = options

    @staticmethod
    def runProgram(scene):
        Scene.next = scene
        while Scene.next is not None:
            current = Scene.getScene(Scene.next)
            if not current:
                raise RuntimeError("Scene named '{}' is not created.".format(Scene.next))
            else:
                Scene.next = None
                if not current.loaded:
                    current.load()
                    current.loaded = True
                current.run()
                if current.exiting:
                    del Scene.scenes[Scene.scenes.index(current)]


    def __init__(self, name, display):
        self.display = display
        self.name = name
        self.loaded = False
        self.active = False
        self.exiting = False
        self.drawable = set()
        self.resources = Resources()
        Scene.scenes.append(self)

    def load(self):
        raise NotImplementedError('Override load method in child class')

    def run(self):
        raise NotImplementedError('Override run method in child class')

    def suspend(self):
        raise NotImplementedError('Override call method in child class')

    def exit(self):
        raise NotImplementedError('Override exit method in child class')

    def getOptions(self):
        return Scene.options

    def switchScene(self, name):
        Scene.next = name
        self.suspend()
