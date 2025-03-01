import pygame
import sys
import math
import database
import time
import threading
import random
import combat

class GameUI:
    def __init__(self, screenScale, fontSizes, studentName, mainSubroutines, animationController, textController):
        self.screenScale = screenScale
        self.buttons = {}
        self.font = pygame.font.Font(None, fontSizes['large'])
        self.smallFont = pygame.font.Font(None, fontSizes['small'])
        self.statsFont = pygame.font.Font(None, fontSizes['stats'])
        self.window = None
        self.screen = 'start menu'
        self.password = ''
        self.networkPin = ''
        self.uniqueID = ''
        self.accountKey = 0
        self.characterName = ''
        self.characterPOS = [[0, 0], 'w']
        self.running = True
        self.sound = True
        self.statsText = {'combined stats':[], 'account 1 stats':[], 'account 2 stats':[], 'account 3 stats':[]}
        self.questionText = {'question screen':[[], [], [], [], []], 'questionKey':0}
        self.studentName = studentName
        self.character = [combat.PlayableCharacter(studentName, 25, None, 1, 'fist', 1), 'idle']
        self.monster = None
        self.mainSubroutines = mainSubroutines
        self.animationController = animationController
        self.textController = textController
        self.newEquip = [[], []]

    def initialize_buttons(self):
        self.buttons = {
            'start menu': [
                [True, [1946, 2569], self.start_game, 'sprites/buttons/start button.png'],
                [True, [2906, 3529], self.options_start_menu, 'sprites/buttons/options button start menu.png'],
                [True, [3866, 4489], self.statistics_start_menu, 'sprites/buttons/statistics button start menu.png']
            ],
            'options menu': [
                [False, [1266, 1557], self.sound_off, 'sprites/buttons/sound on.png'],
                [False, [1266, 1557], self.sound_on, 'sprites/buttons/sound off.png'],
                [True, [1971, 2262], database.delete_all_accounts, 'sprites/buttons/delete button.png'],
                [True, [1, 98], [self.new_screen, 'start menu'], 'sprites/buttons/back arrow.png'],
            ],
            'combined stats': [
                [True, [572, 863], [self.new_screen, 'account 1 stats'], 'sprites/buttons/right one.png'],
                [True, [1, 98], [self.new_screen, 'start menu'], 'sprites/buttons/back arrow.png'],
                [False, [9999, 9999], [], 'sprites/buttons/empty sprite.png'],
            ],
            'account 1 stats': [
                [True, [481, 772], [self.new_screen, 'combined stats'], 'sprites/buttons/left combined.png'],
                [True, [572, 863], [self.new_screen, 'account 2 stats'], 'sprites/buttons/right two.png'],
                [True, [1, 98], [self.new_screen, 'start menu'], 'sprites/buttons/back arrow.png'],
            ],
            'account 2 stats': [
                [True, [481, 772], [self.new_screen, 'account 1 stats'], 'sprites/buttons/left one.png'],
                [True, [572, 863], [self.new_screen, 'account 3 stats'], 'sprites/buttons/right three.png'],
                [True, [1, 98], [self.new_screen, 'start menu'], 'sprites/buttons/back arrow.png'],
            ],
            'account 3 stats': [
                [True, [481, 772], [self.new_screen, 'account 2 stats'], 'sprites/buttons/left two.png'],
                [True, [1, 98], [self.new_screen, 'start menu'], 'sprites/buttons/back arrow.png'],
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
                [True, [1, 98], [self.new_screen, 'start menu'], 'sprites/buttons/back arrow.png']
            ],
            'password creator': [
                [True, [2505, 2519], self.empty_def, 'sprites/buttons/password too short.png'],
                [False, [2505, 2519], self.empty_def, 'sprites/buttons/no symbols.png'],
                [False, [2505, 2519], self.empty_def, 'sprites/buttons/no lowercase.png'],
                [False, [2505, 2519], self.empty_def, 'sprites/buttons/no capital letter.png'],
                [False, [2505, 2519], self.empty_def, 'sprites/buttons/no numbers.png'],
                [False, [2505, 2519], self.upload_password, 'sprites/buttons/upload password.png'],
                [True, [1, 98], [self.new_screen, 'character select menu'], 'sprites/buttons/back arrow.png']
            ],
            'load account': [
                [True, [2505, 2519], [self.check_password, 1], 'sprites/buttons/upload password.png'],
                [False, [2505, 2519], self.empty_def, 'sprites/buttons/incorrect password.png'],
                [False, [2505, 2519], self.empty_def, 'sprites/buttons/correct password.png'],
                [True, [1, 98], [self.new_screen, 'character select menu'], 'sprites/buttons/back arrow.png']
            ],
            'networking': [
                [True, [1, 98], [self.new_screen, 'start menu'], 'sprites/buttons/back arrow.png'],
                [False, [1173, 1187], [self.mainSubroutines[0], self], 'sprites/buttons/upload password.png'],
            ],
            'tutorial start': [
            ],
            'tutorial part2': [
            ],
            'new equip': [
                [True, [3858, 4741], [self.equip, ''], 'sprites/buttons/old.png'],
                [True, [3901, 4784], [self.equip, ''], 'sprites/buttons/new.png'],
                [False, [9999, 9999], [self.new_screen, ''], 'sprites/buttons/empty sprite.png']
            ],
            'question screen': [
                [True, [2600, 3597], [self.question_checker, 'incorrect'], 'sprites/buttons/question box a.png'],
                [True, [2644, 3641], [self.question_checker, 'incorrect'], 'sprites/buttons/question box b.png'],
                [True, [4040, 5037], [self.question_checker, 'incorrect'], 'sprites/buttons/question box c.png'],
                [True, [4084, 5081], [self.question_checker, 'incorrect'], 'sprites/buttons/question box d.png'],
                [False, [9999, 9999], [self.new_screen, ''], 'sprites/buttons/empty sprite.png']
            ],
            'battle': [
                [True, [4044, 4265], [self.combat_phase, 'normal attack'], 'sprites/buttons/normal attack.png'],
                [True, [4087, 4308], [self.combat_phase, 'heavy attack'], 'sprites/buttons/heavy attack.png'],
                [True, [4620, 4841], [self.combat_phase, 'dodge'], 'sprites/buttons/dodge.png'],
                [True, [4663, 4884], self.empty_def, 'sprites/buttons/special attack.png'],
                [False, [9999, 9999], [self.new_screen, ''], 'sprites/buttons/empty sprite.png'],
                [False, [2049, 2255], self.empty_def, 'sprites/buttons/victory.png'],
                [False, [2049, 2255], self.empty_def, 'sprites/buttons/defeat.png']
            ],
            'exploration': [
            ],
            'village1': [
            ],
            'dungeon': [
            ],
            'shop': [
                [True, [2214, 2602], [self.shop_weapon, 'n'], 'sprites/animations/combat/ normal.png'],
                [True, [2224, 2612], [self.shop_weapon, 's'], 'sprites/animations/combat/ normal.png'],
                [True, [2237, 2625], [self.shop_weapon, 'g'], 'sprites/animations/combat/ normal.png'],
                [True, [2250, 2638], [self.shop_weapon, 'l'], 'sprites/animations/combat/ normal.png'],
                [True, [2261, 2649], [self.shop_armour, 'n'], 'sprites/animations/combat/ normal.png'],
                [True, [2270, 2658], [self.shop_armour, 's'], 'sprites/animations/combat/ normal.png'],
                [True, [2281, 2669], [self.shop_armour, 'g'], 'sprites/animations/combat/ normal.png'],
                [True, [2292, 2680], [self.shop_armour, 'l'], 'sprites/animations/combat/ normal.png'],
                [True, [1, 98], [self.new_screen, 'village1'], 'sprites/buttons/back arrow.png']
            ],
        }
    #all buttons, ordered by the screen, saved as the key
    #order of button, whether it is visible, bounds, what to run when pressed, sprite path

    def empty_def(self):
        pass

    def question_checker(self, answer):
        if answer == 'incorrect':
            database.update_question('incorrect', self.questionText['questionKey'], self.accountKey)
            self.questions()
        else:
            database.update_question('correct', self.questionText['questionKey'], self.accountKey)
            self.new_screen(self.buttons['question screen'][4][2][1])

    def start_combat(self, type):
        self.questions()
        if self.buttons['battle'][4][2][1] == '':
            self.buttons['battle'][4][2][1] = self.screen
        self.buttons['battle'][5][0] = False
        self.buttons['battle'][6][0] = False
        self.screen = 'battle'
        self.monster = [combat.Monster(self.character[0].get_lvl(), type), 'idle']
    
    def combat_phase(self, button):
        self.character, self.monster = combat.player_combat(self.character, self.monster, button)
        if self.monster[0].get_currentHp() > 0:
            self.character, self.monster = combat.monster_combat(self.character, self.monster)
        elif self.monster[0].get_currentHp() < 1:
            gains = {'grunt':2, 'elite':4, 'boss':8}
            self.buttons['battle'][5][0] = True
            self.render()
            time.sleep(3)
            database.update_account_attribute('kills', 1, self.accountKey)
            self.character[0].set_money(self.character[0].get_money() + gains[self.monster[0].get_type()])
            self.character[0].update_exp(gains[self.monster[0].get_type()])
            database.update_account_attribute('money', gains[self.monster[0].get_type()], self.accountKey)
            database.update_account_attribute('exp', gains[self.monster[0].get_type()], self.accountKey)
            if isinstance(self.buttons['battle'][4][2][1], str):
                self.new_screen(self.buttons['battle'][4][2][1])
            else:
                self.buttons['battle'][4][2][1](self)
        
        if self.character[0].get_currentHp() < 1:
            self.buttons['battle'][6][0] = True
            self.render()
            time.sleep(3)
            database.update_account_attribute('deaths', 1, self.accountKey)
            if isinstance(self.buttons['battle'][4][2][1], str):
                self.new_screen(self.buttons['battle'][4][2][1])
            else:
                self.buttons['battle'][4][2][1](self)
    
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
        self.screen = 'options menu'
        if self.sound:
            self.buttons['options menu'][0][0] = True
        else:
            self.buttons['options menu'][0][0] = False

    def new_weapon(self, newWeapon, rarity):
        self.screen = 'new equip'
        try:
            oldWeapon = self.character[0].get_weapon()
            oldMod = self.character[0].get_weaponModifier()
        except:
            oldWeapon = 'fist'
            oldMod = 1

        newWeapon = newWeapon[len(rarity):].strip()
        newMod = combat.rarityConverter[rarity[:1]]

        # Update button actions correctly
        self.buttons['new equip'][0][2] = [self.equip, f"{oldWeapon} {oldMod}"]
        self.buttons['new equip'][1][2] = [self.equip, f"{newWeapon} {newMod}"]
        self.newEquip = [[newWeapon, newMod], [oldWeapon, oldMod]]

        self.equipRun = True
        while self.equipRun and self.screen == 'new equip':
            for event in pygame.event.get():
                self.handle_event(event)
            self.render()
    
    def new_armour(self, newArmour, rarity):
        self.screen = 'new equip'
        try:
            if self.character[0].get_armour():
                oldArmour = self.character[0].get_armour()
                oldMod = float(str(2-self.character[0].get_armourModifier())[:4])
            else:
                oldArmour = 'None'
                oldMod = 1
        except:
            oldArmour = None
            oldMod = 1

        newArmour = newArmour[len(rarity):]
        newMod = combat.rarityConverter[rarity[:1]]

        if oldArmour is None:
            oldArmour = 'None'

        # Update button actions correctly
        self.buttons['new equip'][0][2] = [self.equip, f"{oldArmour} {oldMod}"]
        self.buttons['new equip'][1][2] = [self.equip, f"{newArmour} {newMod}"]
        self.newEquip = [[newArmour, newMod], [oldArmour, oldMod]]

        self.equipRun = True
        while self.equipRun and self.screen == 'new equip':
            for event in pygame.event.get():
                self.handle_event(event)
            self.render()
    
    def equip(self, stats):
        self.equipRun = False
        print(stats)
        try:
            mod = float(stats[-4:])
            name = stats[:-4].strip()
        except:
            mod = 1
            name = stats[:-1].strip()

        print(mod)
        print(name)

        weapons = ['fist', 'bow', 'sword']
        armors = ['nanoplate', 'titanweave', 'plasmaweave']

        if name in weapons:
            rarity = combat.reverseWeaponRarityConverter[mod]
            newWeapon = name
            self.character[0].set_weapon(newWeapon)
            self.character[0].set_weaponModifier(mod)

            database.update_account_equipment('weapon', newWeapon, mod, self.accountKey)

        elif name in armors:
            rarity = combat.reverseArmourRarityConverter[float((str(2-mod))[:4])]
            newArmour = name
            self.character[0].set_armour(newArmour)
            self.character[0].set_armourModifier(float((str(2-mod))[:4]))  

            database.update_account_equipment('armour', newArmour, float((str(2-mod))[:4]), self.accountKey)          
        
        self.new_screen('village1')

    def sound_off(self):
        self.buttons['options menu'][0][0] = False
        self.buttons['options menu'][1][0] = True
        self.sound = False

        self.render()

    def sound_on(self):
        self.buttons['options menu'][0][0] = True
        self.buttons['options menu'][1][0] = False
        self.sound = True
        
        self.render()

    def statistics_start_menu(self):
        self.screen = 'combined stats'
        accounts = database.load_all_accounts()
        accountsNumber = len(accounts)
        placement = [9999, 9999, 9999, 1183, 1669, 9999, 2159, 9999, 2735, 3107, 3591]
        for i in range(3, 11):
            if i == 5 or i == 7: 
                pass
            else:
                if accountsNumber == 3:
                    self.statsText['combined stats'].append([[str((float(accounts[0][i] + accounts[1][i] + accounts[2][i])) / 3)], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 1 stats'].append([[str(float(accounts[0][i]))], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 2 stats'].append([[str(float(accounts[1][i]))], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 3 stats'].append([[str(float(accounts[2][i]))], self.statsFont, placement[i], (255, 255, 255)])
                elif accountsNumber == 2:
                    self.statsText['combined stats'].append([[str((float(accounts[0][i] + accounts[1][i])) / 2)], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 1 stats'].append([[str(float(accounts[0][i]))], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 2 stats'].append([[str(float(accounts[1][i]))], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 3 stats'].append([['N/A'], self.statsFont, placement[i], (255, 255, 255)])
                elif accountsNumber == 1:
                    self.statsText['combined stats'].append([[str(float(accounts[0][i]))], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 1 stats'].append([[str(float(accounts[0][i]))], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 2 stats'].append([['N/A'], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 3 stats'].append([['N/A'], self.statsFont, placement[i], (255, 255, 255)])
                else:
                    self.statsText['combined stats'].append([['N/A'], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 1 stats'].append([['N/A'], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 2 stats'].append([['N/A'], self.statsFont, placement[i], (255, 255, 255)])
                    self.statsText['account 3 stats'].append([['N/A'], self.statsFont, placement[i], (255, 255, 255)])
        self.render()

    def questions(self):
        
        if self.screen != 'question screen':
            self.buttons['question screen'][4][2][1] = self.screen
            self.screen = 'question screen'
        
        slots = [1, 2, 3, 4]
        placement = [296, 2895, 2938, 4431, 4378]

        question, questionKey = database.get_question(self.accountKey)

        self.questionText['question screen'][0] = [TextController.wrap_text(TextController, question[0], self.smallFont, 1600), self.smallFont, placement[0], (255, 255, 255)]
        placement.pop(0)
        self.questionText['questionKey'] = questionKey

        correctSlot = random.randint(0, 3)
        self.buttons['question screen'][correctSlot][2][1] = 'correct'
        self.questionText['question screen'][slots[correctSlot]] = [TextController.wrap_text(TextController, question[1], self.smallFont, 600), self.smallFont, placement[correctSlot], (255, 255, 255)]
        slots.pop(correctSlot)
        placement.pop(correctSlot)

        incorrect = [question[2], question[3], question[4]]

        for i in range(3):
            randomSlot = random.randint(0, 2-i)
            self.questionText['question screen'][slots[randomSlot]] = [TextController.wrap_text(TextController, incorrect[randomSlot], self.smallFont, 600), self.smallFont, placement[i], (255, 255, 255)]
            slots.pop(randomSlot)
            incorrect.pop(randomSlot)
    
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
    
    def new_screen(self, newScreen):
        if newScreen == 'start menu':
            self.statsText = {'combined stats':[], 'account 1 stats':[], 'account 2 stats':[], 'account 3 stats':[]}
        self.screen = newScreen
        self.render()
    #return to previous screen

    def dungeon(self):
        rooms = ['grunt', 'grunt', 'grunt', 'elite', 'elite', 'boss']
        for i in range(6):
            self.screen = 'dungeon'
            self.render()
            self.textController.typewriter_text(self, self.font, f'Floor {i+1}', 2058, 2000)
            image = pygame.image.load(f'sprites/characters/{rooms[i]} slime.png')
            self.window.blit(self.scale_sprite(image), self.quadrant_to_coordinates(3497))
            time.sleep(3)
            self.start_combat(f'{rooms[i]}')
            while self.screen == 'battle' or self.screen == 'question screen':
                for event in pygame.event.get():
                    self.handle_event(event)
                self.render()
            if self.character[0].get_currentHp() < 1:
                break

        if self.character[0].get_currentHp() >= 1:
            self.textController.typewriter_text(self, self.font, f'Treasure Floor', 2051, 2000)
            image = pygame.image.load(f'sprites/animations/misc/macguffin1.png')
            self.window.blit(self.scale_sprite(image), self.quadrant_to_coordinates(3497))
            time.sleep(3)
            self.textController.stop_all_text()
            self.render()
            text = 'You pick up the mysterious item on the floor. The design and rough sides show that it is clearly part of a larger piece. Maybe exploring more dungeons will unlock more pieces.'
            self.textController.typewriter_text(self, self.smallFont, text, 2028, 1000)
            time.sleep(12)
            self.characterPOS = [[900, 1000], 'w']
            self.screen = 'village1'
        else:
            self.dungeon_failure()

    def dungeon_failure(self):
        text = 'The slime deals the final blow and leaves you dazed on the floor. You wake up several hours later, mysteriously in the village entrance once more.'
        self.textController.typewriter_text(self, self.smallFont, text, 2028, 1000)
        time.sleep(10)
        self.character[0].update_currentHp(self.character[0].get_maxHp() - self.character[0].get_currentHp())
        self.character[0].update_currentStm(self.character[0].get_maxStm() - self.character[0].get_currentStm())
        self.characterPOS = [[900, 1000], 'w']
        self.screen = 'village1'

    def shop(self):
        for i in range(8):
            if i <= 3:
                item = combat.weapon[random.randint(0, 1)].strip()
                self.buttons['shop'][i][2][1] = f'n{item}'
                self.buttons['shop'][i][3] = f'sprites/animations/combat/{item} normal.png'
            else:
                item = combat.armour[random.randint(0, 2)].strip()
                self.buttons['shop'][i][2][1] = f'n{item}'
                self.buttons['shop'][i][3] = f'sprites/animations/combat/{item} normal.png'
        self.screen = 'shop'

    def shop_armour(self, armour):
        moneyCost = {'n':10, 's':25, 'g':50, 'l':100}
        characterMoney = self.character[0].get_money()
        if characterMoney >= moneyCost[armour[:1]]:
            self.character[0].set_money(characterMoney - moneyCost[armour[:1]])
            self.new_armour(armour[1:], armour[:1])
    
    def shop_weapon(self, weapon):
        moneyCost = {'n':10, 's':25, 'g':50, 'l':100}
        characterMoney = self.character[0].get_money()
        if characterMoney >= moneyCost[weapon[:1]]:
            self.character[0].set_money(characterMoney - moneyCost[weapon[:1]])
            self.new_weapon(weapon[1:], weapon[:1])

    def exploration(self):
        self.screen = 'exploration'
        self.render()
        #encounter = random.randint(1, 100)
        encounter = 85
        encounterRandomness = random.randint(1, 100)
        x, y = self.quadrant_to_coordinates(1578)

        if encounter <= 55:
            image = pygame.image.load('sprites/characters/grunt slime.png')
            self.window.blit(self.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * (2/3)), int(image.get_height() * (2/3))))), (x, y))
            pygame.display.flip()
            time.sleep(5)
            self.buttons['battle'][4][2][1] == 'village1'
            self.start_combat('grunt')

        elif encounter <= 70:
            image = pygame.image.load('sprites/characters/elite slime.png')
            self.window.blit(self.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * (2/3)), int(image.get_height() * (2/3))))), (x, y))
            pygame.display.flip()
            time.sleep(5)
            self.buttons['battle'][4][2][1] == 'village1'
            self.start_combat('elite')

        elif encounter <= 75:
            image = pygame.image.load('sprites/characters/boss slime.png')
            self.window.blit(self.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * (2/3)), int(image.get_height() * (2/3))))), (x, y))
            pygame.display.flip()
            time.sleep(5)
            self.buttons['battle'][4][2][1] == 'village1'
            self.start_combat('boss')


        elif encounter <= 80:
            weaponType = combat.weapon[random.randint(0, 1)]
            image = pygame.image.load(f'sprites/animations/combat/{weaponType.strip()} normal.png')
            self.window.blit(self.scale_sprite(pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))), (x, y))
            if encounterRandomness <= 55:
                newWeapon = f'{combat.rarity[0]}{weaponType}'
                rarity = combat.rarity[0]
            elif encounterRandomness <= 75:
                newWeapon = f'{combat.rarity[1]}{weaponType}'
                rarity = combat.rarity[1]
            elif encounterRandomness <= 95:
                newWeapon = f'{combat.rarity[2]}{weaponType}'
                rarity = combat.rarity[2]
            else:
                newWeapon = f'{combat.rarity[3]}{weaponType}'
                rarity = combat.rarity[3]
            pygame.display.flip()
            time.sleep(5)
            self.new_weapon(newWeapon, rarity)

        elif encounter <= 85:
            armourType = combat.armour[random.randint(0, 2)]
            image = pygame.image.load(f'sprites/animations/combat/{armourType.strip()} normal.png')
            self.window.blit(self.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * 2), int(image.get_height() * 2)))), (x, y))
            if encounterRandomness <= 55:
                newArmour = f'{combat.rarity[0]}{armourType}'
                rarity = combat.rarity[0]
            elif encounterRandomness <= 75:
                newArmour = f'{combat.rarity[1]}{armourType}'
                rarity = combat.rarity[1]
            elif encounterRandomness <= 95:
                newArmour = f'{combat.rarity[2]}{armourType}'
                rarity = combat.rarity[2]
            else:
                newArmour = f'{combat.rarity[3]}{armourType}'
                rarity = combat.rarity[3]
            pygame.display.flip()
            time.sleep(5)
            self.new_armour(newArmour, rarity)

        else:
            amount = random.randint(1, 10)
            image = pygame.image.load(f'sprites/animations/misc/coin.png')
            self.window.blit(self.scale_sprite(pygame.transform.scale(image, (int(image.get_width() * 2), int(image.get_height() * 2)))), (x, y))
            pygame.display.flip()
            time.sleep(5)
            self.character[0].set_money(self.character[0].get_money() + amount)

        while self.screen == 'battle' or self.screen == 'new equip' or self.screen == 'question screen':
            for event in pygame.event.get():
                self.handle_event(event)
            self.render()

        database.update_account_info(self.character[0].get_exp(), self.character[0].get_money(), self.character[0].get_armour(), 
                                     self.character[0].get_armourModifier(), self.character[0].get_weapon(), self.character[0].get_weaponModifier(),self.accountKey)

        self.character[0].update_currentHp(self.character[0].get_maxHp() - self.character[0].get_currentHp())
        self.character[0].update_currentStm(self.character[0].get_maxStm() - self.character[0].get_currentStm())

        self.screen = 'village1'
        self.render()
    
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
            self.accountKey = accountKey
        else: 
            self.buttons['load account'][0][0] = False
            self.buttons['load account'][1][0] = True
        #check for character name to see if the tutorial needs to be ran

        self.character[0].name = database.load_account_attribute('characterName', accountKey)[0]

        if self.character[0].name == 'Unknown':
            tutorial_call = self.mainSubroutines[1]
            tutorial_call(self, accountKey)
        else:
            self.load_save_state(accountKey)

        self.render()

    def load_save_state(self, accountKey):
        save = database.load_account(accountKey)[0]
        name, exp, armour, armourModifier, weapon, weaponModifier = save
        self.characterName = name
        self.character[0] = combat.PlayableCharacter(name, exp, armour, armourModifier, weapon, weaponModifier)
        self.characterPOS = [[900, 1000], 'w']
        self.screen = 'village1'

    def upload_password(self):
        hashedPassword = database.hashing_algorithm(self.password)
        accountKey = database.table_accounts_insertion('Unknown', hashedPassword, 25, 1, None, 1, 'fist', 1, 0, 0)
        database.weight_insertion(accountKey)
        self.password = ''
        self.buttons['password creator'][5][0] = False
        self.buttons['password creator'][0][0] = True
        self.start_game()
    #upload the hashed password to the database and update the weights table
    
    def network_pin_enterer(self, key):
        if key == 'backspace':
            self.networkPin = self.networkPin[:-1]
        elif len(self.networkPin) < 5:
            self.networkPin += key

        if len(self.networkPin) == 5:
            self.buttons['networking'][1][0] = True
    
    def tutorial_name_enterer(self, key):
        if key == 'backspace':
            self.characterName = self.characterName[:-1]
        elif key == 'enter':
            self.character[0].name = self.characterName
        elif isinstance(key, str) and len(self.characterName) < 12:
            self.characterName += key
        self.render()
    
    def render(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/backdrops/{self.screen}.png')), (0, 0))

        self.button_blitter()

        self.window.blit(self.scale_sprite(pygame.image.load('sprites/buttons/exit.png')), self.quadrant_to_coordinates(95))

        if self.uniqueID == '' and self.characterName != '':
            self.window.blit(self.scale_sprite(pygame.image.load('sprites/buttons/no connection.png')), self.quadrant_to_coordinates(3))
        elif self.characterName != '':
            self.window.blit(self.scale_sprite(pygame.image.load('sprites/buttons/connection.png')), self.quadrant_to_coordinates(3))  
        
        text = 'Your memory is foggy, what is your name again?'

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
        elif self.screen == 'tutorial start' and any(threads[2] == text for threads in self.textController.threads):
            rectangle = pygame.Rect(10, 400, 1450, 50)
            password_text = self.smallFont.render(self.characterName, True, (255, 255, 255))
            self.window.blit(password_text, (rectangle.x + 5, rectangle.y + 5))

        elif self.screen in ['combined stats', 'account 1 stats', 'account 2 stats', 'account 3 stats']:
            textToBlit = self.statsText[self.screen]
            for lines in textToBlit:
                self.render_text(lines[0], lines[1], lines[2], lines[3])

        elif self.screen == 'question screen':
            textToBlit = self.questionText[self.screen]
            for lines in textToBlit:
                self.render_text(lines[0], lines[1], lines[2], lines[3])
        
        elif self.screen == 'battle':
            enemyStamina = [f'Stm: {max(0, int(self.monster[0].get_currentStm()))}']
            enemyHp = [f'Hp: {max(0, int(self.monster[0].get_currentHp()))}']
            playerStamina = [f'Stm: {max(0, int(self.character[0].get_currentStm()))}']
            playerHp = [f'Hp: {max(0, int(self.character[0].get_currentHp()))}']

            self.render_text(enemyStamina, self.smallFont, 194, (255, 255, 255))
            self.render_text(enemyHp, self.smallFont, 674, (255, 255, 255))
            self.render_text(playerStamina, self.smallFont, 2949, (255, 255, 255))
            self.render_text(playerHp, self.smallFont, 3333, (255, 255, 255))

            if (self.monster[0].get_currentHp() / self.monster[0].get_maxHp()) > 0.5:
                x, y = self.quadrant_to_coordinates(68)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/characters/{self.monster[0].get_type()} slime.png')), (x, y))
            elif (self.monster[0].get_currentHp() / self.monster[0].get_maxHp()) > 0:
                x, y = self.quadrant_to_coordinates(68)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/characters/{self.monster[0].get_type()} slime hurt.png')), (x, y))
            else:
                x, y = self.quadrant_to_coordinates(68)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/characters/{self.monster[0].get_type()} slime dead.png')), (x, y))

            x, y = self.quadrant_to_coordinates(2320)
            self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/characters/character combat.png')), (x, y))

            if self.character[1] == 'normal':
                x, y = self.quadrant_to_coordinates(2901)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/animations/combat/{self.character[0].get_weapon()[-5:].strip()} normal.png')), (x, y))

            elif self.character[1] == 'heavy':
                x, y = self.quadrant_to_coordinates(2901)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/animations/combat/{self.character[0].get_weapon()[-5:].strip()} heavy.png')), (x, y))
            
            elif self.character[1] == 'dodge':
                x, y = self.quadrant_to_coordinates(2901)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/animations/combat/dodge.png')), (x, y))
            
            elif self.character[1] == 'special':
                x, y = self.quadrant_to_coordinates(2901)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/animations/combat/{self.character[0].get_weapon()[-5:].strip()} special.png')), (x, y))

            if self.monster[1] == 'normal':
                x, y = self.quadrant_to_coordinates(841)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/animations/combat/{self.monster[0].get_type()} normal.png')), (x, y))

            elif self.monster[1] == 'heavy':
                x, y = self.quadrant_to_coordinates(841)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/animations/combat/{self.monster[0].get_type()} heavy.png')), (x, y))

            elif self.monster[1] == 'dodge':
                x, y = self.quadrant_to_coordinates(841)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/animations/combat/dodge.png')), (x, y))

            elif self.monster[1] == 'special':
                x, y = self.quadrant_to_coordinates(841)
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/animations/combat/special.png')), (x, y))
        
        elif self.screen == 'new equip':
            if self.newEquip[1][0] != 'None':
                x, y = self.quadrant_to_coordinates(1654)
                image = pygame.image.load(f'sprites/animations/combat/{self.newEquip[1][0]} normal.png')
                self.window.blit(self.scale_sprite(pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))), (x, y))

            if self.newEquip[0][0] not in ['fist', 'sword', 'bow', 'nanoplate', 'titanweave', 'plasmaweave']:
                x, y = self.quadrant_to_coordinates(1697)
                image = pygame.image.load(f'sprites/animations/combat/{self.newEquip[0][0][1:]} normal.png')
                self.window.blit(self.scale_sprite(pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))), (x, y))
            else:
                x, y = self.quadrant_to_coordinates(1697)
                image = pygame.image.load(f'sprites/animations/combat/{self.newEquip[0][0]} normal.png')
                self.window.blit(self.scale_sprite(pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))), (x, y))

            self.render_text([str(self.newEquip[1][1])], self.statsFont, 3292, (255, 255, 255))

            self.render_text([str(self.newEquip[0][1])], self.statsFont, 3336, (255, 255, 255))

        elif self.screen == 'village1':
            if self.characterPOS[1] == 'w':
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/characters/character up.png')), (self.characterPOS[0][0], self.characterPOS[0][1]))
            elif self.characterPOS[1] == 'a':
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/characters/character left.png')), (self.characterPOS[0][0], self.characterPOS[0][1]))
            elif self.characterPOS[1] == 's':
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/characters/character down.png')), (self.characterPOS[0][0], self.characterPOS[0][1]))
            else:
                self.window.blit(self.scale_sprite(pygame.image.load(f'sprites/characters/character right.png')), (self.characterPOS[0][0], self.characterPOS[0][1]))
      
        pygame.display.update()
    
    def render_text(self, text, font, startQuadrant, colour):
        x, y = self.quadrant_to_coordinates(startQuadrant)
        for line in text:
            textSurface = font.render(line, True, colour)
            self.window.blit(textSurface, (x, y))
            y += font.get_height()

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
            'networking': self.handle_networking_key,
            'tutorial start': self.handle_tutorial_name,
            'village1': self.handle_village_movement,
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
    
    def handle_tutorial_name(self, event):
        text = 'Your memory is foggy, what is your name again?'
        if any(threads[2] == text for threads in self.textController.threads) and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.tutorial_name_enterer('backspace')
            elif event.key == pygame.K_RETURN:
                self.tutorial_name_enterer('enter')
            elif event.unicode.isprintable():
                self.tutorial_name_enterer(event.unicode)

    def handle_village_movement(self, event):
        keys = pygame.key.get_pressed()  # Get the current state of all keys

        if keys[pygame.K_w]:
            self.characterPOS[0][1] = max(0, self.characterPOS[0][1] - 30)
        
        if keys[pygame.K_a]:
            self.characterPOS[0][0] = max(0, self.characterPOS[0][0] - 30)
        
        if keys[pygame.K_s]:
            self.characterPOS[0][1] = min(1030, self.characterPOS[0][1] + 30)
        
        if keys[pygame.K_d]:
            self.characterPOS[0][0] = min(1870, self.characterPOS[0][0] + 30)

        if self.characterPOS[0][0] <= 130 and (self.characterPOS[0][1] >= 380 and self.characterPOS[0][1] <= 610):
            self.characterPOS = [[900, 1000], 'w']
            self.dungeon()

        elif (self.characterPOS[0][0] <= 1040 and self.characterPOS[0][0] >= 810) and self.characterPOS[0][1] <= 130:
            self.characterPOS = [[900, 1000], 'w']
            self.shop()

        elif self.characterPOS[0][0] >= 1780 and (self.characterPOS[0][1] >= 440 and self.characterPOS[0][1] <= 550):
            self.characterPOS = [[900, 1000], 'w']
            self.exploration()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.render()
        self.quit_game()

class AnimationController():
    def __init__(self):
        self.threads = [] #list to store stop events

    def start_loop_animation(self, timeDelay, loops, name, states, startQuadrant, endQuadrant, game_ui):
        def loop_animation_thread():
            for i in range(loops):
                for state in range(states):
                    image = pygame.image.load(f'sprites/animations/{name}/state {state+1}')
                    scaledImage = game_ui.scale_sprite(image)
                    coords1 = game_ui.quadrant_to_coordinates(startQuadrant)
                    coords2 = game_ui.quadrant_to_coordinates(endQuadrant)
                    difference  = ((coords1[0] - coords2[0]), (coords1[1] - coords2[1]))
                    game_ui.window.blit(scaledImage, coords1)
                    pygame.display.update(pygame.rect(coords1, difference))
                    time.sleep(timeDelay)
        
        thread = threading.Thread(target=loop_animation_thread, daemon=True)
        thread.start()

    def start_continuous_animation(self, timeDelay, name, states, repeats, startQuadrant, endQuadrant, game_ui):
        stopEvent = threading.Event()

        def animation_thread():
            while not stopEvent.is_set():
                for state in range(states):
                    for i in range(repeats):
                        if stopEvent.is_set():
                            return 
                        image = pygame.image.load(f'sprites/animations/{name}/state {state+1}.png')
                        scaledImage = game_ui.scale_sprite(image)
                        coords1 = game_ui.quadrant_to_coordinates(startQuadrant)
                        coords2 = game_ui.quadrant_to_coordinates(endQuadrant)
                        difference  = ((coords1[0] - coords2[0]), (coords1[1] - coords2[1]))
                        game_ui.window.blit(scaledImage, game_ui.quadrant_to_coordinates(startQuadrant))
                        pygame.display.update(pygame.Rect(coords1, difference))
                        time.sleep(timeDelay)

        thread = threading.Thread(target=animation_thread, daemon=True)
        thread.start()
        self.threads.append((name, stopEvent))

    def stop_animation(self, index):
        if -1 < index < len(self.threads):
            stopEvent = self.threads[index][1]
            stopEvent.set()
    
    def stop_all_animations(self):
        for stopEvent in self.threads:
            stopEvent[1].set()
    
class TextController:
    def __init__(self):
        self.threads = []

    def typewriter_text(self, game_ui, font, text, startQuadrant, maxWidth, colour=(255, 255, 255)):
        stopEvent = threading.Event()

        def start_typewriter_text():
            currentIndex = 0
            self.text = []
            
            for line in lines:
                if stopEvent.is_set():
                    break  

                self.text.append('')
                for char in line:
                    if stopEvent.is_set():
                        break  

                    for count in range(6):
                        if count == 0:
                            self.text[-1] += char
                            currentIndex += 1

                        game_ui.render_text(self.text, font, startQuadrant, colour)
                        pygame.display.update() 
                        time.sleep(1/120)

                        if stopEvent.is_set():
                            break 

                if stopEvent.is_set():
                    break 

            self.check_threads()

        lines = self.wrap_text(text, font, maxWidth)
        thread = threading.Thread(target=start_typewriter_text, daemon=True)
        thread.start()  
        self.threads.append((thread, stopEvent, text))

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
            thread, stopEvent, text = self.threads[i]
            if not thread.is_alive():
                self.threads.pop(i)

    def stop_all_text(self):
        for thread, stopEvent, text in self.threads:
            stopEvent.set()  

        for thread, stopEvent, text in self.threads:
            thread.join()

        self.threads.clear()
