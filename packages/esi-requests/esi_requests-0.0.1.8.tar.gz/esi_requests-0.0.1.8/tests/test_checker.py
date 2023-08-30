"""
Test cases for ESIRequestChecker and ESIEndpointChecker.

Contributed by ChatGPT.

(c) 2023 by Hanbo Guo
"""

import os
import json
import unittest
from unittest.mock import patch, Mock
from esi_requests.checker import ESIEndpointChecker


class TestESIEndpointChecker(unittest.TestCase):
    """Checks the status of an ESI endpoint.

    Example:
        ```python
        checker = ESIEndpointChecker()
        if checker('/characters/{character_id}/'):
            print("Endpoint is operational")
        else:
            print("Endpoint is down")
        ```
    """
    def setUp(self):
        self.checker = ESIEndpointChecker()
    
    def tearDown(self):
        del self.checker

    def test_init(self):
        self.assertTrue(self.checker.enabled)
        self.assertTrue(self.checker.fd.name.endswith('status.json'))

    def test_fd_expired(self):
        checker = ESIEndpointChecker()
        checker.status_parsed = None
        self.assertTrue(checker.fd_expired)
        checker.status_parsed = {'fake_endpoint': True}
        self.assertFalse(checker.fd_expired)

    @patch('esi_requests.checker.requests.get')
    def test___call__(self, mock_get):
        # set up the mock response
        route = '/v1/characters/123/'
        mock_status = [{'route': route, 'status': 'green'}]
        mock_response = Mock()
        mock_response.json.return_value = mock_status
        mock_get.return_value = mock_response

        # test with no existing status.json file
        checker = ESIEndpointChecker()
        checker.fd_path = os.path.join(os.path.dirname(__file__), "status.json")
        if os.path.isfile(checker.fd_path):
            os.remove(checker.fd_path)
        self.assertTrue(checker(route))
        self.assertEqual(checker.status_parsed, {route: True})
        self.assertTrue(os.path.isfile(checker.fd_path))

        # test with existing status.json
        checker = ESIEndpointChecker()
        with open(checker.fd_path, "w") as f:
            json.dump({route: False}, f)
        self.assertFalse(checker(route))
        self.assertEqual(checker.status_parsed, {route: True})

    def test_parse_status_json(self):
        status = [{"route": "/v1/characters/123/", "status": "green"}]
        expected_parsed_status = {"/v1/characters/123/": True}
        checker = ESIEndpointChecker()
        parsed_status = checker._parse_status_json(status)
        self.assertEqual(parsed_status, expected_parsed_status)

if __name__ == '__main__':
    unittest.main()

