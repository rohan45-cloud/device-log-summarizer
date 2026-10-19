import unittest

from sanitize import clean_sensor_readings
class TestSensorCleaning(unittest.TestCase):
    def test_mixed_values(self):
        self.assertEqual(
            clean_sensor_readings(["12", None, -4, "bad", 501, 2.5]),
            [12.0, 500.0, 2.5],
        )

    def test_empty_values(self):
        self.assertEqual(clean_sensor_readings([]), [])

    def test_all_invalid_values(self):
        self.assertEqual(clean_sensor_readings([None, "oops", -1]), [])


if __name__ == "__main__":
    unittest.main()
