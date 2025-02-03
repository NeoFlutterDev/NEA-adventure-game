import random
import math

def player_combat(player, monster, buttonPressed, monsterDodgeValue = 75):
    playerStm = player.get_currentStm
    playerMaxStm = player.get_maxStm
    playerAtk = player.get_atk
    playerWpnMod = player.get_weaponModifier
    monsterAmrMod = monster.get_armourModifier
    if buttonPressed == 'attack' and playerStm >= 5:
        player.update_currentStm(-5)
        playerStm -= 5
        if random.randint(1, 100) < monsterDodgeValue:
            monster.update_currentHp(-(playerAtk * playerWpnMod * monsterAmrMod))
        return 75
    #the player dodge value
    elif buttonPressed == 'heavy attack' and playerStm >= 15:
        player.update_currentStm(-15)
        if random.randint(1, 100) < monsterDodgeValue + 15:
            monster.update_currentHp(-(playerAtk * 1.5 * playerWpnMod * monsterAmrMod))
        return 100
    elif buttonPressed == 'dodge':
        player.set_currentStm(25)
        if playerStm > playerMaxStm:
            player.set_currentStm(playerMaxStm)
        return 25
    elif buttonPressed == 'special' and playerStm >= 50:
        player.special_atk()

def monster_combat(player, monster, playerDodgeValue = 75):
    bias = monster.get_bias
    monsterStm = monster.get_currentStm
    monsterMaxStm = monster.get_maxStm
    monsterAtk = monster.get_atk
    monsterWpnMod = monster.get_weaponModifier
    playerAmrMod = player.get_armourModifier
    #changes the chance, higher bias = more likely to use specials/heavy attacks
    #lower bias = more likely to dodge or attack, monsters with no special will have a bias of -25 or lower
    randomSelector = random.randint(1, 100) + bias
    monsterStm = monster.get_currentStm
    if randomSelector > 75 and monsterStm >= 50:
        monster.special()
    elif randomSelector > 50 and monsterStm >= 15:
        monsterStm -= 15
        if random.randint(1, 100) < playerDodgeValue + 15:
            player.update_currentHp(-(monsterAtk * 1.5 * monsterWpnMod * playerAmrMod))
    elif randomSelector < 26 and monsterStm >= 5:
        monsterStm -= 5
        if random.randint(1, 100) < playerDodgeValue:
            player.update_currentHp(-(monsterAtk * monsterWpnMod * playerAmrMod))
    else:
        player.set_currentStm(25)
        if monsterStm > monsterMaxStm:
            monster.set_currentStm(monsterMaxStm)

class PlayableCharacter:
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp
        self.lvl = math.trunc(2.5 * (math.sqrt(self.exp) - 5))
        self.money = 0
        self.armour = None
        self.armourModifier = 1
        self.weapon = None
        self.weaponModifier = 1
        self.atk = math.trunc(1.5 * self.lvl + 100)
        self.maxHp = math.trunc(((self.lvl / 4.624) + 10)**2)
        self.currentHp = self.maxHp
        self.maxStm = math.trunc(4 * self.lvl + 100)
        self.currentStm = self.maxStm
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

#25 xp is lvl 1 (baseline)

weapon = ['sword', 'axe', 'halberd', 'hammer', 'spear']
armour = ['chain', 'plate', 'fur']
rarity = ['novice', 'standard', 'great', 'legendary']
typeConverter = {'grunt':[[1, 2], -30], 'miniboss':[[2, 3], -15], 'boss':[[4, 4], 15]}
rarityConverter = {'n': 1.05, 's':1.15, 'g':1.25, 'l':1.4}

class Monster:
    def __init__(self, playerLvl, type):
        self.lvl = playerLvl + random.randint(-5, 5)
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
        #whether the enemy is a grunt, miniboss or boss
    
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