import datetime
import pandas as pd

from sempy.fabric._client._dataset_xmla_client import DatasetXmlaClient
from sempy.fabric._client._dataset_rest_client import DatasetRestClient
from sempy.fabric._client._rest_api import _PBIRestAPI
from sempy.fabric._client._utils import _init_analysis_services, _get_workspace_url
from sempy.fabric._environment import get_workspace_id
from sempy.fabric._token_provider import SynapseTokenProvider, _get_token_seconds_remaining, TokenProvider
from sempy.fabric._utils import is_valid_uuid
from sempy.fabric.exceptions import DatasetNotFoundException, WorkspaceNotFoundException

from functools import lru_cache
from uuid import UUID
from typing import Optional, Union


class WorkspaceClient:
    """
    Accessor class for a Power BI workspace.

    The workspace can contain multiple Datasets, which can be accessed via
    a PowerBIClient obtained via :meth:`get_dataset_client`.

    The class is a thin wrapper around
    `Microsoft.AnalysisServices.Tabular.Server <https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.server?view=analysisservices-dotnet>`_
    client that accesses cloud Power BI workspace and its Tabular Object Model (TOM)
    via the XMLA interface. The client caches the connection to the server for faster performance.

    Parameters
    ----------
    workspace : str or UUID
        PowerBI Workspace Name or UUID object containing the workspace ID.
    token_provider : TokenProvider, default=None
        Implementation of :class:`~sempy.fabric._token_provider.TokenProvider` that can provide auth token
        for access to the PowerBI workspace. Will attempt to acquire token
        from its execution environment if not provided.
    """
    def __init__(self, workspace: Optional[Union[str, UUID]] = None, token_provider: Optional[TokenProvider] = None):

        _init_analysis_services()
        import Microsoft.AnalysisServices.Tabular as TOM

        self.tom_server = TOM.Server()
        self.token_provider = token_provider or SynapseTokenProvider()
        self._rest_api = _PBIRestAPI(token_provider=self.token_provider)
        self._connection = None
        self._cached_dataset_client = lru_cache()(
            lambda dataset_name, ClientClass: ClientClass(
                self,
                dataset_name,
                token_provider=self.token_provider
            )
        )

        self._workspace_id: Optional[str]
        self._workspace_name: str

        if workspace is None:
            self._workspace_id = get_workspace_id()
            self._workspace_name = self._rest_api.get_workspace_name_from_id(self._workspace_id)
        elif isinstance(workspace, UUID):
            self._workspace_id = str(workspace)
            self._workspace_name = self._rest_api.get_workspace_name_from_id(self._workspace_id)
        elif isinstance(workspace, str):
            if workspace == "My workspace":
                # To the best of our tribal knowledge, there is no way to find the ID for "My workspace"
                # from the outside of that workspace. So this leaves us with a truly Houdini option
                # of leaving the _workspace_id as None and treating None as "My workpaces's ID" later
                # in the code.
                self._workspace_id = None
                self._workspace_name = "My workspace"
            else:
                workspace_id = self._rest_api.get_workspace_id_from_name(workspace)
                if workspace_id is None:
                    if is_valid_uuid(workspace):
                        self._workspace_id = workspace
                        self._workspace_name = self._rest_api.get_workspace_name_from_id(self._workspace_id)
                    else:
                        raise WorkspaceNotFoundException(workspace)
                else:
                    self._workspace_id = workspace_id
                    self._workspace_name = workspace
        else:
            raise TypeError(f"Unexpected type {type(workspace)} for \"workspace\"")

        # A Houdini catch-all for various ways in which an Id for "My workspace" could be
        # passed explicitly via string or UUID. It standardizes the ID of "My workspace"
        # on value None, which is forced upon us by wonderous inconsistencies of PBI REST API:
        if self._workspace_name == "My workspace":
            self._workspace_id = None

    def get_workspace_id(self) -> Optional[str]:
        """
        Get workspace ID of associated workspace.

        None, if executed for "My workspace".

        Returns
        -------
        String
            Workspace ID.
        """
        return self._workspace_id

    def get_workspace_name(self) -> str:
        """
        Get name ID of associated workspace.

        Returns
        -------
        String
            Workspace name.
        """
        return self._workspace_name

    def get_connection(self):
        """
        Connect to PowerBI TOM Server, or returns server if already connected.

        Returns
        -------
        Microsoft.AnalysisServices.Tabular.Server
            XMLA client with a cached connection to a PowerBI Tabular Object Model server.
        """
        if self._connection is None or not self._check_token_valid():
            self._connection = self._connect_tom_server()

        return self._connection

    def _check_token_valid(self):
        return _get_token_seconds_remaining(self.token_provider()) > 60

    def _connect_tom_server(self):
        workspace_url = _get_workspace_url(self.get_workspace_name())
        self.tom_server.Connect(f"DataSource={workspace_url};Password={self.token_provider()};Application Name=SemPy")
        return self.tom_server

    def get_datasets(self) -> pd.DataFrame:
        """
        Get a list of datasets in a PowerBI workspace.

        Each dataset is derived from
        `Microsoft.AnalysisServices.Tabular.Database <https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.database?view=analysisservices-dotnet>`__

        The dataframe contains the following columns:

        - Dataset Name `see <https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.namedcomponent.name?view=analysisservices-dotnet#microsoft-analysisservices-namedcomponent-name>`__
        - Created Date `see <https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.majorobject.createdtimestamp?view=analysisservices-dotnet#microsoft-analysisservices-majorobject-createdtimestamp>`__
        - ID `see <https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.namedcomponent.id?view=analysisservices-dotnet#microsoft-analysisservices-namedcomponent-id>`__
        - Last Update `see <https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.core.database.lastupdate?view=analysisservices-dotnet#microsoft-analysisservices-core-database-lastupdate>`__

        Returns
        -------
        DataFrame
            Pandas DataFrame listing databases and their attributes.
        """  # noqa: E501
        databases = []

        # Alternative implementation using REST API
        # + returns the most updated dataset list (using XMLA caches the TOM model)
        # + returns default datasets too
        # - these might not work with XMLA client
        # - less metadata

        # REST displays most up-to-date list of datasets, but the discover/read operations in XMLA
        # are cached at the time of initialization and may not know about recently added/deleted datasets.
        # We are choosing XMLA to maintain consistency between what the user sees with list_datasets and
        # read_table operations.

        # for item in self._rest_api.get_workspace_datasets(self.get_workspace_id()):
        #     databases.append({
        #         'Dataset ID': item['id'],
        #         'Dataset Name': item['name'],
        #         'CreatedDate': datetime.datetime.strptime(item['createdDate'], "%Y-%m-%dT%H:%M:%S.%fZ"),
        #     })

        # TODO: figure out how to refresh list of TOM databases without re-establishing the connection (costly)
        for item in self.get_connection().Databases:
            # PowerBI is known to throw exceptions on individual attributes e.g. due to Vertipaq load failure
            # Careful with adding additional attributes here, can take a long time to load
            # e.g. EstimatedSize & CompatibilityLevel can be very slow
            try:
                databases.append({'Dataset Name': item.Name,
                                  'Dataset ID': item.ID,
                                  'Created Timestamp': self._get_xmla_datetime_utc(item.CreatedTimestamp),
                                  'Last Update': self._get_xmla_datetime_utc(item.LastUpdate)})
            except Exception as ex:
                databases.append({'Dataset Name': item.Name, 'Error': str(ex)})

        return pd.DataFrame(databases)

    def get_dataset(self, dataset: Union[str, UUID]):
        """
        Get PowerBI dataset for a given dataset_name.

        The dataset is derived from
        `Microsoft.AnalysisServices.Tabular.Database <https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.database?view=analysisservices-dotnet>>`_

        Parameters
        ----------
        dataset : str or UUID
            Dataset name UUID object containing the dataset ID.

        Returns
        -------
        Dataset
            PowerBI Dataset represented as TOM Database object.
        """
        client = self.get_dataset_client(dataset)

        for item in self.get_connection().Databases:
            if item.Name == client._dataset_name:
                return item

        # Executing the following is very unlikely, because an exception should have
        # occured during dataset resolution. The only conceivable way is if the dataset
        # got deleted before we retrieved the list with self.get_connection().Databases.
        raise DatasetNotFoundException(str(dataset), self.get_workspace_name())

    def get_tmsl(self, dataset: Union[str, UUID]) -> str:
        """
        Retrieve the TMSL for a given dataset.

        Parameters
        ----------
        dataset : str or UUID
            Name or UUID of the dataset to list the measures for.

        Returns
        -------
        str
            TMSL for the given dataset.
        """
        tabular_database = self.get_dataset(dataset)

        import Microsoft.AnalysisServices.Tabular as TOM

        return TOM.JsonSerializer.SerializeDatabase(tabular_database)

    def list_measures(self, dataset: Union[str, UUID]) -> pd.DataFrame:
        """
        Retrieve all measures associated with the given dataset.

        Each measure is derived from
        `Microsoft.AnalysisServices.Tabular.Measure <https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure?view=analysisservices-dotnet>`__

        Parameters
        ----------
        dataset : str or UUID
            Name or UUID of the dataset to list the measures for.

        Returns
        -------
        DataFrame
            Pandas DataFrame listing measures and their attributes.
        """
        client = self.get_dataset_client(dataset)

        measures = []
        database = self.get_dataset(client._dataset_name)
        for table in database.Model.Tables:
            for measure in table.Measures:
                measure_dict = {'Table Name': table.Name,
                                'Measure Name': measure.Name,
                                'Measure Expression': measure.Expression,
                                'Measure Data Type': measure.DataType.ToString()}
                measures.append(measure_dict)
        return pd.DataFrame(measures)

    def get_dataset_client(self, dataset: Union[str, UUID], use_xmla: bool = False) -> Union[DatasetRestClient, DatasetXmlaClient]:
        """
        Get PowerBIClient for a given dataset name or GUID.

        The same cached reusable instance is returned for each dataset.

        Parameters
        ----------
        dataset : str or UUID
            Dataset name or UUID object containing the dataset ID.
        use_xmla : bool, default=False
            Whether or not to use XMLA as the backend for the client.
            If there are any issues using the default Client, make this argument True.

        Returns
        -------
        DatasetRestClient or DatasetXmlaClient
            Client facilitating data retrieval from a specified dataset.
        """
        ClientClass = DatasetXmlaClient if use_xmla else DatasetRestClient
        return self._cached_dataset_client(dataset, ClientClass)

    def _is_internal(self, table) -> bool:
        if table.IsPrivate:
            return True
        # annotations = list(table.Annotations)
        for annotation in table.Annotations:
            if annotation.Name == "__PBI_LocalDateTable":
                return True
        return False

    def _get_xmla_datetime_utc(self, xmla_datetime) -> datetime.datetime:
        utc_dt_str = xmla_datetime.ToUniversalTime().ToString()
        return datetime.datetime.strptime(utc_dt_str, "%m/%d/%Y %H:%M:%S")

    def __repr__(self):
        return f"PowerBIWorkspace('{self.get_workspace_name()}')"
