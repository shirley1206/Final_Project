import unittest
from Housing_final import *
from model import *


class TestDatabase(unittest.TestCase):

	def test_housing_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		sql = 'SELECT Housing FROM Housing'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('Park Place of Northville',), result_list)
		self.assertEqual(len(result_list), 638)

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

class TestDataStorage(unittest.TestCase):
	def test_get_housing(self):
		results = get_housing(sortby="name", sortorder="desc", bed="3", bath="3", buildingtype="1", pet="", parking="", search="")
		self.assertEqual(results[7][0], '930 Church St. Unit B')
		self.assertEqual(results[1][5], '$850 ')

		results = get_housing(search="kerrytown")
		self.assertEqual(results[0][0],'Short term leases in historic Kerrytown House, huge bedRooms, close to central campus')
		self.assertEqual(results[1][4], 'Apartment')

unittest.main()
