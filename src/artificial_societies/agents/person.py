
from dataclasses import dataclass


@dataclass
class PersonAgent:
    person_id: int
    age: int
    education_level: str
    income: float
    resources: float
    risk_perception: float
    trust_level: float
    preparedness: float

    def update_risk_perception(
        self,
        neighboring_decisions,
        social_influence_strength=0.3
    ):

        if not neighboring_decisions:
            return self.risk_perception

        concern_decisions = {
            "prepare",
            "seek_information",
            "evacuate"
        }

        concerned = sum(
            decision in concern_decisions
            for decision in neighboring_decisions
        )

        social_concern = concerned / len(
            neighboring_decisions
        )

        updated_perception = (
            self.risk_perception
            + social_influence_strength
            * (social_concern - self.risk_perception)
        )

        return max(0.0, min(1.0, updated_perception))

    def make_decision(
        self,
        crisis_severity: float,
        risk_perception=None
    ):

        if risk_perception is None:
            risk_perception = self.risk_perception

        perceived_risk = (
            crisis_severity * risk_perception
        )

        if perceived_risk >= 0.7:

            if self.preparedness >= 0.6:
                return "evacuate"

            return "seek_information"

        if perceived_risk >= 0.4:
            return "prepare"

        return "continue_normal_activity"
