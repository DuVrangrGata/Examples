import pygame, random
import numpy as np

width, height = 601, 601
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        result = (self.x <= point[0] and
                  self.x + self.w >= point[0] and
                  self.y <= point[1] and
                  self.y + self.h >= point[1])
        return result

class Quadtree:
    def __init__(self, boundaries):
        self.boundaries = boundaries
        self.numOfPoints = 2
        self.values = []
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None
        self.has_child = False

    def draw(self, window):
        pygame.draw.rect(window, blue, (self.boundaries.x, self.boundaries.y, self.boundaries.w, self.boundaries.h), 2)
        if self.has_child is True:
            self.top_left.draw(window)
            self.top_right.draw(window)
            self.bottom_left.draw(window)
            self.bottom_right.draw(window)

    def add_point(self, p):
        if self.boundaries.contains(p) == True:
            self.values.append(p)
        else:
            return
        if self.has_child is True:
            self.top_left.add_point(p)
            self.top_right.add_point(p)
            self.bottom_left.add_point(p)
            self.bottom_right.add_point(p)

        if len(self.values) > self.numOfPoints and self.has_child is False:
            self.new_layer()

    def new_layer(self):
        self.top_left     = Quadtree(Rectangle(self.boundaries.x, self.boundaries.y, self.boundaries.w / 2, self.boundaries.h / 2))
        self.top_right    = Quadtree(Rectangle(self.boundaries.x + self.boundaries.w / 2, self.boundaries.y, self.boundaries.w / 2, self.boundaries.h / 2))
        self.bottom_left  = Quadtree(Rectangle(self.boundaries.x, self.boundaries.y + self.boundaries.h / 2, self.boundaries.w / 2, self.boundaries.h / 2))
        self.bottom_right = Quadtree(Rectangle(self.boundaries.x + self.boundaries.w / 2, self.boundaries.y + self.boundaries.h / 2, self.boundaries.w / 2, self.boundaries.h / 2))
        for point in self.values:
            self.top_left.add_point(point)
            self.top_right.add_point(point)
            self.bottom_left.add_point(point)
            self.bottom_right.add_point(point)
        self.has_child = True

pygame.init()

pygame.display.set_caption('Quadtree')
window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

running = True

bounds = Rectangle(0, 0, 600, 600)

qt = Quadtree(bounds)

points = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print('Closed')
        if event.type == pygame.MOUSEBUTTONDOWN:
            point = np.array([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]])
            points.append(point)
            qt.add_point(point)
            print('Anzahl Punkte:', len(points))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                for _ in range(100):
                    point = np.array([random.randrange(0, width), random.randrange(0, height)])
                    points.append(point)
                    qt.add_point(point)
                print('Anzahl Punkte:', len(points))
            # elif event.key == pygame.K_d:
            #     points.clear()
            #     print('Anzahl Punkte:', len(points))

    window.fill(white)



    qt.draw(window)
    for point in points:
        pygame.draw.circle(window, red, (point[0], point[1]), 2)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
