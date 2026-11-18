from dataclasses import dataclass


@dataclass
class InstitutionAgent:
    institution_id: int
    name: str
    resources: float
    response_capacity: int
    trust_level: float

    def provide_support(self, requested_people: int) -> dict:
        affordable_people = max(0, int(self.resources // 2))

        supported_people = max(
            0,
            min(
                requested_people,
                self.response_capacity,
                affordable_people
            )
        )

        resources_used = supported_people * 2

        self.resources -= resources_used

        return {
            "institution": self.name,
            "supported_people": supported_people,
            "resources_used": resources_used,
            "remaining_resources": self.resources
        }

    def issue_warning(self, crisis_severity: float) -> str:
        if crisis_severity >= 0.7:
            return "Emergency warning"

        if crisis_severity >= 0.4:
            return "Risk alert"

        return "Normal monitoring"
