
from dataclasses import dataclass, field
from collections import Counter

from src.artificial_societies.agents.household import HouseholdAgent


@dataclass
class CommunityAgent:
    community_id: int
    households: list[HouseholdAgent] = field(default_factory=list)

    @property
    def household_count(self):
        return len(self.households)

    @property
    def total_population(self):
        return sum(
            household.household_size
            for household in self.households
        )

    def average_preparedness(self):
        people = [
            person
            for household in self.households
            for person in household.members
        ]

        if not people:
            return 0.0

        return sum(
            person.preparedness for person in people
        ) / len(people)

    def get_people(self):
        return [
            person
            for household in self.households
            for person in household.members
        ]

    def community_response(self, crisis_severity):
        decisions = []

        for household in self.households:
            decisions.extend(
                household.household_decisions(crisis_severity)
            )

        return dict(Counter(decisions))

    def individual_responses(
        self,
        crisis_severity,
        network=None,
        social_influence=False,
        social_influence_strength=0.3
    ):

        people = self.get_people()

        # First calculate initial decisions for everyone.
        initial_decisions = {
            person.person_id: person.make_decision(
                crisis_severity
            )
            for person in people
        }

        responses = []

        for person in people:

            original_risk = person.risk_perception

            neighboring_decisions = []

            if social_influence and network is not None:

                neighbors = network.get_neighbors(
                    person.person_id
                )

                neighboring_decisions = [
                    initial_decisions[neighbor_id]
                    for neighbor_id in neighbors
                    if neighbor_id in initial_decisions
                ]

                updated_risk = person.update_risk_perception(
                    neighboring_decisions,
                    social_influence_strength
                )

            else:
                updated_risk = original_risk

            decision = person.make_decision(
                crisis_severity,
                risk_perception=updated_risk
            )

            responses.append({
                "person_id": person.person_id,
                "risk_perception": original_risk,
                "updated_risk_perception": updated_risk,
                "preparedness": person.preparedness,
                "neighboring_decisions": neighboring_decisions,
                "decision": decision
            })

        return responses
