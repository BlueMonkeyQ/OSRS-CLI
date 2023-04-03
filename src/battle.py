import enemy
import random
import math
from functions import *

# Used to track xp gained for each stat within the fight
attack = 0
strength = 0
defense = 0
hp = 0

def xp_track(a,s,d,h):
    '''
    Allocate combat xp to the appropriate stat for tracking in post combat
    '''
    # Allows us to mutate global variables for tracking xp
    global attack
    global strength
    global defense
    global hp

    attack += a
    strength += s
    defense += d
    hp += h


def battle_init(player,location,mob_db):
    '''
    Where we initialize a enemy for the player to fight
    This depends on the players location
    Gets a list of available mobs within the current location
    Chooses one at random

    @args:
    -   player object
    -   players location
    -   mob_db object
    '''

    # Wont let the player attempt a fight if they have 0 hp
    if player.get_hp() > 0:
        # Gets list of available mobs based on location
        mobs = mob_db.get_area_mobs(location)

        # For locations that only have 1 location
        if len(mobs) == 1:
            e = mobs[0]
        # Chooses a mob at random from the list
        else:
            mob = random.randint(0,len(mobs)-1)
            e = mobs[mob]

        battle_menu(player,e)

def battle_menu(player,e):
    '''
    Where the Player interacts with the fight
    Displays both the player and the enemy's: Name, HP
    Fight: Calls combat()
    Style: Calls player.style()
    Stats: Calls player.stats()
    Run: Flee from battle and return to hub()
    '''
    
    # Run until either the player wins/loses or runs
    while True:
        # Catch non integer inputs
        try:
            print(f'{e.get_name():<10} - {e.get_hp():>3}/{e.get_max_hp():<3} {"#"*hp_ticks(e.get_hp(),e.get_max_hp())}')
            print(f'{player.get_name():<10} - {player.get_hp():>3}/{player.get_max_hp():<3} {"#"*hp_ticks(player.get_hp(),player.get_max_hp())}')
            print(f'Style {player.get_style()}')
            print(f'1) Fight\n2) Style\n0) Run')
            choice = read_input(player)
        except ValueError:
            continue
        if choice == 1:
            # Returns to journey() on a win/lose
            if not combat(player, e):
                e.reset_hp()
                break
        elif choice == 2:
            # Display the style screen
            player.change_style()
        elif choice == 0:
            # return to journey()
            e.reset_hp()
            break

def post_battle_win(player, e):
    '''
    WIP
    '''
    print('Win')
    print('Gold Gained')
    print(f'Gold: {e.get_gold()}')
    print('XP Gained')
    print(f'Attack XP: {attack}')
    print(f'Strength XP: {strength}')
    print(f'Defense XP: {defense}')
    print(f'Hp XP: {hp}')
    #Slayer
    if player.get_on_task() == True:
        if player.get_task() == e.get_id():
            player.set_amount(1)
            player.set_slayer_xp(e.get_max_hp()*1000)
            print(f'Slayer XP: {e.get_max_hp()*1000}')
            print(f'Slayer Progress {player.get_amount()}/{player.get_init_amount()}')
        if player.get_amount() == player.get_init_amount():
            player.slayer_completed()
            print('Slayer Task Completed')

    player.set_gold(e.get_gold())

    # Drop Table
    for drop in e.get_drop_table():
        chance = (drop[1]/100)*100
        roll = random.randint(0,100)
        print(f'Chance: {chance} Roll: {roll}')
        if roll <= chance:
            amount = random.randint(1,drop[2])
            print(f'Amount: {amount}')
            if amount != 0:
                player.add_inventory(drop[0],amount)

    wait_input()

def post_battle_lose(player):
    '''
    WIP
    '''
    print('Lose')
    print('XP Gained')
    print(f'Attack XP: {attack}')
    print(f'Strength XP: {strength}')
    print(f'Defense XP: {defense}')
    print(f'Hp XP: {hp}')
    wait_input()

def combat(player, e):
    '''
    Combat Log where it displays damage given and taken via player and enemy
    Player always starts 1st
    -   Call hit_chance() determine if player/enemy rolled a hit
    -   Call damage() to roll the damage given to player/enemy

    If enemy hp <= 0 -> WIN; If player hp <= 0 -> LOSE

    @args:
    -   player object
    -   enemy object

    @return:
    -   return True if neither parties win
    -   return False if one party wins
    '''

    print('Combat Console')
    # True if player rolled a hit chance
    if hit_chance(player.get_attack(),e.get_defense()):
        # Damage given
        dmg = damage(player.get_strength())
        # Allocate XP of damage given based upon style used
        h = 0
        a, s, d = player.combat_xp(dmg)
        xp_track(a,s,d,h)
        # subtract the enemy hp by damage
        e.set_hp(-dmg)
        print(f'Player Hit: {dmg}')
    # False hit chance aka they missed
    else:
        print('Player Hit 0')
    # Check if enemy died from player's hit
    if e.get_hp() <= 0:
        # return to hub()
        post_battle_win(player, e)
        return False
    # Enemy is still alive
    else:
        # True if enemy rolled a hit chance
        if hit_chance(e.get_attack(),player.get_defense()):
            # Damage given
            dmg = damage(e.get_strength())
            # Allocate XP of damage given based upon style used
            h = dmg
            a, s, d = 0,0,0
            xp_track(a,s,d,h)
            # subtract player hp by damage
            player.set_hp(-dmg)
            # Allocate HP xp based upon damage taken
            print(f'Enemy Hit: {dmg}')
        # False hit chance aka they missed
        else:
            print('Enemy Hit 0')
    # Checks if player died from enemy's hit
    if player.get_hp() <= 0:
        # return to hub()
        post_battle_lose(player)
        return False
    # Nobody died, return to battle_menu()
    return True

def hit_chance(attack, defense):
    '''
    Takes the attackers attack level
    Takes the defenders defense level
    Algorithm for hit chance is loosely based on how OSRS does it

    -   If attack is >= defense:    (1 - ((defense+2)/(2*(attack+1))))*100
    -   If attack < defense:        (attack/(2*(defense+1)))*100

    Then rolls a number between 1-100 and hits if roll is <= chance
    @args:
    -   

    @returns:
    -   True if roll was within chance range
    -   False if roll was outside chance range
    '''
    
    # If the attackers attack level is >= the defenders defense level
    if attack >= defense:
        chance = int((1 - ((defense+2)/(2*(attack+1))))*100)
    # The attackers attack level is < the defenders defense level
    else:
        chance = int((attack/(2*(defense+1)))*100)
    # Roll a random number between 1-100
    roll = random.randint(1,100)
    # If roll is within the range of chance
    if roll <= chance:
        return True
    # Roll was outside the range of chance
    else:
        return False

def damage(strength):
    '''
    Rolls the amount of damage; Loosely based on how OSRS does it
    -   max hit: ((.5*(strength+64))/640)*100
    -   roll: random number between 1-max hit

    @args:
    -   strength level of party

    @returns: 
    -   roll as damage
    '''

    # Set the Max Hit possible based upon the parties strength stat
    max = int(((.5*(strength+64))/640)*100)
    # Roll between 1-Max
    roll = random.randint(1,max)
    return roll

def hp_ticks(hp,max_hp):
    '''
    Calculate the number of HP ticks to display ranging from 0-10
    based upon the current hp and max hp

    @args:
    -   current hp of the party
    -   max hp of the party

    @returns: 
    -   number of ticks 
    '''

    # Normalize the percent between hp & max hp to a scale of 100
    percent = (hp/max_hp)*100
    # Take that percent and reduce it to a scale of 10 rounded down
    ticks = math.floor(percent/10)
    return ticks