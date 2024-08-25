import random

def player_combat(player, monster, button_pressed, monsterDodgeValue = 75):
    if button_pressed == 'attack' and player.get_currentStm >= 5:
        player.set_currentStm(-5)
        if random.randint(1, 100) < monsterDodgeValue:
            monster.set_currentHp(-(player.get_atk * player.get_weaponModifier * monster.get_armourModifier * monsterDodgeValue))
        playerDodgeValue = 75
    elif button_pressed == 'heavy attack' and player.get_currentStm >= 15:
        player.set_currentStm(-15)
        if random.randint(1, 100) < monsterDodgeValue + 15:
            monster.set_currentHp(-(player.get_atk * 1.5 * player.get_weaponModifier * monster.get_armourModifier * monsterDodgeValue))
        playerDodgeValue = 100
    elif button_pressed == 'dodge':
        player.set_currentStm(25)
        if player.get_currentStm > player.get_maxStm:
            player.set_currentStm(player.get_maxStm)
        playerDodgeValue = 25
    elif button_pressed == 'special':
        player.special_atk()

def monster_combat(player, monster, playerDodgeValue = 75):
    if monster.get_currentStm <= 5:
        monster.set_currentStm(25)
        if monster.get_currentStm > monster.get_maxStm:
            monster.set_currentStm(monster.get_maxStm)
        monsterDodgeValue = 25
    

player_combat(Human(100), Human(20), 'attack')