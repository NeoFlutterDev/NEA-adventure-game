import pygame
import student_communication
import tutorial
from game_ui import GameUI

pygame.init()

screenScale = [pygame.display.Info().current_w / 1920, pygame.display.Info().current_h / 1080]
fontSizes = {'large': 130, 'small': 60}
studentName = input('Enter your name')

def connect_to_network():
    global networkPin, uniqueID, studentName, characterName

    success, uniqueID = student_communication.first_connection(networkPin, studentName, characterName)

#all buttons, ordered by the screen, saved as the key
buttons = {
    'start menu': [
        [True, [1946, 2569], self.start_game, 'sprites/buttons/start button.png'], 
        [True, [2906, 3529], self.options_start_menu, 'sprites/buttons/options button start menu.png'], 
        [True, [3866, 4489], self.statistics_start_menu, 'sprites/buttons/statistics button start menu.png']
    ],
    'character select menu': [
        [False, [1146, 1243], [self.bin_account, 1], 'sprites/buttons/bin.png'],
        [False, [2874, 2971], [self.bin_account, 2], 'sprites/buttons/bin.png'],
        [False, [4602, 4699], [self.bin_account, 3], 'sprites/buttons/bin.png'],
        [False, [760, 859], [self.load_account, 1], 'sprites/buttons/load.png'],
        [False, [2488, 2587], [self.load_account, 2], 'sprites/buttons/load.png'],
        [False, [4216, 4315], [self.load_account, 3], 'sprites/buttons/load.png'],
        [True, [711, 1114], self.make_save, 'sprites/buttons/new game.png'],
        [True, [2439, 2842], self.make_save, 'sprites/buttons/new game.png'],
        [True, [4167, 4570], self.make_save, 'sprites/buttons/new game.png'],
        [True, [1, 98], [self.go_back, 'start menu'], 'sprites/buttons/back arrow.png']
    ],
    'password creator': [
        [True, [2505, 2519], self.empty_def, 'sprites/buttons/password too short.png'],
        [False, [2505, 2519], self.empty_def, 'sprites/buttons/no symbols.png'],
        [False, [2505, 2519], self.empty_def, 'sprites/buttons/no lowercase.png'],
        [False, [2505, 2519], self.empty_def, 'sprites/buttons/no capital letter.png'],
        [False, [2505, 2519], self.empty_def, 'sprites/buttons/no numbers.png'],
        [False, [2505, 2519], self.upload_password, 'sprites/buttons/upload password.png'],
        [True, [1, 98], [self.go_back, 'character select menu'], 'sprites/buttons/back arrow.png']
    ],
    'load account': [
        [True, [2505, 2519], [self.check_password, 1], 'sprites/buttons/upload password.png'],
        [False, [2505, 2519], self.empty_def, 'sprites/buttons/incorrect password.png'],
        [False, [2505, 2519], self.empty_def, 'sprites/buttons/correct password.png'],
        [True, [1, 98], [self.go_back, 'character select menu'], 'sprites/buttons/back arrow.png']
    ],
    'networking': [
        [True, [1, 98], [self.go_back, 'start menu'], 'sprites/buttons/back arrow.png'],
        [False, [1173, 1187], connect_to_network, 'sprites/buttons/upload password.png'],  
    ],
}
#order of button, whether it is visible, bounds, what to run when pressed, sprite path

ui = GameUI(screenScale, buttons, fontSizes)
ui.initialize_window()
ui.run()

#quit Pygame and program
pygame.quit()
sys.exit()