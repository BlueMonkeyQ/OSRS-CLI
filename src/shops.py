from functions import *
from items import find_item_id

def get_shop_info(option):
    '''
    Searches shop dictionary for a shop that matches players option
    @args:
    -   option: shop dictionary name value

    @returns:
    -   shop entry
    '''

    for shop in shops['shops']:
        if shop['name'] == option:
            return shop

def shop_menu(player, areas):
    '''
    Displays all shops in current area
    @args:
    -   player object
    -   current area dictionary
    '''
    
    while True:
        try:
            count = 0
            clean_screen()
            print(f'{player.get_location()} - Shops\n')
            for shop in areas['shops']:
                count += 1
                print(f'{count}) {shop}')
            print('0) Back')
            choice = read_input(player)
        except ValueError:
            continue

        if 0 <= choice <= count:
            if choice == 0:
                break
            shop_dialog(player,get_shop_info(areas['shops'][choice-1]))

def shop_dialog(player, shop):
    '''
    Displays a shops inventory
    @args:
    -   player object
    -   shop dictionary
    '''

    while True:
        try:
            count = 0 # Track available user input choices
            clean_screen()
            print(f'{shop["name"]}\n')
            # Shop sells Items
            if shop['inv'] == 1:
                for id in shop['inventory']:
                    count += 1
                    item = find_item_id(id)
                    print(f'{count}) {item["name"]} {item["value"]}')
            # Shop sells service
            if shop['service'] == 1:
                items = list(shop['services'].keys())
                for item, price in shop['services'].items():
                    count += 1
                    print(f'{count}) {item} {price}')
            print('0) Back')
            choice = read_input(player)
        except:
            continue

        if 0 <= choice <= count:
            if choice == 0:
                break
            if shop['inv'] == 1:
                # Get amount player wants to buy
                while True:
                    try:
                        amount = int(input('Amount ::>> '))
                    except:
                        continue
                    if 0 <= amount <= 1000000:
                        break
                # Attempt to see if the player can afford the item
                item = find_item_id(shop['inventory'][choice-1])
                price = amount * item["value"]
                if payment(player,price):
                    player.add_inventory(item["id"],amount)
                else:
                    print('You dont have enough GP!')
            elif shop['service'] == 1:
                # Attempt to see if the player can afford the service
                if payment(player,shop['service'][items[choice-1]]):
                    print(f'Purchased: {items[choice-1]}!')