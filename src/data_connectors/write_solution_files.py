import numpy as np

from src.data_connectors.read_input_files import Instance
from src.genetic_algorithm import time_allocation


def write_to_txt_file(text_to_write: list[str], intance_number: int = None, filename: str = None) -> None:
    if not filename:
        filename = f"data/solutions/solution_{intance_number}.txt"
    with open(filename, "w") as f:
        for line in text_to_write:
            f.write(line)
            f.write("\n")


def generate_text_to_write(
    intance_number: int, result: tuple, times_of_populations: dict
) -> list[str]:
    instance_solution_text = [
        f"Optimal Solution - Instance {intance_number} - Makespan {result[2]} - Total search duration (seconds) {result[3]:.2f}",
        " ",
    ]
    for resource in times_of_populations.keys():
        instance_solution_text.append(f"Resource {resource}")
        for job in times_of_populations[resource].keys():
            instance_solution_text.append(
                f"Job {job} [{times_of_populations[resource][job][0]} - {times_of_populations[resource][job][1]}]"
            )
    return instance_solution_text


def find_times_of_best_solution(instance: Instance, result: tuple) -> dict:
    better_solution = result[0][result[1].index(result[2])]
    return time_allocation.get_all_time_allocations(instance, better_solution)


def write_solution_to_file(instance: Instance, intance_number: int, result: tuple) -> None:
    times_of_better_solution = find_times_of_best_solution(instance, result)
    text_to_write = generate_text_to_write(intance_number, result, times_of_better_solution)
    write_to_txt_file(text_to_write, intance_number)
