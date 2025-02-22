import random
import time
import database
import combat
import pygame
pygame.init

def dungeon(ui):
    pass

def shop(ui):
    pass

def exploration(ui):
    returnScreen = ui.screen
    ui.screen = 'exploration'
    encounter = random.randint(1, 100)
    encounterRandomness = random.randint(1, 100)
    x, y = ui.quadrant_to_coordinates(1577)
    if encounter <= 55:
        image = pygame.image.load('sprites/characters/grunt slime.png')
        ui.window.blit(ui.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * (2/3)), int(image.get_height() * (2/3))))), (x, y))
        pygame.display.flip()
        time.sleep(5)
        ui.start_combat('grunt')

    elif encounter <= 70:
        image = pygame.image.load('sprites/characters/elite slime.png')
        ui.window.blit(ui.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * (2/3)), int(image.get_height() * (2/3))))), (x, y))
        pygame.display.flip()
        time.sleep(5)
        ui.start_combat('elite')

    elif encounter <= 75:
        image = pygame.image.load('sprites/characters/boss slime.png')
        ui.window.blit(ui.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * (2/3)), int(image.get_height() * (2/3))))), (x, y))
        pygame.display.flip()
        time.sleep(5)
        ui.start_combat('boss')

    elif encounter <= 80:
        weaponType = combat.weapon[random.randint(0, 1)]
        image = pygame.image.load(f'sprites/animations/combat/{weaponType.strip()} normal.png')
        ui.window.blit(ui.scale_sprite(pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))), (x, y))
        if encounterRandomness <= 55:
            newWeapon = f'{combat.rarity[0]}{weaponType}'
            rarity = combat.rarity[0]
        elif encounterRandomness <= 75:
            newWeapon = f'{combat.rarity[1]}{weaponType}'
            rarity = combat.rarity[1]
        elif encounterRandomness <= 95:
            newWeapon = f'{combat.rarity[2]}{weaponType}'
            rarity = combat.rarity[2]
        else:
            newWeapon = f'{combat.rarity[3]}{weaponType}'
            rarity = combat.rarity[3]
        pygame.display.flip()
        time.sleep(5)
        ui.new_weapon(newWeapon, rarity)

    elif encounter <= 85:
        armourType = combat.armour[random.randint(0, 2)]
        image = pygame.image.load(f'sprites/animations/combat/{armourType.strip()} normal.png')
        ui.window.blit(ui.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * 2), int(image.get_height() * 2)))), (x, y))
        if encounterRandomness <= 55:
            newArmour = f'{combat.rarity[0]}{armourType}'
            rarity = combat.rarity[0]
        elif encounterRandomness <= 75:
            newArmour = f'{combat.rarity[1]}{armourType}'
            rarity = combat.rarity[1]
        elif encounterRandomness <= 95:
            newArmour = f'{combat.rarity[2]}{armourType}'
            rarity = combat.rarity[2]
        else:
            newArmour = f'{combat.rarity[3]}{armourType}'
            rarity = combat.rarity[3]
        pygame.display.flip()
        time.sleep(5)
        ui.new_armour(newArmour, rarity)

    else:
        amount = random.randint(1, 10)
        image = pygame.image.load(f'sprites/animations/combat/coin.png')
        ui.window.blit(ui.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * 2), int(image.get_height() * 2)))), (x, y))
        pygame.display.flip()
        time.sleep(5)
        ui.character[0].set_money(ui.character[0].get_money() + amount)
    
    database.update_account_info(ui.character[0].get_exp(), ui.character[0].get_money(), ui.character[0].get_weapon(), ui.character[0].get_weaponModifier(),
                                ui.character[0].get_armour(), ui.character[0].get_armourModifier(), ui.accountKey)
    ui.screen = returnScreen