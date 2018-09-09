from objects import *

highest = 0
global_learning_rate = 0.1

def nextGeneration(objects, total, global_learning_rate_):

    global_learning_rate = global_learning_rate_

    newobjects = []

    calculateFitness(objects)
    
    for i in range(0, total):
        vater = pickOne(objects)
        mutter = pickOne(objects)
        childsbrain = vater.brain.crossover(mutter.brain)
        child = Bird(childsbrain)
        child.mutate()
        newobjects.append(child)

    objects.clear()

    return newobjects

def calculateFitness(objects):
    summe = 0
    index = 0
    global highest
    
    for i in range(0, len(objects)):
        if highest < objects[i].score:
            highest = objects[i].score
            print('Highscore :' + str(highest))
            index = i
            
    saveChampion('best-brain.txt', objects[index])

    for i in objects:
        i.score *= i.score
            
    for i in objects:
        summe += i.score

    for i in objects:
        if summe is not 0:
            i.fitness = i.score / summe

def pickOne(b):
    global global_learning_rate
    index = 0
    r = random.random()

    while r > 0:
        #print('Index: ' + str(index))
        #print('Laenge b: ' + str(len(b)))
        #print('r: ' + str(r))
        r -= b[index].fitness
        index += 1
    index -= 1
    
    pickedOne = b[index].copy()
    pickedOne.brain.setLearning_rate(global_learning_rate)
    return pickedOne


def saveChampion(path, obj):
    obj.brain.save(path)

