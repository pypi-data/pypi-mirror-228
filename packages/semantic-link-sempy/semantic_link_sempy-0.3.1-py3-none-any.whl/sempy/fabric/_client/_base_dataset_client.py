from uuid import UUID
import pandas as pd
import re
from abc import abstractmethod
from collections import defaultdict
import warnings

from sempy.fabric._dataframe._fabric_dataframe import FabricDataFrame
from sempy.fabric._client._rest_api import _PBIRestAPI
from sempy.fabric.exceptions import DatasetNotFoundException
from sempy.fabric._token_provider import SynapseTokenProvider, TokenProvider
from sempy.fabric._metadatakeys import MetadataKeys
from sempy.fabric._utils import is_valid_uuid

from typing import Any, Optional, Union, List, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from sempy.fabric._client import WorkspaceClient


class BaseDatasetClient():
    """
    Client for access to Power BI data in a specific dataset (database).

    Each client will usually map to a Dataset (Database) i.e. one or more clients can be instantiated
    within each accessed workspace.

    Parameters
    ----------
    workspace : str or WorkspaceClient
        PowerBI workspace name or workspace client that the dataset originates from.
    dataset : str or UUID
        Dataset name or UUID object containing the dataset ID.
    token_provider : TokenProvider, default=None
        Implementation of TokenProvider that can provide auth token
        for access to the PowerBI workspace. Will attempt to acquire token
        from its execution environment if not provided.
    """
    def __init__(
            self,
            workspace: Union[str, "WorkspaceClient"],
            dataset: Union[str, UUID],
            token_provider: Optional[TokenProvider] = None
    ):
        from sempy.fabric._client import WorkspaceClient
        self.token_provider = token_provider or SynapseTokenProvider()

        self._workspace_client: WorkspaceClient
        if isinstance(workspace, WorkspaceClient):
            self._workspace_client = workspace
        else:
            self._workspace_client = WorkspaceClient(workspace, self.token_provider)

        self._rest_api = _PBIRestAPI(token_provider=self.token_provider)

        workspace_name = self._workspace_client.get_workspace_name()

        if isinstance(dataset, UUID):
            self._dataset_id = str(dataset)
            self._dataset_name = self._rest_api.get_dataset_name_from_id(str(dataset), workspace_name)
        elif isinstance(dataset, str):
            # It is possible to use UUID formatted strings as dataset name, so we need to
            # check first if a name exists before testing for UUID format:
            try:
                self._dataset_id = self._rest_api.get_dataset_id_from_name(dataset, workspace_name)
                self._dataset_name = dataset
            except DatasetNotFoundException:
                if is_valid_uuid(dataset):
                    self._dataset_id = dataset
                    self._dataset_name = self._rest_api.get_dataset_name_from_id(dataset, workspace_name)
                else:
                    raise
        else:
            raise TypeError(f"Unexpected type {type(dataset)} for \"dataset\"")

    def evaluate_dax(self, query: str, pandas_convert_dtypes: bool = True, verbose: int = 0) -> FabricDataFrame:
        """
        Retrieve results of DAX query as a FabricDataFrame.

        Parameters
        ----------
        query : str
            DAX query.
        pandas_convert_dtypes : bool, default=True
            Whether or not to implicitly cast columns to the best possible dtype (supporting pd.NA) using pandas
            `convert_dtypes <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.convert_dtypes.html>`_.
            Turning this off may result in type incompatibility issues between columns of related tables that may
            not have been detected in the PowerBI model due to `DAX implicit type conversion
            <https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-types#implicit-and-explicit-data-type-conversion>_`
            (ex: merges/joins with float vs int columns).
        verbose : int
            Verbosity. 0 means no verbosity.

        Returns
        -------
        FabricDataFrame
            FabricDataFrame converted from the results of a DAX query.
        """
        df = self._evaluate_dax(query, verbose)
        if pandas_convert_dtypes:
            df = df.convert_dtypes(convert_string=True)
        return FabricDataFrame(df, dataset=self._dataset_name, workspace=self._workspace_client.get_workspace_name())

    @abstractmethod
    def _evaluate_dax(self, query: str, verbose: int = 0) -> pd.DataFrame:
        """
        Retrieve results of DAX query as a pandas DataFrame.

        Parameters
        ----------
        query : str
            DAX query.
        verbose : int
            Verbosity. 0 means no verbosity.

        Returns
        -------
        DataFrame
            Pandas DataFrame converted from the results of a DAX query.
        """
        pass

    def evaluate_measure(
        self,
        measure: Union[str, List[str]],
        groupby_columns: Optional[List[Tuple[str, str]]] = None,
        filters: Optional[Dict[Tuple[str, str], List[str]]] = None,
        fully_qualified_columns: Optional[bool] = None,
        num_rows: Optional[int] = None,
        pandas_convert_dtypes: bool = True,
        verbose: int = 0
    ) -> FabricDataFrame:
        """
        Compute PowerBI metric for a given dataset.

        Parameters
        ----------
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
            Whether or not to represent columns in their fully qualified form (TableName[ColumnName]).
            If None, the fully qualified form will only be used if there is a name conflict between columns from different tables.
        num_rows : int, default=None
            How many rows of the table to return. If None, all rows are returned.
        pandas_convert_dtypes : bool, default=True
            Whether or not to implicitly cast columns to the best possible dtype (supporting pd.NA) using pandas
            `convert_dtypes <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.convert_dtypes.html>`_.
            Turning this off may result in type incompatibility issues between columns of related tables that may
            not have been detected in the PowerBI model due to `DAX implicit type conversion
            <https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-types#implicit-and-explicit-data-type-conversion>_`
            (ex: merges/joins with float vs int columns).
        verbose : int
            Verbosity. 0 means no verbosity.

        Returns
        -------
        FabricDataFrame
            :class:`~sempy.fabric.FabricDataFrame` holding the computed measure stratified by groupby columns.
        """
        if groupby_columns is None:
            groupby_columns = []
        [self._validate_tuple(g, "groupby_columns") for g in groupby_columns]

        if filters is None:
            filters = {}
        for table_col, filter_lst in filters.items():
            self._validate_tuple(table_col, "filters")
            if not isinstance(filter_lst, list):
                raise TypeError(f"Filter values must be a list: {type(filter_lst)}")

        columns = [g[1] for g in groupby_columns]
        naming_conflict = len(set(columns)) != len(columns)
        if naming_conflict and fully_qualified_columns is False:
            dupl_columns = [col for col in columns if columns.count(col) > 1]
            raise ValueError(f"Multiple columns with the name(s) '{set(dupl_columns)}' given. Use 'fully_qualified_columns=True' to avoid conflicts.")
        if fully_qualified_columns is None:
            fully_qualified_columns = True if naming_conflict else False
            if verbose > 1:
                print(f"Setting fully_qualified_columns to {fully_qualified_columns}")

        measure_lst = measure if isinstance(measure, list) else [measure]
        # strip [] from each measure
        measure_lst = [m[1:-1] if m.startswith("[") and m.endswith("]") else m for m in measure_lst]

        df = self._evaluate_measure(measure_lst, groupby_columns, filters, num_rows, verbose=verbose)
        if not fully_qualified_columns:
            df = self._simplify_col_names(df)
        if pandas_convert_dtypes:
            df = df.convert_dtypes(convert_string=False)
        # FIXME: We should be able to use the FabricDF constructor here and then rename the columns after,
        # but renaming is not currently propogated in metadata.
        # Rather than relying on auto-resolving column names, we rely on the column-table mappings already provided by groupby column tuples.
        return self._add_column_metadata_from_tuples(df, groupby_columns)

    def _validate_tuple(self, tuple, arg):
        if len(tuple) != 2:
            raise ValueError(f"\"{arg}\" tuple must have 2 elements: (table, column)")
        if not isinstance(tuple[0], str):
            raise TypeError(f"Unexpected type {type(tuple[0])} in \"{arg}\" table name: not a str")
        if not isinstance(tuple[1], str):
            raise TypeError(f"Unexpected type {type(tuple[1])} in \"{arg}\" column name: not a str")

    @abstractmethod
    def _evaluate_measure(
        self,
        measure: Union[str, List[str]],
        groupby_columns: List[Tuple[str, str]],
        filters: Dict[Tuple[str, str], List[str]],
        num_rows: Optional[int] = None,
        batch_size: int = 100000,
        verbose: int = 0
    ) -> pd.DataFrame:
        pass

    def list_relationships(self, exclude_internal=True) -> pd.DataFrame:
        """
        List all relationship found within the PBI model.

        Returns
        -------
        DataFrame
            Pandas DataFrame with one row per relationship.

        Parameters
        ----------
        exclude_internal : bool, default=True
            Whether relationships to internal PowerBI entities should be excluded.
        """
        database = self._workspace_client.get_dataset(self._dataset_name)

        relationships = []
        for relationship in database.Model.Relationships:
            if self._show_relationship(relationship, exclude_internal):
                relationships.append({
                    "Multiplicity": _to_multiplicity(relationship),
                    "From Table": relationship.FromTable.Name,
                    "From Column": relationship.FromColumn.Name,
                    "To Table": relationship.ToTable.Name,
                    "To Column": relationship.ToColumn.Name
                })

        return pd.DataFrame(relationships)

    def read_table(
        self,
        table_name: str,
        fully_qualified_columns: bool = False,
        num_rows: Optional[int] = None,
        multiindex_hierarchies: bool = False,
        pandas_convert_dtypes: bool = True,
        exclude_internal: bool = True,
        verbose: int = 0
    ) -> FabricDataFrame:
        """
        Read specified PBI Dataset tables into FabricDataFrames with populated metadata.

        Parameters
        ----------
        table_name : str
            Name of table from dataset.
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
            not have been detected in the PowerBI model due to `DAX implicit type conversion
            <https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-types#implicit-and-explicit-data-type-conversion>_`
            (ex: merges/joins with float vs int columns).
        exclude_internal : bool, default=True
            Whether internal PowerBI columns should be excluded during the load operation.
        verbose : int
            Verbosity. 0 means no verbosity.

        Returns
        -------
        FabricDataFrame
            DataFrame with metadata from the PBI model.
        """
        database = self._workspace_client.get_dataset(self._dataset_name)
        for table in database.Model.Tables:
            if table.Name == table_name:
                pandas_df = self._get_pandas_table(table.Name, fully_qualified_columns, num_rows, verbose)
                meta_df = self._populate_table_meta(pandas_df, table, fully_qualified_columns, exclude_internal)
                # The dotnet parser for DAX handles standard type conversion from PowerBI data types (including datetime).
                if pandas_convert_dtypes:
                    # Using convert_string=False to follow pd.read_csv behavior which casts string columns as object.
                    meta_df = meta_df.convert_dtypes(convert_string=False)
                for relationship in database.Model.Relationships:
                    if relationship.FromTable.Name == table.Name:
                        self._populate_relationship_meta(relationship, meta_df, exclude_internal)
                if multiindex_hierarchies:
                    meta_df = self._convert_hierarchies(meta_df, table, fully_qualified_columns)
                return meta_df

        raise ValueError(f"'{table_name} is not a valid table in Dataset '{self._dataset_name}'")

    def resolve_metadata(self, columns: List[str], verbose: int = 0) -> Dict[str, Any]:
        """
        Resolve column names to their Power BI metadata.

        Parameters
        ----------
        columns : list of str
            List of column names to resolve. Column names can be in any of the following formats:
            - Column name only: "Column Name"
            - Unquoted table name + column name (if no spaces in table name): "TableName[Column Name]"
            - Quoted table name + column name: "'Table Name'[Column Name]"
        verbose : int
            Verbosity. 0 means no verbosity.

        Returns
        -------
        Dict of str
            Dictionary containing mapping of column name to its metadata.
        """
        database = self._workspace_client.get_dataset(self._dataset_name)

        column_map = defaultdict(lambda: [])
        for table in database.Model.Tables:
            for column in table.Columns:
                column_data = self._get_column_data(table, column)

                # Any syntax for column names valid for DAX is valid here
                # https://learn.microsoft.com/en-us/dax/dax-syntax-reference

                # column name only
                column_map[column.Name].append(column_data)

                # quoted column name
                column_map[f"[{column.Name}]"].append(column_data)

                # unquoted table name (if no spaces in table name)
                if ' ' not in table.Name:
                    column_map[f"{table.Name}[{column.Name}]"].append(column_data)

                # quoted table name
                column_map[f"'{table.Name}'[{column.Name}]"].append(column_data)

        column_metadata = {}
        for column in columns:
            column_data_list = column_map[column]

            num_column_matches = len(column_data_list)

            if num_column_matches == 1:
                if verbose > 0:
                    print(f"Column '{column}' matched to '{column_data_list[0]}'")

                column_metadata[column] = column_data_list[0]
            elif num_column_matches == 0:
                if verbose > 0:
                    print(f"Column '{column}' not found in dataset '{self._dataset_name}'")
            else:
                warnings.warn(f"Ambiguous column name '{column}' found in dataset '{self._dataset_name}': '{column_data_list}'")

        return column_metadata

    def _get_pandas_table(self, table_name, fully_qualified_columns, num_rows, verbose):
        if num_rows is None:
            dax_query = f"EVALUATE '{table_name}'"
        else:
            dax_query = f"EVALUATE TOPN({num_rows}, '{table_name}')"

        df = self._evaluate_dax(dax_query, verbose)

        if not fully_qualified_columns:
            df = self._simplify_col_names(df)

        return df

    def _convert_hierarchies(self, df, table, fully_qualified_columns: bool) -> FabricDataFrame:
        num_hierarchies = len(table.Hierarchies)
        if num_hierarchies > 1:
            raise ValueError(f"Table '{table.Name}' contains {num_hierarchies} hierarchies. Cannot convert multiple hierarchies to MultiIndex.")

        for hierarchy in table.Hierarchies:
            levels = []
            for level in hierarchy.Levels:
                level_name = level.Column.Name if not fully_qualified_columns else f"{table.Name}[{level.Column.Name}]"
                levels.append(level_name)
            df = df.set_index(levels)

        return df

    def _populate_table_meta(self, df, table, fully_qualified_columns: bool, exclude_internal: bool) -> FabricDataFrame:
        # convert TOM table to FabricDataFrame
        table_name = table.Name
        meta_df = FabricDataFrame(df)
        meta_df.column_metadata = {}

        # populate standard column data
        for column in table.Columns:
            column_name = column.Name if not fully_qualified_columns else f"{table_name}[{column.Name}]"
            if exclude_internal and column.Name.startswith("RowNumber"):
                continue

            column_data_type = column.DataType.ToString()
            if column_data_type in ['DateTime', 'Time', 'Date']:
                meta_df[column_name] = pd.to_datetime(df[column_name])

            column_data = self._get_column_data(table, column)
            meta_df.column_metadata[column_name] = column_data

        return meta_df

    def _get_column_data(self, table, column):
        from Microsoft.AnalysisServices.Tabular import CompatibilityViolationException

        column_data = {
            # TODO: should we put these into an enum?
            MetadataKeys.TABLE: table.Name,
            MetadataKeys.COLUMN: column.Name
        }

        # table level
        if self._dataset_name:
            column_data[MetadataKeys.DATASET] = self._dataset_name
        if self._workspace_client._workspace_id:
            column_data[MetadataKeys.WORKSPACE_ID] = self._workspace_client._workspace_id
        if self._workspace_client._workspace_name:
            column_data[MetadataKeys.WORKSPACE_NAME] = self._workspace_client._workspace_name
        if table.Annotations:
            # Excluding keys that are present in all tables or are not valuable to the user to reduce clutter. Ex:
            # {'LinkedQueryName': 'Sales'}
            table_annotations = self._extract_annotations(table, exclude_keys=["LinkedQueryName"])
            if len(table_annotations) > 0:
                column_data[MetadataKeys.TABLE_ANNOTATIONS] = table_annotations

        # column level
        if column.Alignment:
            # The possible values are Default (1), Left (2), Right (3), Center (4).
            # needed for formatting
            column_data[MetadataKeys.ALIGNMENT] = str(column.Alignment)
        if column.Annotations:
            # Excluding keys that are present in all tables or not valuable to the user to reduce clutter. Ex:
            # {'SummarizationSetBy': 'Automatic'}
            # {'Format': '<Format Format="General" />'}
            # {'DataTypeAtRefresh': 'Int64#####not a type'}
            col_annotations = self._extract_annotations(column, exclude_keys=["SummarizationSetBy", "Format", "DataTypeAtRefresh"])
            if len(col_annotations) > 0:
                column_data[MetadataKeys.COLUMN_ANNOTATIONS] = col_annotations
        if column.DataCategory:
            column_data[MetadataKeys.DATA_CATEGORY] = column.DataCategory
        if column.DataType:
            column_data[MetadataKeys.DATA_TYPE] = column.DataType.ToString()
        if column.Description:
            column_data[MetadataKeys.DESCRIPTION] = column.Description
        if column.ErrorMessage:
            column_data[MetadataKeys.ERROR_MESSAGE] = column.ErrorMessage
        try:
            if column.FormatString:
                column_data[MetadataKeys.FORMAT_STRING] = column.FormatString
        except CompatibilityViolationException:
            # computation of compatibility level can take excessive time
            pass
        if column.IsHidden:
            column_data[MetadataKeys.IS_HIDDEN] = column.IsHidden
        if column.IsKey:
            column_data[MetadataKeys.IS_KEY] = column.IsKey
        if column.IsNullable:
            column_data[MetadataKeys.IS_NULLABLE] = column.IsNullable
        if column.IsRemoved:
            column_data[MetadataKeys.IS_REMOVED] = column.IsRemoved
        if column.IsUnique:
            column_data[MetadataKeys.IS_UNIQUE] = column.IsUnique
        if column.LineageTag:
            column_data[MetadataKeys.LINEAGE_TAG] = column.LineageTag
        if column.ModifiedTime:
            column_data[MetadataKeys.MODIFIED_TIME] = column.ModifiedTime.ToString()
        if column.RefreshedTime:
            column_data[MetadataKeys.REFRESHED_TIME] = column.RefreshedTime.ToString()
        if column.SortByColumn:
            column_data[MetadataKeys.SORT_BY_COLUMN] = column.SortByColumn.Name
        if column.SourceLineageTag:
            column_data[MetadataKeys.SOURCE_LINEAGE_TAG] = column.SourceLineageTag
        if column.SummarizeBy:
            column_data[MetadataKeys.SUMMARIZE_BY] = column.SummarizeBy.ToString()

        return column_data

    def _extract_annotations(self, tom_obj, exclude_keys: List[str]) -> Dict[str, str]:
        annotations = {}
        for annotation in tom_obj.Annotations:
            # keys starting with PBI_ appear to be internal use keys
            if annotation.Name not in exclude_keys and not annotation.Name.startswith("PBI_"):
                annotations[annotation.Name] = annotation.Value
        return annotations

    def _populate_relationship_meta(self, relationship, from_dataframe: FabricDataFrame, exclude_internal: bool) -> None:
        # Populate a single relationship in the given table's metadata
        to_table = relationship.ToTable.Name
        to_column = relationship.ToColumn.Name
        from_column = relationship.FromColumn.Name

        if self._show_relationship(relationship, exclude_internal):
            # ignore relationships for which we don't have columns
            col_meta = from_dataframe.column_metadata.get(from_column, None)        # type: ignore

            if col_meta is not None:
                col_meta[MetadataKeys.RELATIONSHIP] = {
                    "to_table": to_table,
                    "to_column": to_column,
                    "multiplicity": _to_multiplicity(relationship)
                }

    def _add_column_metadata_from_tuples(self, df: Union[pd.DataFrame, FabricDataFrame], column_tuples: List[Tuple[str, str]]) -> FabricDataFrame:
        database = self._workspace_client.get_dataset(self._dataset_name)
        tables = {table.Name: table for table in database.Model.Tables}

        if isinstance(df, FabricDataFrame):
            meta_df = df
        else:
            meta_df = FabricDataFrame(df)

        if meta_df.column_metadata is None:
            meta_df.column_metadata = {}

        for table_name, col_name in column_tuples:
            table_tom = tables[table_name]
            for column in table_tom.Columns:
                if column.Name == col_name:
                    meta_df.column_metadata[col_name] = self._get_column_data(tables[table_name], column)

        return meta_df

    def _simplify_col_names(self, df):
        col_names = []
        for col in df.columns:
            match = re.match(r"^.*\[(.*)\]$", col)
            if match:
                col_names.append(match.group(1))
            else:
                col_names.append(col)
        df.columns = col_names
        return df

    def __repr__(self):
        return f"PowerBIClient('{self._workspace_client.get_workspace_name()}[{self._dataset_name}]')"

    def _show_relationship(self, relationship, exclude_internal):
        if exclude_internal:
            if self._workspace_client._is_internal(relationship.FromTable) or self._workspace_client._is_internal(relationship.ToTable):
                return False
        return True


def _to_multiplicity(relationship):
    from_cardinality = relationship.FromCardinality.ToString()
    to_cardinality = relationship.ToCardinality.ToString()
    map = {"One": "1", "Many": "m"}
    return f"{map[from_cardinality]}:{map[to_cardinality]}"
