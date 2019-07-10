'''
Script that will build the item databse for us
'''

import json
import copy
import re
from pprint import pprint

item_types = ['ad', 'as', 'ap', 'mn', 'ar', 'mr', 'hp', 'wi']

basic_stats = {
	
	'ad': '20 ad',
	'as': '15 as',
	'ap': '20 ap',
	'mn': '20 mn',
	'ar': '20 ar',
	'mr': '20 mr',
	'hp': '200 hp',
	'wi': '0' # wildcard
}

# refers to the basic_stats dict so we won't have to refactor
# code has been generated using the utility methods at the end of the file
# will need to be moved out to a utility module
combination_stats = {
	
	'ad': {
		'ad': '{}, {}'.format(basic_stats['ad'], basic_stats['ad']),
		'as': '{}, {}'.format(basic_stats['ad'], basic_stats['as']),
		'ap': '{}, {}'.format(basic_stats['ad'], basic_stats['ap']),
		'mn': '{}, {}'.format(basic_stats['ad'], basic_stats['mn']),
		'ar': '{}, {}'.format(basic_stats['ad'], basic_stats['ar']),
		'mr': '{}, {}'.format(basic_stats['ad'], basic_stats['mr']),
		'hp': '{}, {}'.format(basic_stats['ad'], basic_stats['hp']),
		'wi': '{}, {}'.format(basic_stats['ad'], basic_stats['wi']),
	},
	'as': {
		'ad': '{}, {}'.format(basic_stats['as'], basic_stats['ad']),
		'as': '{}, {}'.format(basic_stats['as'], basic_stats['as']),
		'ap': '{}, {}'.format(basic_stats['as'], basic_stats['ap']),
		'mn': '{}, {}'.format(basic_stats['as'], basic_stats['mn']),
		'ar': '{}, {}'.format(basic_stats['as'], basic_stats['ar']),
		'mr': '{}, {}'.format(basic_stats['as'], basic_stats['mr']),
		'hp': '{}, {}'.format(basic_stats['as'], basic_stats['hp']),
		'wi': '{}, {}'.format(basic_stats['as'], basic_stats['wi'])
	},
	'ap': {
		'ad': '{}, {}'.format(basic_stats['ap'], basic_stats['ad']),
		'as': '{}, {}'.format(basic_stats['ap'], basic_stats['as']),
		'ap': '{}, {}'.format(basic_stats['ap'], basic_stats['ap']),
		'mn': '{}, {}'.format(basic_stats['ap'], basic_stats['mn']),
		'ar': '{}, {}'.format(basic_stats['ap'], basic_stats['ar']),
		'mr': '{}, {}'.format(basic_stats['ap'], basic_stats['mr']),
		'hp': '{}, {}'.format(basic_stats['ap'], basic_stats['hp']),
		'wi': '{}, {}'.format(basic_stats['ap'], basic_stats['wi'])
	},
	'mn': {
		'ad': '{}, {}'.format(basic_stats['mn'], basic_stats['ad']),
		'as': '{}, {}'.format(basic_stats['mn'], basic_stats['as']),
		'ap': '{}, {}'.format(basic_stats['mn'], basic_stats['ap']),
		'mn': '{}, {}'.format(basic_stats['mn'], basic_stats['mn']),
		'ar': '{}, {}'.format(basic_stats['mn'], basic_stats['ar']),
		'mr': '{}, {}'.format(basic_stats['mn'], basic_stats['mr']),
		'hp': '{}, {}'.format(basic_stats['mn'], basic_stats['hp']),
		'wi': '{}, {}'.format(basic_stats['mn'], basic_stats['wi'])

	},
	'ar': {
		'ad': '{}, {}'.format(basic_stats['ar'], basic_stats['ad']),
		'as': '{}, {}'.format(basic_stats['ar'], basic_stats['as']),
		'ap': '{}, {}'.format(basic_stats['ar'], basic_stats['ap']),
		'mn': '{}, {}'.format(basic_stats['ar'], basic_stats['mn']),
		'ar': '{}, {}'.format(basic_stats['ar'], basic_stats['ar']),
		'mr': '{}, {}'.format(basic_stats['ar'], basic_stats['mr']),
		'hp': '{}, {}'.format(basic_stats['ar'], basic_stats['hp']),
		'wi': '{}, {}'.format(basic_stats['ar'], basic_stats['wi'])
	},
	'mr': {
		'ad': '{}, {}'.format(basic_stats['mr'], basic_stats['ad']),
		'as': '{}, {}'.format(basic_stats['mr'], basic_stats['as']),
		'ap': '{}, {}'.format(basic_stats['mr'], basic_stats['ap']),
		'mn': '{}, {}'.format(basic_stats['mr'], basic_stats['mn']),
		'ar': '{}, {}'.format(basic_stats['mr'], basic_stats['ar']),
		'mr': '{}, {}'.format(basic_stats['mr'], basic_stats['mr']),
		'hp': '{}, {}'.format(basic_stats['mr'], basic_stats['hp']),
		'wi': '{}, {}'.format(basic_stats['mr'], basic_stats['wi'])

	},
	'hp': {
		'ad': '{}, {}'.format(basic_stats['hp'], basic_stats['ad']),
		'as': '{}, {}'.format(basic_stats['hp'], basic_stats['as']),
		'ap': '{}, {}'.format(basic_stats['hp'], basic_stats['ap']),
		'mn': '{}, {}'.format(basic_stats['hp'], basic_stats['mn']),
		'ar': '{}, {}'.format(basic_stats['hp'], basic_stats['ar']),
		'mr': '{}, {}'.format(basic_stats['hp'], basic_stats['mr']),
		'hp': '{}, {}'.format(basic_stats['hp'], basic_stats['hp']),
		'wi': '{}, {}'.format(basic_stats['hp'], basic_stats['wi'])
	},
	'wi': {
		'ad': '{}, {}'.format(basic_stats['wi'], basic_stats['ad']),
		'as': '{}, {}'.format(basic_stats['wi'], basic_stats['as']),
		'ap': '{}, {}'.format(basic_stats['wi'], basic_stats['ap']),
		'mn': '{}, {}'.format(basic_stats['wi'], basic_stats['mn']),
		'ar': '{}, {}'.format(basic_stats['wi'], basic_stats['ar']),
		'mr': '{}, {}'.format(basic_stats['wi'], basic_stats['mr']),
		'hp': '{}, {}'.format(basic_stats['wi'], basic_stats['hp']),
		'wi': '{}, {}'.format(basic_stats['wi'], basic_stats['wi'])
	}
}

# keys were generated, descriptions were copied from https://i.imgur.com/FdMYSa9.jpg
# once the game goes out of beta, we can expect the Riot API to help us get this programmatically
combination_specials = {
	'ad ad':'100 crit dmg',
	'ad as':'5% chance each second to crit',
	'ad ap':'heal for 25% of dmg dealt',
	'ad mn':'after ulting, gain 15% mana per atk',
	'ad ar':'revive with 500hp',
	'ad mr':'50% lifesteal',
	'ad hp':'adjacent allies on battle start gain 10% as',
	'ad wi':'become an assassin',
	'as as':'double range, no miss',
	'as ap':'3% atack speed on hit',
	'as mn':'100 splash on every 3rd atk',
	'as ar':'dodge all crits',
	'as mr':'removes one star',
	'as hp':'aa scales with hp, splash dmg',
	'as wi':'become blademaster',
	'ap ap':'50% more ap',
	'ap mn':'200 splash on spell hit',
	'ap ar':'shield near allies for 200hp',
	'ap mr':'200 dmg on spell cast by enemies',
	'ap hp':'spell dmg negates healing',
	'ap wi':'become sorcerer',
	'mn mn':'gain 40 bonus mana after spell casts',
	'mn ar':'adjacent enemies attack 20% slower',
	'mn mr':'high chance of silencing on hit',
	'mn hp':'on death, heal nearby allies for 1000hp',
	'mn wi':'become a demon',
	'ar ar':'reflect 35% of atk dmg dealt',
	'ar mr':'chance to disarm on hit',
	'ar hp':'burn 15% of max hp on hit',
	'ar wi':'become a knight',
	'mr mr':'83% magic resistance',
	'mr hp':'on combat start, banish 1 enemy for 5s',
	'mr wi':'attack 2 extra targets for 50% reduced dmg',
	'hp hp':'regenerate 3% hp per second',
	'hp wi':'become a glacial',
	'wi wi':'get an extra unit on the board'
}


data = {'basic_stats': basic_stats, 'combination_stats': combination_stats, 'combination_specials':combination_specials}

with open('data.json', 'w+') as outfile:
	json.dump(data, outfile, indent=4)


'''
Utility methods for code generation

'''
# builds regex that will be used by the regex_builder_all_components() method
def regex_builder(item1, item2, repeat=False):

	components = ['ad', 'as', 'ap', 'mn', 'ar', 'mr', 'hp', 'wi']

	if repeat:
		t = "re.match(r'(.{}.{}.)', item):".format(item1, item2)
		return t
	else:	
		t = "re.match(r'(.{}.{}.|.{}.{}.)', item):".format(item1, item2, item2, item1)
		return t

# builds regex that will be used by the generate_specials_descrition() method
def regex_builder_all_components():

	li = ['ad', 'as', 'ap', 'mn', 'ar', 'mr', 'hp', 'wi']

	components = []
	hashmap = {}

	# for each component fused with another component
	for item in li:
		for another in li:

			# define hashmap key
			# two versions since ad ap and ap ad are the same
			# we want to avoid recreating the same code
			built_key_v1 = ' '.join((item, another))
			built_key_v2 = ' '.join((another, item))

			# if our combined item hasn't been added to the hashmap yet
			# it means that we haven't went through that combination yet
			# so let's generate the regex for that combination
			# and add it to our hashmap so we don't generate another one for the same item
			if all(key not in hashmap for key in (built_key_v1, built_key_v2)):

				# if our components are the same
				# change the default value of the regex builder
				if item==another:
					s = regex_builder(item, another, repeat=True)
					components.append(s)

				else:
					s = regex_builder(item, another)
					components.append(s)

				# adding the combination to our hashmap
				hashmap[built_key_v1] = built_key_v1
				hashmap[built_key_v2] = built_key_v2

	return components

# adds if, elif to the generated code
def alter_regex_built():
	li = regex_builder_all_components();

	for i,item in enumerate(li):
		if i==0:
			t = 'if ' + '{}'.format(item)
		else:
			t = 'elif ' + '{}'.format(item)
		print(t)

# generates code for the combination_stats js object
# combination_stats holds data for the stats of combined components
# for now, it has to be called for every stat (ad, ap, as, etc.)
def generate_combination_code(stat):

	# copy, for later use
	# li = copy.copy(list(basic_stats.keys()))

	for key in basic_stats:
		t = "'{}': '{{}}, {{}}'.format(basic_stats['{}'], basic_stats['{}']),".format(key, stat, key)
		print(t)

# generates code for values of the combination_specials js object
# written using the regex code generators
def generate_specials_description():

	li2 = []

	description = []

	# bug here
	# we don't want to generate all 64 combinations
	# if we go through the combination once, then 
	for item in item_types:
		for another in item_types:
			t = "'{} {}':".format(item, another)
			li2.append(t)


	for item in li2:
		if re.match(r'(.ad.ad.)', item):
			description.append(r'100 crit dmg')
		elif re.match(r'(.ad.as.|.as.ad.)', item):
			description.append(r'5% chance each second to crit')
		elif re.match(r'(.ad.ap.|.ap.ad.)', item):
			description.append(r'heal for 25% of dmg dealt')
		elif re.match(r'(.ad.mn.|.mn.ad.)', item):
			description.append(r'after ulting, gain 15% mana per atk')
		elif re.match(r'(.ad.ar.|.ar.ad.)', item):
			description.append(r'revive with 500hp')
		elif re.match(r'(.ad.mr.|.mr.ad.)', item):
			description.append(r'50% lifesteal')
		elif re.match(r'(.ad.hp.|.hp.ad.)', item):
			description.append(r'adjacent allies on battle start gain 10% as')
		elif re.match(r'(.ad.wi.|.wi.ad.)', item):
			description.append(r'become an assassin')
		elif re.match(r'(.as.as.)', item):
			description.append(r'double range, no miss')
		elif re.match(r'(.as.ap.|.ap.as.)', item):
			description.append(r'3% atack speed on hit')
		elif re.match(r'(.as.mn.|.mn.as.)', item):
			description.append(r'100 splash on every 3rd atk')
		elif re.match(r'(.as.ar.|.ar.as.)', item):
			description.append(r'dodge all crits')
		elif re.match(r'(.as.mr.|.mr.as.)', item):
			description.append(r'removes one star')
		elif re.match(r'(.as.hp.|.hp.as.)', item):
			description.append(r'aa scales with hp, splash dmg')
		elif re.match(r'(.as.wi.|.wi.as.)', item):
			description.append(r'become blademaster')
		elif re.match(r'(.ap.ap.)', item):
			description.append(r'50% more ap')
		elif re.match(r'(.ap.mn.|.mn.ap.)', item):
			description.append(r'200 splash on spell hit')
		elif re.match(r'(.ap.ar.|.ar.ap.)', item):
			description.append(r'shield near allies for 200hp')
		elif re.match(r'(.ap.mr.|.mr.ap.)', item):
			description.append(r'200 dmg on spell cast by enemies')
		elif re.match(r'(.ap.hp.|.hp.ap.)', item):
			description.append(r'spell dmg negates healing')
		elif re.match(r'(.ap.wi.|.wi.ap.)', item):
			description.append(r'become sorcerer')
		elif re.match(r'(.mn.mn.)', item):
			description.append(r'gain 40 bonus mana after spell casts')
		elif re.match(r'(.mn.ar.|.ar.mn.)', item):
			description.append(r'adjacent enemies attack 20% slower')
		elif re.match(r'(.mn.mr.|.mr.mn.)', item):
			description.append(r'high chance of silencing on hit')
		elif re.match(r'(.mn.hp.|.hp.mn.)', item):
			description.append(r'on death, heal nearby allies for 1000hp')
		elif re.match(r'(.mn.wi.|.wi.mn.)', item):
			description.append(r'become a demon')
		elif re.match(r'(.ar.ar.)', item):
			description.append(r'reflect 35% of atk dmg dealt')
		elif re.match(r'(.ar.mr.|.mr.ar.)', item):
			description.append(r'chance to disarm on hit')
		elif re.match(r'(.ar.hp.|.hp.ar.)', item):
			description.append(r'burn 15% of max hp on hit')
		elif re.match(r'(.ar.wi.|.wi.ar.)', item):
			description.append(r'become a knight')
		elif re.match(r'(.mr.mr.)', item):
			description.append(r'83% magic resistance')
		elif re.match(r'(.mr.hp.|.hp.mr.)', item):
			description.append(r'on combat start, banish 1 enemy for 5s')
		elif re.match(r'(.mr.wi.|.wi.mr.)', item):
			description.append(r'attack 2 extra targets for 50% reduced dmg')
		elif re.match(r'(.hp.hp.)', item):
			description.append(r'regenerate 3% hp per second')
		elif re.match(r'(.hp.wi.|.wi.hp.)', item):
			description.append(r'become a glacial')
		elif re.match(r'(.wi.wi.)', item):
			description.append(r'get an extra unit on the board')
		else:
			raise Exception('There is an error in item_types dict.')

	return list(dict.fromkeys(description)) # removes duplicates, another approach vs what was used in regex_builder_all_components()

# generates code for keys of the combination_specials js object
# in retrospect, better have redundancy than parsing/building a more complicated structure
def generate_specials_keys():
	li = ['ad', 'as', 'ap', 'mn', 'ar', 'mr', 'hp', 'wi']
	hashmap = {}
	keys = []

	for item in li:
		for another in li:
			built_key1 = ' '.join((item, another))
			built_key2 = ' '.join((another, item))

			if all(key not in hashmap for key in (built_key1, built_key2)):

				hashmap[built_key1]=built_key1
				hashmap[built_key2]=built_key2

				keys.append(built_key1)

	return keys

# generates the combination_specials js object by combining keys and values
def generate_specials_dict():

	keys = generate_specials_keys()
	values = generate_specials_description()

	d = dict(zip(keys, values))

	return d

# prints dict with surrounding quotes
# need to fix % signs not being escaped in the future
def print_dict(d):
	d = generate_specials_dict()
	q = '\''
	c = ','

	for i,(k,v) in enumerate(d.items()):
		tu = (q,k,q,':',q,v,q,c)
		
		if i==len(d)-1:
			tu = (q,k,q,':',q,v,q,)

		s = ''.join(tu)
		print(s)







