# Artificial Societies Lab

### An Agent-Based Model of Crisis Information Diffusion and Social Responses

## Overview

Artificial Societies Lab is an exploratory agent-based modeling (ABM) project designed to examine how crisis warnings spread through social networks and how individuals respond to crisis situations within a synthetic community.

The model represents a simplified artificial society composed of individuals, households, social connections, and an emergency institution. It explores the relationships between warning transmission, individual risk perception, social influence, and behavioral responses.

The project aims to provide a computational environment for studying social responses to crises through simulation.

## Research Objectives

- Explore how crisis information spreads through interconnected social networks.
- Examine how warning transmission probability influences the number of informed individuals.
- Investigate the relationship between social influence and individual risk perception.
- Explore how individuals make decisions under different crisis severity levels.
- Examine variations in collective responses across simulation scenarios.

## Model Structure

The artificial society consists of four main components:

**1. Individual Agents**

Each individual is characterized by attributes such as:

- Age
- Education level
- Income
- Available resources
- Risk perception
- Trust level
- Preparedness

Agents make behavioral decisions based on perceived crisis risk and preparedness.

**2. Household Agents**

Individuals are organized into households. Household-level characteristics are used to represent basic social organization within the artificial community.

**3. Social Network**

Individuals are connected through a social network. These connections provide pathways through which crisis warnings can spread.

**4. Institutional Agent**

An emergency institution issues warnings according to crisis severity and provides limited support to individuals.

## Simulation Mechanisms

The model incorporates several mechanisms:

- **Warning Diffusion:** Information spreads between connected individuals according to a specified transmission probability.
- **Risk Perception:** Individual risk perception can change through social influence.
- **Behavioral Decision-Making:** Individuals select responses based on perceived risk and preparedness.
- **Institutional Support:** The emergency institution provides support subject to its available resources and response capacity.

Individuals can make decisions even if they have not received the warning. This represents an intentional model assumption: decisions may also be influenced by their existing risk perceptions.

## Experimental Design

The initial experiments examine three crisis severity levels:

- Low severity: 0.3
- Moderate severity: 0.6
- High severity: 0.9

The model also compares scenarios with and without social influence.

A sensitivity experiment explores combinations of:

- Warning transmission probabilities: 0.1, 0.3, 0.5, and 0.7.
- Social influence strengths: 0.1, 0.3, 0.5, and 0.7.

Each parameter combination is repeated across 10 random seeds, producing 160 simulation runs.

## Initial Simulation Results

The initial experiments show that:

- Higher warning transmission probabilities are associated with greater information diffusion.
- Social influence can affect average risk perception and behavioral responses.
- Different random seeds can produce substantial variation in simulation outcomes.
- The relationship between information diffusion and behavioral response requires further investigation.

These findings are exploratory and describe the behavior of the current simulation model, not verified patterns in real-world populations.

## Technologies

- Python
- Mesa
- NumPy
- Pandas
- NetworkX
- Matplotlib

## Project Structure

```text
artificial_societies_lab/
│
├── src/
│   └── artificial_societies/
│       ├── agents/
│       ├── behavior/
│       ├── networks/
│       ├── simulation/
│       ├── analysis/
│       └── visualization/
│
├── outputs/
│   ├── figures/
│   ├── animations/
│   └── reports/
│
├── run_experiment.py
├── analyze_simulation.py
├── create_animation.py
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/alaamd-1000/artificial-societies-lab.git
cd artificial-societies-lab
```

Install the required Python libraries:

```bash
pip install mesa numpy pandas networkx matplotlib pillow
```

## Run the Simulation

Execute the main experiment:

```bash
python3 run_experiment.py
```

The simulation generates figures, animation files, and experimental reports in the `outputs/` directory.

## Limitations

This project is an exploratory computational model.

Its current limitations include:

- The artificial population does not represent a validated real-world population.
- Individual behavioral rules are simplified.
- Several individual attributes are not yet incorporated into decision-making.
- Model parameters require further empirical justification.
- The number of replications is preliminary.
- The model has not been validated against real crisis response data.

Further development should focus on behavioral realism, empirical calibration, robustness analysis, and validation.

## Future Development

Potential directions include:

- More sophisticated behavioral decision mechanisms.س
- Empirically informed social network structures.
- Integration of real-world disaster and population datasets.
- Expanded institutional interaction mechanisms.
- Additional sensitivity and robustness experiments.
- Comparative analysis across different artificial community structures.

## Research Area

Agent-Based Modeling | Artificial Societies | Computational Social Science | Complex Systems | Crisis Information Diffusion | Social Simulation

---

**Project Status:** Exploratory research project under development.
