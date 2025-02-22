import random
import pygame
pygame.init

def dungeon(ui):
    pass

def shop(ui):
    pass

def exploration(ui):
    ui.screen = 'exploration'
    encounter = random.randint(1, 100)
    if encounter <= 55:
        ui.