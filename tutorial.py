import time
import database
import pygame
pygame.init

def load_tutorial(ui, accountKey):
    ui.screen = 'tutorial start'
    ui.render()
    ui.animationController.start_continuous_animation((1/120), 'campfire', 10, 5, 4688, 5076, ui)
    ui.animationController.start_continuous_animation((1/120), 'campfire character', 1, 1, 4781, 4879, ui)
    #start the tutorial animations, the player and the campfire

    text = 'You wake with a flame dancing across your vision. You do not know where you are, how you got here, or how to escape. The boundless desert surrounding you appears endless, seemingly nothing for miles in every direction.'
    ui.textController.typewriter_text(ui, ui.smallFont, text, 870, 500)
    time.sleep(15)
    #animate the above text onto the screen

    ui.textController.stop_all_text()
    ui.render()

    text = 'Your memory is foggy, what is your name again?'

    ui.textController.typewriter_text(ui, ui.smallFont, text, 870, 500)
    #remove the screen

    while ui.character[0].name == 'Unknown':
        for event in pygame.event.get():
            ui.handle_key_press_event(event)
            ui.render() 
            time.sleep(0.1)
    #freeze the game until the player submits their new name

    ui.textController.stop_all_text()
    text = f'{ui.character[0].name} is a fine name. You sit up noticing a small slime approaching. You raise your fists, and get ready for a battle'
    ui.textController.typewriter_text(ui, ui.smallFont, text, 870, 500)
    time.sleep(5)

    ui.animationController.start_continuous_animation((1/120), 'campfire slime', 6, 20, 4731, 4829, ui)
    time.sleep(3)

    ui.textController.stop_all_text()
    ui.animationController.stop_all_animations()
    ui.buttons['battle'][4][2][1] = tutorial_part2

    ui.start_combat('grunt')
    #animate the text, then the slime, then remove all text and animations and start a battle

def tutorial_part2(ui):
    ui.screen = 'tutorial part2'
    ui.render()
    text = '''The sun rises as the slime splatters upon the ground. The sun illuminates the surrounding desert, far into the distance a small village is visible.
    as you approach it, you see a small shop, a dungeon and a field, filled with slimes and loot.'''

    ui.textController.typewriter_text(ui, ui.smallFont, text, 300, 1500)
    time.sleep(20)
    #animate the new text onto screen

    database.update_account_info(ui.character[0].get_exp(), 
                                 ui.character[0].get_money(),
                                ui.character[0].get_armour(), 
                                ui.character[0].get_armourModifier(), 
                                ui.character[0].get_weapon(), 
                                ui.character[0].get_weaponModifier(), 
                                ui.accountKey)
    
    database.update_characterName(ui.characterName, ui.accountKey)
    #update the database with the characters new name, and their stats

    ui.screen = 'village1'
    ui.characterPOS = [[900, 1000], 'w']
    #send the player to the start of the village