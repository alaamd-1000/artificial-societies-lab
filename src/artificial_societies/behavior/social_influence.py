
import random


def spread_warning(
    network,
    source_person_id,
    transmission_probability=1.0,
    seed=42
):
    rng = random.Random(seed)

    informed = {source_person_id}
    current_round = {source_person_id}

    rounds = [[source_person_id]]

    while current_round:
        next_round = set()

        for person_id in current_round:
            neighbors = network.get_neighbors(person_id)

            for neighbor_id in neighbors:
                if neighbor_id in informed:
                    continue

                if rng.random() < transmission_probability:
                    next_round.add(neighbor_id)

        informed.update(next_round)

        if next_round:
            rounds.append(sorted(next_round))

        current_round = next_round

    return {
        "rounds": rounds,
        "informed_people": sorted(informed),
        "total_informed": len(informed)
    }
