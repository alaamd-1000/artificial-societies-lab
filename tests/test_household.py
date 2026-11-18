import unittest

from src.artificial_societies.agents.person import PersonAgent
from src.artificial_societies.agents.household import HouseholdAgent


class TestHouseholdAgent(unittest.TestCase):

    def create_person(self, person_id, preparedness):
        return PersonAgent(
            person_id=person_id,
            age=30,
            education_level="university",
            income=5000,
            resources=100,
            risk_perception=0.9,
            trust_level=0.8,
            preparedness=preparedness
        )

    def test_household_size(self):
        household = HouseholdAgent(
            1,
            [self.create_person(1, 0.5),
             self.create_person(2, 0.7)]
        )
        self.assertEqual(household.household_size, 2)

    def test_average_preparedness(self):
        household = HouseholdAgent(
            1,
            [self.create_person(1, 0.4),
             self.create_person(2, 0.8)]
        )
        self.assertAlmostEqual(
            household.average_preparedness(), 0.6
        )

    def test_empty_household(self):
        household = HouseholdAgent(1)
        self.assertEqual(household.household_size, 0)
        self.assertEqual(household.average_preparedness(), 0.0)
        self.assertEqual(household.household_decisions(0.5), [])

    def test_household_decisions(self):
        household = HouseholdAgent(
            1,
            [self.create_person(1, 0.8),
             self.create_person(2, 0.3)]
        )
        decisions = household.household_decisions(0.9)

        self.assertEqual(
            decisions,
            ["evacuate", "seek_information"]
        )


if __name__ == "__main__":
    unittest.main()
