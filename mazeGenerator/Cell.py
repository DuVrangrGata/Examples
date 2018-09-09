from engine import *

black = (0, 0, 0)

class Cell:

    def __init__ (self, i, j, w):
        self.i = i
        self.j = j
        self.w = w
        self.walls = [True, True, True, True]
        self.visited = False

    def show(self, window_):
        x = self.i * self.w
        y = self.j * self.w
        if self.visited:
            pygame.draw.rect(window_, (255, 0, 255, 100), (x, y, self.w, self.w), 0)

        # top
        if self.walls[0]:
            pygame.draw.line(window_, 255, (x, y), (x + self.w, y), 1)
        # right
        if self.walls[1]:
            pygame.draw.line(window_, 255, (x + self.w, y), (x + self.w, y + self.w), 1)
        # bottom
        if self.walls[2]:
            pygame.draw.line(window_, 255, (x + self.w, y + self.w), (x, y + self.w), 1)
        # left
        if self.walls[3]:
            pygame.draw.line(window_, 255, (x, y + self.w), (x, y), 1)

    def checkNeighbors(self, cols_, rows_, grid):
        neighbors = []
        index = self.i + self.j * cols_
        right = grid[self.i]
