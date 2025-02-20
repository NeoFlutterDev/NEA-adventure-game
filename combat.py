import random
import math

def player_combat(player, monster, buttonPressed):
    playerStm = int(player[0].get_currentStm())
    playerMaxStm = int(player[0].get_maxStm())
    playerAtk = float(player[0].get_atk())
    playerWpnMod = float(player[0].get_weaponModifier())
    monsterAmrMod = float(monster[0].get_armourModifier())
    monsterDodgeValue = int(monster[0].get_monsterDodgeValue())
    monsterMultiplier = float(monster[0].get_multiplier())

    if buttonPressed == 'normal attack' and playerStm >= 5:
        player[0].update_currentStm(-5)
        if random.randint(1, 100) < monsterDodgeValue:
            monster[0].update_currentHp(-(playerAtk * playerWpnMod * monsterAmrMod * (1 / monsterMultiplier)))
        player[0].update_playerDodgeValue(75)
        return [[player[0], 'normal'], [monster[0], monster[1]]]
    
    elif buttonPressed == 'normal attack' and playerStm < 5:
        return [[player[0], 'normal'], [monster[0], monster[1]]]
    
    elif buttonPressed == 'heavy attack' and playerStm >= 15:
        player[0].update_currentStm(-15)
        if random.randint(1, 100) < monsterDodgeValue + 15:
            monster[0].update_currentHp(-(playerAtk * 1.5 * playerWpnMod * monsterAmrMod * (1 / monsterMultiplier)))
        player[0].update_playerDodgeValue(100)
        return [[player[0], 'heavy'], [monster[0], monster[1]]]
    
    elif buttonPressed == 'heavy attack' and playerStm < 15:
        return [[player[0], 'heavy'], [monster[0], monster[1]]]
    
    elif buttonPressed == 'dodge':
        if playerStm + 25 > playerMaxStm:
            player[0].update_currentStm(-(playerStm+25))
            player[0].update_currentStm(playerMaxStm)
        else:
            player[0].update_currentStm(25)
        player[0].update_playerDodgeValue(25)
        return [[player[0], 'dodge'], [monster[0], monster[1]]]
    
    elif buttonPressed == 'special' and playerStm >= 50:
        player[0].special_atk()
        return [[player[0], 'special'], [monster[0], monster[1]]]
    
    elif buttonPressed == 'special' and playerStm < 50:
        return [[player[0], 'special'], [monster[0], monster[1]]]

def monster_combat(player, monster):
    bias = int(monster[0].get_bias())
    monsterStm = int(monster[0].get_currentStm())
    monsterMaxStm = int(monster[0].get_maxStm())
    monsterAtk = float(monster[0].get_atk())
    monsterWpnMod = float(monster[0].get_weaponModifier())
    monsterMultiplier = float(monster[0].get_multiplier())
    playerAmrMod = float(player[0].get_armourModifier())
    playerDodgeValue = float(player[0].get_playerDodgeValue())
    #changes the chance, higher bias = more likely to use specials/heavy attacks
    #lower bias = more likely to dodge or attack, monsters with no special will have a bias of -25 or lower

    randomSelector = int(random.randint(1, 100)) + bias
    if randomSelector > 75 and monsterStm >= 50:
        monster[0].update_monsterDodgeValue(0)
        return [[player[0], player[1]], [monster[0], 'special']]
    
    elif randomSelector > 50 and monsterStm >= 15:
        monster[0].update_currentStm(-15)
        if random.randint(1, 100) < playerDodgeValue + 15:
            player[0].update_currentHp(-(monsterAtk * 1.5 * monsterWpnMod * playerAmrMod * monsterMultiplier))
        monster[0].update_monsterDodgeValue(100)
        return [[player[0], player[1]], [monster[0], 'heavy']]
    
    elif randomSelector < 26 and monsterStm >= 5:
        monster[0].update_currentStm(-15)
        if random.randint(1, 100) < playerDodgeValue:
            player[0].update_currentHp(-(monsterAtk * monsterWpnMod * playerAmrMod * monsterMultiplier))
        monster[0].update_monsterDodgeValue(75)
        return [[player[0], player[1]], [monster[0], 'normal']]
    
    else:
        player[0].update_currentStm(25)
        if monsterStm > monsterMaxStm:
            monster[0].update_currentStm(monsterMaxStm)
        monster[0].update_monsterDodgeValue(25)
        return [[player[0], player[1]], [monster[0], 'dodge']]

class PlayableCharacter:
    def __init__(self, name, exp, armour = None, armourModifier = 1, weapon = None, weaponModifier = 1):
        self.name = name
        self.exp = exp
        self.lvl = math.trunc(2.5 * (math.sqrt(self.exp) - 5))
        self.money = 0
        self.armour = armour
        self.armourModifier = armourModifier
        self.weapon = weapon
        self.weaponModifier = weaponModifier
        self.atk = math.trunc(1.5 * self.lvl + 100)
        self.maxHp = math.trunc(((self.lvl / 4.624) + 10)**2)
        self.currentHp = self.maxHp
        self.maxStm = math.trunc(4 * self.lvl + 100)
        self.currentStm = self.maxStm
        self.playerDodgeValue = 75
        #defines the base stats of the player
        #as levels go up, health increases the most, followed by stamina, followed by attack

    def update_exp(self, expGain):
        self.exp = self.exp + expGain
        curentLvl = math.trunc(2.5 * (math.sqrt(self.exp) - 5))
        if self.lvl < curentLvl:
            self.lvl = curentLvl
            self.update_atk() 
            self.update_maxHp() 
            self.update_maxStm()

    def get_exp(self):
        return self.exp
    
    def get_lvl(self):
        return self.lvl

    def set_money(self, money):
        self.money = money

    def get_money(self):
        return self.money

    def set_armour(self, armour):
        self.armour = armour

    def get_armour(self):
        return self.armour
    
    def set_armourModifier(self, armourModifier):
        self.armourModifier = armourModifier

    def get_armourModifier(self):
        return self.armourModifier
    
    def set_weapon(self, weapon):
        self.weapon = weapon

    def get_weapon(self):
        return self.weapon
    
    def set_weaponModifier(self, weaponModifier):
        self.weaponModifier = weaponModifier

    def get_weaponModifier(self):
        return self.weaponModifier

    def update_atk(self):
        self.atk = math.trunc(1.5 * self.lvl + 100)

    def get_atk(self):
        return self.atk
    
    def update_maxHp(self):
        self.maxHp = math.trunc(((self.lvl / 4.624) + 10)**2)

    def get_maxHp(self):
        return self.maxHp

    def update_currentHp(self, hpGain):
        self.currentHp = self.currentHp + hpGain
        #if health has been lost enter a negative value for hpGain

    def get_currentHp(self):
        return self.currentHp
    
    def update_maxStm(self):
        self.maxStm = math.trunc(4 * self.lvl + 100)

    def get_maxStm(self):
        return self.maxStm

    def update_currentStm(self, stmGain):
        self.currentStm = self.currentStm + stmGain
        #if stamina has been lost enter a negative value for stmGain

    def get_currentStm(self):
        return self.currentStm
    
    def get_playerDodgeValue(self):
        return self.playerDodgeValue
    
    def update_playerDodgeValue(self, playerDodgeValue):
        self.playerDodgeValue = playerDodgeValue

#25 xp is lvl 1 (baseline)

weapon = ['sword', 'axe', 'halberd', 'hammer', 'spear']
armour = ['chain', 'plate', 'fur']
rarity = ['novice', 'standard', 'great', 'legendary']
typeConverter = {'grunt':[[0, 1], -30, 0.2], 'elite':[[1, 2], -15, 0.4], 'boss':[[3, 3], 15, 0.6]}
rarityConverter = {'n': 1.05, 's':1.15, 'g':1.25, 'l':1.4}

class Monster:
    def __init__(self, playerLvl, type):
        self.lvl = max(1, playerLvl + random.randint(-5, -1))
        self.armour = f'{rarity[random.randint((typeConverter[type][0])[0], (typeConverter[type][0])[1])]} {armour[random.randint(0, 2)]}'
        self.armourModifier = 2 - rarityConverter[self.armour[0]] 
        self.weapon = f'{rarity[random.randint((typeConverter[type][0])[0], (typeConverter[type][0])[1])]} {weapon[random.randint(0, 4)]}'
        self.weaponModifier = rarityConverter[self.armour[0]]
        self.bias = typeConverter[type][1]
        self.atk = math.trunc(1.5 * self.lvl + 100)
        self.maxHp = math.trunc(((self.lvl / 4.624) + 10)**2)
        self.currentHp = self.maxHp
        self.maxStm = math.trunc(4 * self.lvl + 100)
        self.currentStm = self.maxStm
        self.type = type
        self.monsterDodgeValue = 75
        self.multiplier = typeConverter[type][2]
        #whether the enemy is a grunt, elite or boss
    
    def get_lvl(self):
        return self.lvl

    def set_armour(self, armour):
        self.armour = armour

    def get_armour(self):
        return self.armour
    
    def set_armourModifier(self, armourModifier):
        self.armourModifier = armourModifier

    def get_armourModifier(self):
        return self.armourModifier
    
    def set_weapon(self, weapon):
        self.weapon = weapon

    def get_weapon(self):
        return self.weapon
    
    def set_weaponModifier(self, weaponModifier):
        self.weaponModifier = weaponModifier

    def get_weaponModifier(self):
        return self.weaponModifier
    
    def get_bias(self):
        return self.bias
    
    def set_bias(self, bias):
        self.bias = bias

    def update_atk(self):
        self.atk = math.trunc(1.5 * self.lvl + 100)

    def get_atk(self):
        return self.atk
    
    def update_maxHp(self):
        self.maxHp = math.trunc(((self.lvl / 4.624) + 10)**2)

    def get_maxHp(self):
        return self.maxHp

    def update_currentHp(self, hpGain):
        self.currentHp = self.currentHp + hpGain
        #if health has been lost enter a negative value for hpGain

    def get_currentHp(self):
        return self.currentHp
    
    def update_maxStm(self):
        self.maxStm = math.trunc(4 * self.lvl + 100)

    def get_maxStm(self):
        return self.maxStm

    def update_currentStm(self, stmGain):
        self.currentStm = self.currentStm + stmGain
        #if stamina has been lost enter a negative value for stmGain

    def get_currentStm(self):
        return self.currentStm
    
    def get_type(self):
        return self.type
    
    def get_monsterDodgeValue(self):
        return self.monsterDodgeValue
    
    def update_monsterDodgeValue(self, monsterDodgeValue):
        self.monsterDodgeValue = monsterDodgeValue
    
    def get_multiplier(self):
        return self.multiplier