
import networkx as nx


class SocialNetwork:

    def __init__(self):
        self.graph = nx.Graph()

    def add_person(self, person, household_id=None):
        self.graph.add_node(
            person.person_id,
            age=person.age,
            trust=person.trust_level,
            preparedness=person.preparedness,
            household_id=household_id
        )

    def connect_people(
        self,
        person_id_1,
        person_id_2,
        relationship_type="social"
    ):
        self.graph.add_edge(
            person_id_1,
            person_id_2,
            relationship_type=relationship_type
        )

    def get_neighbors(self, person_id):
        return list(self.graph.neighbors(person_id))

    def network_statistics(self):
        return {
            "people": self.graph.number_of_nodes(),
            "connections": self.graph.number_of_edges(),
            "average_connections": (
                2 * self.graph.number_of_edges()
                / self.graph.number_of_nodes()
                if self.graph.number_of_nodes() > 0
                else 0
            ),
            "households": len(set(
                nx.get_node_attributes(
                    self.graph, "household_id"
                ).values()
            ))
        }
