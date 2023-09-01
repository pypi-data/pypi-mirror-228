from decimal import Decimal
import pandas as pd
from uuid import UUID

from sempy.fabric._client._base_dataset_client import BaseDatasetClient
from sempy.fabric._token_provider import TokenProvider

from typing import Optional, Union, List, Tuple, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from sempy.fabric._client import WorkspaceClient


class DatasetRestClient(BaseDatasetClient):
    """
    Client for access to Power BI data in a specific dataset using REST API calls.

    Parameters
    ----------
    workspace : str or WorkspaceClient
        PowerBI workspace name or workspace client that the dataset originates from.
    dataset : str
        Dataset name or GUID.
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
        BaseDatasetClient.__init__(self, workspace, dataset, token_provider)

    def _format_measure_df(self, columns: List[dict], rows: List[list], measure: Union[str, List[str]]) -> pd.DataFrame:
        if isinstance(measure, str):
            measure = [measure]

        gb_cols = columns[len(measure):]
        gb_col_names = []
        datetimes = []
        decimals = []
        for gb_col in gb_cols:
            col_name = f"{gb_col['source']['table']}[{gb_col['source']['column']}]"
            gb_col_names.append(col_name)
            if gb_col["type"] == 2:
                decimals.append(col_name)
            elif gb_col["type"] == 7:
                datetimes.append(col_name)

        res_columns = measure + gb_col_names
        df = pd.DataFrame(rows, columns=res_columns)
        df[datetimes] = df[datetimes].apply(pd.to_datetime)
        for decimal_col in decimals:    # type: ignore
            # Converting from float to Decimal results in exact conversion, which may add unintended places to
            # the Decimal value (ex: Decimal(13.34) = Decimal(13.339999999999999))
            # String to Decimal uses the exact string passed which is what we want (ex: Decimal('13.34') = Decimal(13.34))
            df[decimal_col] = df[decimal_col].astype(str).apply(Decimal)

        # reorder columns so measure is last (match XMLA output)
        res_columns_reordered = gb_col_names + measure
        return df[res_columns_reordered]

    def _evaluate_dax(self, query: str, verbose: int = 0) -> pd.DataFrame:
        rows = self._rest_api.execute_dax_query(self._dataset_id, query)
        return pd.DataFrame(rows)

    def _evaluate_measure(
        self,
        measure: Union[str, List[str]],
        groupby_columns: List[Tuple[str, str]],
        filters: Dict[Tuple[str, str], List[str]],
        num_rows: Optional[int] = None,
        batch_size: int = 100000,
        verbose: int = 0
    ) -> pd.DataFrame:
        groupby_columns_obj = [{"table": g[0], "column": g[1]} for g in groupby_columns]

        if isinstance(measure, str):
            measure = [measure]
        measure_obj = [{"measure": m} for m in measure]

        filter_obj: List[Dict[str, list]] = []
        for table_col, filter_lst in filters.items():
            target = [{"table": table_col[0], "column": table_col[1]}]
            # REST API requires the "in" parameter to have every object as its own list
            filter_in = [[obj] for obj in filter_lst]
            filter_obj.append({"target": target, "in": filter_in})

        columns, rows = self._rest_api.calculate_measure(self._dataset_id, measure_obj, groupby_columns_obj, filter_obj, num_rows, verbose)
        if not columns:
            col_names = [f"{g[0]}[{g[1]}]" for g in groupby_columns]
            col_names.extend(measure)
            return pd.DataFrame({}, columns=col_names)
        else:
            return self._format_measure_df(columns, rows, measure)

    def __repr__(self) -> str:
        return f"DatasetRestClient('{self._workspace_client.get_workspace_name()}[{self._dataset_name}]')"
