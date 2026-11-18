import unittest

from src.artificial_societies.agents.person import PersonAgent
from src.artificial_societies.networks.social_network import SocialNetwork
from src.artificial_societies.behavior.social_influence import spread_warning


class TestSpreadWarning(unittest.TestCase):

    def setUp(self):
        self.network = SocialNetwork()

        for person_id in range(1, 6):
            person = PersonAgent(
                person_id, 30, "university",
                5000, 50, 0.5, 0.7, 0.6
            )
            self.network.add_person(person)

        self.network.connect_people(1, 2)
        self.network.connect_people(2, 3)
        self.network.connect_people(3, 4)
        self.network.connect_people(4, 5)

    def test_source_is_informed(self):
        result = spread_warning(self.network, 1)

        self.assertIn(1, result["informed_people"])

    def test_probability_one_reaches_all_connected_people(self):
        result = spread_warning(
            self.network,
            1,
            transmission_probability=1.0
        )

        self.assertEqual(result["total_informed"], 5)
        self.assertEqual(result["informed_people"], [1, 2, 3, 4, 5])

    def test_probability_zero_reaches_only_source(self):
        result = spread_warning(
            self.network,
            1,
            transmission_probability=0.0
        )

        self.assertEqual(result["informed_people"], [1])
        self.assertEqual(result["total_informed"], 1)

    def test_warning_spreads_in_rounds(self):
        result = spread_warning(
            self.network,
            1,
            transmission_probability=1.0
        )

        self.assertEqual(
            result["rounds"],
            [[1], [2], [3], [4], [5]]
        )

    def test_same_seed_produces_same_result(self):
        result1 = spread_warning(
            self.network, 1, 0.5, seed=42
        )
        result2 = spread_warning(
            self.network, 1, 0.5, seed=42
        )

        self.assertEqual(result1, result2)

    def test_disconnected_person_is_not_informed(self):
        isolated_person = PersonAgent(
            6, 35, "secondary",
            4000, 40, 0.4, 0.6, 0.5
        )
        self.network.add_person(isolated_person)

        result = spread_warning(
            self.network,
            1,
            transmission_probability=1.0
        )

        self.assertNotIn(6, result["informed_people"])


if __name__ == "__main__":
    unittest.main()
