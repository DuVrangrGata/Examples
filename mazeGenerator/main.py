from engine import *
import random

w = 25
black = (0, 0, 0)

grid = []

stack = []

start()

window = create_window(1000, 1000)

cols, rows = int(getWidth() / w), int(getHeight() / w)

def index (i, j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return None
    
    return i + j * cols

class Cell:

    def __init__ (self, i, j, w):
        self.i = i
        self.j = j
        self.w = w
        self.walls = [True, True, True, True]
        self.visited = False

    def highlight(self, window_):
        x = self.i * self.w
        y = self.j * self.w
        pygame.draw.rect(window_, ( 0, 0, 0, 100), (x, y, self.w, self.w), 0)
        

    def show(self, window_):
        x = self.i * self.w
        y = self.j * self.w
        if self.visited:
            pygame.draw.rect(window_, (255, 0, 0, 100), (x, y, self.w, self.w), 0)

        # top
        if self.walls[0]:
            pygame.draw.line(window_, (0, 0, 0), (x, y), (x + self.w, y), 2)
        # right
        if self.walls[1]:
            pygame.draw.line(window_, (0, 0, 0), (x + self.w, y), (x + self.w, y + self.w), 2)
        # bottom
        if self.walls[2]:
            pygame.draw.line(window_, (0, 0, 0), (x + self.w, y + self.w), (x, y + self.w), 2)
        # left
        if self.walls[3]:
            pygame.draw.line(window_, (0, 0, 0), (x, y + self.w), (x, y), 2)

    def checkNeighbors(self):
        neighbors = []

        top, right, bottom, left = None, None, None, None
    
        if not index(self.i, self.j - 1) is None:
            top    = grid[index(self.i, self.j - 1)]
        if not index(self.i + 1, self.j) is None:
            right  = grid[index(self.i + 1, self.j)]       
        if not index(self.i, self.j + 1) is None:
            bottom = grid[index(self.i, self.j + 1)]           
        if not index(self.i - 1, self.j) is None:
            left   = grid[index(self.i - 1, self.j)]

        if top != None:
            if not top.visited:
                neighbors.append(top)
        if right != None:
            if not right.visited:
                neighbors.append(right)
        if bottom != None:
            if not bottom.visited:
                neighbors.append(bottom)
        if left != None:
            if not left.visited:
                neighbors.append(left)

        if len(neighbors) > 0:
            r = random.randrange(0, len(neighbors))
            return neighbors[r]
        else:
            return None

            
for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j, w)
        grid.append(cell)

current = grid[0]

def removeWalls(a, b):
    x = a.i - b.i
    if x is 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x is -1:
        a.walls[1] = False
        b.walls[3] = False
    y = a.j - b.j
    if y is 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y is -1:
        a.walls[2] = False
        b.walls[0] = False
        


isRunning = True

while isRunning:
    if isClosing():
        isRunning = False

    window.fill((255, 255, 255))

    for c in grid:
        c.show(window)

    current.visited = True
    current.highlight(window)
    nextOne = current.checkNeighbors()
    if nextOne != None:
        nextOne.visited = True

        stack.append(current)

        removeWalls(current, nextOne)
        
        current = nextOne

    elif len(stack) > 0:
        current = stack.pop()

    update(60)

exit()
