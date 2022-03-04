import pygame


class Display:
    def __init__(self, width, height, title=' ', fullscreen=False, backgroundColor=(0, 0, 0)):
        pygame.init()
        pygame.display.set_caption(title)
        pygame.display.set_icon(pygame.image.load('files/ships/player.png'))
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.fullscreen = fullscreen
        self.backgroundColor = backgroundColor
        if fullscreen:
            self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        self.FPS = 60



    def __onScreen(self, obj):
        if obj.x > self.width or obj.x + obj.width < 0:
            return False
        if obj.y > self.height or obj.y + obj.height < 0:
            return False
        return True

    def display(self, drawable):
        drawable = sorted(drawable, key=lambda x: x.layer)
        self.clock.tick(self.FPS)
        self.screen.fill(self.backgroundColor)
        for obj in drawable:
            if obj.visible and self.__onScreen(obj):
                obj.draw(self.screen)
        pygame.display.flip()

    def getFrameTime(self) -> float:
        return self.clock.get_time()

    def getFPS(self) -> float:
        if self.getFrameTime() == 0:
            return 0
        return 1/(self.getFrameTime()/1000)
