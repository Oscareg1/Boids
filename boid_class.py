import pygame
from abc import ABC, abstractmethod
import random
import time
import math

pygame.init()

# Global Settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SPEED = 0.5
NUMBER_OF_BOIDS = 50
SIGHT_RANGE = 10

# Abstract class for all enteties
class Enteties(ABC):
    
    # Update position
    @abstractmethod
    def update(self):
        pass

    # Draw the object
    @abstractmethod
    def draw(self):
        pass

class Boid(Enteties, pygame.sprite.Sprite):

    def __init__(self, x ,y):
        image = pygame.image.load('Boid.png')
        self.image = pygame.transform.scale(image, (42,30))
        # Start with a random position
        self.position = pygame.math.Vector2(x,y)
        self.velocity = pygame.math.Vector2(random.uniform(-1,1), random.uniform(-1,1)).normalize() * SPEED
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
        steeringvelocity = (pygame.math.Vector2(cohesion.x , cohesion.y).normalize() * SPEED) - self.velocity
        self.velocity += steeringvelocity * 0.01
        self.velocity = self.velocity.normalize() * SPEED

    def alignment(self):
        alignment = pygame.math.Vector2(0,0)
        for b in self.boids:
            alignment = alignment + (b.velocity)

        alignment /= len(self.boids)
        alignment = alignment - self.velocity

        # Adding alignment force
        self.velocity += alignment *0.01
        self.velocity = self.velocity.normalize() * SPEED

    def seperation(self):
        # Calculating and applying seperation force by distance
        # The seperation force only applies if the distance to a boid is 
        # less than half the Sight Range
        for b in self.boids:
            if (self.position.distance_to(b.position) < (SIGHT_RANGE / 1.5)):
                seperation_force = 1 / self.position.distance_to(b.position) 
                seperation_vector = (self.position - b.position) / 2
                self.velocity += seperation_vector * seperation_force
                self.velocity = self.velocity.normalize() * SPEED

    def draw (self, screen):
        self.update(self.boids)
        screen.blit(self.image, (self.position.x, self.position.y))

class Hoik(Boid):
    pass

# Controls all the boids
class Flock():

    def __init__(self):
        self.boids = [Boid(random.randrange(0, SCREEN_WIDTH), random.randrange(0,SCREEN_HEIGHT)) for _ in range(NUMBER_OF_BOIDS)]


    def collision(self):
        for i in range(NUMBER_OF_BOIDS):
            nearby_boids = []
            too_close_boids = []
            for j in range(NUMBER_OF_BOIDS):
                # Boid can not collide with itself
                if( i != j ):
                    if(self.boids[j].position.distance_to(self.boids[i].position)) < 60:
                        nearby_boids.append(self.boids[j])

                    if(self.boids[j].position.distance_to(self.boids[i].position)) < 30:
                        too_close_boids.append(self.boids[j])
            
            if nearby_boids:
                self.boids[i].update(nearby_boids)

 
    def update_boids(self, screen):
        self.collision()
        for i in range(NUMBER_OF_BOIDS):
            self.boids[i].draw(screen)

    
running = True

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
flock = Flock()

while(running):
    
    display.fill((0,0,0))
    flock.update_boids(display)
    pygame.display.flip()

