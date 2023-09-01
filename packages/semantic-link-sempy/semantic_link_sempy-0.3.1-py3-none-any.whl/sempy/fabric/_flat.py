import graphviz
import pandas as pd
import datetime
from uuid import UUID

from sempy.fabric._dataframe._fabric_dataframe import FabricDataFrame
from sempy.fabric._client import DatasetXmlaClient
from sempy.fabric._cache import _get_or_create_workspace_client
from sempy.fabric._utils import _get_relationships
from sempy.relationships import plot_relationship_metadata
from sempy.relationships._utils import _to_dataframe_dict
from sempy.relationships._validate import _list_relationship_violations
from sempy._utils._log import log, log_tables

from typing import Dict, List, Optional, Tuple, Union


@log
def list_datasets(workspace: Optional[Union[str, UUID]] = None) -> pd.DataFrame:
    """
    List datasets in a `Fabric workspace <https://learn.microsoft.com/en-us/fabric/get-started/workspaces>`_.

    Parameters
    ----------
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing databases and their attributes.
    """
    return _get_or_create_workspace_client(workspace).get_datasets()


@log
def list_measures(dataset: Union[str, UUID], workspace: Optional[Union[str, UUID]] = None) -> pd.DataFrame:
    """
    Retrieve all measures associated with the given dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list the measures for.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing measures and their attributes.
    """
    return _get_or_create_workspace_client(workspace).list_measures(dataset)


@log
def read_table(
    dataset: Union[str, UUID],
    table: str,
    fully_qualified_columns: bool = False,
    num_rows: Optional[int] = None,
    multiindex_hierarchies: bool = False,
    pandas_convert_dtypes: bool = True,
    workspace: Optional[Union[str, UUID]] = None,
    verbose: int = 0
) -> FabricDataFrame:
    """
    Read a PowerBI table into a FabricDataFrame.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list the measures for.
    table : str
        Name of the table to read.
    fully_qualified_columns : bool, default=False
        Whether or not to represent columns in their fully qualified form (TableName[ColumnName]).
    num_rows : int, default=None
        How many rows of the table to return. If None, all rows are returned.
    multiindex_hierarchies : bool, default=False
        Whether or not to convert existing `PowerBI Hierarchies <https://learn.microsoft.com/en-us/power-bi/create-reports/service-metrics-get-started-hierarchies>`_
        to pandas MultiIndex.
    pandas_convert_dtypes : bool, default=True
        Whether or not to implicitly cast columns to the best possible dtype (supporting pd.NA) using pandas
        `convert_dtypes <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.convert_dtypes.html>`_.
        Turning this off may result in type incompatibility issues between columns of related tables that may
        not have been detected in the PowerBI model due to `DAX implicit type conversion <https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-types#implicit-and-explicit-data-type-conversion>`_
        (e.g. merges/joins with float vs int columns).
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    verbose : int
        Verbosity. 0 means no verbosity.

    Returns
    -------
    FabricDataFrame
        Dataframe for the given table name with metadata from the PowerBI model.
    """  # noqa E501
    return _get_or_create_workspace_client(workspace) \
        .get_dataset_client(dataset, use_xmla=True) \
        .read_table(table, fully_qualified_columns, num_rows, multiindex_hierarchies, pandas_convert_dtypes, verbose=verbose)


@log
def get_tmsl(dataset: Union[str, UUID], workspace: Optional[Union[str, UUID]] = None) -> str:
    """
    Retrieve the Tabular Model Scripting Language (`TMSL <https://learn.microsoft.com/en-us/analysis-services/tmsl/tabular-model-scripting-language-tmsl-reference?view=asallproducts-allversions>`_) for a given dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list the measures for.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    str
        `TMSL <https://learn.microsoft.com/en-us/analysis-services/tmsl/tabular-model-scripting-language-tmsl-reference?view=asallproducts-allversions>`_ for the given dataset.
    """ # noqa E501
    workspace_client = _get_or_create_workspace_client(workspace)
    return workspace_client.get_tmsl(dataset)


@log
def list_tables(
    dataset: Union[str, UUID],
    include_columns: bool = False,
    include_partitions: bool = False,
    workspace: Optional[Union[str, UUID]] = None
) -> pd.DataFrame:
    """
    List all tables in a dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list the measures for.
    include_columns : bool, default=False
        Whether or not to include column level information.
        Cannot be combined with include_partitions.
    include_partitions : bool, default=False
        Whether or not to include partition level information.
        Cannot be combined with include_columns.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        Dataframe listing the tables and optional columns.
    """
    if include_columns and include_partitions:
        raise ValueError("Cannot include both columns and partitions.")

    workspace_client = _get_or_create_workspace_client(workspace)
    tabular_database = workspace_client.get_dataset(dataset)

    rows: List[Dict] = []

    for table in tabular_database.Model.Tables:
        if workspace_client._is_internal(table):
            continue
        row = {
            "Name":        table.Name,
            "Description": table.Description,
        }

        if include_partitions:
            row["Partition Name"] = [p.Name for p in table.Partitions]
            row["Partition Refreshed Time"] = [
                # Convert date via ISO format string operations carefully avoiding function calls
                # that may involve TZ environment interpreatation. This is in line with PBI general
                # use of unspecified timezones.
                datetime.datetime.strptime(p.RefreshedTime.ToString("s"), "%Y-%m-%dT%H:%M:%S")
                for p in table.Partitions
            ]

        if include_columns:
            columns = []
            for column in table.Columns:
                if column.Name.startswith("RowNumber"):
                    continue
                columns.append(column.Name)
            row["Column"] = columns

        rows.append(row)

    df = pd.DataFrame(rows)
    if include_columns:
        df = df.explode("Column")
    if include_partitions:
        df = df.explode(["Partition Name", "Partition Refreshed Time"])

    return df


@log
def evaluate_measure(
    dataset: Union[str, UUID],
    measure: Union[str, List[str]],
    groupby_columns: Optional[List[Tuple[str, str]]] = None,
    filters: Optional[Dict[Tuple[str, str], List[str]]] = None,
    fully_qualified_columns: Optional[bool] = None,
    num_rows: Optional[int] = None,
    pandas_convert_dtypes: bool = True,
    use_xmla: bool = False,
    workspace: Optional[Union[str, UUID]] = None,
    verbose: int = 0
) -> FabricDataFrame:
    """
    Compute PowerBI `measure <https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures>`_ for a given dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list the measures for.
    measure : str or list of str
        Name of the measure, or list of measures to compute.
    groupby_columns : list, default=None
        List of columns to group by as tuples of table and column name.
    filters : dict, default=None
        Dictionary containing a list of column values to filter the output by, where
        the key is a tuple of table and column name (currently only supports the "in" filter).
        For example, to specify that in the "State" table the "Region" column can only be "East"
        or "Central" and that the "State" column can only be "WA" or "CA" the resulting filter would look like::

            {
                ('State', 'Region'):    ["East", "Central"],
                ('State', 'State'):     ["WA", "CA"]
            }
    fully_qualified_columns : bool, default=None
        Whether or not to represent columns in their fully qualified form (TableName[ColumnName] for dimensions).
        Measures are always represented without the table name.
        If None, the fully qualified form will only be used if there is a name conflict between columns from different tables.
    num_rows : int, default=None
        How many rows of the table to return. If None, all rows are returned.
    pandas_convert_dtypes : bool, default=True
        Whether or not to implicitly cast columns to the best possible dtype (supporting pd.NA) using pandas 
        `convert_dtypes <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.convert_dtypes.html>`_.
        Turning this off may result in type incompatibility issues between columns of related tables that may
        not have been detected in the PowerBI model due to `DAX implicit type conversion <https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-types#implicit-and-explicit-data-type-conversion>`_ 
        (ex: merges/joins with float vs int columns).
    use_xmla : bool, default=False
        Whether or not to use `XMLA <https://learn.microsoft.com/en-us/analysis-services/xmla/xml-for-analysis-xmla-reference?view=asallproducts-allversions>`_ 
        as the backend for evaluation. When False, REST backend will be used.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    verbose : int
        Verbosity. 0 means no verbosity.

    Returns
    -------
    FabricDataFrame
        :class:`~sempy.fabric.FabricDataFrame` holding the computed measure stratified by groupby columns.
    """  # noqa E501

    # The REST API does not allow for pagination when using the "top" feature. Since the maximum page size is
    # 30,000 rows, we prevent the user from triggering pagination with num_rows set.
    if not use_xmla and (num_rows and num_rows > 30000):
        if verbose > 0:
            print(f"Provided num_rows ({num_rows}) is greater than 30,000. Switching to XMLA backend.")
        use_xmla = True
    return _get_or_create_workspace_client(workspace) \
        .get_dataset_client(dataset, use_xmla=use_xmla) \
        .evaluate_measure(measure, groupby_columns, filters, fully_qualified_columns, num_rows, pandas_convert_dtypes, verbose)     # type: ignore


@log
def evaluate_dax(
    dataset: Union[str, UUID],
    dax_string: str,
    pandas_convert_dtypes: bool = True,
    workspace: Optional[Union[str, UUID]] = None,
    verbose: int = 0
) -> FabricDataFrame:
    """
    Compute `DAX <https://learn.microsoft.com/en-us/dax/>`_ query for a given dataset.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list the measures for.
    dax_string : str
        The DAX query.
    pandas_convert_dtypes : bool, default=True
        Whether or not to implicitly cast columns to the best possible dtype (supporting pd.NA) using pandas
        `convert_dtypes <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.convert_dtypes.html>`_.
        Turning this off may result in type incompatibility issues between columns of related tables that may
        not have been detected in the PowerBI model due to `DAX implicit type conversion
        <https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-types#implicit-and-explicit-data-type-conversion>`_
        (ex: merges/joins with float vs int columns).
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID.
        Defaults to None which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.
    verbose : int
        Verbosity. 0 means no verbosity.

    Returns
    -------
    FabricDataFrame
        :class:`~sempy.fabric.FabricDataFrame` hsolding the result of the DAX query.
    """
    client: DatasetXmlaClient = _get_or_create_workspace_client(workspace).get_dataset_client(dataset, use_xmla=True)  # type: ignore
    return client.evaluate_dax(dax_string, pandas_convert_dtypes, verbose)


@log_tables
def plot_relationships(
    tables: Union[Dict[str, FabricDataFrame], List[FabricDataFrame]],
    include_columns='keys',
    missing_key_errors='raise',
    *,
    graph_attributes: Optional[Dict] = None
) -> graphviz.Digraph:
    """
    Visualize relationship dataframe with a graph.

    Parameters
    ----------
    tables : dict[str, sempy.fabric.FabricDataFrame] or list[sempy.fabric.FabricDataFrame]
        A dictionary that maps table names to the dataframes with table content.
        If a list of dataframes is provided, the function will try to infer the names from the
        session variables and if it cannot, it will use the positional index to describe them in
        the results.
        It needs to provided only when `include_columns` = 'all' and it will be used
        for mapping table names from relationships to the dataframe columns.
    include_columns : str, default='keys'
        One of 'keys', 'all', 'none'. Indicates which columns should be included in the graph.
    missing_key_errors : str, default='raise'
        One of 'raise', 'warn', 'ignore'. Action to take when either table or column
        of the relationship is not found in the elements of the argument *tables*.
    graph_attributes : dict, default=None
        Attributes passed to graphviz. Note that all values need to be strings. Useful attributes are:

        - *rankdir*: "TB" (top-bottom) or "LR" (left-right)
        - *dpi*:  "100", "30", etc. (dots per inch)
        - *splines*: "ortho", "compound", "line", "curved", "spline" (line shape)

    Returns
    -------
    graphviz.Digraph
        Graph object containing all relationships.
        If include_attributes is true, attributes are represented as ports in the graph.
    """
    named_dataframes = _to_dataframe_dict(tables)
    relationships = _get_relationships(named_dataframes)
    return plot_relationship_metadata(
        relationships,
        tables,
        include_columns=include_columns,
        missing_key_errors=missing_key_errors,
        graph_attributes=graph_attributes)


@log
def list_relationships(
    dataset: Union[str, UUID],
    workspace: Optional[Union[str, UUID]] = None
) -> pd.DataFrame:
    """
    List all relationship found within the Power BI model.

    Parameters
    ----------
    dataset : str or uuid.UUID
        Name or UUID of the dataset to list the measures for.
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None
        which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per relationship.
    """
    return _get_or_create_workspace_client(workspace).get_dataset_client(dataset, use_xmla=True).list_relationships()


@log_tables
def list_relationship_violations(
        tables: Union[Dict[str, FabricDataFrame], List[FabricDataFrame]],
        missing_key_errors='raise',
        coverage_threshold: float = 1.0,
        n_keys: int = 10
) -> pd.DataFrame:
    """
    Validate if the content of tables matches relationships.

    Relationships are extracted from the metadata in FabricDataFrames.
    The function examines results of joins for provided relationships and
    searches for inconsistencies with the specified relationship multiplicity.

    Relationships from empty tables (dataframes) are assumed as valid.

    Parameters
    ----------
    tables : dict[str, sempy.fabric.FabricDataFrame] or list[sempy.fabric.FabricDataFrame]
        A dictionary that maps table names to the dataframes with table content.
        If a list of dataframes is provided, the function will try to infer the names from the
        session variables and if it cannot, it will use the positional index to describe them in
        the results.
    missing_key_errors : str, default='raise'
        One of 'raise', 'warn', 'ignore'. Action to take when either table or column
        of the relationship is not found in the elements of the argument *tables*.
    coverage_threshold : float, default=1.0
        Fraction of rows in the "from" part that need to join in inner join.
    n_keys : int, default=10
        Number of missing keys to report. Random collection can be reported.

    Returns
    -------
    pandas.DataFrame
        Dataframe with relationships, error type and error message.
        If there are no violations, returns an empty DataFrame.
    """
    named_dataframes = _to_dataframe_dict(tables)
    relationships = _get_relationships(named_dataframes)
    return _list_relationship_violations(named_dataframes, relationships, missing_key_errors, coverage_threshold, n_keys)


@log
def resolve_workspace_id(workspace: Optional[Union[str, UUID]] = None) -> Optional[UUID]:
    """
    Resolve the workspace name or ID to the workspace UUID.

    Parameters
    ----------
    workspace : str or uuid.UUID, default=None
        The Fabric workspace name or UUID object containing the workspace ID. Defaults to None
        which resolves to the workspace of the attached lakehouse
        or if no lakehouse attached, resolves to the workspace of the notebook.

    Returns
    -------
    uuid.UUID or None
        The workspace UUID, or None if My Workspace.
    """
    workspace_id = _get_or_create_workspace_client(workspace).get_workspace_id()

    return UUID(workspace_id) if workspace_id else None
