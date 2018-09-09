from objects import Bird, Pipe
from engine import *
from ga import *
import random, math
import tensorflow as tf

start()

window = create_window(600, 400)

#def getHeight():
#    return 400

#def getWidth():
#    return 600

def loadChampion(path):
    loadedbrain = NeuralNetwork(1, 1, 1)
    loadedbrain.load(path)
    champion = Bird(loadedbrain)
    return champion

def saveChampion(path, bird):
    bird.brain.save(path)

total = 500
path = "best-brain.txt"
birds = []
savedbirds = []
pipes = []
counter = 0
global_learning_rate = 0.1
threshhold = 5000000
usermode = False
onebirdmode = False
championmode = False
loadTraining = False
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
    loadTraining = False
    cycles = 1
    total = 1

if loadTraining is True:
    loadedBird = loadChampion('mastered-treshhold.txt')
    loadedBird.score = 4000
    savedbirds.append(loadedBird)
    birds = nextGeneration(savedbirds, total, global_learning_rate)
else:
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
        if i.score > threshhold:
            i.brain.save('mastered-treshhold.txt')
            print('theshhold is beaten')
            isRunning = False



    for i in range(len(birds) - 1, -1, -1):
        if birds[i].offScreen is True:
            if onebirdmode is True:
                print('Score: ' + str(birds[i].score))
            savedbirds.append(birds.pop(i))


    if len(birds) is 0 and championmode is False:
        counter = 0
        birds = nextGeneration(savedbirds, total, global_learning_rate)
        pipes.clear()


    window.fill((0, 0, 0))
    for i in birds:
        i.show(window)
    for i in pipes:
        i.show(window)


    update(60)

exit()
