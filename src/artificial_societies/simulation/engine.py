
import random
from collections import Counter

from src.artificial_societies.simulation.data_collector import (
    SimulationDataCollector
)


class SimulationEngine:

    def __init__(self, community, network, institution):
        self.community = community
        self.network = network
        self.institution = institution
        self.results = []
        self.data_collector = SimulationDataCollector()

    def run(
        self,
        crisis_severity,
        source_person_id,
        social_influence=False,
        social_influence_strength=0.3,
        transmission_probability=0.3,
        max_rounds=20,
        seed=42
    ):

        people = self.community.get_people()

        if not people:
            raise ValueError("The community has no people.")

        if not 0 <= crisis_severity <= 1:
            raise ValueError(
                "crisis_severity must be between 0 and 1."
            )

        if max_rounds < 1:
            raise ValueError("max_rounds must be at least 1.")

        people_by_id = {
            person.person_id: person
            for person in people
        }

        community_person_ids = set(people_by_id.keys())
        network_person_ids = set(self.network.graph.nodes)

        missing_person_ids = (
            community_person_ids - network_person_ids
        )

        if missing_person_ids:
            raise ValueError(
                "Some community members are missing from the "
                f"social network: {sorted(missing_person_ids)}"
            )

        if source_person_id not in people_by_id:
            raise ValueError("Source person does not exist.")

        if not 0 <= transmission_probability <= 1:
            raise ValueError(
                "transmission_probability must be between 0 and 1."
            )

        if not 0 <= social_influence_strength <= 1:
            raise ValueError(
                "social_influence_strength must be between 0 and 1."
            )

        original_perceptions = {
            person.person_id: person.risk_perception
            for person in people
        }

        rng = random.Random(seed)

        warning = self.institution.issue_warning(
            crisis_severity
        )

        informed = {source_person_id}

        previous_decisions = {
            person.person_id: person.make_decision(
                crisis_severity
            )
            for person in people
        }

        round_history = []

        try:
            for round_number in range(1, max_rounds + 1):
                newly_informed = set()

                for person_id in sorted(informed):
                    neighbors = self.network.get_neighbors(person_id)

                    for neighbor_id in neighbors:
                        if neighbor_id not in informed:
                            if rng.random() < transmission_probability:
                                newly_informed.add(neighbor_id)

                informed.update(newly_informed)

                updated_perceptions = {}

                for person in people:
                    current_perception = person.risk_perception

                    if social_influence and person.person_id in informed:
                        neighbors = self.network.get_neighbors(
                            person.person_id
                        )

                        neighboring_decisions = [
                            previous_decisions[neighbor_id]
                            for neighbor_id in neighbors
                            if (
                                neighbor_id in previous_decisions
                                and neighbor_id in informed
                            )
                        ]

                        updated_perceptions[person.person_id] = (
                            person.update_risk_perception(
                                neighboring_decisions,
                                social_influence_strength
                            )
                        )
                    else:
                        updated_perceptions[person.person_id] = (
                            current_perception
                        )

                for person in people:
                    person.risk_perception = (
                        updated_perceptions[person.person_id]
                    )

                current_decisions = {
                    person.person_id: person.make_decision(
                        crisis_severity
                    )
                    for person in people
                }

                decision_counts = dict(
                    Counter(current_decisions.values())
                )

                average_risk = sum(
                    person.risk_perception for person in people
                ) / len(people)

                round_result = {
                    "round": round_number,
                    "informed_people": len(informed),
                    "newly_informed": len(newly_informed),
                    "informed_ids": sorted(informed),
                    "average_risk_perception": average_risk,
                    "decisions": decision_counts
                }

                round_history.append(round_result)
                previous_decisions = current_decisions

                remaining_possible_contacts = any(
                    any(
                        neighbor_id not in informed
                        for neighbor_id in self.network.get_neighbors(
                            person_id
                        )
                    )
                    for person_id in informed
                )

                if not remaining_possible_contacts:
                    break

            final_decisions = round_history[-1]["decisions"]
            evacuation_count = final_decisions.get("evacuate", 0)

            final_individual_responses = [
                {
                    "person_id": person.person_id,
                    "risk_perception": original_perceptions[
                        person.person_id
                    ],
                    "updated_risk_perception": person.risk_perception,
                    "preparedness": person.preparedness,
                    "decision": person.make_decision(crisis_severity)
                }
                for person in people
            ]

            support = self.institution.provide_support(
                evacuation_count
            )

            result = {
                "crisis_severity": crisis_severity,
                "warning": warning,
                "informed_people": len(informed),
                "population": self.community.total_population,
                "decisions": final_decisions,
                "individual_responses": final_individual_responses,
                "round_history": round_history,
                "rounds_completed": len(round_history),
                "institutional_support": support,
                "social_influence": social_influence,
                "social_influence_strength": social_influence_strength,
                "transmission_probability": transmission_probability
            }

            self.results.append(result)
            self.data_collector.collect(result)

            return result

        finally:
            for person in people:
                person.risk_perception = (
                    original_perceptions[person.person_id]
                )
