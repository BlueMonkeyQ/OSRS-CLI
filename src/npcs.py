import random
from functions import *
from enemy import mob_db

def get_npc_info(option):
    '''
    Search npcs.json for selected npc and
    return all information related to it

    @args:
    -   npc choice

    @returns:
    -   Dictionary of the npc data
    '''
    for npc in npcs['npcs']:
        if npc['name'] == option:
            return npc

def npc_menu(player, areas):
    '''
    Displays all npcs in current area
    @args:
    -   player object
    -   current area dictionary
    '''

    while True:
        try:
            count = 0
            clean_screen()
            print(f'{player.get_location()} - NPCs\n')
            for npc in areas['npcs']:
                count += 1
                print(f'{count}) {npc}')
            print('0) Back')
            choice = read_input(player)
        except ValueError:
            continue

        if 0 <= choice <= count:
            if choice == 0:
                break
            npc_dialog(player,get_npc_info(areas['npcs'][choice-1]))

def npc_dialog(player, npc):
    '''
    Displays a npcs dialog options
    @args:
    -   player object
    -   shop dictionary
    '''

    while True:
        try:
            count = 0
            clean_screen()
            print(f'{npc["name"]}\n')

            # Slayer NPC
            if npc['slayer'] == 1:
                count += 1
                print(f'{count}) Task')
                count += 1
                print(f'{count}) About')
                if player.get_on_task() == True:
                    count += 1
                    print(f'{count}) Help')

            # Thieving NPC
            if npc['thieving'] == 1:
                count += 1
                print(f'{count}) PickPocket')
            
            print('0) Back')
            choice = read_input(player)
        except ValueError:
            continue

        if 0 <= choice <= count:
            if choice == 0:
                break

            # Slayer
            if npc['slayer'] == 1:
                if choice == 1:
                    assign_slayer_task(player, npc['assign'], npc['amount'])
                elif choice == 2:
                    clean_screen()
                    print(f'{npc["name"]}\n')
                    print('Available Task')
                    for task in npc['assign']:
                        e = mob_db.get_mob(task)
                        print(f'{e.get_name()} Lvl: {e.combat_level()}')
                    print(f'Average Combat Lvl {mob_db.get_average_combat_lvl(npc["assign"])}')
                    wait_input()
                elif choice == 3:
                    e = mob_db.get_mob(player.get_task())
                    print('Your currently on a task')
                    print(f'Kill {player.get_amount()} {e.get_name()}s')
                    print(f'Killed: {player.get_amount()}/{player.get_init_amount()}')
                    print(f'{e.get_name()}s are found at:')
                    for area in e.get_locations():
                        print(area)

            # Thieving
            if npc['thieving'] == 1:
                if choice == 1:
                    # Check if players thieving level meets the requirement
                    if player.get_thieving() >= npc['req']:
                        # Check if health is above 0
                        if player.get_hp() != 0:
                            while True:
                                xp_gained = 0
                                chance = round(npc['chance'] + (player.get_thieving()/3),2)
                                roll = random.randint(1,100)
                                if roll <= chance:
                                    print(f'Pickpocketing {npc["name"]}... Successfull')
                                    player.add_inventory(npc['drop_table'][0],1)
                                    player.set_thieving_xp(npc['xp'])
                                    xp_gained += npc['xp']
                                # Failed - take damage
                                else:
                                    print(f'Pickpocketing {npc["name"]}... Youve been caught and hit')
                                    player.set_hp(-2)
                                    wait_input()
                                    break
                        else:
                            print('Cant Pickpocket with no HP')
                    else:
                        print(f'Need level {npc["req"]} in order to pickpocket')



def assign_slayer_task(player, assign, amount):
    '''
    Assignes a slayer task to the player based upon the options of the slayer master
    Can only assign a slayer task if there is none active

    @args:
    -   player object
    -   assign: list of available slayer task
    -   amount: base number of task amount
    '''

    id = random.randint(0,len(assign)-1)
    id = assign[id]
    amount = random.randint((amount*.5),amount+(amount*.5))

    if player.get_on_task() == False:
        print('New Slayer Task')
        print(f'Kill {amount} {mob_db.get_mob_name(id)}s')
        player.slayer_assigned(True,id,amount)
    else:
        print('Your currently on a task')
        print(f'Kill {player.get_init_amount()} {mob_db.get_mob_name(player.get_task())}s')
    wait_input()
