
import os
import matplotlib.pyplot as plt
import networkx as nx

from matplotlib.animation import FuncAnimation, PillowWriter
from src.artificial_societies.networks.social_network import SocialNetwork
from src.artificial_societies.behavior.social_influence import spread_warning
from src.artificial_societies.agents.person import PersonAgent

# Create five people
people = [
    PersonAgent(1, 25, "university", 5000, 80, 0.95, 0.9, 0.9),
    PersonAgent(2, 40, "secondary", 3000, 40, 0.90, 0.3, 0.3),
    PersonAgent(3, 32, "university", 6000, 100, 0.65, 0.8, 0.8),
    PersonAgent(4, 55, "primary", 2000, 20, 0.50, 0.4, 0.4),
    PersonAgent(5, 19, "secondary", 1500, 15, 0.30, 0.7, 0.7)
]

# Build social network
network = SocialNetwork()

for person in people:
    network.add_person(person)

for i in range(1, 5):
    network.connect_people(i, i + 1)

# Calculate warning spread
result = spread_warning(network, source_person_id=1)
rounds = result["rounds"]

# Prepare animation
fig, ax = plt.subplots(figsize=(8, 6))
positions = nx.spring_layout(network.graph, seed=42)


def update(frame):
    ax.clear()

    informed = set()

    for group in rounds[:frame + 1]:
        informed.update(group)

    colors = [
        "tomato" if node in informed else "lightgray"
        for node in network.graph.nodes()
    ]

    nx.draw_networkx(
        network.graph,
        positions,
        ax=ax,
        with_labels=True,
        node_color=colors,
        node_size=1400,
        edge_color="gray"
    )

    ax.set_title(f"Warning Spread - Round {frame + 1}")
    ax.axis("off")


animation = FuncAnimation(
    fig,
    update,
    frames=len(rounds),
    interval=1200,
    repeat=True
)

os.makedirs("outputs/animations", exist_ok=True)

animation.save(
    "outputs/animations/warning_spread.gif",
    writer=PillowWriter(fps=1)
)

plt.close(fig)

print("Animation saved successfully!")
print("Total informed people:", result["total_informed"])
