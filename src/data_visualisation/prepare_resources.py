import numpy as np
import pandas as pd

from src.data_connectors.read_input_files import Instance


def expand_the_resources(df: pd.DataFrame) -> pd.DataFrame:
    df_individuals = df[~df.Resource.str.contains("-")]
    df_individuals["is_team"] = 0

    df_teams = df[df.Resource.str.contains("-")]

    df_teams_1 = df_teams.copy(deep=True)
    df_teams_1["Resource"] = df_teams_1["Resource"].astype(str).str[0]
    df_teams_1["is_team"] = 1

    df_teams_2 = df_teams.copy(deep=True)
    df_teams_2["Resource"] = df_teams_2["Resource"].astype(str).str[-1]
    df_teams_2["is_team"] = 1

    df = pd.concat([df_individuals, df_teams_1, df_teams_2], axis=0)

    return df


def add_resource_type(df: pd.DataFrame, instance: Instance) -> pd.DataFrame:
    df_map_resource_ids = instance.df_resources
    df_map_resource_ids = df_map_resource_ids.rename(columns={"Id": "Resource"})
    df_map_resource_ids["Resource_Category"] = (
        df_map_resource_ids["Type"].astype(str) + "-" + df_map_resource_ids["Resource"].astype(str)
    )
    df["Resource"] = df["Resource"].astype(str)
    df_map_resource_ids["Resource"] = df_map_resource_ids["Resource"].astype(str)
    df = df.merge(
        df_map_resource_ids[["Resource", "Resource_Category"]], how="inner", on="Resource"
    )
    df["Resource"] = df["Resource_Category"]
    df.drop(["Resource_Category"], axis=1, inplace=True)
    df = df.sort_values("Resource")
    return df


def add_predecessor_flag(df: pd.DataFrame, instance: Instance) -> pd.DataFrame:
    df["has_successors"] = np.where(
        df.Task.isin(instance.df_predecessor_sucessor.Predecessor.unique()), 1, 0
    )
    return df
