import logging
import os
from enum import Enum

import pandas as pd
from pandas.tseries.offsets import DateOffset

from src.data_connectors import read_input_files
from src.data_connectors.read_input_files import Instance


class LineInfoOfSolutions(Enum):
    START = -1
    READ_RESOURCE = 1
    READ_JOB_AND_TIMES = 2


def read_solutions_file(filename: str) -> pd.DataFrame:
    with open(filename) as f:
        lines = f.readlines()

    header = lines[0]
    _ = lines[1]

    df = pd.DataFrame(columns=["Resource", "Task", "Start", "Finish"])
    current_resource = None
    for line in lines[2:]:
        stripped_line = line.strip()
        array_line = stripped_line.split(" ")

        if "Resource" in stripped_line:
            current_resource = array_line[-1]

        if "Job" in stripped_line:
            task = array_line[1]
            start = array_line[2].replace("[", "")
            finish = array_line[4].replace("]", "")

            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        {
                            "Resource": [current_resource],
                            "Task": [task],
                            "Start": [start],
                            "Finish": [finish],
                        },
                    ),
                ],
                axis=0,
            )
    return df.reset_index(drop=True)


def add_job_id(df_solution: pd.DataFrame, instance: Instance) -> pd.DataFrame:
    df_ws = instance.df_workingspace_id.copy(deep=True)
    df_ws["Job"] = df_ws["WorkingSpace"]
    df_ws["Task"] = df_ws["Id"].astype(int)
    df_solution["Task"] = df_solution["Task"].astype(int)
    df_with_job = df_solution.merge(df_ws[["Job", "Task"]], how="inner", on="Task")
    return df_with_job


def convert_times_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    df["Start"] = pd.to_datetime(df["Start"], unit="h")
    df["Finish"] = pd.to_datetime(df["Finish"], unit="h")
    df["Start"] = df["Start"] + DateOffset(years=2023 - 1970)
    df["Finish"] = df["Finish"] + DateOffset(years=2023 - 1970)
    return df


def get_solution_from_instance(
    solutions_path: str, instances_path: str, instance_number: int
) -> pd.DataFrame:
    try:
        df = read_solutions_file(os.path.join(solutions_path, f"solution_{instance_number}.txt"))
    except FileNotFoundError:
        df = read_solutions_file(os.path.join(solutions_path, f"Solution_{instance_number}.txt"))
    except Exception as e:
        logging.error(f"Exception on reading solutions file: {e}")
    instance = read_input_files.read_file(
        os.path.join(instances_path, f"Instance_{instance_number}.txt")
    )

    df = add_job_id(df, instance)
    df = convert_times_to_datetime(df)
    return df
