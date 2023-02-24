import logging
import os
import pickle

import numpy as np
from tqdm import tqdm

from src.data_connectors import read_input_files, write_solution_files
from src.genetic_algorithm import constants, genetic_algorithm

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f"{os.getcwd()}")
    instances_list = constants.INSTANCES_LIST
    instances_path = constants.INSTANCES_PATH
    max_limit_time_sec = constants.MAX_TIME_LIMIT_SEC
    logging.info(f"Running for: {len(instances_list)} instances")
    ga_results = []

    for instance_number in tqdm(instances_list):
        ins_x = read_input_files.read_file(
            os.path.join(instances_path, f"Instance_{instance_number}.txt")
        )
        logging.info(f"Running GA for instance {instance_number}...")
        if constants.MMTSP_WITH_SAC:
            result = genetic_algorithm.genetic_algorithm_mmtsp_sac(ins_x, max_limit_time_sec)
        else:
            result = genetic_algorithm.genetic_algorithm_mmtsp(ins_x, max_limit_time_sec)

        ga_results.append(result + (instance_number,))
        write_solution_files.write_solution_to_file(ins_x, instance_number, result)
        logging.info(f"GA for instance {instance_number} has finished!")

    if constants.MMTSP_WITH_SAC:
        with open("data/solutions/all_ga_MMTSP_SAC.pkl", "wb") as f:
            pickle.dump(ga_results, f)
    else:
        with open("data/solutions/all_ga_MMTSP.pkl", "wb") as f:
            pickle.dump(ga_results, f)
