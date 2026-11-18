
from dataclasses import dataclass, field
from typing import List

from src.artificial_societies.agents.person import PersonAgent


@dataclass
class HouseholdAgent:
    household_id: int
    members: List[PersonAgent] = field(default_factory=list)

    @property
    def household_size(self) -> int:
        return len(self.members)

    def average_preparedness(self) -> float:
        if not self.members:
            return 0.0

        return sum(
            person.preparedness for person in self.members
        ) / len(self.members)

    def household_decisions(self, crisis_severity: float) -> list:
        return [
            person.make_decision(crisis_severity)
            for person in self.members
        ]
