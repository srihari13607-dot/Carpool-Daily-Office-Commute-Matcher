import unittest
from matcher.sample_data import get_sample_commuters
from matcher.engine import CommuteMatchingEngine
from matcher.models import UserRole

class MatcherTests(unittest.TestCase):
    def test_sample_data_exists(self):
        self.assertGreater(len(get_sample_commuters()),0)

    def test_rider_matching_returns_list(self):
        people = get_sample_commuters()
        rider = next(u for u in people if u.role == UserRole.RIDER)
        result = CommuteMatchingEngine().find_matches_for_rider(rider,people,0)
        self.assertIsInstance(result,list)

    def test_alternating_pairs_returns_list(self):
        result = CommuteMatchingEngine().find_alternating_pairs(get_sample_commuters())
        self.assertIsInstance(result,list)

if __name__ == "__main__":
    unittest.main()
