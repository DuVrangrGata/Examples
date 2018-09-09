import math, random, pygame
from Objekts import Rocket, mapValue, Obstacle
#import numpy as np

width, height = 400, 300

#lifespan = 200

lifespan = 1000
total = 100

highscore = 0

pygame.init()

pygame.display.set_caption('Smart Rockets')

window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

class Population:

    def __init__(self, size, lifespan, goal):
        self.rockets = []
        for _ in range (0, size):
            r = Rocket(width, height, lifespan, goal)
            self.rockets.append(r)

    def run (self, window_):
        for rocket in self.rockets:
            rocket.update()
            rocket.show(window_, pygame)

    def intersect(self, obst, pop, middle=False):
        for i in range(len(self.rockets) - 1, -1, -1):
            if self.rockets[i].intersect(obst.left, obst.top, obst.right, obst.bottom, middle):
                pop.rockets.append(self.rockets.pop(i))


def nextGeneration(oldPopulation, goal):
    newPopulation = Population(total, lifespan, goal)
    newPopulation.rockets.clear()
    calculateFitness(oldPopulation)
    for i in range(total):
        parentDNA = pickOne(oldPopulation)
        child = Rocket(width, height, lifespan, goal, dna=parentDNA)
        newPopulation.rockets.append(child)
    return newPopulation

def calculateFitness(population):
    global highscore
    summe = 0
    for i in range(0, len(population.rockets)):
        if highscore < population.rockets[i].score:
            highscore = population.rockets[i].score
            print('Highscore :' + str(highscore))
    for i in population.rockets:
        i.score *= i.score
    for i in population.rockets:
        summe += i.score
    for i in population.rockets:
        if summe is not 0:
            i.fitness = i.score / summe

def pickOne(population):
    index = 0
    r = random.random()
    while r > 0:
        r -= population.rockets[index].fitness
        index += 1
    index -= 1
    pickedOneDNA = population.rockets[index].dna
    return pickedOneDNA

obstacles = []

y = mapValue(height - 20, 0, height, height, 0)
goal = Obstacle(width / 2 - 20, y, 40, 40, (0, 255, 0))

population = Population(total, lifespan, goal)
deadPop = Population(total, lifespan, goal)
deadPop.rockets.clear()

y = mapValue(height - 150, 0, height, height, 0)
obstacles.append(Obstacle(120, y, width - 240, 20, (255, 0, 0)))
y = mapValue(5, 0, height, height, 0)
obstacles.append(Obstacle(0, y, width, 5, (255, 0, 0)))
y = mapValue(height, 0, height, height, 0)
obstacles.append(Obstacle(0, y, 5, height, (255, 0, 0)))
y = mapValue(height, 0, height, height, 0)
obstacles.append(Obstacle(width - 5, y, 5, height, (255, 0, 0)))
y = mapValue(height, 0, height, height, 0)
obstacles.append(Obstacle(0, y, width, 5, (255, 0, 0)))

#rocket = Rocket(width, height, lifespan)

isRunning = True
frames = 0

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            print('Sucessfully closed')


    window.fill((0, 0, 0))

    #rocket.update()
    #rocket.show(window, pygame)

    for obst in obstacles:
        population.intersect(obst, deadPop)
        obst.show(window, pygame)


    population.intersect(goal, deadPop, middle=True)
    goal.show(window, pygame)

    population.run(window)

    if len(population.rockets) == 0:
        population = nextGeneration(deadPop, goal)

    frames += 1
    pygame.display.update()
    clock.tick(200)
    print(clock.get_fps())


pygame.quit()
