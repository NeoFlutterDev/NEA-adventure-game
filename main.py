import pygame
import student_communication
import tutorial
from game_ui import GameUI

pygame.init()

screenScale = [pygame.display.Info().current_w / 1920, pygame.display.Info().current_h / 1080]
fontSizes = {'large': 130, 'small': 60}
studentName = input('Enter your name')

def connect_to_network(ui):
    global networkPin, uniqueID, studentName, characterName

    success, uniqueID = student_communication.first_connection(ui.networkPin, ui.studentName, ui.characterName)

def tutorial_call(ui, accountKey):
    tutorial.load_tutorial(ui, accountKey)

mainSubroutines = [lambda: connect_to_network(ui), lambda accountKey: tutorial_call(ui, accountKey)]

ui = GameUI(screenScale, fontSizes, studentName, mainSubroutines)
ui.initialize_buttons(connect_to_network)
ui.initialize_window()
ui.run()

#quit Pygame and program
pygame.quit()
sys.exit()
