import random
from classes import Human

def player_combat(player, monster, button_pressed, monsterDodgeValue = 75):
    playerStm = player.get_currentStm
    playerMaxStm = player.get_maxStm
    playerAtk = player.get_atk
    playerWpnMod = player.get_weaponModifier
    monsterAmrMod = monster.get_armourModifier
    if button_pressed == 'attack' and playerStm >= 5:
        player.update_currentStm(-5)
        playerStm -= 5
        if random.randint(1, 100) < monsterDodgeValue:
            monster.update_currentHp(-(playerAtk * playerWpnMod * monsterAmrMod))
        return 75
    #the player dodge value
    elif button_pressed == 'heavy attack' and playerStm >= 15:
        player.update_currentStm(-15)
        if random.randint(1, 100) < monsterDodgeValue + 15:
            monster.update_currentHp(-(playerAtk * 1.5 * playerWpnMod * monsterAmrMod))
        return 100
    elif button_pressed == 'dodge':
        player.set_currentStm(25)
        if playerStm > playerMaxStm:
            player.set_currentStm(playerMaxStm)
        return 25
    elif button_pressed == 'special' and playerStm >= 50:
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

player_combat(Human(100), Human(20), 'attack')
