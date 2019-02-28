#!/bin/env python3
import pygame
from display import Display
from gameoverscene import GameOverScene
from hiscores import HiScoresScene
from menu import Menu
from optionsscene import OptionsScene
from scene import Scene
from levels import Level1


def main():
    Scene.loadOptions()
    pygame.mixer.pre_init(44100, -16, 1, 1024)
    pygame.init()
    info = pygame.display.Info()
    #display = Display(1366, 768, fullscreen=False)
    display = Display(info.current_w, info.current_h, fullscreen=bool(int(Scene.options['FULLSCREEN'])))
    Menu('menu', display, 'files/graphic/menu.jpg')
    Level1('level_1', display, 'files/graphic/stars.png')
    GameOverScene('gameover', display, 'files/graphic/stars.png', '.scores')
    HiScoresScene('hiscores', display, 'files/graphic/stars.png', '.scores')
    OptionsScene('options', display, 'files/graphic/stars.png')
    pygame.mixer.music.load('files/sound/music.ogg')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    Scene.runProgram('menu')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
