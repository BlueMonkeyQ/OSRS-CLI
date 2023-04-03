from functions import *
import random

def agility_menu(player):
    '''
    
    '''
    while True:
        try:
            clean_screen()
            print(f'{player.get_location()} Agility Course\n')
            print('1) Agility\t0) Back')
            choice = read_input(player)
        except ValueError:
            continue

        if 0 <= choice <= 1:
            if choice == 0:
                break
            elif choice == 1:
                if player.get_hp() > 0:
                    agility_course(player)
                else:
                    print('Hp is 0')

def agility_course(player):
    '''
    
    '''
    # Get players location and check if they meet skill requirment
    if player.get_location() == 'Draynor Village':
        if player.get_agility() >= 0:
            count = 1
            for section in range(1,6):
                chance = round(70 + (player.get_agility()/3),2)
                roll = random.randint(1,100)
                if roll <= chance:
                    count += 1
                    xp = 16.75
                    print(f'Rooftop Section: {count}... Successfull +{xp} xp')
                    player.set_agility_xp(xp)
                else:
                    print(f'Rooftop Section: {count}... Failed -2 hp')
                    player.set_hp(-2)
                    wait_input()
                    break
            if count == 5:
                xp = 41.8
                print(f'Draynor Village Agility Course Completed! +{xp} xp')
                player.set_agility_xp(xp)
                wait_input()
    elif player.get_location() == 'Al Kharid':
        if player.get_agility() >= 12:
            count = 1
            for section in range(1,8):
                chance = round(70 + (player.get_agility()/3),2)
                roll = random.randint(1,100)
                if roll <= chance:
                    count += 1
                    xp = 28.6
                    print(f'Rooftop Section: {count}... Successfull +{xp} xp')
                    player.set_agility_xp(xp)
                else:
                    print(f'Rooftop Section: {count}... Failed -2 hp')
                    player.set_hp(-2)
                    wait_input()
                    break
            if count == 5:
                xp = 86.5
                print(f'Draynor Village Agility Course Completed! +{xp} xp')
                player.set_agility_xp(xp)
                wait_input()
        else:
            print('Agility Requirement: 12')
            wait_input()
