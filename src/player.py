from math import remainder
from functions import *
from enemy import mob_db
from items import *
import random

class Player():
    '''
    This class represents the player and information
    Name, Stats, Specific Functions
    '''
    def __init__(self):
        # XP related to the skill
        self.hp_xp = 867
        self.attack_xp = 2000
        self.strength_xp = 2000
        self.defense_xp = 2000
        self.prayer_xp = 0
        self.slayer_xp = 0
        self.agility_xp = 0
        self.crafting_xp = 0
        self.thieving_xp = 0
        # General info
        self.name = 'Player'
        self.gold = 0
        self.location = 'Lumbridge'
        self.max_hp = get_level(self.hp_xp)
        self.hp = self.max_hp
        #Slayer
        self.on_task = False
        self.task = 0
        self.init_amount = 0
        self.amount = 0
        # Style determines what XP to grant when fighting
        self.style = 'Accuracy'
        # Inventory
        self.inventory = [] # list of item objects max of 28
        self.bank = [] # infinite list of item ID's and amount

    def combat_level(self):
        '''
        Gets the players combat level
        Algorithm is loosely based on the OSRS one
        '''

        base = (1/4)*(get_level(self.defense_xp)+get_level(self.hp_xp)+(get_level(self.prayer_xp)*(1/2)))
        melee = (13/40)*(get_level(self.attack_xp)+get_level(self.strength_xp))
        final = round(base + (melee),2)
        return final

    def stats(self):
        '''
        Displays the character stats
        '''

        #clean_screen()
        print('Character Info')
        print(f'{self.name}')
        print(f'Gold: {self.gold}')
        print('Slayer')
        if self.task != 0:
            print(f'Task: {mob_db.get_mob_name(self.task)}')
        else:
            print(f'Task: None')
        print('Character Stats')
        print(f'HP: {self.hp}/{self.max_hp}')
        print(f'Attack: {get_level(self.attack_xp)} XP: {self.attack_xp}')
        print(f'Strength: {get_level(self.strength_xp)} XP: {self.strength_xp}')
        print(f'Defense: {get_level(self.defense_xp)} XP: {self.defense_xp}')
        print(f'Prayer: {get_level(self.prayer_xp)} XP: {self.prayer_xp}')
        print(f'Combat Level: {self.combat_level()}')
        print(f'Slayer: {get_level(self.slayer_xp)} XP: {self.slayer_xp}')
        print(f'Thieving: {get_level(self.thieving_xp)} XP: {self.thieving_xp}')
        print(f'Agility: {get_level(self.agility_xp)} XP: {self.agility_xp}')
        wait_input()


    def display_bank(self):
        '''

        '''
        count = 0
        print('Bank\n')
        for slot in self.bank:
            count += 1
            item = find_item_id(slot[0])
            print(f'{count}) {item["name"]} #{slot[1]}')
    
    def add_bank(self,id,amount):
        '''
        
        '''
        # check if item exist in bank
        found = False
        for item in self.bank:
            if item[0] == id:
                found = True
                item[1] += amount

        if not found:
            self.bank.append([id,amount])
        
    def remove_bank(self,id,amount):
        '''
        
        '''
        # find item in bank tuple
        for item in self.bank:
            if item[0] == id:
                item[1] += amount
                if item[1] == 0:
                    self.bank.remove(item)

    def inventory_menu(self):
        '''
        
        '''
        while True:
            try:
                clean_screen()
                self.display_inventory()
                print('1) Use\t2) Drop\t3) Info\t0) Back')
                choice = int(input(':: >> '))
            except ValueError:
                continue

            if 0 <= choice <= 3:
                if choice == 0:
                    break
                
                elif choice == 1:
                    while True:
                        try:
                            clean_screen()
                            self.display_inventory()
                            position = int(input('Use [Id] ::>> '))
                        except ValueError:
                            continue
                        # Check if ID user entered is a position inside player inventory
                        if 0 <= position <= len(self.get_inventory()):
                            if position == 0:
                                break
                            item = self.inventory[position-1]
                            if item.get_use() == 'Open':
                                value = 0
                                for stack in range(1,item.get_stack()):
                                    value += random.randint(1,item.get_value())
                                self.inventory.remove(item)
                                self.set_gold(value)

    def display_inventory(self):
        '''
        
        '''
        count = 0
        print('Inventory')
        for inv in self.inventory:
            count += 1
            print(f'{count}) {inv.get_name()} #{inv.get_stack()}')

    def get_inventory_id(self,position):
        '''
        
        '''
        item = self.inventory[position]
        id = item.get_id()
        stack = item.get_stack()
        return [id, stack]

    def add_inventory(self,id,amount):
        '''
        
        '''
        # Get item values
        item = find_item_id(id)
        remainder = 0
        # check if item exist in inventory
        found = False
        for inv in self.inventory:
            if inv.get_id() == id:
                found = True
                # Add amount to items stack
                remainder = inv.add_stack(amount)
        # Add new Item Object
        if found == False:
            if len(self.inventory) < 28:
                new_item = Item(item['id'],item['name'],item['use'],item['value'],item['max_stack'],item['stack'],item['attack'],item['strength'],item['defense'],item['hp'])
                remainder = new_item.add_stack(amount)
                self.inventory.append(new_item)
            else:
                print(f'Full inventory: Added to bank {item["name"]} #{amount}')
                self.add_bank(id, amount)
                return 0
        # If added amount to item is over its max stack; then create new items until reminder is = 0
        while True:
            if remainder != 0:
                if len(self.inventory) < 28:
                    new_item = Item(item['id'],item['name'],item['use'],item['value'],item['max_stack'],item['stack'],item['attack'],item['strength'],item['defense'],item['hp'])
                    remainder = new_item.add_stack(remainder)
                    self.inventory.append(new_item)
                else:
                    print(f'Full inventory: Added to bank {item["name"]} #{remainder}')
                    self.add_bank(id, remainder)
                    break
            else:
                break

    def remove_inventory(self,id,amount):
        '''
        
        '''
        # Get item values
        remainder = 0
        for inv in reversed(self.inventory):
            if inv.get_id() == id:
                remainder = inv.remove_stack(amount)
                amount = remainder
                if remainder <= 0:
                    self.inventory.remove(inv)
                elif remainder >= 0:
                    break

        # check if amount removing makes stack = 0; remove from inventory list

        # keep item in inv just update the removed amount from stack

    def slayer_assigned(self,set,id,amount):
        self.on_task = set
        self.task = id
        self.init_amount = amount
        self.amount = 0

    def slayer_completed(self):
        self.on_task = False
        self.task = 0
        self.init_amount = 0
        self.amount = 0

    def rest(self):
        '''
        Resets players HP back to full
        '''
        self.hp = self.max_hp

    def change_style(self):
        '''
        Switches the attack stance for the player
        Stances affect how xp is allocated
        '''

        while True:
            try:
                clean_screen()
                print('Style')
                print('1) Accuracy\n2) Power\n3) Guard\n0) Exit')
                choice = int(input(':: >> '))
            except:
                continue
            if choice == 1:
                self.set_style('Accuracy')
                break
            elif choice == 2:
                self.set_style('Power')
                break
            elif choice == 3:
                self.set_style('Guard')
                break

    def combat_xp(self,xp):
        '''
        Depending on style used by the player; allocate xp to that stats
        XP is = to damage given * 4
        -   Accuracy: Attack xp
        -   Power: Strength xp
        -   Guard: Defense xp

        @return:
        -   XP gained for each stat for post combat information
        '''
        attack = 0
        strength = 0
        defense = 0

        if self.style == 'Accuracy':
            self.set_attack(xp*4)
            attack = xp*4
        elif self.style == 'Power':
            self.set_strength(xp*4)
            strength = xp*4
        elif self.style == 'Guard':
            self.set_defense(xp*4)
            defense = xp*4
        return attack,strength,defense

    #-------------------- Getters --------------------
    def get_name(self):
        return self.name
    def get_gold(self):
        return self.gold
    def get_max_hp(self):
        return self.max_hp
    def get_hp(self):
        return self.hp
    def get_style(self):
        return self.style
    def get_attack(self):
        return get_level(self.attack_xp)
    def get_strength(self):
        return get_level(self.strength_xp)
    def get_defense(self):
        return get_level(self.defense_xp)
    def get_hp_xp(self):
        return get_level(self.hp_xp)
    def get_thieving(self):
        return get_level(self.thieving_xp)
    def get_agility(self):
        return get_level(self.agility_xp)
    def get_location(self):
        return self.location
    def get_on_task(self):
        return self.on_task
    def get_task(self):
        return self.task
    def get_init_amount(self):
        return self.init_amount
    def get_amount(self):
        return self.amount
    def get_inventory(self):
        return self.inventory
    def get_bank(self):
        return self.bank

    #-------------------- Setters --------------------
    def set_name(self, name):
        self.name = name
    def set_gold(self, gold):
        self.gold += gold
    def set_hp(self, hp):
        self.hp += hp
        if self.hp <= 0:
            self.hp = 0
    def set_style(self, style):
        self.style = style
    def set_attack(self, xp):
        self.attack_xp += xp
    def set_strength(self, xp):
        self.strength_xp += xp
    def set_defense(self, xp):
        self.defense_xp += xp
    def set_hp_xp(self, xp):
        self.hp_xp += xp
    def set_location(self, location):
        self.location = location
    def set_amount(self, amount):
        self.amount += amount
    def set_slayer_xp(self, xp):
        self.slayer_xp += xp
    def set_thieving_xp(self, xp):
        self.thieving_xp += xp
    def set_agility_xp(self, xp):
        self.agility_xp += xp