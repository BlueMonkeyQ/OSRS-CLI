import player
from maps import world_map
from functions import *

def main_menu():
    while True:
        try:
            clean_screen()
            print('Main Menu')
            print('1) New Game\n2) Load Game\n3) Help\n0) Exit')
            choice = int(input(':: >> '))
        except ValueError:
            continue

        if choice == 1:
            p = player.Player()
            new_game(p)
            world_map(p)

        elif choice == 2:
            p = player.Player()
            # p.add_inventory(25,100)
            load_game()
            world_map(p)

        elif choice == 3:
            info()

        elif choice == 0:
            break

def new_game(player):
    '''
    Create a new instance of a player class
    Assign it a name given by the user    
    '''

    print('Enter in your Characters name')
    name = input(':: >> ')
    player.set_name(name)


def load_game():
    pass

def info():
    pass

if __name__ == '__main__':
    main_menu()

    # Testing
    # display_xp_levels()
    # p = player.Player()
    # p.add_inventory(0,1000)
    # bank_menu(p)
    # p.remove_inventory(0,-11)
    # p.stats()
    # p.add_inventory(0,10)
    # p.remove_inventory(0,-3)
    # p.stats()
