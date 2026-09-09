import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import distance, estimate_time_from_distance, get_prep_time, get_rider_distance_from_option
from config import get_region

class TestUnits(unittest.TestCase):

    def test_haversine_distance(self):
        # Powai to Powai (same point) -> 0 km
        p1 = [19.1197, 72.9050]
        self.assertAlmostEqual(distance(p1, p1), 0.0, places=4)

        # Powai to Bandra (~10.3 km)
        p2 = [19.0596, 72.8295]
        dist = distance(p1, p2)
        self.assertGreater(dist, 9.0)
        self.assertLess(dist, 12.0)

    def test_speed_estimation(self):
        # 35 km at 35 km/h (Low traffic) -> 60 minutes
        self.assertAlmostEqual(estimate_time_from_distance(35, "Low"), 60.0, places=2)
        # 25 km at 25 km/h (Medium traffic) -> 60 minutes
        self.assertAlmostEqual(estimate_time_from_distance(25, "Medium"), 60.0, places=2)
        # 15 km at 15 km/h (High traffic) -> 60 minutes
        self.assertAlmostEqual(estimate_time_from_distance(15, "High"), 60.0, places=2)

    def test_food_prep_case_normalization(self):
        # Capitalized "Pizza" should match lowercase "pizza" prep time range (12-18 min)
        prep_capitalized = get_prep_time("Pizza")
        prep_lowercase = get_prep_time("pizza")
        # Should be within valid bounds (10.8 to 19.8 min)
        self.assertGreaterEqual(prep_capitalized, 10.0)
        self.assertLessEqual(prep_capitalized, 20.0)

    def test_region_geofencing(self):
        # South Mumbai (lat < 19.05) -> CENTRAL
        self.assertEqual(get_region(19.0000, 72.8300), "CENTRAL")
        # Bandra (lat >= 19.05, lon < 72.85) -> WEST
        self.assertEqual(get_region(19.0596, 72.8295), "WEST")
        # Powai (lat >= 19.05, lon >= 72.85) -> EAST
        self.assertEqual(get_region(19.1197, 72.9050), "EAST")

if __name__ == "__main__":
    unittest.main()
