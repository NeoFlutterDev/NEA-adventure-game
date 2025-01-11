import database

def load_tutorial(ui, accountKey, animationController, textController):
    ui.screen = 'tutorial start'
    ui.render()
    animationController.start_continuous_animation(0.2, 'campfire', 10, 4688, 5076, ui)