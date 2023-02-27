import itertools
from dataclasses import dataclass

from src.data_connectors.read_input_files import Instance
from src.genetic_algorithm import feasibility, first_population, replication
from src.genetic_algorithm.chromosome import Chromosome


def get_possible_modes(instance: Instance) -> list[str]:
    all_modes = []
    for ws in instance.df_workingspace_id.WorkingSpace.unique():
        single_modes = first_population.get_possible_single_modes(instance, ws)
        collab_modes = first_population.get_possible_collaborative_modes(instance, ws)
        all_modes.extend(single_modes)
        all_modes.extend(collab_modes)

    return list(set(all_modes))


def get_time_from_single_resource(instance: Instance, mode: str, task: int) -> int:
    return instance.df_resource_job_time[
        (instance.df_resource_job_time.Resource == int(mode))
        & (instance.df_resource_job_time.Job == task)
    ].Time.item()


def get_time_from_collaboratory_resources(
    instance: Instance, mode1: int, mode2: int, task: int
) -> int | None:
    time_of_task_in_mode = instance.df_resource_resource_job_time[
        (instance.df_resource_resource_job_time.ResourceA == mode1)
        & (instance.df_resource_resource_job_time.ResourceB == mode2)
        & (instance.df_resource_resource_job_time.Job == task)
    ].Time
    if len(time_of_task_in_mode) > 0:
        return time_of_task_in_mode.item()
    else:
        return None


def find_end_time_of_task_in_allocated_modes(allocated_modes: dict, task: int) -> int:
    for k in allocated_modes.keys():
        if task in allocated_modes[k]:
            return allocated_modes[k][task][1]


def find_the_next_time_slot_of_mode(allocated_modes: dict, mode: str) -> int:
    latest_mode = -1
    # find all resources
    resources = []
    if feasibility.is_one_resource_in_mode(mode):
        resources.append(int(mode))
    else:
        val_1, val_2 = mode.split("-")
        resources.append(int(val_1))
        resources.append(int(val_2))

    possible_modes = [
        mode
        for mode in allocated_modes.keys()
        if any(str(resource) in mode for resource in resources)
    ]

    for mode in possible_modes:
        for k in allocated_modes[mode].keys():
            if allocated_modes[mode][k][1] > latest_mode:
                latest_mode = allocated_modes[mode][k][1]

    return latest_mode


def convert_order_of_tasks_to_tasks_ordered(order_of_tasks: list[int]) -> list[int]:
    tasks_ordered = [1] * len(order_of_tasks)
    for i, task_id in enumerate(order_of_tasks):
        tasks_ordered[task_id] = i + 1
    return tasks_ordered


def get_all_time_allocations(instance: Instance, chromosome: Chromosome) -> dict:

    all_modes = get_possible_modes(instance)

    times_allocated = {k: {} for k in all_modes}

    tasks = convert_order_of_tasks_to_tasks_ordered(chromosome.order)

    for task in tasks:
        mode_of_class = chromosome.mode[task - 1]
        if replication.is_int(mode_of_class):
            time_of_task_in_mode = get_time_from_single_resource(instance, mode_of_class, task)
        else:
            resource_1, resource_2 = replication.split_collaboration_into_ints(mode_of_class)
            time_of_task_in_mode = get_time_from_collaboratory_resources(
                instance, int(resource_1), int(resource_2), task
            )
            if not time_of_task_in_mode:
                time_of_task_in_mode = get_time_from_collaboratory_resources(
                    instance, int(resource_2), int(resource_1), task
                )

        if task not in times_allocated[mode_of_class]:
            # Check predecessors # OPTIMISE with single dictionary
            predecessors = instance.df_predecessor_sucessor[
                instance.df_predecessor_sucessor.Sucessor == task
            ].Predecessor.unique()
            # Pick end time of predecessors
            predecessors_allocated_at = -1
            if len(predecessors) > 0:
                for pred in predecessors:
                    previous_predecessor_end_time = find_end_time_of_task_in_allocated_modes(
                        times_allocated, pred
                    )
                    if previous_predecessor_end_time:
                        if previous_predecessor_end_time > predecessors_allocated_at:
                            predecessors_allocated_at = previous_predecessor_end_time

            # Verify if mode is allocated alone or in team already
            mode_available_time = find_the_next_time_slot_of_mode(times_allocated, mode_of_class)
            this_start_time = max(mode_available_time, predecessors_allocated_at) + 1
            this_end_time = this_start_time + time_of_task_in_mode
            times_allocated[mode_of_class][task] = (
                this_start_time,
                this_end_time,
            )
    return times_allocated


def find_makespan(chromosome_time_allocation: dict) -> int:
    makespan = 0
    for k in chromosome_time_allocation.keys():
        for t in chromosome_time_allocation[k].keys():
            end_time = chromosome_time_allocation[k][t][1]
            if end_time > makespan:
                makespan = end_time
    return makespan
