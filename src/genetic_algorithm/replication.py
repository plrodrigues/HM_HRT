import itertools
import logging

from src.data_connectors.read_input_files import Instance
from src.genetic_algorithm.chromosome import Chromosome


def flatten(lst: list) -> list:
    return list(itertools.chain(*lst))


def is_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


def split_collaboration_into_ints(collab_str: str) -> tuple[int, int]:
    val_1, val_2 = collab_str.split("-")
    return int(val_1), int(val_2)


def generate_modes_of_working_space(
    instance: Instance,
    initial_working_space: int,
    working_space: int,
    modes: list[str],
) -> list[str]:
    initial_ws_resources = instance.df_workingspace_resources[
        instance.df_workingspace_resources.WorkingSpace == initial_working_space
    ].Resource.unique()
    ws_resources = instance.df_workingspace_resources[
        instance.df_workingspace_resources.WorkingSpace == working_space
    ].Resource.unique()
    resources_exclusively_in_new_ws = [m for m in ws_resources if m not in initial_ws_resources]

    new_ws_mode = []
    for m in modes:
        if is_int(m):
            if int(m) in ws_resources:
                new_ws_mode.append(m)
            elif len(resources_exclusively_in_new_ws) == 1:
                new_ws_mode.append(str(resources_exclusively_in_new_ws[0]))
            elif len(resources_exclusively_in_new_ws) > 1:
                logging.warning("WHAT TO DO?")
        else:
            m1, m2 = split_collaboration_into_ints(m)
            if (m1 in ws_resources) and (m2 in ws_resources):
                new_ws_mode.append(m)
            elif (m1 in ws_resources) and (m2 not in ws_resources):
                if len(resources_exclusively_in_new_ws) == 1:
                    updated_m = str(m1) + "-" + str(resources_exclusively_in_new_ws[0])
                    new_ws_mode.append(updated_m)
            elif (m2 in ws_resources) and (m1 not in ws_resources):
                if len(resources_exclusively_in_new_ws) == 1:
                    updated_m = str(resources_exclusively_in_new_ws[0]) + "-" + str(m2)
                    new_ws_mode.append(updated_m)
    return new_ws_mode


def generate_new_mode_with_replication(instance: Instance, chromosome: Chromosome) -> list[str]:
    # Generate modes for remaining working spaces
    all_new_modes = []
    logging.debug(
        f"generate_new_mode_with_replication(): Non replicated chromosome: {len(chromosome.mode)}"
    )
    for ws in instance.df_workingspace_resources.WorkingSpace.unique():
        if ws == 1:
            all_new_modes.append(chromosome.mode)
        else:
            mode_for_ws = generate_modes_of_working_space(instance, 1, ws, chromosome.mode)
            all_new_modes.append(mode_for_ws)
    logging.debug(
        f"generate_new_mode_with_replication(): Replicated crhomosome: {len(flatten(all_new_modes))}"
    )
    return flatten(all_new_modes)


def generate_new_orders_with_replication(instance: Instance, chromosome: Chromosome) -> list[int]:
    # Generate orders for remaining working spaces, knowing that they have
    # to follow a replication SAC method
    new_orders = []
    working_spaces = instance.df_workingspace_resources.WorkingSpace.unique()
    for i in range(len(working_spaces)):
        ws_order = [(x * 3) + i for x in chromosome.order]
        new_orders.append(ws_order)
    return flatten(new_orders)


def update_chromosome_with_replication(instance: Instance, chromosome: Chromosome) -> Chromosome:
    return Chromosome(
        mode=generate_new_mode_with_replication(instance, chromosome),
        order=generate_new_orders_with_replication(instance, chromosome),
    )
