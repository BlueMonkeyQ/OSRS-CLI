from itertools import count
from math import remainder
from pathlib import Path
import json

filepath = Path('data/items.json')
with open(filepath) as file: data = json.load(file)
item_list = data['items']

def find_item_id(id):
    for _ in item_list:
        if _['id'] == id:
            return _

class Item():
    '''
    
    '''

    def __init__(self,id,name,use,value,max_stack,stack,attack,strength,defense,hp):
        self.id = id # id
        self.name = name  # name
        self.use = use # how item can be used
        self.value = value  # gold value
        self.max_stack = max_stack  # max number player can stack in inv
        self.stack = stack  # current stack amount
        self.attack = attack  # attack bonus
        self.strength = strength  # strength bonus
        self.defense = defense  # defense bonus
        self.hp = hp  # heal hp amount

    #-------------------- Getters --------------------
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_use(self):
        return self.use
    def get_value(self):
        return self.value
    def get_max_stack(self):
        return self.max_stack
    def get_stack(self):
        return self.stack
    def get_attack(self):
        return self.attack
    def get_strength(self):
        return self.strength
    def get_defense(self):
        return self.defense
    def get_hp(self):
        return self.hp

    #-------------------- Setters --------------------
    def add_stack(self,amount):
        # Check if stack is at limit
        if self.stack == self.max_stack:
            return amount
        self.stack += amount
        if self.stack > self.max_stack:
            remainder = self.stack - self.max_stack
            self.stack = self.max_stack
            return remainder
        return 0
    
    def remove_stack(self,amount):
        self.stack += amount
        if self.stack == 0:
            return 0
        else:
            return self.stack
