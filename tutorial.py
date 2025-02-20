import database

def load_tutorial(ui, accountKey):
    ui.screen = 'tutorial start'
    ui.render()
    ui.animationController.start_continuous_animation((1/120), 'campfire', 10, 5, 4688, 5076, ui)
    #ui.textController.typewriter_text(ui, ui.font, )