import unittest

from teamfight_tactics import Component

class ComponentTesting(unittest.TestCase):

	def setUp(self):
		self.component = Component('Name', 'Stats')

	def tearDown(self):
		pass

	def test_description(self):
		desc = 'Name gives Stats and no specials.'
		self.assertEqual(self.component.description(), desc)

# run this if it's called by the terminal
if __name__ == '__main__':
	unittest.main()