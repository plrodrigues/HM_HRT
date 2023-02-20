import random

from src.genetic_algorithm.chromosome import Chromosome


def one_point_crossover(
    parent_1: Chromosome, parent_2: Chromosome
) -> tuple[Chromosome, Chromosome]:
    # perform one point crossover between two chromosomes
    # Choose a random crossover point
    crossover_point = random.randint(1, len(parent_1.mode) - 1)

    # Create the first offspring chromosome
    offspring_1 = Chromosome(
        mode=parent_1.mode[:crossover_point] + parent_2.mode[crossover_point:],
        order=parent_1.order,
    )

    # create the second offspring chromosome
    offspring_2 = Chromosome(
        mode=parent_2.mode[:crossover_point] + parent_1.mode[crossover_point:],
        order=parent_2.order,
    )

    return offspring_1, offspring_2


def uniform_crossover(
    parent_1: Chromosome, parent_2: Chromosome, probability: float = 0.5
) -> tuple[Chromosome, Chromosome]:
    # Perform uniform crossover between two chromosomes
    offspring_1_order = parent_1.mode
    offspring_2_order = parent_2.mode

    # For each gene, swap with the corresponding gene from the other chromosome with probability p
    for i in range(len(parent_1.mode)):
        if random.random() < probability:
            offspring_1_order[i], offspring_2_order[i] = offspring_2_order[i], offspring_1_order[i]

    offspring_1 = Chromosome(mode=offspring_1_order, order=parent_1.order)
    offspring_2 = Chromosome(mode=offspring_2_order, order=parent_2.order)

    return offspring_1, offspring_2


def generate_next_population_with_crossover(
    all_survival_chromosomes: list[Chromosome], makespan_all_survival_chromosomes: list[int]
) -> list[Chromosome]:
    new_generation = []

    sorted_chromosomes = [
        i for i, _ in sorted(enumerate(makespan_all_survival_chromosomes), key=lambda x: x[1])
    ]
    orded_by_fitness = sorted(
        all_survival_chromosomes,
        key=lambda obj: sorted_chromosomes.index(all_survival_chromosomes.index(obj)),
    )

    for i in range(0, len(orded_by_fitness) - 1, 2):
        parent_1 = orded_by_fitness[i]
        parent_2 = orded_by_fitness[i + 1]

        offspring_1, offspring_2 = one_point_crossover(parent_1, parent_2)
        offspring_3, offspring_4 = uniform_crossover(parent_1, parent_2)

        new_generation.append(offspring_1)
        new_generation.append(offspring_2)
        new_generation.append(offspring_3)
        new_generation.append(offspring_4)

    return new_generation


def swap_mutation(chromosome: Chromosome) -> Chromosome:
    # Choose two random indices to swap
    idx1, idx2 = random.sample(range(len(chromosome.order)), 2)
    # Swap the values at the chosen indices
    chromosome.order[idx1], chromosome.order[idx2] = chromosome.order[idx2], chromosome.order[idx1]
    return chromosome


def swap_mutation_at_probability(chromosome: Chromosome, probability: float = 0.5) -> Chromosome:
    n_times = int(round(len(chromosome.order) * probability, 0))
    it = 0
    while it < n_times:
        chromosome = swap_mutation(chromosome)
        it += 1
    return chromosome
