import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Load simulation data
file_path = "outputs/reports/warning_transmission_rounds.csv"

df = pd.read_csv(file_path)

if df.empty:
    raise ValueError("The simulation data file is empty.")

df = df.sort_values("round")

os.makedirs("outputs/figures", exist_ok=True)
os.makedirs("outputs/reports", exist_ok=True)


# 2. Warning diffusion
plt.figure(figsize=(10, 6))

plt.plot(
    df["round"],
    df["informed_people"],
    marker="o",
    linewidth=2
)

plt.xlabel("Simulation Round")
plt.ylabel("Number of Informed People")
plt.title("Warning Diffusion Across Simulation Rounds")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "outputs/figures/warning_diffusion.png",
    dpi=300
)
plt.close()


# 3. Risk perception
plt.figure(figsize=(10, 6))

plt.plot(
    df["round"],
    df["average_risk_perception"],
    marker="o",
    linewidth=2
)

plt.xlabel("Simulation Round")
plt.ylabel("Average Risk Perception")
plt.title("Evolution of Average Risk Perception")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "outputs/figures/risk_perception.png",
    dpi=300
)
plt.close()


# 4. Behavioral responses
decision_columns = [
    "evacuate",
    "seek_information",
    "prepare",
    "continue_normal_activity"
]

available_decisions = [
    column for column in decision_columns
    if column in df.columns
]

if available_decisions:

    plt.figure(figsize=(11, 6))

    for decision in available_decisions:
        plt.plot(
            df["round"],
            df[decision],
            marker="o",
            label=decision
        )

    plt.xlabel("Simulation Round")
    plt.ylabel("Number of People")
    plt.title("Behavioral Responses Across Simulation Rounds")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "outputs/figures/behavioral_responses.png",
        dpi=300
    )
    plt.close()


# 5. Descriptive statistics
statistics = df[
    [
        "informed_people",
        "newly_informed",
        "average_risk_perception"
    ]
].describe()

statistics.to_csv(
    "outputs/reports/simulation_statistics.csv"
)


# 6. Display results
print("\nSIMULATION ANALYSIS COMPLETED")

print("Number of rounds:", len(df))

print(
    "Final informed people:",
    df["informed_people"].iloc[-1]
)

print(
    "Final average risk perception:",
    round(df["average_risk_perception"].iloc[-1], 3)
)

print("\nDescriptive Statistics:")
print(statistics)

print("\nFigures saved in: outputs/figures/")
print("Statistics saved in: outputs/reports/")
