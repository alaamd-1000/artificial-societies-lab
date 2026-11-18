import unittest

from src.artificial_societies.agents.person import PersonAgent
from src.artificial_societies.networks.social_network import SocialNetwork


class TestSocialNetwork(unittest.TestCase):

    def setUp(self):
        self.network = SocialNetwork()

        self.person1 = PersonAgent(
            1, 30, "university", 5000, 50, 0.6, 0.8, 0.7
        )

        self.person2 = PersonAgent(
            2, 40, "secondary", 4000, 40, 0.5, 0.6, 0.5
        )

        self.person3 = PersonAgent(
            3, 25, "primary", 3000, 30, 0.4, 0.7, 0.6
        )

    def test_add_person(self):
        self.network.add_person(self.person1, household_id=1)

        self.assertIn(1, self.network.graph.nodes)
        self.assertEqual(
            self.network.graph.nodes[1]["household_id"], 1
        )

    def test_connect_people(self):
        self.network.add_person(self.person1)
        self.network.add_person(self.person2)

        self.network.connect_people(1, 2)

        self.assertTrue(self.network.graph.has_edge(1, 2))

    def test_network_is_undirected(self):
        self.network.add_person(self.person1)
        self.network.add_person(self.person2)

        self.network.connect_people(1, 2)

        self.assertIn(2, self.network.get_neighbors(1))
        self.assertIn(1, self.network.get_neighbors(2))

    def test_get_neighbors(self):
        for person in [self.person1, self.person2, self.person3]:
            self.network.add_person(person)

        self.network.connect_people(1, 2)
        self.network.connect_people(1, 3)

        self.assertCountEqual(
            self.network.get_neighbors(1), [2, 3]
        )

    def test_network_statistics(self):
        self.network.add_person(self.person1, household_id=1)
        self.network.add_person(self.person2, household_id=1)
        self.network.add_person(self.person3, household_id=2)

        self.network.connect_people(1, 2)
        self.network.connect_people(2, 3)

        stats = self.network.network_statistics()

        self.assertEqual(stats["people"], 3)
        self.assertEqual(stats["connections"], 2)
        self.assertAlmostEqual(stats["average_connections"], 4 / 3)
        self.assertEqual(stats["households"], 2)


if __name__ == "__main__":
    unittest.main()
