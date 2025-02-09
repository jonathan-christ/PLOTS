import pandas as pd
import plotly.express as px

DATA_SRC = "data/bar_assignment.csv"

"""
    Create a horizontal stacked bar chart
    Transform 1 into “Yes” and 0 into “No”
    Follow the plot specification for bar plot
"""


def format_data(data: pd.Series) -> pd.Series:
    """
    This function takes a pandas Series as an argument and returns a new pandas Series.

    It takes a pandas Series that contains the data for the bar plot, and transforms it into the
    required format for the bar plot. This includes transforming the 1s and 0s into "Yes" and "No",
    grouping the data by label and count, and renaming the columns to "OPTION" and "COUNT".

    Parameters
    ----------
    data : pd.Series
        The pandas Series containing the data for the bar plot.

    Returns
    -------
    pd.Series
        The transformed pandas Series in the required format for the bar plot.
    """

    # idea is,
    #   1 = yes, 0 = no => convert => make as column because its an attribute, solution = group by count
    #   needs total option / vote count per label, solution = group by label
    formatted_data = (
        data.replace({1: "Yes", 0: "No"})
        .groupby(
            ["LABEL", "COUNT"]
        )  # groups by label, with respective Yes and No options
        .size()  # adds another column that determines the count per option
        .reset_index()  # normalizes/formats the data to be readable by graph function
        .rename(columns={0: "COUNT", "COUNT": "OPTION"})  # rename columns accordingly
    )

    return formatted_data


def plot(data: pd.Series) -> None:
    """
    Creates a horizontal stacked bar chart from the given DataFrame and displays it.

    Parameters
    ----------
    data : pd.DataFrame
        The DataFrame containing the data to plot.
    """

    fig = px.bar(
        data,
        x="COUNT",
        y="LABEL",
        color="OPTION",
        barmode="stack",
        orientation="h",
        color_discrete_map={"Yes": "blue", "No": "red"},
        category_orders={"LABEL": data["LABEL"].unique()[::-1]},  # based on format
        title="Labels and Corresponding Yes or No Vote Counts",
        text=data["COUNT"],
    )

    fig.update_layout(
        font_size=20,
        font_weight="bold",
        font_color="black",
        title_y=0.975,
        legend=dict(orientation="h", yanchor="bottom", xanchor="left", y=1, x=0),
    )
    fig.show()

    return fig


def execute() -> None:
    """
    This function reads the data from the csv file located at DATA_SRC,
    formats the data for the bar plot using the format_data function, and
    then plots the bar chart using the plot function.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    data = pd.read_csv(DATA_SRC)
    formatted_data = format_data(data)

    print(formatted_data)
    return plot(formatted_data)
