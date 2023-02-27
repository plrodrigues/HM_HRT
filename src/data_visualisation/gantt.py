import pandas as pd
import plotly.express as px

from src.genetic_algorithm import constants


def plot_gantt_chart(df: pd.DataFrame, instance_number: int) -> None:
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Resource",
        color="Job",
        hover_data=["Task"],
        text="Task",
        color_continuous_scale=constants.GANTT_COLORMAP,
        title=f"Gantt Schedule for Instance {instance_number}",
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))

    fig.show()


def plot_gantt_chart_with_teams(df: pd.DataFrame, instance_number: int) -> None:
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Resource",
        color="Job",
        hover_data=["Task"],
        text="Task",
        pattern_shape="is_team",
        color_continuous_scale=constants.GANTT_COLORMAP,
        title=f"Gantt Schedule for Instance {instance_number} - with team work identifyed as different color texture",
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))

    fig.show()


def plot_gantt_chart_with_predecessor_flag(df: pd.DataFrame, instance_number: int) -> None:
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Resource",
        color="Job",
        hover_data=["Task"],
        text="Task",
        category_orders={"has_successors": [1, 0]},
        pattern_shape="has_successors",
        color_continuous_scale=constants.GANTT_COLORMAP,
        title=f"Gantt Schedule for Instance {instance_number} - with not predecessor tasks identifyed as different color texture",
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))

    fig.show()
