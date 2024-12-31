import pygame
import student_communication
import tutorial
import game_ui
import sys

pygame.init()

screenScale = [pygame.display.Info().current_w / 1920, pygame.display.Info().current_h / 1080]
fontSizes = {'large': 130, 'small': 60}
studentName = input('Enter your name')

def connect_to_network(ui):
    success, uniqueID = student_communication.first_connection(ui.networkPin, ui.studentName, ui.characterName)
    
    if success == True:
        ui.uniqueID = uniqueID

def tutorial_call(ui, accountKey, animationController, textController):
    tutorial.load_tutorial(ui, accountKey, animationController, textController)

mainSubroutines = [lambda ui: connect_to_network(ui), lambda ui, accountKey, animationController, textController: tutorial_call(ui, accountKey, animationController, textController)]

animationController = game_ui.AnimationController()
textController = game_ui.TextController()

ui = game_ui.GameUI(screenScale, fontSizes, studentName, mainSubroutines, animationController, textController)
ui.initialize_buttons()
ui.initialize_window()
ui.run()

#quit Pygame and program
pygame.quit()
sys.exit()
