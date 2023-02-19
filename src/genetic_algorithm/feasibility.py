import pandas as pd

from src.data_connectors.read_input_files import Instance
from src.genetic_algorithm.chromosome import Chromosome


def is_chromosome_precedence_feasible(
    instance: Instance, chromosome: Chromosome
) -> bool:
    # Verify that the precedence of tasks is valid with precedence given

    tasks = [x for x in range(1, len(chromosome.order) + 1)]

    allocated_prior_tasks = []

    for n in range(len(chromosome.order)):
        sucessor = tasks[chromosome.order.index(n)]
        predecessors = instance.df_predecessor_sucessor[
            instance.df_predecessor_sucessor["Sucessor"] == sucessor
        ].Predecessor.unique()

        if len([x for x in predecessors if x not in allocated_prior_tasks]) > 0:
            return False
        allocated_prior_tasks.append(sucessor)

    return True


def is_one_resource_in_mode(mode: str) -> bool:
    if len(mode) == 1:
        return True
    else:
        return False


def is_one_resource_task_possible(
    df_resource_job_time: pd.DataFrame, mode: int, task: int
) -> bool:
    if (
        len(
            df_resource_job_time[
                (df_resource_job_time.Resource == mode)
                & (df_resource_job_time.Job == task)
            ]
        )
        >= 1
    ):
        return True
    else:
        return False


def is_collaborative_resource_task_possible(
    df_resource_resource_job_time: pd.DataFrame, mode: str, task: int
) -> bool:
    if (
        len(
            df_resource_resource_job_time[
                (df_resource_resource_job_time.Resources == mode)
                & (df_resource_resource_job_time.Job == task)
            ]
        )
        >= 1
    ):
        return True
    else:
        return False


def is_chromosome_task_mode_feasible(
    instance: Instance, chromosome: Chromosome
) -> bool:
    # Verify that the mode assigned can perform the task allocated
    are_genes_possible = []
    for n in range(len(chromosome.order)):
        task_id = n + 1
        pair_mode_task = (chromosome.mode[n], task_id)

        mode_condition = is_one_resource_in_mode(pair_mode_task[0])
        is_feasible_one = False
        is_feasible_collab = False

        if mode_condition:
            if is_one_resource_task_possible(
                instance.df_resource_job_time,
                int(pair_mode_task[0]),
                pair_mode_task[1],
            ):
                is_feasible_one = True
            else:
                print("1 resource not possible")
                is_feasible_one = False
        else:
            if is_collaborative_resource_task_possible(
                instance.df_resource_resource_collaboration(),
                pair_mode_task[0],
                pair_mode_task[1],
            ):
                is_feasible_collab = True
            else:
                print("more resources not possible")
                is_feasible_collab = False
        are_genes_possible.append(is_feasible_one or is_feasible_collab)

    return all(are_genes_possible)
