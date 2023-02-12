import numpy as np
import pandas as pd


def find_tasks_without_predecessor(
    df_predecessor_sucessor: pd.DataFrame,
) -> list[int]:
    # Returns the tasks without processors 
    successors = df_predecessor_sucessor.Sucessor.unique()
    first_tasks = df_predecessor_sucessor[
        ~df_predecessor_sucessor.Predecessor.isin(successors)
    ].Predecessor.unique().tolist()
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