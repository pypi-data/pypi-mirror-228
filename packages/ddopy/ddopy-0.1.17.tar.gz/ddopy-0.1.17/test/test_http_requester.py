# write unit tests for database_manager.py

import unittest
from ddopy.http.http_requester import HttpRequester


class TestHttpRequester(unittest.TestCase):
    def test_request(self):
        object = HttpRequester()
        url = "https://httpbin.org/post"
        object.set_base_url(url)
        object.add_header("Content-Type", "application/json")
        payload = {"key1": "value1", "key2": "value2"}
        response = object.post_request(payload)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json["url"], url)
        self.assertEqual(response_json["headers"]["Content-Type"], "application/json")
        self.assertEqual(response_json["json"], payload)
