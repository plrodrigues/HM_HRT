from dataclasses import dataclass
from enum import Enum

import pandas as pd


class LineInfo(Enum):
    START = -1
    READ_TYPE_ID = 1
    READ_WORKINGSPACE_RESOURCE = 2
    READ_WORKINGSPACE_ID = 3
    READ_PROCESSOR_SUCESSOR = 4
    READ_RESOURCE_JOB_TIME = 5
    READ_RESOURCE_RESOURCE_JOB_TIME = 6


@dataclass(slots=True)
class Instance:
    df_setup: pd.DataFrame
    df_resources: pd.DataFrame
    df_workingspace_resources: pd.DataFrame
    df_workingspace_id: pd.DataFrame
    df_predecessor_sucessor: pd.DataFrame
    df_resource_job_time: pd.DataFrame
    df_resource_resource_job_time: pd.DataFrame = pd.DataFrame()

    def df_resource_resource_collaboration(self) -> pd.DataFrame:
        self.df_resource_resource_job_time["Resources"] = (
            self.df_resource_resource_job_time["ResourceA"].astype(str)
            + "-"
            + self.df_resource_resource_job_time["ResourceB"].astype(str)
        )
        return self.df_resource_resource_job_time


def populate_df_with_str_int(df: pd.DataFrame, space_separated_values: str):
    new_row = space_separated_values.split(" ")
    df.loc[len(df)] = [new_row[0], int(new_row[1])]


def populate_df_with_ints(df: pd.DataFrame, space_separated_values: str):
    new_row = [int(i) for i in space_separated_values.split(" ")]
    df.loc[len(df)] = new_row


def read_file(filename: str) -> Instance:
    with open(filename) as f:
        lines = f.readlines()

    n_humans = lines[0].strip().split(" ")[1]
    n_robots = lines[1].strip().split(" ")[1]
    n_workingspaces = lines[2].strip().split(" ")[1]
    df_setup = pd.DataFrame(
        {
            "Humans": n_humans,
            "Robots": n_robots,
            "WorkingSpaces": n_workingspaces,
        },
        index=[0],
    )

    df_resources = pd.DataFrame(columns=["Type", "Id"])
    df_workingspace_resources = pd.DataFrame(
        columns=["WorkingSpace", "Resource"]
    )
    df_workingspace_id = pd.DataFrame(columns=["WorkingSpace", "Id"])

    df_predecessor_sucessor = pd.DataFrame(columns=["Predecessor", "Sucessor"])

    df_resource_job_time = pd.DataFrame(columns=["Resource", "Job", "Time"])

    df_resource_resource_job_time = pd.DataFrame(
        columns=["ResourceA", "ResourceB", "Job", "Time"]
    )

    line_info = LineInfo.START
    for line in lines[3:]:
        stripped_line = line.strip()
        if stripped_line in [
            "",
            "Resources",
            "Jobs",
            "Precedence Constraints",
            "OperationTimes",
            "Collaborative Operation Times",
            "End",
        ]:
            continue

        if stripped_line == "Type Id":
            line_info = line_info.READ_TYPE_ID
            continue

        if stripped_line == "WorkingSpace Resource":
            line_info = line_info.READ_WORKINGSPACE_RESOURCE
            continue

        if stripped_line == "WorkingSpace Id":
            line_info = line_info.READ_WORKINGSPACE_ID
            continue

        if stripped_line == "Predecessor Sucessor":
            line_info = line_info.READ_PROCESSOR_SUCESSOR
            continue

        if stripped_line == "Resource Job Time":
            line_info = line_info.READ_RESOURCE_JOB_TIME
            continue

        if stripped_line == "Resource Resource Job Time":
            line_info = line_info.READ_RESOURCE_RESOURCE_JOB_TIME
            continue

        if line_info == line_info.READ_TYPE_ID:
            populate_df_with_str_int(df_resources, stripped_line)

        if line_info == line_info.READ_WORKINGSPACE_RESOURCE:
            populate_df_with_ints(df_workingspace_resources, stripped_line)

        if line_info == line_info.READ_WORKINGSPACE_ID:
            populate_df_with_ints(df_workingspace_id, stripped_line)

        if line_info == line_info.READ_PROCESSOR_SUCESSOR:
            populate_df_with_ints(df_predecessor_sucessor, stripped_line)

        if line_info == line_info.READ_RESOURCE_JOB_TIME:
            populate_df_with_ints(df_resource_job_time, stripped_line)

        if line_info == line_info.READ_RESOURCE_RESOURCE_JOB_TIME:
            populate_df_with_ints(df_resource_resource_job_time, stripped_line)

    instance = Instance(
        df_setup=df_setup,
        df_resources=df_resources,
        df_workingspace_resources=df_workingspace_resources,
        df_workingspace_id=df_workingspace_id,
        df_predecessor_sucessor=df_predecessor_sucessor,
        df_resource_job_time=df_resource_job_time,
        df_resource_resource_job_time=df_resource_resource_job_time,
    )

    return instance
