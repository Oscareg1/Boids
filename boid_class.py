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
NUMBER_OF_BOIDS = 10
SIGHT_RANGE = 60

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

    def update(self):
        self.position += self.velocity
        self.hitbox = pygame.Rect(self.position[0] - 30, self.position[1] - 36, SIGHT_RANGE/2, SIGHT_RANGE/2)

        if self.position.x > SCREEN_WIDTH:
            self.position.x = 1

        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 1

        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH-1

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT-1

    def draw (self, screen):
        self.update()
        screen.blit(self.image, (self.position.x, self.position.y))

# Hoiks should have same characteristics as Boids.
# The changes should be:
# 1. The hoiks should not have a seperation force, however it should apply
# a stronger seperation force to the boids.
# 2. The hoiks should also have a slightly greater speed than the Boids so
# that it is able to 'catch' up to the Boids.
# 3. Upon colliding with a Boid, the Boid should be removed, and it
# should grant the Hoik with some "buff".
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
                    if(self.boids[j].position.distance_to(self.boids[i].position)) < SIGHT_RANGE:
                        nearby_boids.append(self.boids[j])

                    #if(self.boids[j].position.distance_to(self.boids[i].position)) < 30:
                    #    too_close_boids.append(self.boids[j])

            if nearby_boids:
                cohesion = pygame.math.Vector2(0,0)
                alignment = pygame.math.Vector2(0,0)
                for b in nearby_boids:
                    cohesion = cohesion + (b.position)
                    alignment = alignment + (b.velocity)

                    # Calculating and applying seperation force by distance
                    # The seperation force only applies if the distance to a boid is 
                    # less than half the Sight Range
                    if (self.boids[i].position.distance_to(b.position) < (SIGHT_RANGE / 1.5)):
                        seperation_force = 0.5 / self.boids[i].position.distance_to(b.position) 
                        seperation_vector = (self.boids[i].position - b.position) / 2
                        self.boids[i].velocity += seperation_vector * seperation_force
                        self.boids[i].velocity = self.boids[i].velocity.normalize() * SPEED


                cohesion /= len(nearby_boids)
                cohesion = cohesion - self.boids[i].position

                alignment /= len(nearby_boids)
                alignment = alignment - self.boids[i].velocity

                # Adding cohesion force
                steeringvelocity = (pygame.math.Vector2(cohesion.x , cohesion.y).normalize() * SPEED) - self.boids[i].velocity
                self.boids[i].velocity += steeringvelocity * 0.005
                self.boids[i].velocity = self.boids[i].velocity.normalize() * SPEED

                # Adding alignment force
                self.boids[i].velocity += alignment *0.01
                self.boids[i].velocity = self.boids[i].velocity.normalize() * SPEED

            '''
            if too_close_boids:

                seperation = pygame.math.Vector2(0,0)

                for b in too_close_boids:
                    seperation = seperation + (b.position)

                seperation /= len(too_close_boids)

                seperation = self.boids[i].position - seperation

                # Adding seperation force
                seperationvelocity = (pygame.math.Vector2(seperation.x, seperation.y).normalize() * SPEED) - self.boids[i].velocity
                self.boids[i].velocity += seperationvelocity * 0.05
                self.boids[i].velocity = self.boids[i].velocity.normalize() * SPEED
            '''

                
                


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

