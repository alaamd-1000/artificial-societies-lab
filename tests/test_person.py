import unittest

from src.artificial_societies.agents.person import PersonAgent


class TestPersonAgent(unittest.TestCase):

    def setUp(self):
        self.person = PersonAgent(
            person_id=1,
            age=35,
            education_level="university",
            income=5000,
            resources=50,
            risk_perception=0.8,
            trust_level=0.7,
            preparedness=0.8
        )

    def test_high_risk_and_high_preparedness_evacuates(self):
        decision = self.person.make_decision(0.9)
        self.assertEqual(decision, "evacuate")

    def test_high_risk_and_low_preparedness_seeks_information(self):
        self.person.preparedness = 0.4
        decision = self.person.make_decision(0.9)
        self.assertEqual(decision, "seek_information")

    def test_medium_risk_prepares(self):
        decision = self.person.make_decision(
            0.6,
            risk_perception=0.8
        )
        self.assertEqual(decision, "prepare")

    def test_low_risk_continues_normal_activity(self):
        decision = self.person.make_decision(
            0.3,
            risk_perception=0.5
        )
        self.assertEqual(decision, "continue_normal_activity")

    def test_empty_neighbor_decisions_keep_current_perception(self):
        updated = self.person.update_risk_perception([])
        self.assertEqual(updated, 0.8)

    def test_social_influence_updates_perception(self):
        updated = self.person.update_risk_perception(
            ["evacuate", "prepare", "continue_normal_activity"],
            social_influence_strength=0.3
        )
        self.assertAlmostEqual(updated, 0.76)

    def test_updated_perception_does_not_change_original_value(self):
        self.person.update_risk_perception(
            ["evacuate", "prepare"]
        )
        self.assertEqual(self.person.risk_perception, 0.8)


if __name__ == "__main__":
    unittest.main()
