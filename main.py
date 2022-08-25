# Attempt to create a survivor rogue-like game like Vampire Survivors

import pygame
import os
import random
import math

# Set screen dimensions
screen_length = 300
screen_height = 300
dim_field = (screen_length, screen_height)
screen = pygame.display.set_mode(dim_field)
(centerx, centery) = screen.get_rect().center

# imports from assets
background = pygame.image.load(os.path.join("assets","Grey_full.png"))

# player class 
class player:
    def __init__(self):
        '''Create player rectangle and set it in the center'''
        self.sizex = 10
        self.sizey = 10
        self.x = centerx
        self.y = centery
        # keep player centered
        self.rect = pygame.Rect(self.x - self.sizex // 2, self.y - self.sizey // 2, self.sizex, self.sizey) 

        '''Set player attributes'''
        self.health = 100


    def move(self, direction, speed = 5):
        '''Moves enemies in a way that looks like the player is moving'''
        for enemy in enemies:
            if direction == "left":
                enemy.rect.move_ip(speed, 0)
            elif direction == "right":
                enemy.rect.move_ip(-speed, 0)
            elif direction == "up":
                enemy.rect.move_ip(0, speed)
            elif direction == "down":
                enemy.rect.move_ip(0, -speed)
# enemy class
class enemy:
    def __init__(self, distance = random.randrange(100,150)):
        '''Creates enemy at a random point around the player'''
        self.sizex = 10
        self.sizey = 10
        self.angle = random.random() * (math.pi*2)
        # x distance and y distance -> diagonal/hypotenuse from center
        self.x = centerx + int(distance * math.cos(self.angle))
        self.y = centery + int(distance * math.sin(self.angle))
        self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)
        enemies.append(self)

    def move(self, speed = 3):
        '''Moves the enemy towards the player at any given moment'''
        if self.rect.colliderect(player):
            if player.health > 0:
                player.health += -1
                print(player.health)
            else:
                print("You are dead")
            return
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                self.rect.move_ip(5, 5)
                enemy.rect.move_ip(-5, -5)
        self.x, self.y = self.rect.center
        self.distancex = self.x - player.x 
        self.distancey = self.y - player.y 
        try:
            self.angle = math.atan(self.distancey / self.distancex)
        # If self.distancex is 0, then the angle is pi/2 or -pi/2
        except ZeroDivisionError:
            if self.distancey > 0:
                self.angle = -math.pi/2
            elif self.distancey < 0:
                self.angle = math.pi/2
        self.movex = int(speed * math.cos(self.angle))
        self.movey = int(speed * math.sin(self.angle))
        if self.x > player.x:
            self.movex = -self.movex
            self.movey = -self.movey
        self.rect.move_ip(self.movex, self.movey)

# projectile class
class projectile:
    def __init__(self, size = 5):
        self.x, self.y = player.rect.topleft
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        projectiles.append(self)

player = player()
projectiles = []
p1 = projectile()
p2 = projectile()
p3 = projectile()
enemies = []
e1 = enemy()
e2 = enemy()
e3 = enemy()
e4 = enemy()


#clock
clock = pygame.time.Clock()
FPS = 60
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_w]:
            player.move("up")
        if keys[pygame.K_a]:
            player.move("left")
        if keys[pygame.K_s]:
            player.move("down")
        if keys[pygame.K_d]:
            player.move("right")
    # Quit game
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                running = False


    screen.blit(background,(0,0))
    pygame.draw.rect(screen, (0, 255, 0), player.rect)
    for enemy in enemies:
        enemy.move()
        pygame.draw.rect(screen, (255, 0, 0), enemy)
    for projectile in projectiles:
        pygame.draw.rect(screen, (0, 0, 255), projectile)
    pygame.display.update()