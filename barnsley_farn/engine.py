# Version 1.1

import pygame, sys

def start():
    pygame.init()
    global clock
    clock = pygame.time.Clock()

def translate(coords, width, height):
    return (coords[0] + width, coords[1] + height)

def create_window(width_, height_):
    global window, window_height, window_width, window_title
    window_width, window_height = width_, height_
    window_title = 'Test'
    pygame.display.set_caption(window_title)
    window = pygame.display.set_mode((window_width, window_height), pygame.HWSURFACE| pygame.DOUBLEBUF)
    return window

def mapValue(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)

def update(tick):
    clock.tick(tick)
    pygame.display.update()

def exit():
    pygame.quit()
    sys.exit()

def getWidth():
    return window_width

def getHeight():
    return window_height

def isClosing():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False
