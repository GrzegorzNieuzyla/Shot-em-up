import pygame


class EventHandler:
    MOUSE_LEFT = 1
    MOUSE_MIDDLE = 2
    MOUSE_RIGHT = 3
    NEXT_FRAME_EVENT = pygame.USEREVENT

    def __init__(self, keyboard=True, mouse=True):
        self.listeners = {}
        self.keyboard = keyboard
        self.mouse = mouse
        self.keyboardPress = {}
        self.keyboardHold = {}
        self.mousePress = {}

    def recheck(self):
        for key in self.keyboardHold:
            if self.keyboardHold[key]:
                self.keyboardHold[key] = pygame.key.get_pressed()[key]


    def handle(self):
        """
        Process events for current frame
        """
        pygame.event.post(pygame.event.Event(EventHandler.NEXT_FRAME_EVENT, {}))
        self.keyboardPress = self.keyboardPress.fromkeys(self.keyboardPress, False)
        self.mousePress = self.mousePress.fromkeys(self.mousePress, None)
        for event in pygame.event.get():
            if self.keyboard:
                if event.type == pygame.KEYDOWN:
                    self.keyboardPress[event.key] = True
                    self.keyboardHold[event.key] = True
                if event.type == pygame.KEYUP:
                    self.keyboardHold[event.key] = False
            if self.mouse:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePress[event.button] = event.pos
            if event.type in self.listeners.keys():
                for func in self.listeners[event.type]:
                    func(event)

    def removeEventListener(self, event, func):
        self.listeners[event].remove(func)


    def removeObjectFromListener(self, func):
        self.listeners = {k: v for k, v in self.listeners if v != func}

    def addEventListener(self, event, func):
        if event not in self.listeners.keys():
            self.listeners[event] = []
        self.listeners[event].append(func)

    def getAnyKey(self):
        for key in self.keyboardPress.keys():
            if self.keyboardPress[key]:
                return key
        return None


    def getKey(self, key):
        """
        returns True if key was pressed in last frame
        """
        if key not in self.keyboardPress.keys():
            self.keyboardPress[key] = False
        return self.keyboardPress[key]

    def getMouse(self, button):
        """
        returns mouse position if mouse button was pressed in last frame, otherwise None
        """
        if button not in self.mousePress.keys():
            self.mousePress[button] = None
        return self.mousePress[button]

    def getMousePressed(self, button):
        """
        returns True if mouse button is being held
        """
        return pygame.mouse.get_pressed()[button]

    def getKeyPressed(self, key):
        """
        returns True if key is being held
        """
        if key not in self.keyboardHold.keys():
            self.keyboardHold[key] = False
        return self.keyboardHold[key]
