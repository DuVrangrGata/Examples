from engine import *
import random, math
from NeuralNetwork import *
from objects import *

start()

window = create_window(600, 400)

def getHeight():
    return 400

def getWidth():
    return 600

def loadChampion(path):
    loadedbrain = NeuralNetwork(1, 1, 1)
    loadedbrain.load(path)
    champion = Bird(loadedbrain)
    return champion

def saveChampion(path, bird):
    bird.brain.save(path)

total = 100
path = "best-brain.txt"
birds = []
savedbirds = []
pipes = []
counter = 0
highest = 0
global_learning_rate = 0.1
usermode = True
onebirdmode = False
championmode = False

isRunning = True

if usermode is True:
    onebirdmode = True
    championmode = False

if championmode is True:
    usermode = False
    onebirdmode = True
    champion = loadChampion(path)
    birds.append(champion)

    
if onebirdmode is True:
    cycles = 1
    total = 1

if championmode is False:
    for i in range(0, total):
        birds.append(Bird())
            

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and usermode is True:
                birds[0].up()

            if event.key == pygame.K_RETURN and usermode is False:
                print('saved')
                saveChampion('brain.txt', birds[0])

            if event.key == pygame.K_l and usermode is False:
                global_learning_rate *= 0.9
                print('new learning_rate: ' + str(global_learning_rate))

            if event.key == pygame.K_r and usermode is False:
                global_learning_rate = 0.1
                print('new learning_rate: ' + str(global_learning_rate))
            

            
    if counter % 75 is 0:
        pipes.append(Pipe())
    
    counter += 1

    for i in range(len(pipes) - 1, -1, -1):
        pipes[i].update()

        for j in range(len(birds) - 1, -1, -1):
            if pipes[i].hits(birds[j]):
                if onebirdmode is True:
                    print('Score: ' + str(birds[j].score))
                savedbirds.append(birds.pop(j))
                
            if pipes[i].offscreen() is True:
                pipes.pop(i)

    for i in birds:
        if usermode is False:
            i.think(pipes)
        i.update()

    
    for i in range(len(birds) - 1, -1, -1):
        if birds[i].offScreen is True:
            if onebirdmode is True:
                print('Score: ' + str(birds[j].score))
            savedbirds.append(birds.pop(j))
                

    if len(birds) is 0:
        if onebirdmode is False:
            counter = 0
            nextGeneration()
            pipes.clear()
        else:
            birds.append(savedbirds[0].copy())
            counter = 0
            pipes.clear()
            savedbirds.clear()
            
    window.fill((0, 0, 0))
    for i in birds:
        i.show(window)
    for i in pipes:
        i.show(window)


    update(60)

exit()
