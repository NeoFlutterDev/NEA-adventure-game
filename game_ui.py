import pygame
import sys
import math
import database
import time
import threading

class GameUI:
    def __init__(self, screenScale, fontSizes, studentName, mainSubroutines, animationController, textController):
        self.screenScale = screenScale
        self.buttons = {}
        self.font = pygame.font.Font(None, fontSizes['large'])
        self.smallFont = pygame.font.Font(None, fontSizes['small'])
        self.window = None
        self.screen = 'start menu'
        self.password = ''
        self.networkPin = ''
        self.uniqueID = ''
        self.characterName = ''
        self.running = True
        self.studentName = studentName
        self.mainSubroutines = mainSubroutines
        self.animationController = animationController
        self.textController = textController

    def initialize_buttons(self):
        self.buttons = {
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
                [False, [1173, 1187], self.mainSubroutines[0], 'sprites/buttons/upload password.png'],
            ],
        }
    #all buttons, ordered by the screen, saved as the key
    #order of button, whether it is visible, bounds, what to run when pressed, sprite path

    def empty_def(self):
        pass
    
    def initialize_window(self):
        info_object = pygame.display.Info()
        self.window = pygame.display.set_mode((info_object.current_w, info_object.current_h), pygame.FULLSCREEN)
        pygame.display.set_caption('Ancient Discovery')

    #scales sprites based upon the screen size
    def scale_sprite(self, image):
        return pygame.transform.scale(image, (
            int(image.get_width() * self.screenScale[0]),
            int(image.get_height() * self.screenScale[1])
        ))
    
    def button_blitter(self):
        button_options = self.buttons[self.screen]
        for button in button_options:
            if button[0]:
                self.window.blit(pygame.image.load(button[3]), self.quadrant_to_coordinates(button[1][0]))
    #load all buttons on the current screen which are enabled

    def coordinates_to_quadrant(self, coordinates):
        quadrantX = coordinates[0] / (20 * self.screenScale[0])
        quadrantY = coordinates[1] / (20 * self.screenScale[1])
        return (math.trunc(quadrantY) * 96) + math.trunc(quadrantX) + 1
    
    def quadrant_to_coordinates(self, quadrant):
        quadrant -= 1
        coordinateX = (quadrant % 96) * 20 * self.screenScale[0]
        coordinateY = (quadrant // 96) * 20 * self.screenScale[1]
        return [coordinateX, coordinateY]
    
    def quadrant_checker(self, buttonQuadrant1, buttonQuadrant2, pressedQuadrant):
        quadrantX = pressedQuadrant % 96
        quadrantY = pressedQuadrant // 96
        quadrant1X, quadrant1Y = buttonQuadrant1 % 96, buttonQuadrant1 // 96
        quadrant2X, quadrant2Y = buttonQuadrant2 % 96, buttonQuadrant2 // 96
        return (quadrant1Y <= quadrantY <= quadrant2Y) and (quadrant1X <= quadrantX <= quadrant2X)
    
    def search_buttons(self, searchQuadrant):
        buttonOptions = self.buttons.get(self.screen, [])
        for button in buttonOptions:
            is_active, (q1, q2), action, sprite = button
            if is_active and self.quadrant_checker(q1, q2, searchQuadrant):
                return action
        return self.empty_def #default action if no button is found
    #find the button pressed based upon the given quadrant and current screen
    
    #change to the character select menu and load all the accounts
    def start_game(self):
        self.screen = 'character select menu'
        accounts = database.load_accounts()
        for i in range(len(accounts)):
            self.buttons['character select menu'][i][0] = True
            self.buttons['character select menu'][i][2] = [self.bin_account, int(accounts[i][0])]
            self.buttons['character select menu'][i+3][0] = True
            self.buttons['character select menu'][i+3][2] = [self.load_account, int(accounts[i][0])]
            self.buttons['character select menu'][i+6][0] = False
        self.render()
    
    def options_start_menu(self):
        pass

    def statistics_start_menu(self):
        pass
    
    def bin_account(self, accountKey):
        database.delete_account(accountKey)
        for i in range(3):
            self.buttons['character select menu'][i][0] = False
            self.buttons['character select menu'][i+3][0] = False
            self.buttons['character select menu'][i+6][0] = True
        self.start_game()
    #delete an account and then reload the screen and accounts

    def load_account(self, accountKey):
        self.buttons['load account'][0][2] = [self.check_password, accountKey]
        self.window.fill((0, 0, 0))
        self.screen = 'load account'
    
    def make_save(self): 
        self.window.fill((0, 0, 0))
        self.screen = 'password creator'
        #move to the password screen
    
    def go_back(self, newScreen):
        self.screen = newScreen
    #return to previous screen
    
    def password_buttons_false(self):
        for i in range(6):
            self.buttons['password creator'][i][0] = False
    #return the password criteria buttons to default
    
    def password_text_field_creation(self, key):
        symbols = '[@_!#$%^&*()<>?/\|}{~:]'
        self.password_buttons_false()
        
        if key == 'backspace':
            self.password = self.password[:-1]
        elif len(self.password) < 18 and key.isprintable():
            self.password += key
        
        #validate password criteria in order of most important to least
        if len(self.password) < 8:
            self.buttons['password creator'][0][0] = True  # Password too short
        elif not any(char in symbols for char in self.password):
            self.buttons['password creator'][1][0] = True  #no symbols
        elif not any(char.islower() for char in self.password):
            self.buttons['password creator'][2][0] = True  #no lowercase
        elif not any(char.isupper() for char in self.password):
            self.buttons['password creator'][3][0] = True  #no capitals
        elif not any(char.isdigit() for char in self.password):
            self.buttons['password creator'][4][0] = True  #no numbers
        else:
            self.buttons['password creator'][5][0] = True  #submit password
        
        self.render()
    #check if the password is viable after appending/deleting a character

    def password_text_field_checking(self, key):
        self.buttons['load account'][0][0] = True
        self.buttons['load account'][1][0] = False
        self.buttons['load account'][2][0] = False
        
        if key == 'backspace':
            self.password = self.password[:-1]
        elif len(self.password) < 18 and key.isprintable():
            self.password += key
        
        self.render()

    def check_password(self, accountKey):
        hashedPassword = database.hashing_algorithm(self.password)
        if hashedPassword == database.load_account_attribute('encryptedPassword', accountKey)[0]:
            self.buttons['load account'][0][0] = False
            self.buttons['load account'][2][0] = True
        else: 
            self.buttons['load account'][0][0] = False
            self.buttons['load account'][1][0] = True
        #check for character name to see if the tutorial needs to be ran

        self.characterName = database.load_account_attribute('characterName', accountKey)[0]

        if self.characterName == 'Unknown':
            tutorial_call = self.mainSubroutines[1]
            tutorial_call(self, accountKey, self.animationController, self.textController)
        else:
            load_save_state(accountKey)

        self.render()

    def upload_password(self):
        hashedPassword = database.hashing_algorithm(self.password)
        database.table_accounts_insertion('Unknown', hashedPassword, 1, 1, None, None)
        self.password = ''
        self.buttons['password creator'][5][0] = False
        self.buttons['password creator'][0][0] = True
        self.start_game()
    #upload the hashed password to the database
    
    def network_pin_enterer(self, key):
        if key == 'backspace':
            self.networkPin = self.networkPin[:-1]
        elif len(self.networkPin) < 5:
            self.networkPin += key

        if len(self.networkPin) == 5:
            self.buttons['networking'][1][0] = True
    
    def render(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/backdrops/{self.screen}.png')), (0, 0))

        self.button_blitter()

        self.window.blit(self.scale_sprite(pygame.image.load('sprites/buttons/exit.png')), self.quadrant_to_coordinates(95))

        if self.uniqueID == '' and self.characterName != '':
            self.window.blit(self.scale_sprite(pygame.image.load('sprites/buttons/no connection.png')), self.quadrant_to_coordinates(3))
        elif self.characterName != '':
            self.window.blit(self.scale_sprite(pygame.image.load('sprites/buttons/connection.png')), self.quadrant_to_coordinates(3))  
        
        if self.screen == 'password creator' or self.screen == 'load account':
            rectangle = pygame.Rect(150, 370, 1580, 100)
            pygame.draw.rect(self.window, (180, 180, 180), rectangle)
            password_text = self.font.render(self.password, True, (255, 255, 255))
            self.window.blit(password_text, (rectangle.x + 5, rectangle.y + 5))
        elif self.screen == 'networking':
            rectangle = pygame.Rect(400, 170, 1450, 50)
            pygame.draw.rect(self.window, (180, 180, 180), rectangle)
            password_text = self.smallFont.render(self.networkPin, True, (255, 255, 255))
            self.window.blit(password_text, (rectangle.x + 5, rectangle.y + 5))
        #draw password text if on the password creator, load account or networking screen
      
        pygame.display.update()
    
    def render_text(self, text, font, startQuadrant, colour):
        x, y = self.quadrant_to_coordinates(startQuadrant)
        for line in text:
            textSurface = font.render(line, True, colour)
            self.window.blit(textSurface, (x, y))
            y += font.get_height()
            pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click_event()
        elif event.type == pygame.KEYDOWN:
            self.handle_key_press_event(event)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_mouse_click_event(self):
        mousePos = pygame.mouse.get_pos()
        mouseQuadrant = self.coordinates_to_quadrant(mousePos)
        
        if mouseQuadrant in [95, 96, 191, 192]:
            self.quit_game()
        elif mouseQuadrant in [3, 4, 99, 100] and self.screen not in ['networking', 'load account'] and self.characterName != '':
            self.buttons['networking'][0][2][1] = self.screen
            self.screen = 'networking'
        else:
            self.handle_button_click_event()
    
    def handle_button_click_event(self):
        mousePos = pygame.mouse.get_pos()
        mouseQuadrant = self.coordinates_to_quadrant(mousePos)

        buttonAction = self.search_buttons(mouseQuadrant)
        if isinstance(buttonAction, list):
            action, parameter = buttonAction
            action(parameter)
        else:
            buttonAction()
    
    def handle_key_press_event(self, event):
        screenKeyHandlers = {
            'password creator': self.handle_password_creator_key,
            'load account': self.handle_load_account_key,
            'networking': self.handle_networking_key
        }
        handle = screenKeyHandlers.get(self.screen)
        if handle:
            handle(event)

    def handle_password_creator_key(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.password_text_field_creation('backspace')
        else:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.password_text_field_creation(event.unicode.upper())
            else:
                self.password_text_field_creation(event.unicode)
        
    def handle_load_account_key(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.password_text_field_checking('backspace')
        else:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.password_text_field_checking(event.unicode.upper())
            else:
                self.password_text_field_checking(event.unicode)

    def handle_networking_key(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.network_pin_enterer('backspace')
        elif event.unicode.isdigit():
            self.network_pin_enterer(event.unicode)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.render()
        self.quit_game()

class AnimationController():
    def __init__(self):
        self.threads = [] #list to store stop events

    def start_loop_animation(self, timeDelay, loops, name, states, quadrant, game_ui):
        def loop_animation_thread():
            for i in range(loops):
                for state in range(states):
                    image = pygame.image.load(f'sprites/animations/{name}/state {state+1}')
                    scaledImage = game_ui.scale_sprite(image)
                    game_ui.window.blit(scaledImage, game_ui.quadrant_to_coordinates(quadrant))
                    pygame.display.update()
                    time.sleep(timeDelay)
        
        thread = threading.Thread(target=loop_animation_thread, daemon=True)
        thread.start()

    def start_continuous_animation(self, timeDelay, name, states, quadrant, game_ui):
        stopEvent = threading.Event()

        def animation_thread():
            while not stopEvent.is_set():
                for state in range(states):
                    if stopEvent.is_set():
                        return 
                    image = pygame.image.load(f'sprites/animations/{name}/state {state+1}')
                    scaledImage = self.scale_sprite(image)
                    game_ui.window.blit(scaledImage, game_ui.quadrant_to_coordinates(quadrant))
                    pygame.display.update()
                    time.sleep(timeDelay)

        thread = threading.Thread(target=animation_thread, daemon=True)
        thread.start()
        self.threads.append((thread, stopEvent))

    def stop_animation(self, index):
        if -1 < index < len(self.threads):
            animation, stopEvent = self.threads[index]
            stopEvent.set()
    
    def stop_all_animations(self):
        for animation, stopEvent in self.threads:
            stopEvent.set()
    
class TextController:
    def __init__(self):
        self.threads = [] #list to store current text

    def typewriter_text(self, game_ui, font, text, startQuadrant, maxWidth, colour=(256, 256, 256)):
        stopEvent = threading.Event()

        def start_typewriter_text():
            currentIndex = 0
            self.text = []
            for line in lines:
                self.text.append('')
                for char in line:
                    self.text[-1] += char
                    currentIndex += 1
                    game_ui.render_text(self.text, font, startQuadrant, colour)
                    time.sleep(0.1)

                    if stopEvent.is_set():
                        self.check_threads()
            self.check_threads()
        
        lines = self.wrap_text(text, font, maxWidth)
        thread = threading.Thread(target=start_typewriter_text, daemon=True)
        thread.start()
        self.threads.append((thread, stopEvent))
    
    def wrap_text(self, text, font, maxWidth):
        words = text.split(' ')
        lines = []
        currentLine = ''

        for word in words:
            test = f'{currentLine} {word}'.strip()
            if font.size(test)[0] <= maxWidth:
                currentLine = test
            else:
                lines.append(currentLine)
                currentLine = word
        lines.append(currentLine)

        return lines    
    
    def check_threads(self):
        for i in range(len(self.threads)-1, -1, -1):
            thread, stop_event = self.threads[i]
            if not thread.is_alive():
                self.threads.pop(i)