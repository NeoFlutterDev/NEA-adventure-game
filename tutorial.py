import database
import time
import pygame
pygame.init

def load_tutorial(ui, accountKey):
    ui.screen = 'tutorial start'
    ui.render()
    ui.animationController.start_continuous_animation((1/120), 'campfire', 10, 5, 4688, 5076, ui)
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
    print('done')