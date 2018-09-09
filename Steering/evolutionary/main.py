import numpy as np
import pygame, random, math

width, height = 800, 600

debugmode = False

mutationrate = 0.1

class Vehicle():
    def __init__(self, x, y, parent_dna=None):
        self.position = np.array([x, y], dtype=np.float64)
        self.radius = 10
        self.maxspeed = 5
        self.maxforce = 0.5
        self.health = 1
        self.acceleration = np.array([0, 0], dtype=np.float64)
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)], dtype=np.float64)
        self.velocity = np.divide(self.velocity, np.linalg.norm(self.velocity))
        self.velocity = np.multiply(self.velocity, self.maxspeed)
        self.mass = 1
        self.dna = []
        if not parent_dna is None:
            for i, data in enumerate(parent_dna):
                self.dna.append(self.mutate(parent_dna[0], 0.2))
                self.dna.append(self.mutate(parent_dna[1], 0.2))
                self.dna.append(self.mutate(parent_dna[2], 10))
                self.dna.append(self.mutate(parent_dna[3], 10))
        else:
            #Food Weight
            self.dna.append(random.uniform(-3, 3))
            #Poison Weight
            self.dna.append(random.uniform(-3, 3))
            #Food Perception
            self.dna.append(random.uniform(5, 100))
            #Poison Perception
            self.dna.append(random.uniform(5, 100))

    def update(self):
        self.health -= 0.002
        self.velocity = np.add(self.velocity, self.acceleration)
        self.velocity = np.clip(self.velocity, -self.maxspeed, self.maxspeed)
        self.position = np.add(self.position, self.velocity)
        self.acceleration = np.multiply(self.acceleration, 0)

    def mutate(self, data, scalar):
        if random.random() < mutationrate:
            data += random.uniform(-scalar, scalar)
        return data

    def applyForce(self, force):
        self.acceleration = np.divide(np.add(force, self.acceleration), self.mass)

    def applyBehaviors(self, good, bad):

        steerG = self.eat(good, 0.1, self.dna[2])
        steerB = self.eat(bad, -1, self.dna[3])

        steerG = np.multiply(steerG, self.dna[0])
        steerB = np.multiply(steerB, self.dna[1])

        self.applyForce(steerG)
        self.applyForce(steerB)
        # if math.isnan(mouseX) is False and math.isnan(mouseY) is False:
        #     seekForce = self.seek(np.array([mouseX, mouseY]))
        #     self.applyForce(seekForce)
        #
        # seperateForce = self.seperate(vehicles)
        # self.applyForce(seperateForce)


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
        if debugmode is True:
            points = self.calculatePoints(debug = True)
            pygame.draw.line(window, (0, 255, 0), (int(self.position[0]), int(self.position[1])), (points[0]), 2)
            pygame.draw.line(window, (255, 0, 0), (int(self.position[0]), int(self.position[1])), (points[1]))
            pygame.draw.polygon(window, (127, 127, 127, 127), points[2:len(points)])
            pygame.draw.polygon(window, (200, 200, 200), points[2:len(points)], 1)
            pygame.draw.circle(window, (0, 255, 0), (int(self.position[0]), int(self.position[1])), int(self.dna[2]), 1)
            pygame.draw.circle(window, (255, 0, 0), (int(self.position[0]), int(self.position[1])), int(self.dna[3]), 1)
        else:
            pygame.draw.polygon(window, (127, 127, 127, 127), self.calculatePoints())
            pygame.draw.polygon(window, (200, 200, 200), self.calculatePoints(), 1)

    def borders(self):
        if self.position[0] < -self.radius:
            self.position[0] = width + self.radius
        if self.position[1] < -self.radius:
            self.position[1] = height + self.radius
        if self.position[0] > width + self.radius:
            self.position[0] = -self.radius
        if self.position[1] > height + self.radius:
            self.position[1] = -self.radius

    def clone(self):
        if random.random() < 0.001:
            return Vehicle(self.position[0], self.position[1], self.dna)
        else:
            return None

    def boundaries(self):
        d = 10
        desired = np.array([np.nan])

        if self.position[0] < d:
            desired = np.array([self.maxspeed, self.velocity[1]])
        elif self.position[0] > width - d:
            desired = np.array([-self.maxspeed, self.velocity[1]])
        if self.position[1] < d:
            desired = np.array([self.velocity[0], self.maxspeed])
        elif self.position[1] > height - d:
            desired = np.array([self.velocity[0], -self.maxspeed])

        if np.isnan(desired)[0] == False:
            desired = np.divide(desired, np.linalg.norm(desired))
            desired = np.multiply(desired, self.maxspeed)
            steer = np.subtract(desired, self.velocity)
            steer = np.clip(steer, -self.maxforce, self.maxforce)
            self.applyForce(steer)



    def eat(self, list, nutrition, perception):
        record = math.inf
        closestIndex = None
        for i in range(len(list)-1, -1, -1):
            d = np.linalg.norm(self.position - list[i])
            if d < self.maxspeed:
                list.pop(i)
                self.health += nutrition
            else:
                if d < record and d < perception:
                    record = d
                    closestIndex = list[i]
        if not closestIndex is None:
            return self.seek(closestIndex)
        return np.array([0, 0])

    def dead(self):
        return (self.health < 0)

    def rotate_around_middle(self, xy, radians):
        x, y = xy
        offset_x = self.position[0]
        offset_y = self.position[1]
        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = math.cos(radians)
        sin_rad = math.sin(radians)
        qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
        return qx, qy


    def calculatePoints(self, debug=False):
        def get_radians(v1, v2):
            # v1 and v2 cannot be zero vectors
            v1_u = np.divide(v1, np.linalg.norm(v1))
            v2_u = np.divide(v2, np.linalg.norm(v2))
            return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

        a = self.radius / 2
        points = []
        null_vector = np.array([0, -1])
        radians = get_radians(null_vector, self.velocity)
        if self.velocity[0] > 0:
            radians *= -1

        if debug == True:
            x = self.position[0]
            y = self.position[1] - self.dna[0] * 25
            points.append(self.rotate_around_middle((x, y), radians))

            x = self.position[0]
            y = self.position[1] - self.dna[1] * 25
            points.append(self.rotate_around_middle((x, y), radians))

        x = self.position[0] - a
        y = self.position[1] + a
        points.append(self.rotate_around_middle((x, y), radians))

        x = self.position[0]
        y = self.position[1] - self.radius
        points.append(self.rotate_around_middle((x, y), radians))

        x = self.position[0] + a
        y = self.position[1] + a
        points.append(self.rotate_around_middle((x, y), radians))

        return points

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Steering')

window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
alpha_window = pygame.Surface((width, height), pygame.SRCALPHA)

running = True

frames = 0

vehicles = []
food = []
poison = []

for _ in range(10):
    food.append(np.array([random.randint(0, width), random.randint(0, height)]))

for _ in range(5):
    poison.append(np.array([random.randint(0, width), random.randint(0, height)]))

for _ in range(10):
    vehicles.append(Vehicle(int(width / 2), int(height / 2)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print('Closed with Errorcode: 0')
        if event.type == pygame.MOUSEBUTTONDOWN:
            vehicles.append(Vehicle(int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1])))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                debugmode = not debugmode
                print('DEBUGMODE:', debugmode)




    # The fun part

    window.fill((51, 51, 51))
    alpha_window.fill((51, 51, 51, 0))

    if random.random() < 0.1:
        food.append(np.array([random.randint(0, width), random.randint(0, height)]))
    if random.random() < 0.01:
        poison.append(np.array([random.randint(0, width), random.randint(0, height)]))

    for f in food:
        pygame.draw.circle(window, (0, 255, 0), (int(f[0]), int(f[1])), 2)

    for p in poison:
        pygame.draw.circle(window, (255, 0, 0), (p[0], p[1]), 2)

    for i in range(len(vehicles) - 1, -1, -1):
        vehicles[i].applyBehaviors(food, poison)
        # vehicle.eat(food)
        # vehicle.eat(poison)
        vehicles[i].update()
        #vehicle.borders()
        vehicles[i].boundaries()
        vehicles[i].render(alpha_window)

        newVehicle = vehicles[i].clone()
        if not newVehicle is None:
            vehicles.append(newVehicle)

        if vehicles[i].dead() is True:
            food.append(np.array([vehicles[i].position[0], vehicles[i].position[1]]))
            vehicles.pop(i)



    window.blit(alpha_window, (0, 0))
    # Engine Stuff
    pygame.display.update()
    frames += 1
    clock.tick(60)
    #print(clock.get_fps())

pygame.quit()
