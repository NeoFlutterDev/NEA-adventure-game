import pygame
import database
import sys
import math
import student_communication

pygame.init()

#get display information and set up screenScale
infoObject = pygame.display.Info()
screenScale = [infoObject.current_w / 1920, infoObject.current_h / 1080]

#initialize the game window
window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('Ancient Discovery')

#game state
running = True
font = pygame.font.Font(None, 130)
smallFont = pygame.font.Font(None, 60)
screen = 'start menu'
password = ''
networkPin = ''


#scales sprites based upon the screen size
def scale_sprite(image):
    return pygame.transform.scale(image, (
        int(image.get_width() * screenScale[0]),
        int(image.get_height() * screenScale[1])
    ))

#change to the character select menu and load all the accounts
def start_game():
    global screen, buttons
    screen = 'character select menu'
    accounts = database.load_accounts()
    for i in range(len(accounts)):
        buttons['character select menu'][i][0] = True
        buttons['character select menu'][i][2] = [bin_account, int(accounts[i][0])]
        buttons['character select menu'][i+3][0] = True
        buttons['character select menu'][i+3][2] = [load_account, int(accounts[i][0])]
        buttons['character select menu'][i+6][0] = False

def options_start_menu():
    pass

def statistics_start_menu():
    pass

def empty_def():
    pass

#delete an account and then reload the screen and accounts
def bin_account(accountKey):
    global buttons, screen
    database.delete_account(accountKey)
    for i in range(3):
        buttons['character select menu'][i][0] = False
        buttons['character select menu'][i+3][0] = False
        buttons['character select menu'][i+6][0] = True
    window.fill((0, 0, 0))
    start_game()

def load_account(accountKey):
    global screen, buttons
    buttons['load account'][0][2] = [check_password, accountKey]
    window.fill((0, 0, 0))
    screen = 'load account'

#move to the password screen
def make_save():
    global screen 
    window.fill((0, 0, 0))
    screen = 'password creator'

#return to start menu
def go_back(newScreen):
    global screen
    screen = newScreen

#clear the password criteria buttons
def password_buttons_false():
    global buttons
    for i in range(6):
        buttons['password creator'][i][0] = False

#check if the password is viable after appending/deleting a character
def passwordTextFieldCreation(key):
    global password, buttons
    symbols = '[@_!#$%^&*()<>?/\|}{~:]'
    password_buttons_false()
    
    if key == 'backspace':
        password = password[:-1]
    elif len(password) < 18 and key.isprintable():
        password += key
    
    #validate password criteria in order of most important to least
    if len(password) < 8:
        buttons['password creator'][0][0] = True  # Password too short
    elif not any(char in symbols for char in password):
        buttons['password creator'][1][0] = True  #no symbols
    elif not any(char.islower() for char in password):
        buttons['password creator'][2][0] = True  #no lowercase
    elif not any(char.isupper() for char in password):
        buttons['password creator'][3][0] = True  #no capitals
    elif not any(char.isdigit() for char in password):
        buttons['password creator'][4][0] = True  #no numbers
    else:
        buttons['password creator'][5][0] = True  #submit password

#upload the hashed password to the database
def upload_password():
    global password
    hashedPassword = database.hashing_algorithm(password)
    database.table_accounts_insertion('Unknown', hashedPassword, 1, 1, None, None)
    password = ''
    buttons['password creator'][5][0] = False
    buttons['password creator'][0][0] = True
    start_game()

def passwordTextFieldChecking(key):
    global password, buttons    

    buttons['load account'][1][0] = False
    buttons['load account'][0][0] = True
    
    if key == 'backspace':
        password = password[:-1]
    elif len(password) < 18 and key.isprintable():
        password += key

    pygame.display.update()
    
def check_password(accountKey):
    global password, buttons

    hashedPassword = database.hashing_algorithm(password)
    if hashedPassword == database.load_account_password(accountKey)[0]:
        print('correct')
    else: 
        buttons['load account'][0][0] = False
        buttons['load account'][1][0] = True

def network_pin_enterer(key):
    global networkPin
    global buttons

    if key == 'backspace':
        networkPin = networkPin[:-1]
    elif len(networkPin) < 4:
        networkPin += key

    if len(networkPin) == 4:
        buttons['networking'][1][0] = True

    pygame.display.update()

def connect_to_network():
    global networkPin

    student_communication.client_program(networkPin)


#determine quadrant based upon given coordinates
def coordinates_to_quadrant(coordinates):
    quadrantX = coordinates[0] / (20 * screenScale[0])
    quadrantY = coordinates[1] / (20 * screenScale[1])
    return (math.trunc(quadrantY) * 96) + math.trunc(quadrantX) + 1
    #quadrants range from 1 to 5184

#determine coordinates based upon given quadrant
def quadrant_to_coordinates(quadrant):
    quadrant -= 1
    coordinateX = (quadrant % 96) * 20 * screenScale[0]
    coordinateY = (quadrant // 96) * 20 * screenScale[1]
    return [coordinateX, coordinateY]

#check if the pressed quadrant is part of the button
def quadrant_checker(buttonQuadrant1, buttonQuadrant2, pressedQuadrant):
    quadrantX = pressedQuadrant % 96
    quadrantY = pressedQuadrant // 96
    q1X, q1Y = buttonQuadrant1 % 96, buttonQuadrant1 // 96
    q2X, q2Y = buttonQuadrant2 % 96, buttonQuadrant2 // 96
    return (q1Y <= quadrantY <= q2Y) and (q1X <= quadrantX <= q2X)

#find the button pressed based upon the given quadrant and current screen
def search_buttons(searchQuadrant):
    global buttons, screen
    buttonOptions = buttons.get(screen, [])
    for button in buttonOptions:
        is_active, (q1, q2), action, sprite = button
        if is_active and quadrant_checker(q1, q2, searchQuadrant):
            return action
    return empty_def  #default action if no button is found

#all buttons, ordered by the screen, saved as the key
buttons = {
    'start menu': [
        [True, [1946, 2569], start_game, 'sprites/buttons/start button.png'], 
        [True, [2906, 3529], options_start_menu, 'sprites/buttons/options button start menu.png'], 
        [True, [3866, 4489], statistics_start_menu, 'sprites/buttons/statistics button start menu.png']
    ],
    'character select menu': [
        [False, [1146, 1243], [bin_account, 1], 'sprites/buttons/bin.png'],
        [False, [2874, 2971], [bin_account, 2], 'sprites/buttons/bin.png'],
        [False, [4602, 4699], [bin_account, 3], 'sprites/buttons/bin.png'],
        [False, [760, 859], [load_account, 1], 'sprites/buttons/load.png'],
        [False, [2488, 2587], [load_account, 2], 'sprites/buttons/load.png'],
        [False, [4216, 4315], [load_account, 3], 'sprites/buttons/load.png'],
        [True, [711, 1114], make_save, 'sprites/buttons/new game.png'],
        [True, [2439, 2842], make_save, 'sprites/buttons/new game.png'],
        [True, [4167, 4570], make_save, 'sprites/buttons/new game.png'],
        [True, [1, 98], [go_back, 'start menu'], 'sprites/buttons/back arrow.png']
    ],
    'password creator': [
        [True, [2505, 2519], empty_def, 'sprites/buttons/password too short.png'],
        [False, [2505, 2519], empty_def, 'sprites/buttons/no symbols.png'],
        [False, [2505, 2519], empty_def, 'sprites/buttons/no lowercase.png'],
        [False, [2505, 2519], empty_def, 'sprites/buttons/no capital letter.png'],
        [False, [2505, 2519], empty_def, 'sprites/buttons/no numbers.png'],
        [False, [2505, 2519], upload_password, 'sprites/buttons/upload password.png'],
        [True, [1, 98], [go_back, 'character select menu'], 'sprites/buttons/back arrow.png']
    ],
    'load account': [
        [True, [2505, 2519], [check_password, 1], 'sprites/buttons/upload password.png'],
        [False, [2505, 2519], empty_def, 'sprites/buttons/incorrect password.png'],
        [True, [1, 98], [go_back, 'character select menu'], 'sprites/buttons/back arrow.png']
    ],
    'networking': [
        [True, [1, 98], [go_back, 'start menu'], 'sprites/buttons/back arrow.png'],
        [False, [1173, 1187], connect_to_network, 'sprites/buttons/upload password.png'],  
    ],
}
#order of button, whether it is visible, bounds, what to run when pressed, sprite path

#load all buttons on the current screen which are enabled
def button_blitter():
    global buttons, screen
    buttonOptions = buttons[screen]
    for button in buttonOptions:
        if button[0]:
            window.blit(pygame.image.load(button[3]), quadrant_to_coordinates(button[1][0]))

#main game loop
while running:
    #load events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouseQuadrant = coordinates_to_quadrant(mouse_pos)
            # print(f"Mouse clicked in quadrant: {mouseQuadrant}")

            if mouseQuadrant in [95, 96, 191, 192]:
                pygame.quit()  #detects if the exit button has been hit
                sys.exit()
            elif mouseQuadrant in [3, 4, 99, 100] and screen != 'networking':
                buttons['networking'][0][2][1] = screen
                screen = 'networking'
            else:
                buttonPressed = search_buttons(mouseQuadrant)
                if isinstance(buttonPressed, list):
                    buttonPressed, parameter = buttonPressed
                    buttonPressed(parameter)
                else:
                    buttonPressed()
        elif event.type == pygame.KEYDOWN:
            if screen == 'password creator':
                if event.key == pygame.K_BACKSPACE:
                    passwordTextFieldCreation('backspace')
                else:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        passwordTextFieldCreation(event.unicode.upper())
                    else:
                        passwordTextFieldCreation(event.unicode)
            elif screen == 'load account':
                if event.key == pygame.K_BACKSPACE:
                    passwordTextFieldChecking('backspace')
                else:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        passwordTextFieldChecking(event.unicode.upper())
                    else:
                        passwordTextFieldChecking(event.unicode)
            elif screen == 'networking':
                if event.key == pygame.K_BACKSPACE:
                    network_pin_enterer('backspace')
                elif event.unicode.isdigit():
                    network_pin_enterer(event.unicode)

    #update the screen based on current screen
    window.blit(scale_sprite(pygame.image.load(f'sprites/backdrops/{screen}.png')), (0, 0))

    #draw buttons on screen
    button_blitter()

    #draw the exit button
    window.blit(scale_sprite(pygame.image.load('sprites/buttons/exit.png')), quadrant_to_coordinates(95))
    window.blit(scale_sprite(pygame.image.load('sprites/buttons/network symbol.png')), quadrant_to_coordinates(3))

    #draw password text if on the password creator, load account or networking screen
    if screen == 'password creator' or screen == 'load account':
        rectangle = pygame.Rect(150, 370, 1580, 100)
        pygame.draw.rect(window, (180, 180, 180), rectangle)
        password_text = font.render(password, True, (255, 255, 255))
        window.blit(password_text, (rectangle.x + 5, rectangle.y + 5))
    elif screen == 'networking':
        rectangle = pygame.Rect(400, 170, 1450, 50)
        pygame.draw.rect(window, (180, 180, 180), rectangle)
        password_text = smallFont.render(networkPin, True, (255, 255, 255))
        window.blit(password_text, (rectangle.x + 5, rectangle.y + 5))

    #update the display
    pygame.display.update()

#quit Pygame and program
pygame.quit()
sys.exit()