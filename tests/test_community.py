import unittest

from src.artificial_societies.agents.person import PersonAgent
from src.artificial_societies.agents.household import HouseholdAgent
from src.artificial_societies.agents.community import CommunityAgent


class TestCommunityAgent(unittest.TestCase):

    def create_person(self, person_id, risk, preparedness):
        return PersonAgent(
            person_id=person_id,
            age=30,
            education_level="university",
            income=5000,
            resources=100,
            risk_perception=risk,
            trust_level=0.8,
            preparedness=preparedness
        )

    def create_community(self):
        household1 = HouseholdAgent(
            1,
            [
                self.create_person(1, 0.9, 0.8),
                self.create_person(2, 0.5, 0.6)
            ]
        )

        household2 = HouseholdAgent(
            2,
            [
                self.create_person(3, 0.3, 0.4)
            ]
        )

        return CommunityAgent(1, [household1, household2])

    def test_household_count(self):
        community = self.create_community()
        self.assertEqual(community.household_count, 2)

    def test_total_population(self):
        community = self.create_community()
        self.assertEqual(community.total_population, 3)

    def test_average_preparedness(self):
        community = self.create_community()
        self.assertAlmostEqual(
            community.average_preparedness(), 0.6
        )

    def test_get_people(self):
        community = self.create_community()
        people = community.get_people()

        self.assertEqual(len(people), 3)
        self.assertEqual(
            [person.person_id for person in people],
            [1, 2, 3]
        )

    def test_empty_community(self):
        community = CommunityAgent(1)

        self.assertEqual(community.household_count, 0)
        self.assertEqual(community.total_population, 0)
        self.assertEqual(community.average_preparedness(), 0.0)
        self.assertEqual(community.get_people(), [])

    def test_community_response_counts_decisions(self):
        community = self.create_community()

        result = community.community_response(0.9)

        self.assertEqual(sum(result.values()), 3)


    def test_social_influence_updates_risk_perception(self):
        from src.artificial_societies.networks.social_network import SocialNetwork

        community = self.create_community()
        people = community.get_people()
        network = SocialNetwork()

        for person in people:
            network.add_person(person)

        network.connect_people(1, 2)

        responses = community.individual_responses(
            0.9, network, True, 0.3
        )

        results = {r["person_id"]: r for r in responses}

        self.assertAlmostEqual(
            results[2]["updated_risk_perception"], 0.65
        )
        self.assertAlmostEqual(
            results[1]["updated_risk_perception"], 0.93
        )
        self.assertAlmostEqual(
            results[3]["updated_risk_perception"], 0.3
        )

    def test_social_influence_preserves_original_perceptions(self):
        from src.artificial_societies.networks.social_network import SocialNetwork

        community = self.create_community()
        people = community.get_people()
        original = {
            p.person_id: p.risk_perception for p in people
        }

        network = SocialNetwork()
        for person in people:
            network.add_person(person)

        network.connect_people(1, 2)

        community.individual_responses(0.9, network, True)

        for person in people:
            self.assertEqual(
                person.risk_perception,
                original[person.person_id]
            )


if __name__ == "__main__":
    unittest.main()
