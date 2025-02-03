import database

def load_tutorial(ui, accountKey):
    ui.screen = 'tutorial start'
    ui.render()
    ui.animationController.start_continuous_animation(0.2, 'campfire', 10, 4688, 5076, ui)
    #ui.textController.