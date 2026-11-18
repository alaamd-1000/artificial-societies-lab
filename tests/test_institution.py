import unittest

from src.artificial_societies.agents.institution import InstitutionAgent


class TestInstitutionAgent(unittest.TestCase):

    def test_support_respects_response_capacity(self):
        institution = InstitutionAgent(
            1, "Test Institution", 1000, 5, 0.8
        )

        result = institution.provide_support(10)

        self.assertEqual(result["supported_people"], 5)

    def test_support_uses_available_resources(self):
        institution = InstitutionAgent(
            1, "Test Institution", 10, 100, 0.8
        )

        result = institution.provide_support(20)

        self.assertEqual(result["supported_people"], 5)
        self.assertEqual(result["resources_used"], 10)
        self.assertEqual(result["remaining_resources"], 0)


if __name__ == "__main__":
    unittest.main()
