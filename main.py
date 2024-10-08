import pygame
import database
pygame.init()
import sys
import math

infoObject = pygame.display.Info()
screenScale = [infoObject.current_w / 1920, infoObject.current_h / 1080]
#this finds the size of the monitor, as well as making an array to scale the game sprites upon
window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('Ancient Discovery')
#initialises the window
running = True
#variable for checking if game is still running
font = pygame.font.Font('spacefont.ttf', 30)
screen = 'start menu'

def scale_sprite(image):
    return pygame.transform.scale(image, (int(image.get_width() * screenScale[0]), int(image.get_height() * screenScale[1])))

def start_game():
    global screen
    global buttons
    screen = 'character select menu'
    accounts = database.load_accounts()
    for i in range(len(accounts)):
        buttons['character select menu'][i][0] = True
        buttons['character select menu'][i][2] = [bin_account, int(accounts[i][0])]
        buttons['character select menu'][i+3][0] = True
        buttons['character select menu'][i+6][0] = False
    
def options_start_menu():
    pass

def statistics_start_menu():
    pass

def empty_def():
    pass

def bin_account(accountKey):
    global screen
    global buttons
    database.delete_account(accountKey)
    for i in range(3):
        buttons['character select menu'][i][0] = False
        ['character select menu'][i+3][0] = False
        buttons['character select menu'][i+6][0] = True
    window.fill(0, 0, 0)
    screen = 'start menu'

def load_account():
    pass

def make_save():
    screen = 'password creator'
    '''password is 8-25 characters, 1 capital, 1 lowercase, 1 number
    if some criteria is not met display the most important one (go in the given order)'''

def go_back_start():
    global screen
    screen = 'start menu'

def coordinates_to_quadrant(coordinates):
    quadrantX = coordinates[0] / (20 * screenScale[0])
    quadrantY = coordinates[1] / (20 * screenScale[1])
    return (math.trunc(quadrantY) * 96) + math.trunc(quadrantX) + 1
'''this finds the quadrant in which the mouse is currently located, by finding which 20 pixels it is located in in both height and width
it then adds these values together, after multiplying the Y quadrant by 96, as there is 96 quadrants per row
the top left quadrant is 1, and the bottom right quadrant is 5184'''

def quadrant_to_coordinates(quadrant):
    quadrant -= 1
    coordinateX = (quadrant % 96) * 20 * screenScale[0]
    coordinateY = (quadrant // 96) * 20 * screenScale[1]
    return [coordinateX, coordinateY]
'''this reverses the quadrant maker, by finding the coordinates used to make the quadrant
the X coordinate is found by the modulo of the quadrant, as the quadrants are counted left to right then down, then multiplied by 20 to find the exact coordinate
the Y coordinate is found by the integer division of the quadrant, as each quadrant down is 96 higher than the previous, due to how it is counted'''

def quadrant_checker(quadrant1, quadrant2, quadrant):
    quadrantX = quadrant % 96
    quadrantY = quadrant // 96
    if (quadrantY >= (quadrant1 // 96)) and (quadrantY <= (quadrant2 // 96)) and (quadrantX >= (quadrant1 % 96)) and (quadrantX <= (quadrant2 % 96)):
        return True
        
def search_buttons(searchQuadrant):
    global buttons
    global screen
    buttonOptions = buttons[screen]
    for button in buttonOptions:
        if button[0] and quadrant_checker(button[1][0], button[1][1], searchQuadrant):
            if isinstance(button[2], list):
                return button[2][0], button[2][1]
            else:
                return button[2]
    return empty_def
    '''gets all the buttons for the current screen, then searches through them one by one
    checks if the button is "on" and whether or not it is where the mouse got pressed
    if it finds the button it returns it, after checking it is has parameters'''
        
buttons = {'start menu':[[True, [1946, 2569], start_game, 'sprites/buttons/start button.png'], 
                         [True, [2906, 3529], options_start_menu, 'sprites/buttons/options button start menu.png'], 
                         [True, [3866, 4489], statistics_start_menu, 'sprites/buttons/statistics button start menu.png']],
            'character select menu': [[False, [1146, 1243], [bin_account, 1], 'sprites/buttons/bin.png'],
                                      [False, [2874, 2971], [bin_account, 2], 'sprites/buttons/bin.png'],
                                      [False, [4602, 4699], [bin_account, 3], 'sprites/buttons/bin.png'],
                                      [False, [760, 859], load_account, 'sprites/buttons/load.png'],
                                      [False, [2488, 2587], load_account, 'sprites/buttons/load.png'],
                                      [False, [4216, 4315], load_account, 'sprites/buttons/load.png'],
                                      [True, [711, 1114], make_save, 'sprites/buttons/new game.png'],
                                      [True, [2439, 2842], make_save, 'sprites/buttons/new game.png'],
                                      [True, [4167, 4570], make_save, 'sprites/buttons/new game.png'],
                                      [True, [1, 98], go_back_start, 'sprites/buttons/back arrow.png']]
                                      } 
'''this stores the information for all buttons except the exit button, as that is the only button that appears on all screens
the dictionary has the screen names as the keys for the buttons, with each value being an array off buttons
each button stores whether it is on or off, the quadrants it appears in, the definition for when it is activated and the name of the button file
the quadrants are the top left quadrant and bottom right, which the sorting algorithm can figure out what quadrants that button covers
example: 'start menu':[['start button, True, [1, 106] start_game]'''

def button_blitter():
    global buttons
    global screen
    buttonOptions = buttons[screen]
    for button in buttonOptions:
        if button[0]:
            window.blit(pygame.image.load(button[3]), quadrant_to_coordinates(button[1][0]))

while running:

    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseQuadrant = coordinates_to_quadrant(pygame.mouse.get_pos())
            #this finds what quadrant the mouse click happened in

            if mouseQuadrant == 95 or mouseQuadrant == 96 or mouseQuadrant == 191 or mouseQuadrant == 192:
                pygame.quit()
                #detects if the exit button has been hit
            
            else: 
                try:
                    buttonPressed, parameter = search_buttons(mouseQuadrant)
                    buttonPressed(parameter)
                except:
                    buttonPressed = search_buttons(mouseQuadrant)
                    buttonPressed()
                    #search to see what button has been pressed, and whether or not is has a parameter to pass, then it executes the given subroutine

    window.blit(scale_sprite(pygame.image.load(f'sprites/backdrops/{screen}.png')), (0, 0))
    #updates the display with the current screen

    button_blitter()
    window.blit(scale_sprite(pygame.image.load('sprites/buttons/exit.png')), (quadrant_to_coordinates(95)))
    #loads, scales and places the button upon the screen

    pygame.display.update()
    #updates the display with all the new changes