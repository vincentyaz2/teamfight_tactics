import unittest
from teamfight_tactics import Basic
from teamfight_tactics import Combined

class ItemTesting(unittest.TestCase):

	def setUp(self):
		self.basic = Basic('ad')
		self.basic2 = Basic('ad')
		self.combined = Combined('hp ad')

	def tearDown(self):
		pass

	def test_basic_creation(self):
		desc = 'ad gives 20 ad and no specials.'
		self.assertEqual(self.basic.description(), desc)

	def test_combined_creation(self):
		desc = 'hp ad gives 200 hp, 20 ad and adjacent allies on battle start gain 10% as.'
		self.assertEqual(self.combined.description(), desc)

	def test_basic_combiningfromname(self):
		desc = 'ad ad gives 20 ad, 20 ad and 100 crit dmg.'
		self.assertEqual(self.basic.combine_fromname('ad').description(), desc)

	def test_basic_combiningfromobject(self):
		desc = 'ad ad gives 20 ad, 20 ad and 100 crit dmg.'
		self.assertEqual(self.basic.combine_fromitemobject(self.basic2).description(), desc)


# run this if it's called by the terminal
if __name__ == '__main__':
	unittest.main()