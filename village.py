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
        pass
        #normal slime
    elif encounter <= 70:
        pass    
        #elite slime
    elif encounter <= 75:
        pass
        #boss slime
    elif encounter <= 80:
        pass
        #free weapon
    elif encounter <= 85:
        pass
        #free armour
    else:
        pass
        #free gold
