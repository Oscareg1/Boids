import pygame
from abc import ABC, abstractmethod
import random

pygame.init()

# Global Settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
NUMBER_OF_BOIDS = 50

# Abstract class for all enteties
class Enteties(ABC):
    
    # Update position
    @abstractmethod
    def update(self):
        pass

    # Make the Boid steer towards other Boids nearby
    @abstractmethod
    def cohesion(self):
        pass

    # Make the Boid steer towards the average Heading of Boids nearby
    @abstractmethod
    def alignment(self):
        pass

    # Make the Boid steer away from other Boids nearby
    @abstractmethod
    def seperation(self):
        pass

    # Draw the object
    @abstractmethod
    def draw(self):
        pass

class Boid(Enteties):

    def __init__(self, x ,y):
        image = pygame.image.load('Boid.png')
        self.image = pygame.transform.scale(image, (42,30))

        # Setting
        self.sight_range = 60
        self.speed = 0.5

        # Start with a random position
        self.position = pygame.math.Vector2(x,y)
        self.velocity = pygame.math.Vector2(random.uniform(-1,1), random.uniform(-1,1)).normalize() * self.speed
        self.boids = []
    

    def update(self, boids):
        self.boids = boids
        
        if self.boids:
            self.cohesion()
            self.alignment()
            self.seperation()
            
        self.position += self.velocity

        if self.position.x > SCREEN_WIDTH:
            self.position.x = 1

        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 1

        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH-1

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT-1

        self.boids = []

    def cohesion(self):
        cohesion = pygame.math.Vector2(0,0)

        for b in self.boids:
            cohesion = cohesion + (b.position)

        cohesion /= len(self.boids)
        cohesion = cohesion - self.position

        # Adding cohesion force
        steeringvelocity = (pygame.math.Vector2(cohesion.x , cohesion.y).normalize() * self.speed) - self.velocity
        self.velocity =  (self.velocity + steeringvelocity * 0.01).normalize() * self.speed
        #self.velocity = self.velocity.normalize() * self.speed

    def alignment(self):
        alignment = pygame.math.Vector2(0,0)
        for b in self.boids:
            alignment = alignment + (b.velocity)

        alignment /= len(self.boids)
        alignment = alignment - self.velocity

        # Adding alignment force
        self.velocity = (self.velocity + alignment *0.01).normalize() * self.speed
        #self.velocity = self.velocity.normalize() * self.speed

    def seperation(self):
        # Calculating and applying seperation force by distance
        # The seperation force only applies if the distance to a boid is 
        # less than half the Sight Range
        for b in self.boids:
            if (self.position.distance_to(b.position) < (self.sight_range / 4)):
                seperation_force = 0.5 / self.position.distance_to(b.position) 
                seperation_vector = (self.position - b.position) 
                self.velocity = (self.velocity + seperation_vector * seperation_force) * self.speed
                #self.velocity = self.velocity.normalize() * self.speed

    def draw (self, screen):
        self.update(self.boids)
        screen.blit(self.image, (self.position.x, self.position.y))

class Hoik(Boid):
     
    def __init__(self, x ,y):
        #Inherit from Boid class
        super().__init__(x,y)
        image = pygame.image.load('Hoik.png')
        self.image = pygame.transform.scale(image, (42,30))
        self.sight_range = 100
        self.speed = 0.3

    # Since the Hoik should not avoid Boids, seperation is not needed
    def seperation(self):
        pass
    
# Controls all the boids
class Flock():

    def __init__(self):
        self.boids = [Boid(random.randrange(0, SCREEN_WIDTH), random.randrange(0,SCREEN_HEIGHT)) for _ in range(NUMBER_OF_BOIDS)]
        self.boids.append(Hoik(random.randrange(0, SCREEN_WIDTH), random.randrange(0, SCREEN_HEIGHT)))
        self.dead_boids = []

    def collision(self):
        for i in range(len(self.boids)):
            nearby_boids = []
            for j in range(len(self.boids) - 1):
                # Boid can not collide with itself
                if( i != j ):
                    if(self.boids[j].position.distance_to(self.boids[i].position)) < self.boids[i].sight_range:
                        nearby_boids.append(self.boids[j])

                if((i == len(self.boids) - 1)):
                    if(self.boids[len(self.boids)- 1].position.distance_to(self.boids[j].position) < 10):
                        if self.boids[j] in self.boids:
                            print("object is in list")
                        self.dead_boids.append(self.boids[j])
            
            if nearby_boids:
                self.boids[i].update(nearby_boids)

        if self.dead_boids:
            for d in self.dead_boids:
                self.boids.remove(d)

            self.dead_boids = []

    def update_boids(self, screen):
        self.collision()
        for i in range(len(self.boids)):
            self.boids[i].draw(screen)

running = True

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
flock = Flock()

while(running):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display.fill((0,0,0))
    flock.update_boids(display)
    pygame.display.flip()
