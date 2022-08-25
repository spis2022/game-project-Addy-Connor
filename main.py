# Attempt to create a survivor rouge-like game like Vampire Survivors

import pygame
import os

# Set screen dimensions
screen_length = 600
screen_height = 600
dim_field = (screen_length, screen_height)
screen = pygame.display.set_mode(dim_field)

# imports from assets
background = pygame.image.load(os.path.join("assets","Grey_full.png"))

# player class 
class player:
    def __init__(self):
        # self.name = name
        self.rect = pygame.Rect(295, 295, 10, 10)

# enemy class

# projectile class

player = player()

running = True
while running:
    for event in pygame.event.get():
    
    # Quit game
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                running = False

    screen.blit(background,(0,0))
    pygame.draw.rect(screen, (255, 0, 0), player.rect)
    pygame.display.update()