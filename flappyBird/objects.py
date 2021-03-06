from engine import *
from NeuralNetwork import *
import random, math

class Bird:
    def __init__(self, brain = None, learning_rate = 0.1):
        self.y = getHeight() / 2
        self.x = 64
        self.r = 12
        self.gravity = 0.7
        self.lift = -20
        self.velocity = 0
        self.score = 0
        self.fitness = 0
        self.learning_rate = learning_rate
        if brain is not None:
            self.brain = brain.copy()
        else:
            self.brain = NeuralNetwork(5, 2, 2, self.learning_rate)

    def show(self, window):
        pygame.draw.circle(window, (255, 255, 255), (int(self.x), int(self.y)), self.r)

    def mutate(self):
        self.brain.mutate(0.1)

    def think(self, pipes):

        closest = Pipe()
        closestD = math.inf
        for i in pipes:
            d = (i.x + i.w) - self.x
            if d < closestD and d > 0:
                closest = i
                closestD = d

        inputs = []
        inputs.append(self.y / getHeight())
        inputs.append(closest.top / getHeight())
        inputs.append(closest.bottom / getHeight())
        inputs.append(closest.x / getHeight())
        inputs.append(self.velocity / 10)
        output = self.brain.feedforward(inputs)
        if output[0] > output[1]:
            self.up()
        
    def update(self):
        self.score += 1
        self.velocity += self.gravity
        self.velocity *= 0.9
        self.y += self.velocity

        if self.y < 0:
            self.y = 0

    def offScreen(self):
        if self.y > getHeight():
            return True
        return False

    def up(self):
        self.velocity += self.lift

    def copy(self):
        return Bird(self.brain)

class Pipe:
    def __init__(self):
        self.empty = 100
        self.centery = random.randrange(self.empty, getHeight() - self.empty)
        self.top = self.centery - self.empty / 2
        self.bottom = getHeight() - (self.centery + self.empty / 2)
        self.x = getWidth()
        self.w = 80
        self.speed = 6

    def show(self, window):
        c = (255, 255, 255)
        pygame.draw.rect(window, c, (self.x, 0, self.w, self.top))
        pygame.draw.rect(window, c, (self.x, getHeight() - self.bottom, self.w, self.bottom))

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        if self.x < -self.w:
            return True
        else:
            return False

    def hits(self, bird):
        if (bird.y - bird.r) < self.top or (bird.y + bird.r) > (getHeight() - self.bottom):
            if bird.x > self.x and bird.x < self.x + self.w:
                return True
        return False
