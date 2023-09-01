import json
import time
import uuid

from sempy.fabric._environment import _get_synapse_endpoint, _get_environment
from sempy.fabric.exceptions import FabricHTTPException, DatasetNotFoundException, WorkspaceNotFoundException
from sempy.fabric._utils import is_valid_uuid
from sempy.fabric._token_provider import SynapseTokenProvider, TokenProvider
from sempy._utils._log import log_retry, log_rest_response, log_rest_request
from requests.adapters import HTTPAdapter, Retry
from requests.sessions import Session
from urllib.parse import quote

from typing import Any, Optional, List, Tuple, Dict


class RetryWithLogging(Retry):
    @log_retry
    def increment(self, *args, **kwargs):
        # FIXME: This is a temporary hack to avoid getting a 403 from throttling by the PowerBI public infra.
        # After exceeding 60 requests/min, the MetadataService returns a 429 error with a "Retry-After" header.
        # This header is rounded down, which means that we may retry milliseconds before the retry window is over.
        # TODO: PowerBI service team to update subsequent response to be a 429 or 423, not a 403 which is not captured by our retry policy.
        response = kwargs['response']
        if response.geturl() and "groups?" in response.geturl():
            retry_after = response.headers.get("Retry-After", 0)
            response.headers["Retry-After"] = str(int(retry_after) + 1)
        return super().increment(*args, **kwargs)


class SessionWithLogging(Session):
    @log_rest_request
    def prepare_request(self, *args, **kwargs):
        return super().prepare_request(*args, **kwargs)


class _PBIRestAPI:
    def __init__(self, token_provider: Optional[TokenProvider] = None):
        self.http = SessionWithLogging()

        @log_rest_response
        def validate_rest_response(response, *args, **kwargs):
            if response.status_code >= 400:
                raise FabricHTTPException(response)
        self.http.hooks["response"] = [validate_rest_response]
        retry_strategy = RetryWithLogging(
            total=10,
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE"],
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )
        retry_adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http.mount("https://", retry_adapter)

        self.token_provider = token_provider or SynapseTokenProvider()
        self.base_url = self._get_base_url()

    def _get_base_url(self):
        # The endpoint api.powerbi.com does not work for REST calls using the "pbi" token due to limited audience
        if _get_environment() == "prod":
            headers = self._get_headers()
            return self.http.get("https://api.powerbi.com/powerbi/globalservice/v201606/clusterdetails", headers=headers).json()["clusterUrl"] + "/"
        else:
            return _get_synapse_endpoint()

    def _get_headers(self) -> dict:
        # this could be static / a function
        correlation_id = str(uuid.uuid4())
        return {'authorization': f'Bearer {self.token_provider()}', 'Accept': 'application/json', 'ActivityId': correlation_id}

    def get_workspace_id_from_name(self, workspace_name: str) -> Optional[str]:
        url = f"{self.base_url}v1.0/myorg/groups?$filter=name eq '{workspace_name}'"
        response = self.http.get(url, headers=self._get_headers())

        value = response.json()['value']
        if len(value) == 0:
            return None
        else:
            return value[0]['id']

    def get_workspace_name_from_id(self, workspace_id: str) -> str:
        # We got shot in the foot by an empty string, which retrieves all workspaces
        # and results in unexpected format of the response, so validate:
        if not is_valid_uuid(workspace_id):
            raise ValueError(f"Invalid UUID '{workspace_id}' in \"workspace_id\"")

        url = f"{self.base_url}v1.0/myorg/groups/{workspace_id}"

        try:
            response = self.http.get(url, headers=self._get_headers())
            return response.json()['name']
        except FabricHTTPException as e:
            if e.status_code == 401:
                if "Calling group APIs not permitted for personal workspace" in e.error_text:
                    return "My workspace"
                else:
                    # If the GUID is does not exist, PBI REST returns "Unauthorized", which goes
                    # against more common practice of 404 "Not found". It's debatable which
                    # way we should be aligning.
                    raise WorkspaceNotFoundException(workspace_id)
            else:
                raise

    def get_workspace_datasets(self, workspace_id: Optional[str] = None):
        if workspace_id:
            url = self.base_url + f"v1.0/myorg/groups/{workspace_id}/datasets"
        else:
            # retrieving datasets from "My workspace" (does not have a group GUID) requires a different query
            url = self.base_url + "v1.0/myorg/datasets"
        res = self.http.get(url, headers=self._get_headers())
        return res.json()["value"]

    def get_dataset_name_from_id(self, dataset_id: str, workspace_name: str) -> str:
        url = self.base_url + f"v1.0/myorg/datasets/{dataset_id}"
        try:
            res = self.http.get(url, headers=self._get_headers())
        except FabricHTTPException as e:
            if e.status_code == 404:
                raise DatasetNotFoundException(dataset_id, workspace_name)
            else:
                raise
        return res.json()["name"]

    def get_dataset_id_from_name(self, dataset_name: str, workspace_name: str) -> str:
        if workspace_name == "My workspace":
            datasets = self.get_workspace_datasets()
        else:
            workspace_id = self.get_workspace_id_from_name(workspace_name)
            datasets = self.get_workspace_datasets(workspace_id)
        for item in datasets:
            if item["name"] == dataset_name:
                return item["id"]
        raise DatasetNotFoundException(dataset_name, str(workspace_name))

    def get_dataset_model_id(self, dataset_id: str):
        url = self.base_url + f"metadata/gallery/SharedDatasets/{dataset_id}"
        res = self.http.get(url, headers=self._get_headers())
        return res.json()['modelId']

    def get_dataset_schema_entitites(self, dataset_id: str):
        dataset_model_id = self.get_dataset_model_id(dataset_id)
        url = self.base_url + "explore/conceptualschema"
        payload = {
            "modelIds": [dataset_model_id],
            "userPreferredLocale": "en-US"
        }
        res = self.http.post(url, json=payload, headers=self._get_headers())
        return res.json()["schemas"][0]["schema"]["Entities"]

    def execute_dax_query(self, dataset_id: str, query: str):
        url = self.base_url + f"v1.0/myorg/datasets/{dataset_id}/executeQueries"
        payload = {
            "queries": [{
                "query": f"{query}"
            }]
        }
        res = self.http.post(url, json=payload, headers=self._get_headers())
        return res.json()["results"][0]["tables"][0]["rows"]

    def calculate_measure(
        self,
        dataset_id: str,
        measure: List[Dict[str, str]],
        groupby_columns: List[Dict[str, str]],
        filters: List[Dict[str, list]],
        num_rows: Optional[int],
        verbose: int
    ) -> Tuple[List[dict], List[list]]:

        # The REST API returns empty results as an error saying "Query evaluation produced no result".
        # We want to return an empty dataframe in this case to match XMLA output.
        # TODO: PBI team should not be throwing an error for empty results (flagging for follow-up)
        try:
            res = self._retrieve_measure(dataset_id, measure, groupby_columns, filters, num_rows, verbose)
        except FabricHTTPException as e:
            if "Query evaluation produced no result" in e.error_text:
                return [], []
            else:
                raise e

        rows = res["rows"]
        columns = res["columns"]

        while "continuationToken" in res:
            cont_token = res["continuationToken"]
            res = self._retrieve_measure(dataset_id, measure, groupby_columns, filters, num_rows, verbose, cont_token=cont_token)
            rows.extend(res["rows"])

        return columns, rows

    def _retrieve_measure(
        self,
        dataset_id: str,
        measure_obj: List[Dict[str, str]],
        groupby_columns_obj: List[Dict[str, str]],
        filter_obj: List[Dict[str, list]],
        num_rows: Optional[int],
        verbose: int,
        cont_token: str = ""
    ):
        url = self.base_url + "v1.0/myOrg/internalMetrics/query"
        payload = {
            "provider": {
                "datasetId": dataset_id
            },
            "metrics": measure_obj,
            "groupBy": groupby_columns_obj,
            "filters": filter_obj,
            "paginationSettings": {
                "continuationToken": cont_token
            },
            "top": num_rows
        }

        headers = self._get_headers()
        if verbose > 0:
            print(f"Executing REST query ({headers['ActivityId']}) with payload: {json.dumps(payload, indent=2)}")
        headers["App-Name"] = "SemPy"
        res = self.http.post(url, json=payload, headers=headers)
        return res.json()

    def upload_pbix(self, dataset_name: str, pbix: bytes, workspace_id: Optional[str] = None):
        url = self.base_url + "/v1.0/myorg"

        # support My Workspace
        if workspace_id is not None:
            url += f"/groups/{workspace_id}"

        url = f"{url}/imports?datasetDisplayName={quote(dataset_name)}"
        url += "&nameConflict=CreateOrOverwrite&skipReport=true&overrideReportLabel=true&overrideModelLabel=true"

        payload: Any = {}
        files = [('', (dataset_name, pbix, 'application/octet-stream'))]

        headers = self._get_headers()
        response = self.http.post(url, headers=headers, data=payload, files=files)

        if response.status_code != 202:
            raise Exception(f"Importing of '{dataset_name}' not accepted. Response code: {response.status_code}")

        attempts = 0
        sleep_factor = 1.5
        while attempts < 10:
            response = self.http.get(url, headers=headers, data=payload, files=files)
            if response.status_code == 200:
                time.sleep(30)
                break
            time.sleep(sleep_factor ** attempts)
            attempts += 1

        if attempts == 10:
            raise TimeoutError("Dataset upload to workspace timed out.")
