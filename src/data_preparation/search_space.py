import numpy as np
import pandas as pd
from src.data_connectors.read_input_files import Instance


def find_tasks_without_predecessor(
    df_predecessor_sucessor: pd.DataFrame,
) -> list[int]:
    # Returns the tasks without processors
    successors = df_predecessor_sucessor.Sucessor.unique()
    first_tasks = (
        df_predecessor_sucessor[
            ~df_predecessor_sucessor.Predecessor.isin(successors)
        ]
        .Predecessor.unique()
        .tolist()
    )
    return first_tasks


def find_main_jobs(
    df_predecessor_sucessor: pd.DataFrame, df_workingspace_id: pd.DataFrame
) -> pd.DataFrame:
    # A main job is composed by several jobs (or tasks)
    first_task_ids = find_tasks_without_predecessor(df_predecessor_sucessor)
    df_map = df_workingspace_id.copy(deep=True)

    df_map["MainJob"] = 0

    for i in range(len(first_task_ids)):
        if i < len(first_task_ids) - 1:
            df_map["MainJob"] = np.where(
                (
                    (df_workingspace_id.Id >= first_task_ids[i])
                    & (df_workingspace_id.Id < first_task_ids[i + 1])
                ),
                i,
                df_map["MainJob"],
            )
        else:
            df_map["MainJob"] = np.where(
                (df_workingspace_id.Id >= first_task_ids[i]),
                i,
                df_map["MainJob"],
            )

    return df_map


def add_main_job_id(
    df_resource_job_time: pd.DataFrame,
    df_map_jobs: pd.DataFrame,
) -> pd.DataFrame:
    df = df_resource_job_time.merge(
        df_map_jobs[["Id", "MainJob"]], how="left", left_on="Job", right_on="Id"
    )
    df.drop(["Id"], axis=1, inplace=True)
    return df


def pivot_data_to_have_one_row_per_task_and_times_of_each_resources_in_same_line(
    df_w_job: pd.DataFrame,
) -> pd.DataFrame:
    df_times_per_resource = pd.pivot_table(
        df_w_job, values="Time", columns=["Resource"], index=["MainJob", "Job"]
    )
    return df_times_per_resource


def pivot_cooperative_times(
    df_resource_resource_job_time: pd.DataFrame,
) -> pd.DataFrame:
    df_coope = df_resource_resource_job_time.copy(deep=True)
    df_coope["RR"] = (
        "T:"
        + df_coope["ResourceA"].astype(str)
        + "-"
        + df_coope["ResourceB"].astype(str)
    )
    df_times_per_resource = pd.pivot_table(
        df_coope, values="Time", columns=["RR"], index=["Job"]
    )
    return df_times_per_resource


def prepare_predecessor_as_list_per_sucessor(
    df_predecessor_sucessor: pd.DataFrame,
) -> pd.DataFrame:
    return (
        df_predecessor_sucessor.groupby("Sucessor")["Predecessor"]
        .apply(list)
        .reset_index(name="Predecessors")
    )


def merge_times_with_list_predecessors(
    df_times: pd.DataFrame, df_predecessors: pd.DataFrame
) -> pd.DataFrame:
    df_times_w_list_predecessors = df_times.merge(
        df_predecessors, how="left", left_on="Job", right_on="Sucessor"
    )
    df_times_w_list_predecessors = df_times_w_list_predecessors.drop(
        "Sucessor", axis=1
    )

    df_times_w_list_predecessors["Predecessors"] = df_times_w_list_predecessors[
        "Predecessors"
    ].apply(lambda x: [] if x is np.NaN else x)
    return df_times_w_list_predecessors


def get_all_times_in_different_columns_per_task(
    ins_x: Instance,
) -> pd.DataFrame:
    # Concatenation of steps
    df_map_jobs = find_main_jobs(
        ins_x.df_predecessor_sucessor, ins_x.df_workingspace_id
    )
    df_w_job = add_main_job_id(ins_x.df_resource_job_time, df_map_jobs)
    df_times_per_resource_individual = pivot_data_to_have_one_row_per_task_and_times_of_each_resources_in_same_line(
        df_w_job
    )
    df_times_per_resource_cooperation = pivot_cooperative_times(
        ins_x.df_resource_resource_job_time
    )

    df_times = df_times_per_resource_individual.reset_index().merge(
        df_times_per_resource_cooperation.reset_index(), how="left", on="Job"
    )
    df_predecessors = prepare_predecessor_as_list_per_sucessor(
        ins_x.df_predecessor_sucessor
    )

    df_times_w_list_predecessors = merge_times_with_list_predecessors(
        df_times, df_predecessors
    )

    return df_times_w_list_predecessors
