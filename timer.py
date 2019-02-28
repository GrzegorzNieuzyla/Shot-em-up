import time


class Timer:
    def __init__(self, duration, repeat=False):
        self.onTimeElapsed = []
        self.shouldTimerEnd = lambda: False
        self.onEnd = []
        self.duration = duration
        self.repeat = repeat
        self.timePassed = 0
        self.timeUpdate = time.time()
        self.toDelete = False
        self.count = 0

    def update(self):
        t = time.time()
        self.timePassed += (t - self.timeUpdate)
        self.timeUpdate = t
        if self.timePassed >= self.duration:
            self.count += 1
            if not self.shouldTimerEnd():
                for func in self.onTimeElapsed:
                    func()
                if self.repeat:
                    self.timePassed = 0
                else:
                    self.toDelete = True
            else:
                self.toDelete = True
            if self.toDelete:
                for func in self.onEnd:
                        func()





