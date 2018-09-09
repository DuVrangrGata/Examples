import pygame, random
import numpy as np
from engine import mapValue

width, height = 1000, 1000

pygame.init()

window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

pygame.display.set_caption("Barnsley Farn")

def f1(point):
    multiplikator = np.array(np.mat('0.0 0.0; 0.0 0.16'))
    return np.dot(multiplikator, point)

def f2(point):
    multiplikator = np.array(np.mat('0.85 0.04; -0.04 0.85'))
    summand = np.array([0, 1.6])
    return np.add(np.dot(multiplikator, point), summand)

def f3(point):
    multiplikator = np.array(np.mat('0.2 -0.26; 0.23 0.22'))
    summand = np.array([0, 1.6])
    return np.add(np.dot(multiplikator, point), summand)

def f4(point):
    multiplikator = np.array(np.mat('-0.15 0.28; 0.26 0.24'))
    summand = np.array([0, 0.44])
    return np.add(np.dot(multiplikator, point), summand)

def iteration(point):
    zufall = random.random()
    if zufall >= 0.99:
        return f1(point)
    elif zufall < 0.99 and zufall >= 0.14:
        return f2(point)
    elif zufall  < 0.14 and zufall >= 0.07:
        return f3(point)
    else:
        return f4(point)

thePoint = np.array([0, 0])

running = True

window.fill((0, 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print('Closed')

    nextPoint = iteration(thePoint)
    drawPointX = mapValue(nextPoint[0], -2.2, 2.7, 0, width)
    drawPointY = mapValue(nextPoint[1], 0, 10, height, 0)
    pygame.draw.circle(window, (255, 255, 255),
    (int(drawPointX), int(drawPointY)), 1)
    thePoint = nextPoint

    pygame.display.update()
    #clock.tick(100)


pygame.quit()
