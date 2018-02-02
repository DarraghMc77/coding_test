import unittest
from customer_invites import get_invited_customers, calculate_distance, parse_json, read_file, convert_to_radians

class CustomerInvitesTest(unittest.TestCase):

    def setUp(self):
        self.test_location = (53.373046, -6.388735)
        self.test_customer = "{\"latitude\": 52.3191841, \"user_id\": 3, \"name\": \"Jack Enright\", \"longitude\": -8.5072391}"
        self.parsed_customers = [{"latitude": 52.3191841, "user_id": 3, "name": "Jack Enright", "longitude": -8.5072391},
                          {"latitude": 51.92893, "user_id": 1, "name": "Alice Cahill", "longitude": -10.27699},
                          {"latitude": 53.2451022, "user_id": 4, "name": "Ian Kehoe", "longitude": -6.238335},
                          {"latitude": 53.1302756, "user_id": 5, "name": "Nora Dempsey", "longitude": -6.2397222}
                          ]

    def test_calculate_distance(self):
        self.assertAlmostEqual(calculate_distance(self.test_location), 9.47, delta=0.1)
        self.assertEqual(self.test_location, self.test_location, 0)

    def test_convert_to_radians(self):
        self.assertEqual(convert_to_radians(self.test_location), (0.9315353845183895, -0.11150446078739992))

    def test_get_invited_customers(self):
        invited_customers = get_invited_customers(self.parsed_customers)
        self.assertEqual(self.parsed_customers[2:], invited_customers)

    def test_parse_json(self):
        self.assertEqual(parse_json(self.test_customer), self.parsed_customers[0])

    def test_parse_json_exceptions(self):
        malformed_json = "{\"latitude\": 52.3191841, \"user_id\" 3, \"name\": \"Jack Enright\", \"longitude\": -8.5072391}"
        with self.assertRaises(SystemExit):
            parse_json(malformed_json)

        missing_latitude = "{\"user_id\": 3, \"name\": \"Jack Enright\", \"longitude\": -8.5072391}"
        with self.assertRaises(SystemExit):
            parse_json(missing_latitude)

        lat_invalid_value = "{\"latitude\": hello, \"user_id\": 3, \"name\": \"Jack Enright\", \"longitude\": -8.5072391}"
        with self.assertRaises(SystemExit):
            parse_json(lat_invalid_value)

    def test_read_file(self):
        with self.assertRaises(SystemExit):
            read_file("invalid_test.txt")


if __name__ == '__main__':
    unittest.main()

