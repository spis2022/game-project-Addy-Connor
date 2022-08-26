# Attempt to create a survivor rogue-like game like Vampire Survivors

import pygame
import os
import random
import math


# Set screen dimensions


# imports from assets
# background_rect = pygame.Rect(screen_length, screen_height, 0, 0)
background_image = pygame.image.load(os.path.join("assets","grass-86.jpg"))

# background
class background:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, image_width, image_height)
        self.x = x
        self.y = y

image_width, image_height = background_image.get_rect().size
print(image_width)
print(image_height)

screen_length = 2 * image_width
screen_height = 2 * image_height
dim_field = (screen_length, screen_height)
screen = pygame.display.set_mode(dim_field)
(centerx, centery) = screen.get_rect().center

# top third
bg1 = background(-image_width, -image_height)
bg2 = background(0, -image_height)
bg3 = background(image_width, -image_height)
# middle third
bg4 = background(-image_width, 0)
bg5 = background(0, 0)
bg6 = background(image_width, 0)
# bottom third
bg7 = background(-image_width, image_height)
bg8 = background(0, image_height)
bg9 = background(image_width, image_height)

background_array = [[bg1, bg2, bg3],
                   [bg4, bg5, bg6],
                   [bg7, bg8, bg9]]

def update_background():
    
    # for row in background_array:
    #     for col in row:
    #         print(f'{col.rect.topleft}\t', end='')
    #     print()
    # print('-------------------')
    
    # Checks right edge
    if background_array[0][2].rect.right < screen_length:
        for i, list in enumerate(background_array):
            list[0].x += image_width * len(list)
            list[0].rect.move_ip(image_width * len(list), 0)
            list.append(list.pop(0))
                
    # Checks left edge
    if background_array[0][0].rect.left > 0:
        for i, list in enumerate(background_array):
            list[2].x += -image_width * len(list)
            list[2].rect.move_ip(-image_width * len(list), 0)
            list.insert(0, list.pop(2))
            
    # Checks top edge
    if background_array[0][0].rect.top > 0:
        # for list in background_array:
        background_array.insert(0, background_array.pop(2))
        for image in background_array[0]:
            image.y += -image_height * len(background_array)
            image.rect.move_ip(0, -image_height * len(background_array))
            
    # Checks bottom edge
    if background_array[2][0].rect.bottom < screen_height:
        # for list in background_array:
        background_array.append(background_array.pop(0))
        for image in background_array[2]:
            image.y += image_height * len(background_array)
            image.rect.move_ip(0, image_height * len(background_array))
                
                


# player class 
class player:
    def __init__(self, health = 100):
        '''Create player rectangle and set it in the center'''
        self.sizex = 10
        self.sizey = 10
        self.x = centerx
        self.y = centery
        # keep player centered
        self.rect = pygame.Rect(self.x - self.sizex // 2, self.y - self.sizey // 2, self.sizex, self.sizey) 

        '''Set player attributes'''
        self.health = health


    def move(self, direction, speed = 10):
        '''Moves enemies in a way that looks like the player is moving'''
        for enemy in enemies:
            if direction == "left":
                enemy.rect.move_ip(speed, 0)
            if direction == "right":
                enemy.rect.move_ip(-speed, 0)
            if direction == "up":
                enemy.rect.move_ip(0, speed)
            if direction == "down":
                enemy.rect.move_ip(0, -speed)
        # for projectile in projectiles:
        #     if direction == "left":
        #         projectile.rect.move_ip(speed, 0)
        #     if direction == "right":
        #         projectile.rect.move_ip(-speed, 0)
        #     if direction == "up":
        #         projectile.rect.move_ip(0, speed)
        #     if direction == "down":
        #         projectile.rect.move_ip(0, -speed)
        for list in background_array:
            for image in list:
                if direction == "left":
                    image.rect.move_ip(speed, 0)
                    image.x += speed
                if direction == "right":
                    image.rect.move_ip(-speed, 0)
                    image.x += -speed
                if direction == "up":
                    image.rect.move_ip(0, speed)
                    image.y += speed
                if direction == "down":
                    image.rect.move_ip(0, -speed)
                    image.y += -speed

# enemy class
class enemy:
    # def __init__(self):
    #     possible_enemies.append(self)
    
    def __init__(self, name, damage = 1, health = 100, speed = 2, distance = random.randrange(centerx - 50, centerx)):
        '''Creates enemy at a random point around the player'''
        self.sizex = 10
        self.sizey = 10
        self.angle = random.random() * (math.pi*2)
        # x distance and y distance -> diagonal/hypotenuse from center
        self.x = centerx + int(distance * math.cos(self.angle))
        self.y = centery + int(distance * math.sin(self.angle))
        self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)
        # enemies.append(self)

        '''Create enemy attributes'''
        self.name = name
        self.damage = damage
        self.health = health
        self.speed = speed

    def move(self):
        '''Moves the enemy towards the player at any given moment'''
        if self.rect.colliderect(player):
            if player.health > 0:
                player.health += -self.damage
                print(player.health)
                if player.health <= 0:
                    print("You are Dead")
                    global running
                    running = False

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
        self.movex = int(self.speed * math.cos(self.angle))
        self.movey = int(self.speed * math.sin(self.angle))
        if self.x > player.x:
            self.movex = -self.movex
            self.movey = -self.movey
        self.rect.move_ip(self.movex, self.movey)

# projectile class
class projectile:
    def __init__(self, size = 5, speed = 2, damage = 10):
        '''Creates projectile on player'''
        self.x, self.y = player.rect.topleft
        self.size = size
        self.speed = speed
        self.damage = damage
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        projectiles.append(self)
        try:
            self.targetx, self.targety = random.choice(enemies).rect.center

            '''Calculate angle to move'''
            self.x, self.y = self.rect.center
            self.distancex = self.x - self.targetx 
            self.distancey = self.y - self.targety 
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
        except:
            print("You win")
            global running
            running = False
            

    def move(self):
        '''Moves projectile'''
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                print("Removed projectile")
                self.__init__()
                enemy.health += -self.damage
                print(f'Enemy { enemy.name } took { self.damage } damage. It has { enemy.health } health left')
                if enemy.health <= 0:
                    print(f'Enemy { enemy.name } has died')
                    enemies.remove(enemy)

        self.x, self.y = self.rect.center
        if self.x > screen_length or self.x < 0:
            self.__init__()
            # print("Hit edge")
        if self.y > screen_height or self.y < 0:
            self.__init__()
            # print("Hit top/bottom")
        self.rect.move_ip(self.movex, self.movey)
        
# experience

player = player()
# possible_enemies = []
enemies = []
# e1 = enemy(1)
# e2 = enemy(2)
# e3 = enemy(3)
# e4 = enemy(4)
enemies.append(enemy(1))
print(enemies)
# # for enemy in enemies:
# #     enemy.generate()
# possible_projectiles = []
# projectiles = []
# p1 = projectile()
# p2 = projectile()
# p3 = projectile()



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
                
    update_background()
    
    # print(background_array)
    for list in background_array:
        for image in list:
            screen.blit(background_image, (image.x, image.y))
    pygame.draw.rect(screen, (0, 255, 0), player.rect)
    for enemy in enemies:
        enemy.move()
        pygame.draw.rect(screen, (255, 0, 0), enemy)
    # for projectile in projectiles:
    #     projectile.move()
    #     pygame.draw.rect(screen, (0, 0, 255), projectile)
    pygame.display.update()