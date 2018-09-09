import numpy as np
import math, random

def mapValue(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

class Rocket:

    def __init__ (self, width, height, lifespan, goal, dna=None):
        self.pos = np.array([width / 2, 26])
        self.w = 5
        self.h = 25
        self.goal = np.array([goal.middleX, goal.middleY])
        self.score = 0
        self.fitness = 0
        self.boundaries = (width, height)
        self.vel = np.array([0, 1])
        self.acc = np.array([0, 0])
        if dna == None:
            self.dna = DNA(lifespan)
        else:
            self.dna = self.mutate(dna)
        self.lifespan = lifespan
        self.counter = 0

    def mutate(self, dna):
        if random.random() < 0.01:
            for x in dna.genes:
                if random.random() < 0.01:
                    x += random.uniform(-0.01, 0.01)
        return dna

    def applyForce(self, force):
        self.acc = np.add(self.acc, force)

    def update(self):
        # calc score
        maxDistance = self.boundaries[1]
        yTemp = mapValue(self.pos[1], 0, self.boundaries[1], self.boundaries[1], 0)
        tempPos = np.array([self.pos[0], yTemp])
        temp = np.subtract(tempPos, self.pos)
        dist = np.linalg.norm(temp)
        if dist < maxDistance:
            value = mapValue(dist, 0, maxDistance, maxDistance, 0)
            self.score = value
        else:
            self.score -= 0

        if not self.counter  >= self.lifespan -1:
            self.counter += 1
            self.applyForce(self.dna.genes[self.counter])
        self.vel = np.add(self.vel, self.acc)
        self.pos = np.add(self.pos, self.vel)
        self.acc = np.multiply(self.acc, 0)

    def show (self, window_, pygame):
        points = self.calculatePoints()
        pygame.draw.polygon(window_, (255, 255, 255), points, 0)

    def rotate_around_middle(self, xy, radians):
        x, y = xy
        offset_x = self.pos[0]
        offset_y = mapValue(self.pos[1], 0, self.boundaries[1], self.boundaries[1], 0)
        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = math.cos(radians)
        sin_rad = math.sin(radians)
        qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
        return qx, qy

    def get_radians(self, v1, v2):
        # v1 and v2 cannot be zero vectors
        v1_u = np.divide(v1, np.linalg.norm(v1))
        v2_u = np.divide(v2, np.linalg.norm(v2))
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def calculatePoints(self):
        points = []
        null_vector = np.array([0, 1])
        radians = self.get_radians(null_vector, self.vel)
        if self.vel[0] > 0:
            radians *= -1

        x = self.pos[0] - self.w / 2
        y = self.pos[1] + self.h / 2
        y_new = mapValue(y, 0, self.boundaries[1], self.boundaries[1], 0)
        points.append(self.rotate_around_middle((x, y_new), radians))

        x = self.pos[0]
        y = self.pos[1] + self.h * 0.66
        y_new = mapValue(y, 0, self.boundaries[1], self.boundaries[1], 0)
        points.append(self.rotate_around_middle((x, y_new), radians))

        x = self.pos[0] + self.w / 2
        y = self.pos[1] + self.h / 2
        y_new = mapValue(y, 0, self.boundaries[1], self.boundaries[1], 0)
        points.append(self.rotate_around_middle((x, y_new), radians))

        x = self.pos[0] + self.w / 2
        y = self.pos[1] - self.h / 2
        y_new = mapValue(y, 0, self.boundaries[1], self.boundaries[1], 0)
        points.append(self.rotate_around_middle((x, y_new), radians))

        x = self.pos[0] - self.w / 2
        y = self.pos[1] - self.h / 2
        y_new = mapValue(y, 0, self.boundaries[1], self.boundaries[1], 0)
        points.append(self.rotate_around_middle((x, y_new), radians))

        return points

    def borders(self):
        if self.pos[0] < -(self.w / 2) :
            self.pos[0] = self.boundaries[0] + (self.w / 2)
        if self.pos[1] < -(self.h / 2):
            self.pos[1] = self.boundaries[1] + (self.h / 2)
        if self.pos[0] > self.boundaries[0] + (self.w / 2):
            self.pos[0] = -(self.w / 2)
        if self.pos[1] > self.boundaries[1] + (self.h / 2):
            self.pos[1] = -(self.h / 2)

    def intersect(self, oleft, otop, oright, obottom, middle=False):
        points = self.calculatePoints()
        xs = []
        ys = []
        for point in points:
            xs.append(point[0])
            ys.append(point[1])

        if middle is False:
            left = min(xs)
            right = max(xs)
            bottom = max(ys)
            top = min(ys)
        else:
            left = self.pos[0]
            right = self.pos[0]
            top = mapValue(self.pos[1], 0, self.boundaries[1], self.boundaries[1], 0)
            bottom = mapValue(self.pos[1], 0, self.boundaries[1], self.boundaries[1], 0)

        negationResult = left >= oright or right <= oleft or top >= obottom or bottom <= otop

        return not negationResult

    def calculateFitness(self):
        pass

class DNA:

    def __init__(self, lifespan):
        self.genes = []
        for i in range(0, lifespan):
            self.genes.append(np.array([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)]))


class Obstacle:
    def __init__(self, x, y, w, h, c=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.left = x
        self.top = y
        self.middleX = x + w / 2
        self.middleY = y + h / 2
        self.right = x + w
        self.bottom = y + h
        if c == None:
            self.c = (255, 255, 255)
        else:
            self.c = c

    def show(self, window, pygame):
        pygame.draw.rect(window, self.c, (self.x, self.y, self.w, self.h))
