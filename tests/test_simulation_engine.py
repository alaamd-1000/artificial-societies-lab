
import unittest

from src.artificial_societies.agents.person import PersonAgent
from src.artificial_societies.agents.household import HouseholdAgent
from src.artificial_societies.agents.community import CommunityAgent
from src.artificial_societies.agents.institution import InstitutionAgent
from src.artificial_societies.networks.social_network import SocialNetwork
from src.artificial_societies.simulation.engine import SimulationEngine


class TestSimulationEngine(unittest.TestCase):

    def setUp(self):
        self.people = [
            PersonAgent(
                1, 30, "university", 5000, 50, 0.8, 0.8, 0.8
            ),
            PersonAgent(
                2, 40, "secondary", 4000, 40, 0.5, 0.6, 0.5
            ),
            PersonAgent(
                3, 25, "primary", 3000, 30, 0.4, 0.7, 0.6
            )
        ]

        household = HouseholdAgent(
            household_id=1,
            members=self.people
        )

        self.community = CommunityAgent(
            community_id=1,
            households=[household]
        )

        self.network = SocialNetwork()

        for person in self.people:
            self.network.add_person(person, household_id=1)

        self.network.connect_people(1, 2)
        self.network.connect_people(2, 3)

        self.institution = InstitutionAgent(
            institution_id=1,
            name="Test Institution",
            resources=1000,
            response_capacity=100,
            trust_level=0.8
        )

        self.engine = SimulationEngine(
            self.community,
            self.network,
            self.institution
        )

    def test_empty_community_raises_error(self):
        empty_community = CommunityAgent(2)

        engine = SimulationEngine(
            empty_community,
            self.network,
            self.institution
        )

        with self.assertRaises(ValueError):
            engine.run(0.9, 1)

    def test_invalid_source_raises_error(self):
        with self.assertRaises(ValueError):
            self.engine.run(0.9, 99)

    def test_invalid_transmission_probability_raises_error(self):
        with self.assertRaises(ValueError):
            self.engine.run(0.9, 1, transmission_probability=1.5)

    def test_invalid_social_influence_strength_raises_error(self):
        with self.assertRaises(ValueError):
            self.engine.run(
                0.9, 1,
                social_influence=True,
                social_influence_strength=-0.1
            )

    def test_invalid_crisis_severity_raises_error(self):
        for severity in [-0.1, 1.1]:
            with self.subTest(severity=severity):
                with self.assertRaises(ValueError):
                    self.engine.run(
                        crisis_severity=severity,
                        source_person_id=1
                    )

    def test_max_rounds_must_be_at_least_one(self):
        with self.assertRaises(ValueError):
            self.engine.run(0.9, 1, max_rounds=0)

    def test_probability_one_informs_all_connected_people(self):
        result = self.engine.run(
            crisis_severity=0.9,
            source_person_id=1,
            transmission_probability=1.0
        )

        self.assertEqual(result["informed_people"], 3)

    def test_probability_zero_informs_only_source(self):
        result = self.engine.run(
            crisis_severity=0.9,
            source_person_id=1,
            transmission_probability=0.0
        )

        self.assertEqual(result["informed_people"], 1)

    def test_original_risk_perceptions_are_restored(self):
        original_values = [
            person.risk_perception for person in self.people
        ]

        self.engine.run(
            crisis_severity=0.9,
            source_person_id=1,
            social_influence=True,
            social_influence_strength=1.0,
            transmission_probability=1.0
        )

        restored_values = [
            person.risk_perception for person in self.people
        ]

        self.assertEqual(restored_values, original_values)

    def test_simulation_stops_after_all_people_are_informed(self):
        result = self.engine.run(
            crisis_severity=0.9,
            source_person_id=1,
            transmission_probability=1.0,
            max_rounds=20
        )

        self.assertEqual(result["informed_people"], 3)
        self.assertEqual(result["rounds_completed"], 2)

    def test_social_influence_strength_does_not_change_information_spread(self):
        result_low = self.engine.run(
            crisis_severity=0.9,
            source_person_id=1,
            social_influence=True,
            social_influence_strength=0.1,
            transmission_probability=0.5,
            seed=42
        )

        result_high = self.engine.run(
            crisis_severity=0.9,
            source_person_id=1,
            social_influence=True,
            social_influence_strength=0.9,
            transmission_probability=0.5,
            seed=42
        )

        self.assertEqual(
            result_low["informed_people"],
            result_high["informed_people"]
        )

    def test_missing_community_member_in_network_raises_error(self):
        incomplete_network = SocialNetwork()

        incomplete_network.add_person(
            self.people[0],
            household_id=1
        )
        incomplete_network.add_person(
            self.people[1],
            household_id=1
        )

        incomplete_network.connect_people(1, 2)

        engine = SimulationEngine(
            self.community,
            incomplete_network,
            self.institution
        )

        with self.assertRaises(ValueError):
            engine.run(
                crisis_severity=0.9,
                source_person_id=1
            )


if __name__ == "__main__":
    unittest.main()
