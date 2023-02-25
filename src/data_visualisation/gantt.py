import pandas as pd
import plotly.express as px


def plot_gantt_chart(df: pd.DataFrame, instance_number: int) -> None:
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Resource",
        color="Job",
        hover_data=["Task"],
        text="Task",
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
        pattern_shape="has_successors",
        title=f"Gantt Schedule for Instance {instance_number} - with predecessor tasks identifyed as different color texture",
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))

    fig.show()
