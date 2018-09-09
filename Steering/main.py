import numpy as np
import pygame, random, math

width, height = 640, 360

class Vehicle():
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=np.float64)
        self.radius = 6
        self.maxspeed = 3
        self.maxforce = 0.2
        self.acceleration = np.array([0, 0], dtype=np.float64)
        self.velocity = np.array([0, 0], dtype=np.float64)
        self.mass = 1

    def update(self):
        self.velocity = np.add(self.velocity, self.acceleration)
        self.velocity = np.clip(self.velocity, -self.maxspeed, self.maxspeed)
        self.position = np.add(self.position, self.velocity)
        self.acceleration = np.multiply(self.acceleration, 0)

    def applyForce(self, force):
        self.acceleration = np.divide(np.add(force, self.acceleration), self.mass)

    def applyBehaviors(self, vehicles, mouseX, mouseY):

        if math.isnan(mouseX) is False and math.isnan(mouseY) is False:
            seekForce = self.seek(np.array([mouseX, mouseY]))
            self.applyForce(seekForce)

        seperateForce = self.seperate(vehicles)
        self.applyForce(seperateForce)


    def seperate(self, vehicles):
        desiredSeperation = 50
        sum = np.array([0])
        count = 0
        for vehicle in vehicles:
            d = np.linalg.norm(self.position - vehicle.position)

            if d > 0 and d < desiredSeperation:
                diff = np.subtract(self.position, vehicle.position)
                diff = np.divide(diff, np.linalg.norm(diff))
                diff = np.divide(diff, d)
                sum = np.add(sum, diff)
                count += 1

        if count > 0:
            sum = np.divide(sum, count)
            sum = np.divide(sum, np.linalg.norm(sum))
            sum = np.multiply(sum, self.maxspeed)
            sum = np.subtract(sum, self.velocity)
            sum = np.clip(sum, -self.maxforce, self.maxforce)
        return sum


    def seek(self, target):
        desired = np.subtract(target, self.position)
        desired = np.divide(desired, np.linalg.norm(desired))
        desired = np.multiply(desired, self.maxspeed)

        steer = np.subtract(desired, self.velocity)
        steer = np.clip(steer, -self.maxforce, self.maxforce)
        return steer

    def render(self, window):
        pygame.draw.circle(window, (127, 127, 127), (int(self.position[0]), int(self.position[1])), self.radius)

    def borders(self):
        if self.position[0] < -self.radius:
            self.position[0] = width + self.radius
        if self.position[1] < -self.radius:
            self.position[1] = height + self.radius
        if self.position[0] > width + self.radius:
            self.position[0] = -self.radius
        if self.position[1] > height + self.radius:
            self.position[1] = -self.radius

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Steering')

window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)

running = True

frames = 0

vehicles = []
#food = []

#for _ in range(10):
#    food.append(np.array([random.randint(0, width), random.randint(0, height)]))

for _ in range(50):
    vehicles.append(Vehicle(random.randint(0, width), random.randint(0, height)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print('Closed with Errorcode: 0')



    # The fun part

    window.fill((51, 51, 51))

    #for f in food:
    #    pygame.draw.circle(window, (0, 255, 0), (f[0], f[1]), 4)

    for vehicle in vehicles:
        vehicle.applyBehaviors(vehicles, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        vehicle.update()
        vehicle.borders()
        vehicle.render(window)

    # Engine Stuff
    pygame.display.update()
    frames += 1
    clock.tick(60)
    #print(clock.get_fps())

pygame.quit()
