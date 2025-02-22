import database
import time
import pygame
pygame.init

def load_tutorial(ui, accountKey):
    ui.screen = 'tutorial start'
    ui.render()
    ui.animationController.start_continuous_animation((1/120), 'campfire', 10, 5, 4688, 5076, ui)
    ui.animationController.start_continuous_animation((1/120), 'campfire character', 1, 1, 4781, 4879, ui)

    text = 'You wake with a flame dancing across your vision. You do not know where you are, how you got here, or how to escape. The bounds of the desert surrounding you is nearly endless, seemingly nothing for miles.'
    ui.textController.typewriter_text(ui, ui.smallFont, text, 870, 500)
    time.sleep(15)

    ui.textController.stop_all_text()
    ui.render()
    text = 'Your memory is foggy, what is your name again?'
    ui.textController.typewriter_text(ui, ui.smallFont, text, 870, 500)

    while ui.character[0].name == 'Unknown':
        for event in pygame.event.get():
            ui.handle_key_press_event(event)
            ui.render() 
            time.sleep(0.1)

    ui.textController.stop_all_text()
    text = f'{ui.character[0].name} is a fine name. You sit up noticing a small slime approaching. You raise your fists, and get ready for a battle'
    ui.textController.typewriter_text(ui, ui.smallFont, text, 870, 500)
    time.sleep(5)
    ui.animationController.start_continuous_animation((1/120), 'campfire slime', 6, 20, 4731, 4829, ui)
    time.sleep(3)
    ui.textController.stop_all_text()
    ui.animationController.stop_all_animations()
    print("Before setting:", ui.buttons['battle'][4][2][1])
    ui.buttons['battle'][4][2][1] = tutorial_part2
    print("After setting:", ui.buttons['battle'][4][2][1])
    ui.start_combat('grunt')

def tutorial_part2(ui):
    print('this loaded!!')
    ui.screen = 'tutorial part2'
    ui.render()