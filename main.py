import pygame
import student_communication
import tutorial
import game_ui
import sys
import database

pygame.init()

database.createDatabase()
#make sure the database is initialized

screenScale = [pygame.display.Info().current_w / 1920, pygame.display.Info().current_h / 1080]
fontSizes = {'large': 130, 'small': 60, 'stats':100}
studentName = input('Enter your name: ')
#get the students name, the ratio of the players display to the regular 1920x1080 display
#and initialize the fonts used by the program

def connect_to_network(ui):
    success, uniqueID = student_communication.first_connection(ui.networkPin, ui.studentName, ui.characterName, ui.accountKey)
    print(success)
    
    if success == True:
        ui.uniqueID = uniqueID
    #make the first connection to the server
    #if it succeeds save the ID sent by the server to the UI instance

def tutorial_call(ui, accountKey):
    tutorial.load_tutorial(ui, accountKey)
    #start the tutorial

mainSubroutines = [lambda ui: connect_to_network(ui), lambda ui, accountKey: tutorial_call(ui, accountKey)]

animationController = game_ui.AnimationController()
textController = game_ui.TextController()
#intialize the two controllers

ui = game_ui.GameUI(screenScale, fontSizes, studentName, mainSubroutines, animationController, textController)
#initialize the ui

ui.initialize_buttons()
ui.initialize_window()
ui.run()
#start the game

pygame.quit()
sys.exit()
#quit Pygame and program
