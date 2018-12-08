import unittest
from Housing_final import *


class TestDatabase(unittest.TestCase):

	def test_housing_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		sql = 'SELECT Housing FROM Housing'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('Park Place of Northville',), result_list)
		self.assertEqual(len(result_list), 643)

		sql = '''
			SELECT Housing, Address, Bed, Bath
			FROM Housing
			WHERE BuildingTypeId="12"
			ORDER BY Bath DESC
		'''
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 13)
		self.assertEqual(result_list[0][3], 6)
		conn.close()

	def test_building_type_table(self):

			conn = sqlite3.connect(DBNAME)
			cur = conn.cursor()

			sql = '''
				SELECT Type
				FROM BuildingType
			'''
			results = cur.execute(sql)
			result_list = results.fetchall()
			self.assertIn(('Condo',), result_list)

			sql = '''
				SELECT COUNT(*)
				FROM BuildingType
			'''
			results = cur.execute(sql)
			count = results.fetchone()[0]
			self.assertTrue(count == 12)

			conn.close()

	def test_pet_table(self):

			conn = sqlite3.connect(DBNAME)
			cur = conn.cursor()

			sql = '''
				SELECT Policy
				FROM Pet
			'''
			results = cur.execute(sql)
			result_list = results.fetchall()
			self.assertIn(('Pets Allowed (Cats, Dogs)',), result_list)
			self.assertEqual(len(result_list), 10)

			conn.close()

	def test_parking_table(self):

			conn = sqlite3.connect(DBNAME)
			cur = conn.cursor()

			sql = '''
				SELECT Type
				FROM Parking
			'''
			results = cur.execute(sql)
			result_list = results.fetchall()
			self.assertIn(('Garage Parking',), result_list)
			self.assertEqual(len(result_list), 9)

			conn.close()


unittest.main()
