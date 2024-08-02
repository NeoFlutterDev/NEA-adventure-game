import math

class Race:
    def __init__(self, exp):
        self.exp = exp
        self.lvl = math.trunc(2.5 * (math.sqrt(self.exp) - 5))
        self.armour = None
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

    def get_exp(self):
        return self.exp

    def set_armour(self, armour):
        self.armour = armour

    def get_armour(self):
        return self.armour

    def update_atk(self):
        self.atk = math.trunc(1.5 * self.lvl + 100)

    def get_atk(self):
        return self.atk
    
    def update_maxHp(self):
        self.maxHp = math.trunc(((self.lvl / 4.624) + 10)**2)

    def get_maxHp(self):
        return self.maxHp

    def set_currentHp(self, hpGain):
        self.currentHp = self.currentHp + hpGain
        #if health has been lost enter a negative value for hpGain

    def get_currentHp(self):
        return self.currentHp
    
    def update_maxStm(self):
        self.maxStm = math.trunc(4 * self.lvl + 100)

    def get_maxStm(self):
        return self.maxStm

    def update_currentStm(self, stmGain):
        self.currentStm = self.currentStm = stmGain
        #if stamina has been lost enter a negative value for stmGain

    def get_currentStm(self):
        return self.currentStm
        
        
class Human(Race):
    def __init__(self, exp):
        super().__init__(exp)
        self.hp = self.hp * 1.5      

human = Human(25)
print(human.hp)
print(human.lvl)
print(human.atk)
print(human.stm)
