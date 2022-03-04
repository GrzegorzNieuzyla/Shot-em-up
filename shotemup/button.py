import pygame


class Button:
    def __init__(self, x, y, width, height, text, fontsize=30,
                 fgcolor=(0x00, 0x00, 0x00), bgcolor=(0xff, 0xff, 0xff), layer=-1, sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.text = text
        self.listeners = []
        self.fontsize = fontsize
        self.font = pygame.font.SysFont(None, self.fontsize)
        self.image = None
        self.textrender = self.font.render(self.text, True, self.fgcolor)
        self.enabled = True
        self.visible = True
        self.layer = layer
        self.sound = sound


    def changeText(self, text):
        self.text = text
        self.textrender = self.font.render(self.text, True, self.fgcolor)


    def addEventListener(self, listener):
        self.listeners.append(listener)

    def feedMouseEvent(self, event):
        if self.enabled:
            x = event.pos[0]
            y = event.pos[1]
            if self.x + self.width > x >= self.x and self.y + self.height > y >= self.y:
                if self.sound:
                    self.sound.play()
                for listener in self.listeners:
                    listener()

    def setbgColor(self, color):
        self.bgcolor = color


    def setImage(self, image, stretch=False):
        self.image = image
        if stretch:
            self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))

    def draw(self, screen):
        if self.enabled:
            if self.image:
                screen.blit(self.image, pygame.Rect(self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(screen, self.bgcolor, pygame.Rect(self.x, self.y, self.width, self.height))
            if self.text:
                screen.blit(self.textrender, self.textrender.get_rect(center=(self.x+self.width/2, self.y+self.height/2)))
