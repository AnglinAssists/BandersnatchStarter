from altair import Chart, Tooltip, Title
from pandas import DataFrame


def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    """
    This function creates and returns a scatter plot with circular marks. The x and
    y-axis are determined by the provided column names from the dataframe, while the
    color encoding and tooltip features are determined by the target column and other
    columns from the dataframe, respectively.

    :arg:
         df (pandas.DataFrame): The input data as a pandas DataFrame containing the data for the monsters and their stats.
         x (str): The column name from the dataframe to be used for the x-axis of the chart

         y (str): The column name from the dataframe to be used for the y-axis of the chart.
         target: The column name from the dataframe used for color encoding in the chart.

    :return:
        altair.Chart:  the generated scatter plot representing the relationships between the variables data in df.
    """
    
    # Create a Chart and assign it to 'graph'
    graph = Chart(
        data=df,
        title=Title(
            text=f"{y} by {x} for {target}",
            subtitle="Hover on the dots to see more details",
            color="gold",
            fontSize=20,
            fontWeight="bold",
        ),
    ).mark_circle(
            size=100
        ).encode(
        x=x, # X variable to X-axis
        y=y, # Y variable to Y-axis
        color=target, # Target Variable to Color
        tooltip=Tooltip(df.columns.to_list()) # Add tooltips based on column names in DataFrame
    ).properties(
            width=500,
            height=500,
            background="white",
            padding=45
        ).configure_legend(
            titleColor="gold",
            labelColor="gold",
            labelFontSize=15,
            titleFontSize=15,
            titleFontWeight="bold",
        ).configure_axis(
            gridColor = "lightgray",
            titleColor = "gold",
            labelColor = "gold",
            titlePadding = 10)
    return graph
