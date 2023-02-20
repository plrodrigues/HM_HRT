import numpy as np

from src.genetic_algorithm.chromosome import Chromosome


def keep_fittest_n_chromosomes(
    all_chromosomes: list[Chromosome], makespan_all_chromosomes: list[int], number_survivers: int
) -> tuple[list[int], list
[Chromosome]]:
    # THIS IS INCORRECTspo
    better_makespans = sorted(makespan_all_chromosomes)[:number_survivers+1]
    max_makespan_limit = np.max(better_makespans)
    fittest_chromosomes = [
        x for x, flag in zip(all_chromosomes, makespan_all_chromosomes < max_makespan_limit) if flag
    ]
    fittest_makespans = [
        x
        for x, flag in zip(makespan_all_chromosomes, makespan_all_chromosomes < max_makespan_limit)
        if flag
    ]
    return fittest_chromosomes, fittest_makespans


def is_this_population_better_than_previous_one(
    previous_population_makespan: list[int] | None, this_population_makespan: list[int]
) -> bool:
    if not previous_population_makespan:
        # This is for the case we are looking at the first population
        return True
    if np.mean(this_population_makespan) < np.mean(previous_population_makespan):
        return True
    else:
        return False
