import pygame
import student_communication
import tutorial
import game_ui
import sys

pygame.init()

screenScale = [pygame.display.Info().current_w / 1920, pygame.display.Info().current_h / 1080]
fontSizes = {'large': 130, 'small': 60, 'stats':100}
studentName = input('Enter your name: ')

def connect_to_network(ui):
    success, uniqueID = student_communication.first_connection(ui.networkPin, ui.studentName, ui.characterName)
    
    if success == True:
        ui.uniqueID = uniqueID

def tutorial_call(ui, accountKey):
    tutorial.load_tutorial(ui, accountKey)

mainSubroutines = [lambda ui: connect_to_network(ui), lambda ui, accountKey: tutorial_call(ui, accountKey)]

animationController = game_ui.AnimationController()
textController = game_ui.TextController()

ui = game_ui.GameUI(screenScale, fontSizes, studentName, mainSubroutines, animationController, textController)
ui.start_combat('grunt')
ui.initialize_buttons()
ui.initialize_window()
ui.run()

#quit Pygame and program
pygame.quit()
sys.exit()
