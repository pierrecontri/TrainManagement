class Chase:

    def __init__(self, size = 128):
        self.counter = 1
        self.orientation = 0
        self.size = size

    def ticks(self):
        if self.orientation  == 0:
            self.counter = self.counter << 1
            if self.counter >= self.size:
                self.orientation  = 1
            elif self.counter < 2:
                self.counter = 2
        else:
            self.counter = self.counter >> 1
            if self.counter < 2:
                self.orientation = 0
                self.counter = 1
        
        return self.counter
