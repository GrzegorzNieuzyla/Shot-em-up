import pygame


class GuiText:
    def __init__(self, x, y, text, fontsize=30, color=(255, 255, 255), layer=5):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.fontsize = fontsize
        self.font = pygame.font.SysFont(None, self.fontsize)
        self.render = self.font.render(self.text, True, self.color)
        self.visible = True
        self.layer = layer
        self.width, self.height = self.getSize()



    def draw(self, screen):
        screen.blit(self.render, (self.x, self.y))

    def changeText(self, text):
        self.text = str(text)
        self.render = self.font.render(self.text, True, self.color)


    def getSize(self):
        return self.render.get_size()