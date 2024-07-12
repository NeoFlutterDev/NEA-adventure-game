import math

class Race:
    def __init__(self, exp):
        self.exp = exp
        self.lvl = math.trunc(2.5 * (math.sqrt(self.exp) - 5))
        self.armour = None
        self.atk = math.trunc(1.5 * self.lvl + 100)
        self.hp = math.trunc(((self.lvl / 4.624) + 10)**2)
        self.stm = math.trunc(4 * self.lvl + 100)
        #defines the base stats of the player
        #as levels go up, health increases the most, followed by stamina, followed by attack
        
class Human(Race):
    def __init__(self, exp):
        

human = Race(25)
print(human.hp)
print(human.lvl)
print(human.atk)
print(human.stm)
