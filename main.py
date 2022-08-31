# Attempt to create a survivor rogue-like game like Vampire Survivors

import pygame
import os
import random
import math
pygame.init()



'''Imports from assets'''

background_image = pygame.image.load(os.path.join("assets","test_bg.png"))
enemy_image = pygame.image.load(os.path.join("assets", "enemy40x40.png"))
player_image_left = pygame.image.load(os.path.join("assets", "wizard-left.png"))
player_image_right = pygame.image.load(os.path.join("assets", "wizard-right.png"))

'''Background'''
class background:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, image_width, image_height)
        self.x = x
        self.y = y

image_width, image_height = background_image.get_rect().size

# Set screen dimensions

# screen_length = 2 * image_width
# screen_height = 2 * image_height
screen_length = 1280
screen_height = 720
dim_field = (screen_length, screen_height)
screen = pygame.display.set_mode(dim_field)
(centerx, centery) = screen.get_rect().center

# Makes transparent background surface
background_rect = pygame.Rect(0, 0, screen_length, screen_height)
trans_surface = pygame.Surface((screen_length, screen_height), pygame.SRCALPHA)
pygame.draw.rect(trans_surface, (255, 255, 255, 0), background_rect)

# Creates background array for infinite mapping
num_of_background_columns = math.ceil(screen_length / image_width) + 1
num_of_background_rows = math.ceil(screen_height / image_height) + 1

background_array = []

# Creating background array but blank
for row in range(num_of_background_rows):
    background_array.append([])
    for column in range(num_of_background_columns):
        background_array[row].append("")

# Filling background array with background values
for row in range(num_of_background_rows):
    for column in range(num_of_background_columns):
        background_array[row][column] = background(image_width * (column), image_height * (row))

last_row = num_of_background_rows - 1
last_column = num_of_background_columns - 1


def update_background():
    
    # for row in background_array:
    #     for col in row:
    #         print(f'{col.rect.topleft}\t', end='')
    #     print()
    # print('-------------------')
    
    # Checks right edge
    if background_array[0][last_column].rect.right < screen_length:
        for i, list in enumerate(background_array):
            list[0].x += image_width * len(list)
            list[0].rect.move_ip(image_width * len(list), 0)
            list.append(list.pop(0))
                
    # Checks left edge
    if background_array[0][0].rect.left > 0:
        for i, list in enumerate(background_array):
            list[last_column].x += -image_width * len(list)
            list[last_column].rect.move_ip(-image_width * len(list), 0)
            list.insert(0, list.pop(last_column))
            
    # Checks top edge
    if background_array[0][0].rect.top > 0:
        # for list in background_array:
        background_array.insert(0, background_array.pop(last_row))
        for image in background_array[0]:
            image.y += -image_height * len(background_array)
            image.rect.move_ip(0, -image_height * len(background_array))
            
    # Checks bottom edge
    if background_array[last_row][0].rect.bottom < screen_height:
        # for list in background_array:
        background_array.append(background_array.pop(0))
        for image in background_array[last_row]:
            image.y += image_height * len(background_array)
            image.rect.move_ip(0, image_height * len(background_array))

def draw_background():
    for list in background_array:
        for image in list:
            screen.blit(background_image, (image.x, image.y))
    
                
'''Timer'''                
def make_time():
    global minutes
    global seconds
    if seconds == 60:
        seconds = 0
        minutes += 1
    seconds_str = str(seconds)
    minutes_str = str(minutes)
    if len(seconds_str) == 1:
        seconds_str = "0" + seconds_str
    if len(minutes_str) == 1:
        minutes_str = "0" + minutes_str
    return minutes_str + ":" + seconds_str

def draw_time():
    text = font.render(game_time, True, green, blue)
    textRectangle = text.get_rect()
    textRectangle.center = (centerx, 9)
    screen.blit(text, textRectangle)

'''Player''' 
class player:
    def __init__(self, health = 100, exp = 0, pickup_range = 20):
        '''Create player rectangle and set it in the center'''
        self.sizex = 40
        self.sizey = 40
        self.x = centerx
        self.y = centery
        # keep player centered
        self.rect = pygame.Rect(0, 0, self.sizex, self.sizey) 
        self.rect.center = (centerx, centery)

        '''Set player attributes'''
        self.health = health
        self.max_health = health
        self.exp = exp
        self.pickup_range = pickup_range
        self.level = 0
        self.exp_to_level = 10
        self.level_up_rate = 1.1
        self.dash_cd = 3000
        self.dash_previous_time = pygame.time.get_ticks()
        self.direction = "right"


        '''Health Bar'''       
        self.health_bar_sizex = self.sizex * 2
        self.health_bar_sizey = 3
        self.health_bar_x = centerx - (self.health_bar_sizex // 2)
        self.health_bar_y = centery - 12
        self.red_health_bar = pygame.Rect(self.health_bar_x, self.health_bar_y, self.health_bar_sizex, self.health_bar_sizey)
        self.green_health_bar = pygame.Rect(self.health_bar_x, self.health_bar_y, self.health_bar_sizex, self.health_bar_sizey)

        '''EXP Bar'''       
        self.exp_sizex = screen_length
        self.exp_sizey = 8
        self.exp_x = 0
        self.exp_y = 0
        self.empty_exp = pygame.Rect(self.exp_x, self.exp_y, self.exp_sizex, self.exp_sizey)
        self.full_exp = pygame.Rect(self.exp_x, self.exp_y, 0, self.exp_sizey)
        self.choose_upgrade = False

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

    def health_bar(self):
        health_percent = self.health / self.max_health
        self.green_health_bar = pygame.Rect(self.health_bar_x, self.health_bar_y, int(health_percent * self.health_bar_sizex), self.health_bar_sizey)

    def exp_bar(self):
        exp_percent = self.exp / self.exp_to_level
        self.full_exp = pygame.Rect(self.exp_x, self.exp_y, int(exp_percent * self.exp_sizex), self.exp_sizey)
        
    def level_up(self):
        if self.exp >= self.exp_to_level:
            self.exp = self.exp - self.exp_to_level
            self.exp_to_level = math.ceil(self.exp_to_level * self.level_up_rate)
            # print("Level up!")
            self.choose_upgrade = True
            try:
                self.upgrades = random.sample(weapons, k = 3)
            except:
                pass
            self.upgrades_surface = {}
            for i, upgrade in enumerate(self.upgrades):
                text = font.render(upgrade.name, True, (255, 255, 255), (50, 50, 50))
                text_rect = text.get_rect()
                text_rect.center = (screen_length // 3 * i + screen_length // 6, centery)
                self.upgrades_surface[upgrade] = [text, text_rect] 
    
def update_player():
    player.health_bar()
    pygame.draw.rect(screen, (255, 0, 0), player.red_health_bar)
    pygame.draw.rect(screen, (0, 200, 0), player.green_health_bar)
    player.exp_bar()
    player.level_up()
    pygame.draw.rect(screen, (100, 100, 100), player.empty_exp)
    pygame.draw.rect(screen, (0, 50, 255), player.full_exp)
    # pygame.draw.rect(screen, (0, 255, 0), player.rect)
    if previous_direction == "right":
        screen.blit(player_image_right, player.rect.topleft)
    if previous_direction == "left":
        screen.blit(player_image_left, player.rect.topleft)


'''Enemy'''
class enemy:
    def __init__(self, damage = 1, health = 20, speed = 2, distance = random.randrange(centerx - 50, centerx)):
        '''Creates enemy at a random point around the player'''
        sizex = 40
        sizey = 40
        angle = random.random() * (math.pi*2)
        # x distance and y distance -> diagonal/hypotenuse from center
        x = centerx + int(distance * math.cos(angle))
        y = centery + int(distance * math.sin(angle))
        self.rect = pygame.Rect(x, y, sizex, sizey)

        '''Set enemy attributes'''
        self.damage = damage
        self.health = health
        self.speed = speed

    def move(self):
        '''Moves the enemy towards the player at any given moment'''
        if self.rect.colliderect(player):
            if player.health > 0:
                player.health += -self.damage
                # print(f'Health: {player.health}')
                if player.health <= 0:
                    print("You are Dead")
                    print(f'You lasted { game_time }')
                    pygame.time.wait(1000)
                    global running
                    running = False

            return
        for enemy in enemies:
            if self.rect.colliderect(enemy):
                self.rect.move_ip(5, 5)
                enemy.rect.move_ip(-5, -5)
        x, y = self.rect.center
        distancex = x - player.x 
        distancey = y - player.y 
        try:
            angle = math.atan(distancey / distancex)
        # If self.distancex is 0, then the angle is pi/2 or -pi/2
        except ZeroDivisionError:
            if distancey > 0:
                angle = -math.pi/2
            elif distancey < 0:
                angle = math.pi/2
        movex = int(self.speed * math.cos(angle))
        movey = int(self.speed * math.sin(angle))
        if x > player.x:
            movex = -movex
            movey = -movey
        self.rect.move_ip(movex, movey)

    def check_health(self):
        if self.health <= 0:
            # print("Dead")
            enemies.remove(self)
            x, y = self.rect.center
            experience.append(exp(x, y, value = 10, size = 8))
            # print(experience)

    def take_damage(self, damage):
        self.health += -damage


def spawn_enemy():
    global number_of_enemies
    for i in range(number_of_enemies):
        enemies.append(enemy())
    number_of_enemies += 3

def update_enemies():
    try:
        for e in enemies:
            e.move()
            e.check_health()
            screen.blit(enemy_image, (e.rect.topleft))
    except:
        pass


'''Weapons'''
class weapon:
    def __init__(self, name, damage, level = 0):
        # my_weapons.append(self)
        self.name = name
        self.damage = damage
        self.level = level
        self.previous_time = pygame.time.get_ticks()

    def level_up(self):
        self.level += 1
        if self.level == 1:
            my_weapons.append(self)

'Weapon - Aura'
class aura(weapon):
    def __init__(self):
        super().__init__("Aura", 10)
        self.size = 40
        self.circle = pygame.draw.circle(screen, (50, 50, 50, 0.1), (centerx, centery), self.size)
        self.cd = 1000
        self.immune = {}

    def use_weapon(self):
        # screen.fill((150, 50, 50, 60), pygame.draw.circle(screen, (50, 50, 50, 0.1), (centerx, centery), self.size), pygame.SRCALPHA)
        pygame.draw.circle(trans_surface, (150, 0, 50, 25), (centerx, centery), self.size)
        # screen.blit(trans_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        # pygame.draw.circle(screen, (255, 255, 255), self.circle)
        targets_index = self.circle.collidelistall(enemies)
        targets_enemies = []
        try:
            for index in targets_index:
                targets_enemies.append(enemies[index])
        except:
            pass
        try:
            for key, value in self.immune.items():
                if current_time - value >= self.cd:
                    del self.immune[key]
        except:
            pass
        try:
            for target in targets_enemies:
                if target in self.immune:
                    pass
                else:
                    target.take_damage(self.damage)
                    self.immune[target] = current_time
        except:
            pass

    def level_up(self):
        super().level_up()
        self.size *= 1.1
        self.circle = pygame.draw.circle(screen, (50, 50, 50, 0.1), (centerx, centery), self.size)
        

'Weapon - Fireball'  
class fireball(weapon):
    def __init__(self):
        super().__init__("Fireball", 15)
        self.size = 5
        self.area = 20
        self.speed = 10
        self.cd = 500
        self.previous_time = pygame.time.get_ticks()
        self.projectiles = []

    def get_target(self):
        targetx, targety = pygame.mouse.get_pos()
        self.projectiles.append(projectile(targetx, targety, size = self.size, speed = self.speed, color = (255, 100, 0)))
    
    def explode(self):
        try:
            for f in self.projectiles:
                x, y = f.rect.center
                if x > screen_length or x < 0 or y > screen_height or y < 0:
                    self.projectiles.remove(f)
                    projectiles.remove(f)
                if f.rect.collidelistall(enemies):
                    self.projectiles.remove(f)
                    # print("Explode!")
                    projectiles.remove(f)
                    area = pygame.draw.circle(screen, (255, 100, 0), (x, y), self.area)
                    targets_index = area.collidelistall(enemies)
                    # print(targets_index)
                    try:
                        for target in targets_index:
                            enemies[target].take_damage(self.damage)
                    except:
                        pass   
        except:
            pass

    def use_weapon(self):
        self.explode()
        if current_time - self.previous_time >= self.cd:
            self.get_target()
            self.previous_time = current_time

    def level_up(self):
        super().level_up()
        self.area *= 2


'Weapon - Water Bolt'
class water_bolt(weapon):
    def __init__(self):
        super().__init__("Water Bolt", 10)
        self.bounces = 3
        self.speed = 10
        self.size = 4
        self.previous_time = pygame.time.get_ticks()
        self.cd = 3000
        self.projectiles = []

    def get_target(self):
        try:
            targetx, targety = random.choice(enemies).rect.center
            self.projectiles.append(projectile(targetx, targety, self.size, self.speed, (0, 0, 255)))
            self.projectiles[-1].bounces = 0
        except:
            pass

    def bounce(self):
        try:
            for w in self.projectiles:
                x, y = w.rect.center
                if x >= screen_length:
                    w.movex = -w.movex
                    w.bounces += 1
                    w.rect.right = screen_length
                    pass
                if x <= 0:
                    w.movex = -w.movex
                    w.bounces += 1
                    w.rect.left = 0
                    pass
                if y >= screen_height:
                    w.movey = -w.movey
                    w.bounces +=1
                    w.bottom = screen_height
                    pass
                if y <= 0:
                    w.movey = -w.movey
                    w.bounces +=1
                    w.top = 0
                    pass
                if w.bounces > self.bounces:
                    self.projectiles.remove(w)
                    projectiles.remove(w)
        except:
            pass

    def check_hit(self):
        try:
            for w in self.projectiles:
                if w.rect.collidelistall(enemies):
                    targets_index = w.rect.collidelistall(enemies)
                    targets_enemies = []
                    try:
                        for index in targets_index:
                            targets_enemies.append(enemies[index])
                    except:
                        pass
                    try:
                        for target in targets_enemies:
                            target.take_damage(self.damage)
                    except:
                        pass 
        except:
            pass

    def use_weapon(self):
        self.bounce()
        self.check_hit()
        if current_time - self.previous_time >= self.cd:
            self.get_target()
            self.previous_time = current_time

    def level_up(self):
        super().level_up()
        # self.speed *= 2
        self.bounces += 1
        self.cd *= 0.5

class chain_lightning(weapon):
    def __init__(self):
        super().__init__("Chain Lightning", 10)
        self.chains = 5
        self.speed = 20
        self.size = 5
        self.chain_radius = 100
        self.previous_time = pygame.time.get_ticks()
        self.cd = 1000
        self.projectiles = []

    def get_target(self):
        try:
            # targetx, targety = random.choice(enemies).rect.center
            targetx, targety = pygame.mouse.get_pos()
            self.projectiles.append(projectile(targetx, targety, self.size, self.speed, (255, 255, 0)))
            self.projectiles[-1].chain = 0
        except:
            pass

    def chain(self):
        try:
            for l in self.projectiles:
                x, y = l.rect.center
                if x >= screen_length or x < 0:
                    self.projectiles.remove(l)
                    projectiles.remove(l)
                    pass
                if y > screen_height or y < 0:
                    self.projectiles.remove(l)
                    projectiles.remove(l)
                    pass
                if l.rect.collidelistall(enemies):
                    target = enemies[l.rect.collidelist(enemies)]
                    target.take_damage(self.damage)
                    l.chain += 1
                    # print("Hit enemy")
                    if l.chain > self.chains:
                        print("Removed lightning")
                        self.projectiles.remove(l)
                        projectiles.remove(l)
                    else:
                        x, y = l.rect.center
                        chain_area = pygame.draw.circle(trans_surface, (255, 255, 0, 100), (x, y), self.chain_radius)
                        possible_chain = chain_area.collidelistall(enemies)
                        # possible_chain = random.randrange(len(enemies))
                        possible_chain.remove(enemies.index(target))
                        try:
                            # chain = random.choice(enemies)
                            # targetx, targety = chain.rect.center
                            chain = random.choice(possible_chain)
                            targetx, targety = enemies[chain].rect.center
                            l.target(targetx, targety)    
                            print("Chained")      
                        except:
                            print("No target")
                            self.projectiles.remove(l)
                            projectiles.remove(l)       
        except:
            pass

    def use_weapon(self):
        # print("Using Weapon")
        if current_time - self.previous_time >= self.cd:
            self.get_target()
            self.previous_time = current_time
        self.chain()
        
    def level_up(self):
        super().level_up()
        self.chains += 1

'''Projectile'''
class projectile:
    def __init__(self, targetx, targety, size = 5, speed = 10, color = (255, 255, 255)):
        '''Creates projectile on player'''
        x, y = player.rect.center
        self.size = size
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.rect.center = (x, y)
        projectiles.append(self)
        self.target(targetx, targety)

    def target(self, targetx, targety):
        '''Calculate angle to move'''
        x, y = player.rect.center
        distancex = x - targetx 
        distancey = y - targety 
        try:
            angle = math.atan(distancey / distancex)
        # If self.distancex is 0, then the angle is pi/2 or -pi/2
        except ZeroDivisionError:
            if distancey >= 0:
                angle = -math.pi/2
            elif distancey < 0:
                angle = math.pi/2
        self.movex = int(self.speed * math.cos(angle))
        self.movey = int(self.speed * math.sin(angle))
        if x > targetx:
            self.movex = -self.movex
            self.movey = -self.movey  

    def move(self):
        '''Moves projectile'''
        self.rect.move_ip(self.movex, self.movey)


weapons = [aura(), fireball(), water_bolt(), chain_lightning()]
my_weapons = []

def update_projectiles():
    try:
        for p in projectiles:
            p.move()
            pygame.draw.rect(screen, p.color, p.rect)
    except:
        pass

def use_weapons():
    for w in my_weapons:
        w.use_weapon()

        
'''Experience'''
class exp:
    def __init__(self, locationx, locationy, value = 1, size = 20):
        self.rect = pygame.Rect(locationx, locationy, size, size)
        self.value = value
        
    def check_pickup(self):
        if self.rect.colliderect(player.rect):
            player.exp += self.value
            # print(f'You have {player.exp} exp')
            experience.remove(self)
            return True

    def pickup_range(self):
        x, y = self.rect.center
        distancex = x - player.x 
        distancey = y - player.y 
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
            
        else:
            return

    def combine_exp(self):
        if self.rect.collidelistall(experience):
            target = experience[self.rect.collidelist(experience)]
            self.value += target.value
            experience.remove(target)

def update_experience():
    try:
        # print(experience)
        for xp in experience:
            xp.combine_exp()
            collected = xp.check_pickup()
            if not collected:
                xp.pickup_range()
            pygame.draw.rect(screen, (0, 100, 200), xp)
    except:
        pass

player = player()
enemies = []
enemies.append(enemy())
projectiles = []
experience = []
# upgrades = []
# upgrades_surface = {}

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
multi_shot = 5

# Pause screen + Timer
paused = False
minutes = 0
seconds = 0
previous_second = pygame.time.get_ticks()
green = (0,255,0)
blue = (0,0,255)
font = pygame.font.SysFont('timesnewroman', 16)
game_time = make_time()

weapons[3].level_up()
print(my_weapons)
# random.choice(weapons).level_up()

previous_direction = "right"

while running and paused is False:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    # print(pygame.time.get_ticks())
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_w]:
            player.move("up")
            player.direction = "up"
        if keys[pygame.K_a]:
            player.move("left")
            player.direction = "left"
            previous_direction = "left"
        if keys[pygame.K_s]:
            player.move("down")
            player.direction = "down"
        if keys[pygame.K_d]:
            player.move("right")
            player.direction = "right"
            previous_direction = "right"
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    # Quit game
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_p:
                paused = True
            if event.key == pygame.K_q:
                running = False
                pygame.quit()
            if event.key == pygame.K_LSHIFT:
                # print("Dash")
                if current_time - player.dash_previous_time >= player.dash_cd:
                    player.move(player.direction, speed = 50)
                    player.dash_previous_time = current_time
                # player.direction
                   
    # Spawns enemies
    if (current_time - enemy_time >= spawn_rate):
        spawn_enemy()
        enemy_time = pygame.time.get_ticks()

    # # Fires projectiles
    # if (current_time - projectile_time >= fire_rate):
    #     projectile_time = pygame.time.get_ticks()
    #     for i in range(multi_shot):
    #         try:
    #             projectiles.append(projectile())
    #         except:
    #             break
    # print(projectiles)

    # Updates game time
    if current_time - previous_second >= 1000:
        seconds += 1
        previous_second = pygame.time.get_ticks()
        game_time = make_time()

    
    update_background()
    draw_background()
    
    use_weapons()
    screen.blit(trans_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    update_experience()
    update_player()
    update_enemies()
    update_projectiles()
    draw_time()

    while paused is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()

    while player.choose_upgrade:
        for upgrade, [text, text_rect] in player.upgrades_surface.items():
            screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for upgrade, [text, text_rect] in player.upgrades_surface.items():
                    if text_rect.collidepoint(x, y):
                        upgrade.level_up()
                        print(f'{upgrade.name}: Level {upgrade.level}')
                        player.choose_upgrade = False
        pygame.display.update()

    pygame.display.update()