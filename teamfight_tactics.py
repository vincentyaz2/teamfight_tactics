'''
Script to help Teamfight Tactics players build 

TODO: 
- move the utility methods to a utility module
- build GUI
- move GUI code in a separate file

'''

'''
Glossary: 

ad for attack damage
as for attack speed
ap for ability power
mn for mana
ar for armor
mr for magic resist
hp for health points
wi for wildcard

'''

from pprint import pprint
from typing import List, Tuple, Type
import json

with open('data.json') as f:
    data = json.load(f)

basic_stats = data['basic_stats']
combination_stats = data['combination_stats']
combination_specials = data['combination_specials']


# returns Dict that maps items to the format stored in the json file
# ex: 'ad ap' and 'ap ad' will both give 'ad ap' 
# I should've stored both combinations in the json file, my bad. 
def get_specials_keys_mapper():
    keys = data['combination_specials'].keys()
    hashtable = {}

    for key in keys:
        t = tuple(key.split())
        a = t[0]
        b = t[1]
        nk1 = a + ' ' + b # new keys
        nk2 = b + ' ' + a

        if nk1 == nk2:
            hashtable[nk1] = key
        else:
            hashtable[nk1] = key
            hashtable[nk2] = key

    return hashtable

# returns a tuple with all the basic items
# ex: 'ad', 'ap', etc.
def get_basic_item_names():
        tu = tuple([item for item in basic_stats.keys()])
        return tu

# returns a tuple with all the combined items
# ex: 'ad ad', 'ad ap', etc.
# calls get_basic_item_names()
def get_combined_item_names():
    basics = get_basic_item_names()
    li = []

    for item in basics:
        for another in basics:
            s = item + ' ' + another
            li.append(s)

    return tuple(li)


special_keys_mapper = get_specials_keys_mapper()

# unused for now
basic_item_names = get_basic_item_names()
combined_item_names = get_combined_item_names()


class Basic:
    def __init__(self, name):
        self.name = name
        self.stat = basic_stats[name]
        self.special = 'no specials' # basic items might have them in the future

    def description(self):
        return '{} gives {} and {}.'.format(self.name, self.stat, self.special)

    def combine_fromname(self, other_item_name:str):
        new_name = self.name + ' ' + other_item_name
        return Combined(new_name)

    def combine_fromitemobject(self, other_item:'Basic'):
        new_name = self.name + ' ' + other_item.name
        return Combined(new_name)


class Combined:
    def __init__(self, name):
        self.name = name

        stat_key1, stat_key2 = name.split()
        self.stat = combination_stats[stat_key1][stat_key2]

        mapped_special_key = special_keys_mapper[name]
        self.special = combination_specials[mapped_special_key]

    def description(self):
        return '{} gives {} and {}.'.format(self.name, self.stat, self.special)


# GUI functions

def build_item(basic_item1, basic_item2):
    return basic_item1.combine_fromname(basic_item2)

print(build_item(Basic('ad'), 'ap').description()) 

# working, more tests in test_teamfight_tactics.py



