import pygame, random

width, height = 1080, 920
resolution = 10
cols = int(width / resolution)
rows = int(height / resolution)

grid = [[random.randint(0, 1) for x in range(rows)] for y in range(cols)]

def countNeighbors(pos):
    summe = 0
    x, y = pos
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + i + cols) % cols
            row = (y + j + rows) % rows
            summe += grid[col][row]
    summe -= grid[x][y]
    return summe

def drawGrid(window):
    window.fill((0, 0, 0))
    for i in range(cols):
        for j in range(rows):
            x = i * resolution
            y = j * resolution
            if grid[i][j] == 1:
                pygame.draw.rect(window, (255, 255, 255), (x, y, resolution, resolution))

def nextGrid():
    next = [[0 for x in range(rows)] for y in range(cols)]
    for i in range(cols):
        for j in range(rows):
            state = grid[i][j]
            neighbors = countNeighbors((i, j))
            if state == 0 and neighbors == 3:
                next[i][j] = 1
            elif state == 1 and (neighbors < 2 or neighbors > 3):
                next[i][j] = 0
            else:
                next[i][j] = state
    return next


pygame.init()

pygame.display.set_caption('Game of Life')
window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

running = True




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drawGrid(window)
    next = nextGrid()
    grid = next

    pygame.display.update()
    clock.tick(60)

pygame.quit()
