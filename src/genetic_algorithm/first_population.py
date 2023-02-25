import itertools

import logging
import random

random.seed(123)
import numpy as np
import pandas as pd

from src.data_connectors.read_input_files import Instance
from src.genetic_algorithm.chromosome import Chromosome


def get_possible_single_modes(instance: Instance, working_space: int = None) -> list[str]:
    # Get possible modes for given working space
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()

    singular_modes = (
        instance.df_resource_job_time[
            instance.df_resource_job_time.Job.isin(
                instance.df_workingspace_id[
                    instance.df_workingspace_id.WorkingSpace == working_space
                ].Id.unique()
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
            instance.df_workingspace_id[
                instance.df_workingspace_id.WorkingSpace == working_space
            ].Id.unique()
        )
    ]["Resources"].unique()
    return collaborative_modes


def get_possible_modes(instance: Instance, working_space: int = None) -> list[str]:
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()

    singular_modes = get_possible_single_modes(instance, working_space)
    collaborative_modes = get_possible_collaborative_modes(instance, working_space)

    possible_modes = np.append(singular_modes, collaborative_modes)
    logging.debug(f"Possible modes: {possible_modes}")
    return possible_modes


def get_total_number_of_tasks_per_working_space(
    instance: Instance, working_space: int = None
) -> int:
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()

    number_of_tasks = len(
        instance.df_workingspace_id[instance.df_workingspace_id.WorkingSpace == working_space]
    )
    logging.debug(f"Number of tasks: {number_of_tasks}")
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
        base_order[i : i + n_elements_to_permute]
        for i in range(0, len(base_order), n_elements_to_permute)
    ]

    permutations_of_oders = [
        list(itertools.permutations(order_section)) for order_section in orders_sections
    ]
    base_len = len(permutations_of_oders[0])
    normalised_permutations_of_oders = []
    for permut in permutations_of_oders:
        if len(permut) < base_len:
            permut = list(itertools.islice(itertools.cycle(permut), base_len))
        normalised_permutations_of_oders.append(permut)

    order_permutations = regroup_permutations(normalised_permutations_of_oders)
    return order_permutations


def get_min_resorce_id(instance: Instance, working_space: int = None) -> list[str]:
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()
    idx = instance.df_resource_job_time.groupby("Job")["Resource"].idxmin()
    df_resource = instance.df_resource_job_time.loc[idx, ["Job", "Resource", "Time"]]
    resources_list = df_resource[
        df_resource.Job.isin(
            instance.df_workingspace_id[
                instance.df_workingspace_id.WorkingSpace == working_space
            ].Id.unique()
        )
    ].Resource.tolist()
    return [str(m) for m in resources_list]


def get_max_resorce_id(instance: Instance, working_space: int = None) -> list[str]:
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()
    idx = instance.df_resource_job_time.groupby("Job")["Resource"].idxmax()
    df_resource = instance.df_resource_job_time.loc[idx, ["Job", "Resource", "Time"]]
    resources_list = df_resource[
        df_resource.Job.isin(
            instance.df_workingspace_id[
                instance.df_workingspace_id.WorkingSpace == working_space
            ].Id.unique()
        )
    ].Resource.tolist()
    return [str(m) for m in resources_list]


def sample_group(grp):
    return grp.sample(1)


def get_random_resorce_id(instance: Instance, working_space: int = None) -> list[str]:
    if not working_space:
        working_space = instance.df_workingspace_id.WorkingSpace.min()

    df_sampled_rows = instance.df_resource_job_time.groupby("Job").apply(sample_group)
    df_sampled_rows = df_sampled_rows.reset_index(level=1, drop=True)

    resources_list = df_sampled_rows[
        df_sampled_rows.Job.isin(
            instance.df_workingspace_id[
                instance.df_workingspace_id.WorkingSpace == working_space
            ].Id.unique()
        )
    ].Resource.tolist()
    return [str(m) for m in resources_list]


def get_permutations_for_specific_tasks(
    tasks: list[int],
) -> list[list[int]]:
    n_elements_to_permute = 5
    orders_sections = [
        tasks[i : i + n_elements_to_permute] for i in range(0, len(tasks), n_elements_to_permute)
    ]

    permutations_of_oders = [
        list(itertools.permutations(order_section)) for order_section in orders_sections
    ]
    base_len = len(permutations_of_oders[0])
    normalised_permutations_of_oders = []
    for permut in permutations_of_oders:
        if len(permut) < base_len:
            permut = list(itertools.islice(itertools.cycle(permut), base_len))
        normalised_permutations_of_oders.append(permut)

    order_permutations = regroup_permutations(normalised_permutations_of_oders)
    return order_permutations


def get_precedence_aware_order(instance: Instance) -> list[list[str]]:
    first_working_space = instance.df_workingspace_id.WorkingSpace.min()
    list_tasks_ws1 = instance.df_workingspace_id[
        instance.df_workingspace_id.WorkingSpace == first_working_space
    ].Id.unique()
    list_tasks_ws1_with_successors = instance.df_predecessor_sucessor[
        instance.df_predecessor_sucessor.Predecessor.isin(list_tasks_ws1)
    ].Predecessor.unique()
    list_tasks_ws1_without_successors = np.array(
        [task for task in list_tasks_ws1 if task not in list_tasks_ws1_with_successors]
    )
    # adjust the values starting in 0
    list_tasks_ws1_with_successors = [x - 1 for x in list_tasks_ws1_with_successors]
    list_tasks_ws1_without_successors = [x - 1 for x in list_tasks_ws1_without_successors]

    permutations_on_predecessor_tasks = get_permutations_for_specific_tasks(
        list_tasks_ws1_with_successors
    )

    permutations_on_no_predecessor_tasks = get_permutations_for_specific_tasks(
        list_tasks_ws1_without_successors
    )
    overal_permutations = []
    for w_pred in permutations_on_predecessor_tasks:
        for wout_pred in permutations_on_no_predecessor_tasks:
            overal_permutations.append(w_pred + wout_pred)
    return overal_permutations


def convert_tasks_ordered_to_order_of_tasks(tasks_ordered: list[int]) -> list[int]:
    task_order = {task_id: i for i, task_id in enumerate(tasks_ordered)}
    order_of_tasks = [task_order[task_id] for task_id in range(len(tasks_ordered))]
    return order_of_tasks


def get_first_population(
    instance: Instance, possible_modes: list[str], number_tasks: int
) -> list[Chromosome]:
    # Chromosomes
    chromosomes = []
    # Order of tasks
    order_permutations = get_permutations_for_order_of_tasks(number_tasks)
    
    # First selection of chromosomes: with resources available
    # From available resources and times
    base_resources = [
        get_min_resorce_id(instance), # preference to humans
        get_max_resorce_id(instance), # preference to robots
        get_random_resorce_id(instance),
    ]
    for modes in base_resources:
        for n_order in order_permutations:
            chromosome_x = Chromosome(mode=modes, order=n_order)
            chromosomes.append(chromosome_x)

    # Second selection of chromosomes: constant modes and permutation of order of tasks
    for n_order in order_permutations:
        for m_mode in possible_modes:
            chromosome_x = Chromosome(mode=[m_mode for _ in range(number_tasks)], order=n_order)
            chromosomes.append(chromosome_x)

    # Third selection of chromosomes: generate permutations of modes and perform permutations
    # on the order of tasks
    n_second_chromosomes = 20 # 100
    for _ in range(n_second_chromosomes):
        for n_order in order_permutations:
            chromosome_x = Chromosome(
                mode=random.choices(possible_modes, k=number_tasks),
                order=n_order,
            )
            chromosomes.append(chromosome_x)
    
    # Fourth selection of chromosomes: precedence aware and available resources
    overal_permutations_precedence_aware = get_precedence_aware_order(instance)
    for modes in base_resources:
        for n_order in overal_permutations_precedence_aware:
            chromosome_x = Chromosome(mode=modes, order=convert_tasks_ordered_to_order_of_tasks(n_order))
            chromosomes.append(chromosome_x)
    
    # Fifth selection of chromosomes: precedence aware and random resources
    for n_order in overal_permutations_precedence_aware:
        chromosome_x = Chromosome(
            mode=random.choices(possible_modes, k=number_tasks),
            order=convert_tasks_ordered_to_order_of_tasks(n_order),
        )
        chromosomes.append(chromosome_x)

    logging.debug(f"Total size of first population: {len(chromosomes)}")
    return chromosomes
