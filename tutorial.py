import database
import time

def load_tutorial(ui, accountKey):
    ui.screen = 'tutorial start'
    ui.render()
    ui.animationController.start_continuous_animation((1/120), 'campfire', 10, 5, 4688, 5076, ui)
    text = 'You wake with a flame dancing across your vision. You do not know where you are, how you got here, or how to escape. The bounds of the desert surrounding you is nearly endless, seemingly nothing for miles.'
    ui.textController.typewriter_text(ui, ui.smallFont, text, 300, 500)
    time.sleep(15)
    ui.textController.stop_all_text()
    text = 'Your memory is foggy, what is your name again?'
    