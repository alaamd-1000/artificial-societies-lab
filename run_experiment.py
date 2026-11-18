
import pandas as pd
import random
import os
import itertools
import json

import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, PillowWriter

from src.artificial_societies.agents.person import PersonAgent
from src.artificial_societies.agents.household import HouseholdAgent
from src.artificial_societies.agents.community import CommunityAgent
from src.artificial_societies.agents.institution import InstitutionAgent
from src.artificial_societies.networks.social_network import SocialNetwork
from src.artificial_societies.simulation.engine import SimulationEngine


# --------------------------------------------------
# 1. Create a heterogeneous population of 100 people
# --------------------------------------------------

random.seed(42)

people = []

education_levels = [
    "primary",
    "secondary",
    "university"
]

for person_id in range(1, 101):

    age = random.randint(18, 75)
    education = random.choice(education_levels)
    income = random.uniform(1000, 10000)
    resources = random.uniform(10, 100)
    risk_perception = random.uniform(0.1, 1.0)
    trust_level = random.uniform(0.1, 1.0)
    preparedness = random.uniform(0.1, 1.0)

    person = PersonAgent(
        person_id,
        age,
        education,
        income,
        resources,
        risk_perception,
        trust_level,
        preparedness
    )

    people.append(person)


print("\nARTIFICIAL SOCIETY")
print("Total population:", len(people))


# --------------------------------------------------
# 2. Create 20 households, each with 5 people
# --------------------------------------------------

households = []

household_size = 5

for i in range(0, len(people), household_size):

    household_id = (i // household_size) + 1

    members = people[i:i + household_size]

    household = HouseholdAgent(
        household_id,
        members
    )

    households.append(household)


community = CommunityAgent(1, households)

print("Total households:", community.household_count)
print("People per household:", household_size)


# --------------------------------------------------
# 3. Build a clustered social network
# --------------------------------------------------

network = SocialNetwork()

# Add people and assign household membership
for household in households:

    for person in household.members:

        network.add_person(
            person,
            household_id=household.household_id
        )


# Create strong connections within each household
for household in households:

    members = household.members

    for person_1, person_2 in itertools.combinations(
        members, 2
    ):

        network.connect_people(
            person_1.person_id,
            person_2.person_id,
            relationship_type="within_household"
        )


# Create connections between neighboring households
for i in range(len(households)):

    current_household = households[i]

    next_household = households[
        (i + 1) % len(households)
    ]

    person_1 = random.choice(current_household.members)
    person_2 = random.choice(next_household.members)

    network.connect_people(
        person_1.person_id,
        person_2.person_id,
        relationship_type="between_households"
    )


print("\nSOCIAL NETWORK")
print(network.network_statistics())


# --------------------------------------------------
# 4. Create a fresh institution for each experiment
# --------------------------------------------------

def create_institution():

    return InstitutionAgent(
        institution_id=1,
        name="Emergency Center",
        resources=1000,
        response_capacity=30,
        trust_level=0.8
    )


# --------------------------------------------------
# 5. Initialize the simulation
# --------------------------------------------------

engine = SimulationEngine(
    community,
    network,
    create_institution()
)


# --------------------------------------------------
# 6. Compare scenarios with and without social influence
# --------------------------------------------------

for severity in [0.3, 0.6, 0.9]:

    # Baseline experiment
    engine.institution = create_institution()

    engine.run(
        crisis_severity=severity,
        source_person_id=1,
        social_influence=False,
        seed=42
    )

    # Social influence experiment
    engine.institution = create_institution()

    engine.run(
        crisis_severity=severity,
        source_person_id=1,
        social_influence=True,
        social_influence_strength=0.3,
        seed=42
    )


# --------------------------------------------------
# 7. Display simulation results
# --------------------------------------------------

df = engine.data_collector.to_dataframe()

print("\nCRISIS SCENARIO RESULTS")

print(
    df[["crisis_severity", "warning", "decisions"]]
    .to_string(index=False)
)


# --------------------------------------------------
# 8. Visualize community responses
# --------------------------------------------------

decision_types = [
    "evacuate",
    "seek_information",
    "prepare",
    "continue_normal_activity"
]

severities = [0.3, 0.6, 0.9]

fig, axes = plt.subplots(
    2, 2,
    figsize=(12, 9)
)

axes = axes.flatten()

for ax, decision in zip(axes, decision_types):

    baseline_counts = []
    social_counts = []

    for severity in severities:

        matching_results = [
            result
            for result in engine.results
            if result["crisis_severity"] == severity
        ]

        baseline = next(
            result for result in matching_results
            if not result["social_influence"]
        )

        social = next(
            result for result in matching_results
            if result["social_influence"]
        )

        baseline_counts.append(
            baseline["decisions"].get(decision, 0)
        )

        social_counts.append(
            social["decisions"].get(decision, 0)
        )

    x = range(len(severities))
    width = 0.35

    ax.bar(
        [i - width / 2 for i in x],
        baseline_counts,
        width,
        label="Without social influence"
    )

    ax.bar(
        [i + width / 2 for i in x],
        social_counts,
        width,
        label="With social influence"
    )

    ax.set_title(decision.replace("_", " ").title())
    ax.set_xlabel("Crisis Severity")
    ax.set_ylabel("Number of People")
    ax.set_xticks(list(x))
    ax.set_xticklabels(severities)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)


fig.suptitle(
    "Comparison of Community Responses Across Crisis Scenarios",
    fontsize=14
)

fig.tight_layout()

os.makedirs("outputs/figures", exist_ok=True)

fig.savefig(
    "outputs/figures/community_responses.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# --------------------------------------------------
# 9. Visualize the household-based social network
# --------------------------------------------------

G = network.graph

node_colors = [
    G.nodes[node]["preparedness"]
    for node in G.nodes()
]

within_edges = [
    (u, v)
    for u, v, data in G.edges(data=True)
    if data["relationship_type"] == "within_household"
]

between_edges = [
    (u, v)
    for u, v, data in G.edges(data=True)
    if data["relationship_type"] == "between_households"
]

positions = nx.spring_layout(
    G,
    seed=42,
    k=0.35
)

fig, ax = plt.subplots(figsize=(13, 10))

nx.draw_networkx_edges(
    G,
    positions,
    edgelist=within_edges,
    ax=ax,
    edge_color="gray",
    width=0.7,
    alpha=0.45
)

nx.draw_networkx_edges(
    G,
    positions,
    edgelist=between_edges,
    ax=ax,
    edge_color="red",
    width=1.8,
    alpha=0.8
)

nx.draw_networkx_nodes(
    G,
    positions,
    ax=ax,
    node_color=node_colors,
    cmap=plt.cm.viridis,
    vmin=0,
    vmax=1,
    node_size=110
)

ax.set_title(
    "Artificial Society: 20 Households and 100 People"
)

sm = plt.cm.ScalarMappable(
    cmap=plt.cm.viridis,
    norm=plt.Normalize(vmin=0, vmax=1)
)

sm.set_array([])

fig.colorbar(
    sm,
    ax=ax,
    label="Preparedness Level"
)

ax.axis("off")
fig.tight_layout()

fig.savefig(
    "outputs/figures/social_network.png",
    dpi=300
)

plt.close(fig)


# --------------------------------------------------
# 10. Get warning transmission from dynamic simulation
# --------------------------------------------------

# Select the last experiment:
# Crisis severity = 0.9
# Social influence = True

dynamic_result = engine.results[-1]

round_history = dynamic_result["round_history"]

if not round_history:
    raise ValueError(
        "No dynamic simulation rounds were recorded."
    )

final_round = round_history[-1]

print("\nDYNAMIC WARNING TRANSMISSION")
print("Transmission rounds:", len(round_history))

print(
    "Total informed people:",
    final_round["informed_people"]
)


# --------------------------------------------------
# 11. Create dynamic warning spread animation
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 9))

positions = nx.spring_layout(
    network.graph,
    seed=42,
    k=0.35
)


def update(frame):

    ax.clear()

    round_data = round_history[frame]

    informed = set(round_data["informed_ids"])

    colors = [
        "tomato" if person_id in informed else "lightgray"
        for person_id in network.graph.nodes()
    ]

    nx.draw_networkx_edges(
        network.graph,
        positions,
        ax=ax,
        edge_color="gray",
        width=0.6,
        alpha=0.4
    )

    nx.draw_networkx_nodes(
        network.graph,
        positions,
        ax=ax,
        node_color=colors,
        node_size=110
    )

    ax.set_title(
        f"Dynamic Warning Spread - Round {round_data['round']}\n"
        f"Informed: {round_data['informed_people']} / {len(people)} | "
        f"Newly informed: {round_data['newly_informed']}"
    )

    ax.axis("off")


animation = FuncAnimation(
    fig,
    update,
    frames=len(round_history),
    interval=1200,
    repeat=True
)

os.makedirs("outputs/animations", exist_ok=True)

animation.save(
    "outputs/animations/warning_spread.gif",
    writer=PillowWriter(fps=1)
)

plt.close(fig)


# --------------------------------------------------
# 12. Save experiment results
# --------------------------------------------------

os.makedirs("outputs/reports", exist_ok=True)


# Save all individual responses
all_responses = []

for result in engine.results:

    for person in result["individual_responses"]:

        all_responses.append({
            "crisis_severity": result["crisis_severity"],
            "social_influence": result["social_influence"],
            "person_id": person["person_id"],
            "risk_perception": person["risk_perception"],
            "updated_risk_perception": person["updated_risk_perception"],
            "preparedness": person["preparedness"],
            "decision": person["decision"]
        })


responses_df = pd.DataFrame(all_responses)

responses_df.to_csv(
    "outputs/reports/social_influence_results.csv",
    index=False
)


# Save experiment summary
summary_rows = []

for result in engine.results:

    row = {
        "crisis_severity": result["crisis_severity"],
        "social_influence": result["social_influence"],
        "informed_people": result["informed_people"],
        "rounds_completed": result["rounds_completed"]
    }

    row.update(result["decisions"])

    summary_rows.append(row)


summary_df = pd.DataFrame(summary_rows)

summary_df.to_csv(
    "outputs/reports/experiment_summary.csv",
    index=False
)


# Save dynamic warning transmission history
round_rows = []

for round_data in round_history:

    row = {
        "round": round_data["round"],
        "informed_people": round_data["informed_people"],
        "newly_informed": round_data["newly_informed"],
        "average_risk_perception": round_data["average_risk_perception"],
        "informed_ids": ";".join(
            map(str, round_data["informed_ids"])
        )
    }

    row.update(round_data["decisions"])

    round_rows.append(row)


rounds_df = pd.DataFrame(round_rows)

rounds_df.to_csv(
    "outputs/reports/warning_transmission_rounds.csv",
    index=False
)


print("\nEXPERIMENT DATA SAVED")

print(
    "Individual results: "
    "outputs/reports/social_influence_results.csv"
)

print(
    "Summary results: "
    "outputs/reports/experiment_summary.csv"
)

print(
    "Warning transmission: "
    "outputs/reports/warning_transmission_rounds.csv"
)


# --------------------------------------------------
# 13. Final summary
# --------------------------------------------------

print("\nSIMULATION COMPLETED")

print("Population:", community.total_population)
print("Households:", community.household_count)
print("Network:", network.network_statistics())

print("Figures saved in: outputs/figures/")
print("Animation saved in: outputs/animations/")
print("Reports saved in: outputs/reports/")


# --------------------------------------------------
# 14. Sensitivity Analysis with Multiple Replications
# --------------------------------------------------

print("\nSTARTING MULTIPLE REPLICATIONS")

transmission_values = [0.1, 0.3, 0.5, 0.7]

social_strength_values = [0.1, 0.3, 0.5, 0.7]

seeds = list(range(42, 52))

replication_results = []

for transmission in transmission_values:

    for strength in social_strength_values:

        for seed in seeds:

            # Create a fresh institution for every experiment
            fresh_institution = create_institution()

            # Create a fresh simulation engine
            sensitivity_engine = SimulationEngine(
                community,
                network,
                fresh_institution
            )

            result = sensitivity_engine.run(
                crisis_severity=0.9,
                source_person_id=1,
                social_influence=True,
                social_influence_strength=strength,
                transmission_probability=transmission,
                max_rounds=20,
                seed=seed
            )

            final_round = result["round_history"][-1]

            replication_results.append({
                "transmission_probability": transmission,
                "social_influence_strength": strength,
                "seed": seed,
                "informed_people": result["informed_people"],
                "evacuate": result["decisions"].get("evacuate", 0),
                "prepare": result["decisions"].get("prepare", 0),
                "seek_information": result["decisions"].get(
                    "seek_information", 0
                ),
                "continue_normal_activity": result["decisions"].get(
                    "continue_normal_activity", 0
                ),
                "average_risk_perception": final_round[
                    "average_risk_perception"
                ],
                "rounds_completed": result["rounds_completed"],
                "resources_remaining": fresh_institution.resources
            })


# --------------------------------------------------
# 15. Save replication results
# --------------------------------------------------

replications_df = pd.DataFrame(replication_results)

replications_df.to_csv(
    "outputs/reports/sensitivity_replications.csv",
    index=False
)


# Calculate mean and standard deviation
metrics = [
    "informed_people",
    "evacuate",
    "prepare",
    "seek_information",
    "continue_normal_activity",
    "average_risk_perception",
    "rounds_completed",
    "resources_remaining"
]

sensitivity_summary = (
    replications_df
    .groupby([
        "transmission_probability",
        "social_influence_strength"
    ])[metrics]
    .agg(["mean", "std"])
    .reset_index()
)

sensitivity_summary.to_csv(
    "outputs/reports/sensitivity_replications_summary.csv",
    index=False
)


# --------------------------------------------------
# 16. Visualize mean warning diffusion
# --------------------------------------------------

informed_means = (
    replications_df
    .groupby([
        "transmission_probability",
        "social_influence_strength"
    ])["informed_people"]
    .mean()
    .unstack()
)

plt.figure(figsize=(9, 6))

plt.imshow(
    informed_means.values,
    aspect="auto",
    origin="lower"
)

plt.colorbar(label="Mean Informed People")

plt.xticks(
    range(len(informed_means.columns)),
    informed_means.columns
)

plt.yticks(
    range(len(informed_means.index)),
    informed_means.index
)

plt.xlabel("Social Influence Strength")
plt.ylabel("Transmission Probability")

plt.title(
    "Mean Warning Diffusion Across 10 Replications"
)

plt.tight_layout()

plt.savefig(
    "outputs/figures/mean_warning_diffusion.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# 17. Save experiment configuration
# --------------------------------------------------

experiment_config = {
    "population_size": len(people),
    "household_count": community.household_count,
    "household_size": household_size,
    "initial_crisis_severity": 0.9,
    "source_person_id": 1,
    "social_influence": True,
    "transmission_probabilities": transmission_values,
    "social_influence_strengths": social_strength_values,
    "random_seeds": seeds,
    "replications_per_combination": len(seeds),
    "total_replications": len(replications_df),
    "maximum_rounds": 20,
    "institution_initial_resources": 1000,
    "institution_response_capacity": 30,
    "institution_trust_level": 0.8
}

with open(
    "outputs/reports/experiment_configuration.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        experiment_config,
        file,
        indent=4
    )


# --------------------------------------------------
# 18. Display replication results
# --------------------------------------------------

print("\nMULTIPLE REPLICATIONS COMPLETED")

print("Total experiments:", len(replications_df))

print(
    "Replications per combination:",
    len(seeds)
)

print("\nMEAN RESULTS:")

print(
    replications_df
    .groupby([
        "transmission_probability",
        "social_influence_strength"
    ])[
        [
            "informed_people",
            "evacuate",
            "average_risk_perception"
        ]
    ]
    .mean()
    .round(3)
)

print("\nSTANDARD DEVIATION:")

print(
    replications_df
    .groupby([
        "transmission_probability",
        "social_influence_strength"
    ])[
        [
            "informed_people",
            "evacuate",
            "average_risk_perception"
        ]
    ]
    .std()
    .round(3)
)


print("\nFILES SAVED:")

print("outputs/reports/sensitivity_replications.csv")

print(
    "outputs/reports/sensitivity_replications_summary.csv"
)

print("outputs/figures/mean_warning_diffusion.png")

print("outputs/reports/experiment_configuration.json")

print("\nALL EXPERIMENTS COMPLETED SUCCESSFULLY")
