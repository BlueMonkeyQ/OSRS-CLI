from battle import battle_init
from functions import *
from shops import shop_menu
from npcs import npc_menu
from enemy import mob_db
from skills import agility_menu


def get_area_info(location):
    '''
    Search maps.json for players current location and
    return all information related to it

    @args:
    -   Player location

    @returns:
    -   Dictionary of the location data
    '''

    for area in map['locations']:
        if area['name'] == location:
            return area

def world_map(player):
    '''
    Menu for traveling. Adjust routes depending on players current location
    If a location allows fighting, then a extra route option 'fight' is available

    @args:
    -   player object
    -   mobs_db object
    '''

    while True:
        # Signifies option for player to pick from
        count = 0
        area_count = 0
        combat_choice = 0
        shop_choice = 0
        bank_choice = 0
        agility_choice = 0
        toll_choice = 0
        shortcut_choice = 0
        # Gets all available routes based on current location
        areas = get_area_info(player.get_location())
        try:
            # Prints Journey Menu
            clean_screen()
            print(f'{player.get_location()}\n')
            
            # Combat
            if areas['combat'] == 1:
                count += 1
                combat_choice = count
                print(f'{count}) Fight')

            # City
            if areas['city'] == 1:
                count += 1
                shop_choice = count
                print(f'{count}) Shops')
                count += 1
                npc_choice = count
                print(f'{count}) NPCs')
            
            #Bank
            if areas['bank'] == 1:
                count += 1
                bank_choice = count
                print(f'{count}) Bank')

            # Agility
            if areas['agility'] == 1:
                count += 1
                agility_choice = count
                print(f'{count}) Rooftop')

            # Toll
            if areas['toll'] == 1:
                count += 1
                toll_choice = count
                print(f'{count}) Toll Gate')

            # Shortcut
            if areas['shortcut'] == 1:
                count += 1
                shortcut_choice = count
                print(f'{count}) Shortcut')

            area_count = count+1
            # Surrounding Areas
            for area in areas['areas']:
                count += 1
                print(f'{count}) {area}')

            choice = read_input(player)
        except ValueError:
            continue
        
        # Sets the range of allowed inputs between 1 and number of areas
        if 1 <= choice <= count:

            if choice == combat_choice and areas['combat'] == 1:
                battle_init(player,player.get_location(),mob_db)
            
            elif choice == shop_choice and areas['city'] == 1:
                shop_menu(player,areas)

            elif choice == bank_choice and areas['bank'] == 1:
                bank_menu(player)
            
            elif choice == agility_choice and areas['agility'] == 1:
                agility_menu(player)

            elif choice == npc_choice and areas['city'] == 1:
                npc_menu(player,areas)

            elif choice == toll_choice and areas['toll'] == 1:
                toll_menu(player,areas)

            elif choice == shortcut_choice and areas['shortcut'] == 1:
                shortcut_menu(player)
            else:
                player.set_location(areas['areas'][choice-area_count])

def toll_menu(player,areas):
    '''
    
    '''
    while True:
        try:
            count = 1
            clean_screen()
            print(f'{player.get_location()} - Toll Gate\n')
            print(f'{count}) 10 GP')
            print('0) Back')
            choice = read_input(player)
        except ValueError:
            continue
            
        if choice == 0:
            break
        elif choice == 1:
            if payment(player,10):
                print('true')
                if player.get_location() == "East Lumbridge":
                    player.set_location('Al Kharid')
                    break
                elif player.get_location() == "Al Kharid":
                    player.set_location('East Lumbridge')
                    break
            else:
                if player.get_location() == "East Lumbridge":
                    print('Cant cross into Al Kharid unless you pay the Toll fee')
                elif player.get_location() == "Al Kharid":
                    print('Cant cross into East Lumbridge unless you pay the Toll fee')

def shortcut_menu(player):
    '''
    
    '''
    
    if player.get_location() == 'Lumbridge Swamp':
        # Skill check
        if player.get_agility() >= 20:
            player.set_location('Al Kharid')
        else:
            print('Agility Requirement: 1')
            wait_input()

    elif player.get_location() == 'Al Kharid':
        # Skill check
        if player.get_agility() >= 20:
            player.set_location('Lumbridge Swamp')
        else:
            print('Agility Requirement: 1')
            wait_input()

def bank_menu(player):
    '''
    
    '''
    while True:
        try:
            player.display_bank()
            player.display_inventory()
            print('1) Add\t2) Remove\t3)Info\t0) Back')
            choice = read_input(player)
        except:
            continue
        print(len(player.get_inventory()))
        if 0 <= choice <= 3:
            # Add item from inv to bank
            if choice == 1:
                while True:
                    player.display_bank()
                    player.display_inventory()
                    position = 0
                    amount = 0
                    try:
                        position,amount = [int(_) for _ in input("Add [Id,Amount] ::>> ").split()]
                    except TypeError:
                        if position == 0:
                            break
                        continue
                    except ValueError:
                        print(position,amount)
                        if position == 0:
                            break
                        continue
                    # Check if ID user entered is a position inside player inventory
                    # and amount is more then 0
                    if 0 <= position <= len(player.get_inventory()):
                        if amount > 0:
                            # get ID and stack of item object of players choice
                            id, stack = player.get_inventory_id(position-1)
                            # if amount to put in is greater then amount in inventory, then put in max amount
                            if amount > stack:
                                amount = stack
                            player.add_bank(id,amount)
                            player.remove_inventory(id,-amount)

            elif choice == 2:
                while True:
                    player.display_bank()
                    player.display_inventory()
                    position = 0
                    amount = 0
                    try:
                        position,amount = [int(_) for _ in input("Remove [Id,Amount] ::>> ").split()]
                    except TypeError:
                        if position == 0:
                            break
                        continue
                    except ValueError:
                        print(position,amount)
                        if position == 0:
                            break
                        continue
                    # Check if ID user entered is a position inside player inventory
                    # and amount is more then 0
                    if 0 <= position <= len(player.get_bank()):
                        if amount > 0:
                            # get ID and stack of item object of players choice
                            id, stack = player.get_bank()[position-1]
                            # if amount to put in is greater then amount in inventory, then put in max amount
                            if amount > stack:
                                amount = stack
                            player.add_inventory(id,amount)
                            player.remove_bank(id,-amount)
            elif choice == 3:
                print('WIP')
                wait_input()
            
            elif choice == 0:
                break