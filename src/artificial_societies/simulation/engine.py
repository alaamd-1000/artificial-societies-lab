
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

        if max_rounds < 1:
            raise ValueError("max_rounds must be at least 1.")

        people_by_id = {
            person.person_id: person
            for person in people
        }

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

        # Save original risk perceptions.
        original_perceptions = {
            person.person_id: person.risk_perception
            for person in people
        }

        rng = random.Random(seed)

        warning = self.institution.issue_warning(
            crisis_severity
        )

        # Initially, only the source person is informed.
        informed = {source_person_id}

        # Initial decisions before the first round.
        previous_decisions = {
            person.person_id: person.make_decision(
                crisis_severity
            )
            for person in people
        }

        round_history = []

        try:

            # Start the simulation rounds.
            for round_number in range(1, max_rounds + 1):

                # 1. Spread warning through the social network.
                newly_informed = set()

                for person_id in sorted(informed):

                    neighbors = self.network.get_neighbors(
                        person_id
                    )

                    for neighbor_id in neighbors:

                        if neighbor_id not in informed:
                            if (
                                rng.random()
                                < transmission_probability
                            ):
                                newly_informed.add(neighbor_id)

                informed.update(newly_informed)

                # 2. Calculate new risk perceptions.
                updated_perceptions = {}

                for person in people:

                    current_perception = (
                        person.risk_perception
                    )

                    if (
                        social_influence
                        and person.person_id in informed
                    ):

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

                # 3. Apply perception updates simultaneously.
                for person in people:

                    person.risk_perception = (
                        updated_perceptions[person.person_id]
                    )

                # 4. Calculate decisions for this round.
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
                    person.risk_perception
                    for person in people
                ) / len(people)

                # 5. Store round results.
                round_result = {
                    "round": round_number,
                    "informed_people": len(informed),
                    "newly_informed": len(newly_informed),
                    "informed_ids": sorted(informed),
                    "average_risk_perception": average_risk,
                    "decisions": decision_counts
                }

                round_history.append(round_result)

                # 6. Stop when information and decisions stabilize.
                if (
                    not newly_informed
                    and current_decisions == previous_decisions
                ):
                    break

                previous_decisions = current_decisions

            # Final decisions.
            final_decisions = round_history[-1]["decisions"]

            evacuation_count = final_decisions.get(
                "evacuate", 0
            )

            # 7. Save individual responses.
            final_individual_responses = [
                {
                    "person_id": person.person_id,
                    "risk_perception": original_perceptions[
                        person.person_id
                    ],
                    "updated_risk_perception": person.risk_perception,
                    "preparedness": person.preparedness,
                    "decision": person.make_decision(
                        crisis_severity
                    )
                }
                for person in people
            ]

            # 8. Calculate institutional support.
            support = self.institution.provide_support(
                evacuation_count
            )

            # 9. Build final experiment result.
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

            # Restore original perceptions after the experiment.
            for person in people:

                person.risk_perception = (
                    original_perceptions[person.person_id]
                )
