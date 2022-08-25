# Attempt to create a survivor rogue-like game like Vampire Survivors

import pygame
import os
import random
import math

# Set screen dimensions
screen_length = 300
screen_height = 300
centerx = screen_length // 2
centery = screen_height // 2
dim_field = (screen_length, screen_height)
screen = pygame.display.set_mode(dim_field)

# imports from assets
background = pygame.image.load(os.path.join("assets","Grey_full.png"))

# player class 
class player:
    def __init__(self):
        '''Create player rectangle and set it in the center'''
        self.sizex = 10
        self.sizey = 10
        # keep player centered
        self.rect = pygame.Rect((screen_length - self.sizex) // 2, (screen_height - self.sizey) // 2, self.sizex, self.sizey) 

    
# enemy class
class enemy:
    def __init__(self, distance):
        '''Creates enemy at a random'''
        self.sizex = 10
        self.sizey = 10
        self.angle = random.random() * 7
        # x distance and y distance -> diagonal/hypotenuse from center
        self.x = centerx + int(distance * math.cos(self.angle))
        self.y = centery + int(distance * math.sin(self.angle))
        self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)
        enemies.append(self)

    def move(self, speed = 10):
        self.distancex = self.x - centerx
        self.distancey = self.y - centery
        self.angle = math.arctan(self.distancey / self.distancex)
        self.rect.move_ip()
        
# projectile class

player = player()
enemies = []
e1 = enemy(random.randrange(100, 150))

#clock
clock = pygame.time.Clock()
FPS = 60
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
    
    # Quit game
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                running = False

    screen.blit(background,(0,0))
    pygame.draw.rect(screen, (255, 0, 0), player.rect)
    pygame.draw.rect(screen, (250,20,20), e1.rect)
    pygame.display.update()