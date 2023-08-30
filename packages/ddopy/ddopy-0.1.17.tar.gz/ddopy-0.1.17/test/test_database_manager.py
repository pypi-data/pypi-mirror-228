# write unit tests for database_manager.py

import unittest
from ddopy.db.database_manager import DatabaseManager
from ddopy.db.model.endpoint_url import EndpointUrl


class TestDatabaseManager(unittest.TestCase):
    def test_database_manager(self):
        db_object = DatabaseManager("sqlite:///test/test.db")
        model_object = EndpointUrl()
        model_object.url = "https://httpbin.org/post"
        model_object.id = "1"

        db_object.set(model_object)
        self.assertIsNotNone(db_object.get(EndpointUrl))
        self.assertEqual(db_object.get(EndpointUrl).url, "https://httpbin.org/post")
        self.assertEqual(db_object.get(EndpointUrl).id, "1")
