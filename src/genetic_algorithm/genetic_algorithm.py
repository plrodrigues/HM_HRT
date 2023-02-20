import datetime

from src.data_connectors.read_input_files import Instance
from src.genetic_algorithm import (
    feasibility,
    first_population,
    fitness,
    next_population,
    replication,
    time_allocation,
)
from src.genetic_algorithm.chromosome import Chromosome


def generate_first_population(instance: Instance) -> list[Chromosome]:
    # Modes
    possible_modes = first_population.get_possible_modes(instance)

    # Tasks
    n_tasks = first_population.get_total_number_of_tasks_per_working_space(instance)

    # Chromosomes
    all_chromosomes = first_population.get_first_population(possible_modes, n_tasks)
    return all_chromosomes


def keep_feasible_chromosomes(
    instance: Instance, all_chromosomes: list[Chromosome]
) -> list[Chromosome]:
    precedence_feasible_chromosomes = []
    for i in range(len(all_chromosomes)):
        chrom = all_chromosomes[i]
        if feasibility.is_chromosome_precedence_feasible(instance, chrom):
            precedence_feasible_chromosomes.append(chrom)

    print(f"From {len(all_chromosomes)} to {len(precedence_feasible_chromosomes)}")

    task_mode_feasible_chromosomes = []
    for i in range(len(precedence_feasible_chromosomes)):
        chrom = precedence_feasible_chromosomes[i]
        if feasibility.is_chromosome_task_mode_feasible(instance, chrom):
            task_mode_feasible_chromosomes.append(chrom)

    print(f"From {len(precedence_feasible_chromosomes)} to {len(task_mode_feasible_chromosomes)}")

    return task_mode_feasible_chromosomes


def add_replication_of_remaining_working_spaces(
    instance: Instance, all_chromosomes: list[Chromosome]
) -> list[Chromosome]:
    # for all feasible chromosomes
    replicated_chromosomes = []
    for chromosome in all_chromosomes:
        replicated_chromosomes.append(
            replication.update_chromosome_with_replication(instance, chromosome)
        )

    print(f"add_replication_of_remaining_working_spaces: {len(replicated_chromosomes)}")
    return replicated_chromosomes


def add_times_and_find_makespan(instance: Instance, all_chromosomes: list[Chromosome]) -> list[int]:
    # for all replicated chromosomes
    time_allocated_chromosomes = []
    for chromosome in all_chromosomes:
        time_allocated_chromosomes.append(
            time_allocation.get_all_time_allocations(instance, chromosome)
        )

    print(f"add_times_and_find_makespan with time: {len(time_allocated_chromosomes)}")

    # for all results
    makespan_all_chromosomes = []
    for chromosome_time_allocation in time_allocated_chromosomes:
        makespan_all_chromosomes.append(time_allocation.find_makespan(chromosome_time_allocation))

    print(f"add_times_and_find_makespan, makespan: {len(makespan_all_chromosomes)}")
    return makespan_all_chromosomes


def keep_fittest_chromosomes(
    task_mode_feasible_chromosomes: list[Chromosome], makespan_all_chromosomes: list[int]
) -> tuple[list[Chromosome], list[int]]:
    fittest_chromosomes, fittest_makespan = fitness.keep_fittest_n_chromosomes(
        task_mode_feasible_chromosomes, makespan_all_chromosomes, 100
    )
    print(f"How many fittest chromosomes: {len(fittest_chromosomes)}")
    return fittest_chromosomes, fittest_makespan


def is_new_population_better_than_previous(
    fittest_chromosomes: list[Chromosome], previous_population_makespan: int = None
) -> bool:
    # if this is the first population
    this_population_makespan = fittest_chromosomes

    should_we_continue = fitness.is_this_population_better_than_previous_one(
        previous_population_makespan, this_population_makespan
    )
    print(f"Should we continue iterating? {should_we_continue}")
    return should_we_continue


def generate_next_population(
    fittest_chromosomes: list[Chromosome], fittest_makespan: list[int], probability: float = 0.4
) -> list[Chromosome]:
    new_generation = next_population.generate_next_population_with_crossover(
        fittest_chromosomes, fittest_makespan
    )
    print("in generation", new_generation[-10, :])
    new_mutated_population = []
    for chromosome in new_generation:
        new_mutated_population.append(
            next_population.swap_mutation_at_probability(chromosome, probability)
        )
    new_chromosomes = fittest_chromosomes.copy()
    new_chromosomes.extend(new_mutated_population)
    print(len(fittest_chromosomes), len(new_mutated_population), len(new_chromosomes))
    return new_chromosomes


def genetic_algorithm(
    instance: Instance, max_limit_time_sec: int = 60 * 60
) -> tuple[list[Chromosome], list[int], dict]:
    population = generate_first_population(instance)
    previous_population = None
    is_better_than_previous = True
    start_time = datetime.datetime.now()
    iteration_time = 0
    probability = 0.5
    minimum_probability = 0.05
    decrease_rate = 0.01
    iteration = 0

    while is_better_than_previous and (iteration_time < max_limit_time_sec):
        feasible_population = keep_feasible_chromosomes(instance, population)
        replicated_population = add_replication_of_remaining_working_spaces(
            instance, feasible_population
        )
        times_of_populations = add_times_and_find_makespan(instance, replicated_population)
        fittest_population, fittest_makespan = keep_fittest_chromosomes(
            replicated_population, times_of_populations
        )
        is_better_than_previous = is_new_population_better_than_previous(
            fittest_population, previous_population
        )
        if is_better_than_previous:
            population = generate_next_population(fittest_population, fittest_makespan, probability)
            print(f"Size new population: {len(population)}")
            print(f"Preview it: {population[:10]}")
            print(f"Preview it last elements: {population[-10:]}")
        end_time = datetime.datetime.now()
        iteration_time = (end_time - start_time).total_seconds()
        probability = max(probability - iteration * decrease_rate, minimum_probability)
        iteration += 1
    return fittest_population, fittest_makespan, times_of_populations
