import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime
from typing import Optional, Union, List

from sempy.functions import (
    semantic_function,
    semantic_parameters
)


def _detect_frequency(df: pd.DataFrame, time_col: str, grouping=None, threshold=0.95):
    """
    Detect whether a time series is regularly spaced, and at what interval.

    Takes a dataframe and a time attribute / column and determines whether it
    describes a regularly spaced time series. Optionally, grouping can be specified,
    in which case each group should be a regularly spaced time series with a common interval.
    If no consistent interval can be found (i.e this is a point process and not a proper time series), None is returned.

    The data is sorted by time_col prior to determining the interval.

    Parameters
    ----------
    df : pd.DataFrame
        Data containing time series.

    time_col : str
        Attribute containing time data.

    grouping : str, Attribute or list of str or Attribute, default=None
        Attribute or column used for grouping. If None, data is assumed to not be grouped.

    threshold : float, default=.95
        Fraction of the data that is required to adhere to the interval (per group).
        This tolerance allows to take into account missing data.

    Returns
    -------
    interval : np.timedelta64 or None
        Spacing of time stamps in time_col or None if no regular spacing is found.

    """

    def _detect_frequency_single(ungrouped_sdf):
        """
        Detect whether a time series is regularly spaced, and at what interval.
        """
        series = pd.to_datetime(ungrouped_sdf[time_col])
        pandas_guess = pd.infer_freq(series)
        if pandas_guess is not None:
            # Pandas returns a string, but we want a timedelta64 to be consistent with the rest of the code.
            # Apparently you can't do to_timedelta with "D", a number is needed.
            return pd.to_timedelta(
                pandas_guess if pandas_guess[0].isnumeric() else f"1{pandas_guess}"
            )
        diff_series = series.sort_values().reset_index(drop=True).diff()
        delta = diff_series.mode().iloc[0]
        # most differences are delta, safe to assume regularly spaces
        if (diff_series == delta).mean() > threshold:
            return delta
        # mode is not common enough to be considered regularly spaces
        return None

    if grouping is None:
        return _detect_frequency_single(df)
    if isinstance(grouping, list) and len(grouping) == 1:
        # pandas 1.5 deprecation work-around
        (grouping,) = grouping
    # if grouping, check delta in each group, and return if they are all the same
    group_deltas = {
        name: _detect_frequency_single(group) for name, group in df.groupby(grouping)
    }
    if len(set(group_deltas.values())) == 1:
        return list(group_deltas.values())[0]
    return None


def _find_pretty_grid(n_plots, max_cols=5):
    """
    Determine a good grid shape for subplots.

    Tries to find a way to arange n_plots many subplots on a grid in a way
    that fills as many grid-cells as possible, while keeping the number
    of rows low and the number of columns below max_cols.

    Parameters
    ----------
    n_plots : int
        Number of plots to arrange.
    max_cols : int, default=5
        Maximum number of columns.

    Returns
    -------
    n_rows : int
        Number of rows in grid.
    n_cols : int
        Number of columns in grid.

    Examples
    --------
    >>> find_pretty_grid(16, 5)
    (4, 4)
    >>> find_pretty_grid(11, 5)
    (3, 4)
    >>> find_pretty_grid(10, 5)
    (2, 5)
    """
    # we could probably do something with prime numbers here
    # but looks like that becomes a combinatorial problem again?
    if n_plots % max_cols == 0:
        # perfect fit!
        # if max_cols is 6 do we prefer 6x1 over 3x2?
        return int(n_plots / max_cols), max_cols
    # min number of rows needed
    min_rows = int(np.ceil(n_plots / max_cols))
    best_empty = max_cols
    best_cols = max_cols
    for cols in range(max_cols, min_rows - 1, -1):
        # we only allow getting narrower if we have more cols than rows
        remainder = (n_plots % cols)
        empty = cols - remainder if remainder != 0 else 0
        if empty == 0:
            return int(n_plots / cols), cols
        if empty < best_empty:
            best_empty = empty
            best_cols = cols
    return int(np.ceil(n_plots / best_cols)), best_cols


@semantic_function("plot_time_series")
@semantic_parameters(time_col=datetime.datetime,
                     numeric_cols=List[Union[int, float]],
                     group_cols=Optional[List[pd.Categorical]])
def _plot_time_series(
    df: pd.DataFrame,
    time_col: str,
    numeric_cols: str,
    group_cols: Optional[str] = None,
    max_cols: int = 5,
    **kwargs,
):
    # basic plots of time series / whether it's ordered
    # detect frequency of regularly spaced time series:
    res = []
    freq = _detect_frequency(df, time_col=time_col, grouping=group_cols)

    col = df[time_col]

    if freq is None or not numeric_cols:
        # if it's evenly spaced we don't plot it
        # unless there's nothing else to plot.
        fig, ax = plt.subplots(1, 2, sharey=True)
        col.plot(title="Time Stamps", ax=ax[0])
        col.hist(ax=ax[1], orientation="horizontal", bins=50)
        ax[1].set_xticks(())
        ax[1].set_title("Observation Frequencies")
        ax[0].set_ylabel(col.name)
        ax[0].set_xlabel("Index")
        res.append(fig)

    if not numeric_cols:
        return res

    group_columns = group_cols if group_cols is not None else []
    numeric_columns = numeric_cols

    # single value column for seaborn, long long format
    df_long = df.melt(
        value_vars=numeric_columns,
        id_vars=[time_col] + group_columns,  # type: ignore
        value_name="sempy_value",
        var_name="sempy_variables",
    )

    facets = df_long.columns.drop([time_col, "sempy_value"])
    # drop columns with unique values from facets
    facets = [f for f in facets if df_long[f].nunique() > 1]

    if not facets:
        # if there are no facets, use lineplot with hue=None
        facets = [None]
    if len(facets) == 1:
        plt.figure()
        # Using errorbar='sd' skips bootstrapping when aggregating, use standard deviation which is much faster.
        res.append(
            sns.lineplot(
                data=df_long, x=time_col, y="sempy_value", hue=facets[0], errorbar="sd"
            )
        )
    elif len(facets) == 2:
        n_plots = df_long[facets[0]].nunique()
        _, col_wrap = _find_pretty_grid(n_plots, max_cols=max_cols)
        g = sns.FacetGrid(
            df_long, col=facets[0], hue=facets[1], col_wrap=col_wrap, **kwargs
        )
        res.append(g.map(sns.lineplot, time_col, "sempy_value", errorbar="sd"))
    elif len(facets) == 3:
        g = sns.FacetGrid(
            df_long, col=facets[0], row=facets[1], hue=facets[2], **kwargs
        )
        res.append(g.map(sns.lineplot, time_col, "sempy_value", errorbar="sd"))
    else:
        raise NotImplementedError(
            "Plotting more than three facets at a time not supported."
        )

    return res
