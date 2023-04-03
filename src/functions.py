import sys
import json
from pathlib import Path

map_path = Path('data/map.json')
with open(map_path) as file: map = json.load(file)

npc_path = Path('data/npcs.json')
with open(npc_path) as file: npcs = json.load(file)

shop_path = Path('data/shops.json')
with open(shop_path) as file: shops = json.load(file)

def save():
    '''
    WIP
    '''
    pass

def end():
    '''
    WIP
    '''
    sys.exit()

def clean_screen():
    '''
    Clears the screen
    '''
    print('\n'*20)

def wait_input():
    '''
    Pauses the screen until user enters
    '''
    temp = input(':: >> ')

def read_input(player):
    '''
    Read in user input and check if that input is a 
    valid global command or integer
    @args:
    -   player object

    @returns:
    -   Valid integer input
    '''

    try:
        choice = input(':: >> ')
        commands(player, choice)
        choice = int(choice)
        return choice
    except ValueError:
        raise
    except SystemExit:
        sys.exit()


def get_level(stat):
    '''
    Returns the level of the given stat based upon the xp amount
    Every level is a 15% increase from the next
    '''
    level = 1
    next_level = 2
    while True:
        xp_needed = int(((next_level-1)+(300*2)*((next_level-1)/7)))
        if stat >= xp_needed:
            level += 1
            next_level += 1
        else:
            break
    return level

def display_xp_levels():
    '''
    Testing Purpose Only as of now
    Displays Each level and the XP needed to reach
    '''

    level = 0
    for i in range(1,100):
        level = i
        next_level = i+1
        xp_needed = int(((next_level-1)+(300*2)*((next_level-1)/7)))
        print(level, xp_needed)

def commands(player, choice):
    '''
    List of global the commands the player can use from anywhere
    '''

    if choice.lower() == 'c':
        player.stats()
    elif choice.lower() == 'i':
        player.inventory_menu()
    elif choice.lower() == 's':
        save()
    elif choice.lower() == 'e':
        raise SystemExit

def payment(player, amount):
    '''
    
    '''
    if player.get_gold() >= amount:
        player.set_gold(-amount)
        return True
    else:
        return False