import logging
import os
import pickle

import numpy as np
from tqdm import tqdm

from src.data_connectors import read_input_files, write_solution_files
from src.genetic_algorithm import genetic_algorithm

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f"{os.getcwd()}")

    instances_path = "data/input/HRTInstances/"
    instances_list = [x for x in range(217, 219)] #337)]
    logging.info(f"Running for: {len(instances_list)} instances")
    max_limit_time_sec = 10 #240
    ga_results = []

    for instance_number in tqdm(instances_list):
        ins_x = read_input_files.read_file(
            os.path.join(instances_path, f"Instance_{instance_number}.txt")
        )
        result = genetic_algorithm.genetic_algorithm(ins_x, max_limit_time_sec=30)
        ga_results.append(result)
        write_solution_files.write_solution_to_file(ins_x, instance_number, result)

    with open("data/solutions/all_ga.pkl", "wb") as f:
        pickle.dump(ga_results, f)
