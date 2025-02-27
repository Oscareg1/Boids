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
NUMBER_OF_BOIDS = 20
SIGHT_RANGE = 50

# Abstract class for all enteties
class Enteties(ABC):
    # Calculate the direction of the boid
    @abstractmethod
    def direction(self):
        pass
    
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
        self.position = pygame.Vector2(x,y)
        self.velocity = pygame.math.Vector2(random.uniform(-1,1), random.uniform(-1,1)).normalize() * SPEED

    def direction(self, avg_x, avg_y):
        pass

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


# Controls all the boids
class Flock():

    def __init__(self):
        self.boids = [Boid(random.randrange(0,SCREEN_WIDTH),random.randrange(0,SCREEN_HEIGHT)) for _ in range(NUMBER_OF_BOIDS)]

    def collision(self):
        for i in range(NUMBER_OF_BOIDS):
            avg_x = []
            avg_y = []
            temp_x = 0
            temp_y = 0
            for j in range(NUMBER_OF_BOIDS):
                # Boid can not collide with itself
                if( i != j ):
                    # Find all colliding boids and save their position
                    if (self.boids[i].hitbox.colliderect(self.boids[j].hitbox)):
                        if not (self.boids[j].position[0]) in avg_x:
                            avg_x.append(self.boids[j].position[0])
                        if not self.boids[j].position[1] in avg_y: 
                            avg_y.append(self.boids[j].position[1])

            # Calculate the average position of all colliding boids
            if (not len(avg_x) == 0) and (not len(avg_y) == 0):
            
                for i in range(len(avg_x)-1):
                    temp_x += avg_x[i]
                temp_x = temp_x / (len(avg_x))
        
                for i in range(len(avg_y)-1):
                    temp_y += avg_y[i]
                temp_y = temp_y / len(avg_y)
            
            # Change direction of boid to average position of all colliding boids
            #self.boids[i].direction(temp_x, temp_y)
                


    def update_boids(self, screen):
        self.collision()
        for i in range(NUMBER_OF_BOIDS):
            self.boids[i].draw(screen)

boids = [Boid(random.randrange(0,SCREEN_WIDTH),random.randrange(0,SCREEN_HEIGHT)) for _ in range(NUMBER_OF_BOIDS)]
    
running = True

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

while(running):
    display.fill((0,0,0))
    
    for b in boids:
        b.update()
        b.draw(display)
        
    pygame.display.flip()

