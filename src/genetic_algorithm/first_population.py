import itertools
import random

random.seed(123)
import numpy as np

from src.data_connectors.read_input_files import Instance
from src.genetic_algorithm.chromosome import Chromosome


def get_possible_single_modes(instance: Instance, working_space: int = None) -> list[str]:
    # Get possible modes for given working space
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()

    singular_modes = (
        instance.df_resource_job_time[
            instance.df_resource_job_time.Job.isin(
                instance.df_workingspace_id[instance.df_workingspace_id.WorkingSpace == working_space].Id.unique()
            )
        ]
        .Resource.unique()
        .astype(str)
    )
    return singular_modes


def get_possible_collaborative_modes(instance: Instance, working_space: int = None) -> list[str]:
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()

    df_collaborations = instance.df_resource_resource_collaboration()
    collaborative_modes = df_collaborations[
        df_collaborations.Job.isin(
            instance.df_workingspace_id[instance.df_workingspace_id.WorkingSpace == working_space].Id.unique()
        )
    ]["Resources"].unique()
    return collaborative_modes


def get_possible_modes(instance: Instance, working_space: int = None) -> list[str]:
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()

    singular_modes = get_possible_single_modes(instance, working_space)
    collaborative_modes = get_possible_collaborative_modes(instance, working_space)

    possible_modes = np.append(singular_modes, collaborative_modes)
    print(f"Possible modes: {possible_modes}")
    return possible_modes


def get_total_number_of_tasks_per_working_space(instance: Instance, working_space: int = None) -> int:
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()

    number_of_tasks = len(instance.df_workingspace_id[instance.df_workingspace_id.WorkingSpace == working_space])
    print(f"Number of tasks: {number_of_tasks}")
    return number_of_tasks


def regroup_permutations(
    permutations_of_oders: list[list[tuple[int]]],
) -> list[list[int]]:
    result = []
    for i in range(len(permutations_of_oders[0])):
        temp = []
        for j in range(len(permutations_of_oders)):
            temp.extend(list(permutations_of_oders[j][i]))
        result.append(temp)
    return result


def get_permutations_for_order_of_tasks(
    number_of_tasks: int,
) -> list[list[int]]:
    base_order = [x for x in range(number_of_tasks)]
    n_elements_to_permute = 5
    orders_sections = [
        base_order[i : i + n_elements_to_permute] for i in range(0, len(base_order), n_elements_to_permute)
    ]

    permutations_of_oders = [list(itertools.permutations(order_section)) for order_section in orders_sections]
    order_permutations = regroup_permutations(permutations_of_oders)
    return order_permutations


def get_first_population(possible_modes: list[str], number_tasks: int) -> list[Chromosome]:
    # Chromosomes
    chromosomes = []
    # Order of tasks
    order_permutations = get_permutations_for_order_of_tasks(number_tasks)

    # First selection of chromosomes: constant modes and permutation of order of tasks
    for n_order in order_permutations:
        for m_mode in possible_modes:
            chromosome_x = Chromosome(mode=[m_mode for _ in range(number_tasks)], order=n_order)
            chromosomes.append(chromosome_x)

    # Second selection of chromosomes: generate permutations of modes and perform permutations on the order of tasks
    n_second_chromosomes = 50
    for _ in range(n_second_chromosomes):
        for n_order in order_permutations:
            chromosome_x = Chromosome(
                mode=random.choices(possible_modes, k=number_tasks),
                order=n_order,
            )
            chromosomes.append(chromosome_x)

    print(f"Total size of first population: {len(chromosomes)}")
    return chromosomes
