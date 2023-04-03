from functions import get_level
from pathlib import Path
import json

class MobDB():

    def __init__(self):
        self.mob_list = []
        
        filepath = Path('data/mobs.json')
        with open(filepath) as file: data = json.load(file)

        for _ in data['mobs']:
            mob = Mob(_['id'],_['name'],_['gold'], _['max_hp'], _['attack'], _['strength'], _['defense'],_['locations'],_['drop_table'])
            self.mob_list.append(mob)
            

    def get_mob(self, id):
        for _ in self.mob_list:
            if(_.get_id() == id):
                return _

    def get_mob_name(self, id):
        for _ in self.mob_list:
            if(_.get_id() == id):
                return _.get_name()

    def get_area_mobs(self,location):
        mobs = []
        for _ in self.mob_list:
            if location in _.get_locations():
                mobs.append(_)
        return mobs

    def get_average_combat_lvl(self,ids):
        combat_lvl = 0
        for id in ids:
            mob = self.get_mob(id)
            combat_lvl += mob.combat_level()
        average = round(combat_lvl/len(ids),2)
        return average
    

    def display_mobs(self):
        print(self.mob_list)
        
class Mob():
    '''
    This class represents the mob and information
    Name, Stats, Specific Functions
    '''

    def __init__(self, id, name, gold, max_hp, attack, strength, defense, locations, drop_table):
        self.id = id
        self.name = name
        self.gold = gold
        self.max_hp = get_level(max_hp)
        self.hp = self.max_hp
        self.locations = locations
        self.drop_table = drop_table
        # XP related to the skill
        self.attack_xp = attack
        self.strength_xp = strength
        self.defense_xp = defense
        self.prayer_xp = 0

    def reset_hp(self):
        self.hp = self.max_hp

    def combat_level(self):
        '''
        Gets the players combat level
        Algorithm is loosely based on the OSRS one
        '''

        base = (1/4)*(get_level(self.defense_xp)+get_level(self.max_hp)+(get_level(self.prayer_xp)*(1/2)))
        melee = (13/40)*(get_level(self.attack_xp)+get_level(self.strength_xp))
        final = round(base + (melee),2)
        return final

    #-------------------- Getters --------------------
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_gold(self):
        return self.gold
    def get_max_hp(self):
        return self.max_hp
    def get_hp(self):
        return self.hp
    def get_attack(self):
        return get_level(self.attack_xp)
    def get_strength(self):
        return get_level(self.strength_xp)
    def get_defense(self):
        return get_level(self.defense_xp)
    def get_locations(self):
        return self.locations
    def get_drop_table(self):
        return self.drop_table

    #-------------------- Setters --------------------
    def set_hp(self, hp):
        self.hp += hp

mob_db = MobDB()