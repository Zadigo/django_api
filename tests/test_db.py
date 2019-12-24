import unittest
from django_api.db.database import Database, Functions
from django_api.db.errors import SchemaError

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_api\\db\\database.json'

TEST_DATA = {
    "name": "Kendall",
    "surname": "Jenner",
    "location": {
        "country": "USA",
        "city": "Los Angeles"
    },
    "age": 22,
    "related": []
}

class TestFunctions(unittest.TestCase):
    pass

class TestDatabase (unittest.TestCase):
    def setUp(self):
        self.database = Database(path_or_url=PATH)

    def test_has_data(self):
        self.assertIsInstance(self.database.db_data, dict)
    
    def test_schema_validity(self):
        # Should fail with a SchemaError
        self.assertRaises(SchemaError, self.database.check_schema({}))

    def test_get_function(self):
        item = self.database.manager.get(name='Kendall')[0]
        self.assertEqual(len(item), 1)
        self.assertDictEqual(item, TEST_DATA)

    def test_complex_get_function(self):
        # country = USA
        item = self.database.manager.get(location__country='USA')[0]
        self.assertDictEqual(item, TEST_DATA)
        # name = Kendall AND surname = Jenner
        item = self.database.manager.get(name='Kendall', surname='Jenner')
