from engine import *
import random

frameCount = 0
symbolSize = 26

class Symbol:
    
    def __init__ (self, x, y, speed, first):
        self.x = x
        self.y = y
        self.value = None
        self.speed = speed
        self.switchInterval = random.randrange(2, 20)
        self.first = first

    def setToRandomSymbol(self):
        if frameCount % self.switchInterval is 0:
            code = 0x30A0 + random.randint(0, 96)
            self.value = chr(code)

    def render(self, window_):
        if self.first is True:
            c = ( 255, 255, 255)
        else:
            c = ( 0, 255, 70)
        self.setToRandomSymbol()
        ts = myfont.render(self.value, True, c, ())
        window_.blit(ts, (self.x, self.y))
        self.rain()
        
    def rain (self):
        if self.y >= getHeight():
            self.y = 0
        else:
            self.y += self.speed


window = create_window(1440, 900)
        
class Stream:
    
    def __init__ (self):
        self.symbols = []
        self.totalSymbols = random.randint(5, 30)
        self.speed = random.randint(5, 20)


    def generateSymbols(self, x, y):
        first = int(random.randint(0, 4)) == 1
        for i in range (self.totalSymbols):
            sy = Symbol(x, y, self.speed, first)
            self.symbols.append(sy)
            y -= symbolSize
            first = False

    def render (self, window_):
        for i in self.symbols:
            i.render(window_)
        
start()

myfont = pygame.font.Font('font.ttf', symbolSize)

streams = []

black = (0, 0, 0)

x = 0

for i in range(int(getWidth() / symbolSize)):
    stream = Stream()
    stream.generateSymbols(x, random.randint(-1000, 0))
    streams.append(stream)
    x += symbolSize


isRunning = True

while isRunning:
    if isClosing():
        isRunning = False
        
    window.fill((0, 0, 0, 150))

    for i in streams:
        i.render(window)
    
    frameCount += 1

    update(30)

exit()
