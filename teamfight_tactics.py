'''
Script to help with decision making in Teamfight Tactics.
'''

class Item():
    def __init__(self, name, stat, special):
        self.name = name
        self.stat = stat
        self.special = special

    def description(self):
        return '{} gives {} and {}.'.format(self.name, self.stat, self.special)


class Component(Item):
    def __init__(self, name, stat, special='no specials'):
        self.name = name
        self.stat = stat
        self.special = special


    def combine(self, component):
        pass



# test = Component('BF sword', '20 ad')

# desc = test.description()

# print(desc)







# Quickly list the champions offered