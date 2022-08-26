# Attempt to create a survivor rogue-like game like Vampire Survivors

import pygame
import os
import random
import math


# Set screen dimensions


# imports from assets
# background_rect = pygame.Rect(screen_length, screen_height, 0, 0)
background_image = pygame.image.load(os.path.join("assets","grass-86.jpg"))
enemy_image = pygame.image.load(os.path.join("assets", "enemy.png"))

# background
class background:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, image_width, image_height)
        self.x = x
        self.y = y

image_width, image_height = background_image.get_rect().size
# print(image_width)
# print(image_height)

# screen_length = 2 * image_width
# screen_height = 2 * image_height
screen_length = 300
screen_height = 300
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
    def __init__(self, health = 100, exp = 0, pickup_range = 20):
        '''Create player rectangle and set it in the center'''
        self.sizex = 10
        self.sizey = 10
        self.x = centerx
        self.y = centery
        # keep player centered
        self.rect = pygame.Rect(self.x - self.sizex // 2, self.y - self.sizey // 2, self.sizex, self.sizey) 

        '''Set player attributes'''
        self.health = health
        self.exp = exp
        self.pickup_range = pickup_range


    def move(self, direction, speed = 5):
        '''Moves enemies in a way that looks like the player is moving'''
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
        try:
            for enemy in enemies:
                if direction == "left":
                    enemy.rect.move_ip(speed, 0)
                if direction == "right":
                    enemy.rect.move_ip(-speed, 0)
                if direction == "up":
                    enemy.rect.move_ip(0, speed)
                if direction == "down":
                    enemy.rect.move_ip(0, -speed)
        except:
            pass
        try:
            for projectile in projectiles:
                if direction == "left":
                    projectile.rect.move_ip(speed, 0)
                if direction == "right":
                    projectile.rect.move_ip(-speed, 0)
                if direction == "up":
                    projectile.rect.move_ip(0, speed)
                if direction == "down":
                    projectile.rect.move_ip(0, -speed)
        except:
            pass
        try:
            for xp in experience:
                if direction == "left":
                    xp.rect.move_ip(speed, 0)
                if direction == "right":
                    xp.rect.move_ip(-speed, 0)
                if direction == "up":
                    xp.rect.move_ip(0, speed)
                if direction == "down":
                    xp.rect.move_ip(0, -speed)
        except:
            pass

# enemy class
class enemy:
    def __init__(self, damage = 1, health = 20, speed = 2, distance = random.randrange(centerx - 50, centerx)):
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
        # self.name = name
        self.damage = damage
        self.health = health
        self.speed = speed

    def move(self):
        '''Moves the enemy towards the player at any given moment'''
        if self.rect.colliderect(player):
            if player.health > 0:
                player.health += -self.damage
                print(f'Health: {player.health}')
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

def spawn_enemy():
    global number_of_enemies
    for i in range(number_of_enemies):
        enemies.append(enemy())
    number_of_enemies += 1

        
# projectile class
class projectile:
    def __init__(self, size = 5, speed = 10, damage = 10):
        '''Creates projectile on player'''
        try:
            self.x, self.y = player.rect.topleft
            self.size = size
            self.speed = speed
            self.damage = damage
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
            # projectiles.append(self)
        
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
            if self.x > self.targetx:
                self.movex = -self.movex
                self.movey = -self.movey
        except:
            if self in projectiles:
                projectiles.remove(self)
            

    def move(self):
        '''Moves projectile'''
        try:
            for enemy in enemies:
                if self.rect.colliderect(enemy):
                    # print("Removed projectile")
                    projectiles.remove(self)
                    enemy.health += -self.damage
                    # print(f'Enemy { enemy.name } took { self.damage } damage. It has { enemy.health } health left')
                    if enemy.health <= 0:
                        experience.append(exp(self.x, self.y))
                        enemies.remove(enemy)
        except:
            pass

        self.x, self.y = self.rect.center
        if self.x > screen_length or self.x < 0:
            projectiles.remove(self)
            # print("Hit edge")
        if self.y > screen_height or self.y < 0:
            projectiles.remove(self)
            # print("Hit top/bottom")
        self.rect.move_ip(self.movex, self.movey)
        
# experience
class exp:
    def __init__(self, locationx, locationy, value = 1, size = 4):
        self.rect = pygame.Rect(locationx, locationy, size, size)
        self.value = value
        self.x = locationx
        self.y = locationy
        
    def check_pickup(self):
        if self.rect.colliderect(player):
            player.exp += self.value
            print(f'You have {player.exp} exp')
            experience.remove(self)
            return True

    def pickup_range(self):
        self.x, self.y = self.rect.center
        distancex = self.x - player.x 
        distancey = self.y - player.y 
        distance = math.sqrt(distancex ** 2 + distancey ** 2)
        if distance < player.pickup_range:
            move_dist = (player.pickup_range / distance) + 1
            if move_dist > distance:
                move_dist = distance
            try:
                angle = math.atan(distancey / distancex)
            # If self.distancex is 0, then the angle is pi/2 or -pi/2
            except ZeroDivisionError:
                if distancey > 0:
                    angle = -math.pi/2
                elif distancey < 0:
                    angle = math.pi/2
            movex = int(move_dist * math.cos(angle))
            movey = int(move_dist * math.sin(angle))
            if self.x > player.x:
                movex = -movex
                movey = -movey
            self.rect.move_ip(movex, movey)
            
            self.check_pickup
        else:
            return

player = player()
enemies = []
enemies.append(enemy())
projectiles = []
experience = []


#clock
clock = pygame.time.Clock()
FPS = 60
running = True
number_of_enemies = 1
# spawn_enemy_event = pygame.event.Event(spawn_enemy())
spawn_enemy_event = pygame.USEREVENT + 1
enemy_time = pygame.time.get_ticks()
projectile_time = pygame.time.get_ticks()
spawn_rate = 5000
fire_rate = 1000
multi_shot = 2

while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    # print(pygame.time.get_ticks())
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
                
    # Spawns enemies
    if (current_time - enemy_time > spawn_rate):
        spawn_enemy()
        enemy_time = pygame.time.get_ticks()

    # Fires projectiles
    if (current_time - projectile_time > fire_rate):
        for i in range(multi_shot):
            projectiles.append(projectile())
        projectile_time = pygame.time.get_ticks()
    # print(projectiles)

    update_background()
    for list in background_array:
        for image in list:
            screen.blit(background_image, (image.x, image.y))
    pygame.draw.rect(screen, (0, 255, 0), player.rect)
    try:
        for e in enemies:
            e.move()
            # pygame.draw.rect(screen, (255, 0, 0), e)
            screen.blit(enemy_image, (e.rect.topleft))
    except:
        pass
    try:
        for p in projectiles:
            p.move()
            pygame.draw.rect(screen, (0, 0, 255), p)
    except:
        pass
    try:
        for xp in experience:
            collected = xp.check_pickup()
            if not collected:
                xp.pickup_range()
            pygame.draw.rect(screen, (0, 100, 200), xp)
    except:
        pass
    pygame.display.update()