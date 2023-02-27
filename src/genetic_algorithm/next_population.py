import copy
import random

from src.genetic_algorithm.chromosome import Chromosome
from src.data_connectors.read_input_files import Instance


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
    all_survival_chromosomes_to_generation = all_survival_chromosomes.copy()

    sorted_chromosomes = [
        i for i, _ in sorted(enumerate(makespan_all_survival_chromosomes), key=lambda x: x[1])
    ]
    orded_by_fitness = sorted(
        all_survival_chromosomes_to_generation,
        key=lambda obj: sorted_chromosomes.index(all_survival_chromosomes_to_generation.index(obj)),
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


def generate_next_population_with_crossover_with_random_survival_parents(
    all_survival_chromosomes: list[Chromosome]
) -> list[Chromosome]:
    new_generation = []
    all_survival_chromosomes_to_generation = all_survival_chromosomes.copy()
    shuffle_chromosomes = random.sample(all_survival_chromosomes_to_generation, len(all_survival_chromosomes_to_generation))
    pairs_shuffle_chromosomes = [(shuffle_chromosomes[i], shuffle_chromosomes[i + 1]) for i in range(0, len(shuffle_chromosomes), 2)]

    for parent_1, parent_2 in pairs_shuffle_chromosomes:
        offspring_1, offspring_2 = one_point_crossover(parent_1, parent_2)
        offspring_3, offspring_4 = uniform_crossover(parent_1, parent_2)

        new_generation.append(offspring_1)
        new_generation.append(offspring_2)
        new_generation.append(offspring_3)
        new_generation.append(offspring_4)

    return new_generation


def swap_mutation_in_order(chromosome: Chromosome) -> Chromosome:
    # Choose two random indices to swap
    idx1, idx2 = random.sample(range(len(chromosome.order)), 2)
    # Swap the values at the chosen indices
    chromosome.order[idx1], chromosome.order[idx2] = chromosome.order[idx2], chromosome.order[idx1]
    return chromosome


def mutation_in_mode(chromosome: Chromosome, instance:Instance) -> Chromosome:
    # Choose a random indices
    idx = random.choice(range(len(chromosome.mode)))
    # Select a mode to get
    working_space = instance.df_workingspace_id[instance.df_workingspace_id.Id == (idx + 1)].WorkingSpace.values[0]
    possible_modes = instance.df_workingspace_resources[instance.df_workingspace_resources.WorkingSpace == working_space].Resource.unique()

    chromosome.mode[idx] = str(random.choice(possible_modes))
    return chromosome


def swap_mutation_at_probability(chromosome: Chromosome, instance: Instance, probability: float = 0.5) -> Chromosome:
    variable_probability = random.uniform(0, probability)
    n_times = int(round(len(chromosome.order) * variable_probability, 0))
    it = 0
    # print(f"Mutating {n_times} times.")
    while it < n_times:
        chromosome = swap_mutation_in_order(chromosome)
        chromosome = mutation_in_mode(chromosome, instance)
        it += 1
    return chromosome


def remove_duplicated_chromosomes(new_chromosomes: list[Chromosome]) -> list[Chromosome]:
    # go element by element
    duplicated_chromosome_indexes = []
    for i in range(len(new_chromosomes) - 1):
        for j in range(i + 1, len(new_chromosomes)):
            if new_chromosomes[i].is_equal(new_chromosomes[j]):
                duplicated_chromosome_indexes.append(j)

    unique_chromosomes = [
        j for i, j in enumerate(new_chromosomes) if i not in duplicated_chromosome_indexes
    ]

    return unique_chromosomes
