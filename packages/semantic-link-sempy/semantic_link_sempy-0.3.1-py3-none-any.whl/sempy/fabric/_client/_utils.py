import os
import sys
from pathlib import Path
from typing import Union, Optional, Callable
from uuid import UUID


import requests
from azure.core.credentials import AccessToken
from azure.storage.blob import BlobServiceClient

from sempy.fabric._environment import _get_pbi_uri
from sempy.fabric._client._rest_api import _PBIRestAPI
import sempy.fabric as fabric


def _download_pbix(dataset,
                   storage_account="https://mmlspark.blob.core.windows.net/",
                   container="publicwasb") -> bytes:
    service = BlobServiceClient(account_url=storage_account, credential=None)

    # download azure blob using blob service client in service
    blob_client = service.get_blob_client(container, blob=f"SemPy/pbi_data/{dataset}.pbix")
    return blob_client.download_blob().readall()


def import_pbix_sample(dataset: str, workspace: Optional[Union[str, UUID]] = None):
    """
    Import sample .pbix file to the workspace.

    Parameters
    ----------
    dataset : str
        Name of the dataset.
    workspace_id : str
        PowerBI Workspace Name or UUID object containing the workspace ID.
    """
    import_pbix(dataset,
                lambda: _download_pbix(dataset),
                workspace)


def import_pbix_from_http(dataset_name: str, pbix_url: str, workspace: Optional[Union[str, UUID]] = None):
    """
    Import .pbix file from http(s) to the workspace.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset.
    pbix_url : str
        URL to the .pbix file.
    workspace_id : str
        PowerBI Workspace Name or UUID object containing the workspace ID.
    """
    import_pbix(dataset_name,
                lambda: requests.get(pbix_url).content,
                workspace)


def import_pbix(dataset_name: str, file_download: Callable[[], bytes], workspace: Optional[Union[str, UUID]] = None):
    """
    Import .pbix file to the workspace.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset.
    file_download : Callable[[], bytes]
        A callback to retrieve the .pbix file content. The callback should return the .pbix file content as bytes.
        It is only called when the dataset is not found in the workspace.
    workspace_id : str
        PowerBI Workspace Name or UUID object containing the workspace ID.
    """

    workspace_id = fabric.resolve_workspace_id(workspace)
    if workspace_id is not None:
        workspace_id = str(workspace_id)

    # query dataset
    rest = _PBIRestAPI()
    existing_datasets = rest.get_workspace_datasets(workspace_id)

    # check if dataset w/o extension is already exists
    if dataset_name in [row["name"] for row in existing_datasets]:
        print(f"Dataset '{dataset_name}' already in the workspace '{workspace}' ({workspace_id})")
        return

    rest.upload_pbix(dataset_name, file_download(), workspace_id)


def _get_workspace_url(workspace: str) -> str:
    url = f"{_get_pbi_uri()}v1.0/myorg/"
    if workspace == "My workspace":
        return url
    else:
        return f"{url}{workspace}"


def _init_analysis_services() -> None:
    from clr_loader import get_coreclr
    from pythonnet import set_runtime

    my_path = Path(__file__).parent

    rt = get_coreclr(runtime_config=os.fspath(my_path / ".." / ".." / "dotnet.runtime.config.json"))
    set_runtime(rt)

    import clr
    assembly_path = my_path / ".." / ".." / "lib"
    sys.path.append(os.fspath(assembly_path))
    clr.AddReference(os.fspath(assembly_path / "Microsoft.AnalysisServices.Tabular.dll"))
    clr.AddReference(os.fspath(assembly_path / "Microsoft.AnalysisServices.AdomdClient.dll"))
    clr.AddReference(os.fspath(assembly_path / "SemPyParquetWriter.dll"))


class AADCredential:
    def __init__(self, token, **kwargs):
        self.token = token

    def get_token(self, *scopes, **kwargs):
        return self.token


def upload_to_lakehouse(dir_or_file, workspace_id, lakehouse_id, onelake_url, bearer_token):
    t = AccessToken(token=bearer_token, expires_on=1684934721)
    service = BlobServiceClient(account_url=f"https://{onelake_url}", credential=AADCredential(token=t))
    container_client = service.get_container_client(workspace_id)

    path_to_remove = ""

    def upload_blob(file_path_on_local, file_path_on_azure):
        with open(file_path_on_local, "rb") as data:
            container_client.upload_blob(name=f'{lakehouse_id}/Files/{file_path_on_azure}', data=data, overwrite=True)
            # print("uploaded file ---->", file_path_on_local)

    if os.path.isfile(dir_or_file):
        upload_blob(dir_or_file, dir_or_file.replace(path_to_remove, ""))
    else:
        for root, dirs, files in os.walk(dir_or_file):
            if files:
                for file in files:
                    file_path_on_azure = os.path.join(root, file).replace(path_to_remove, "")
                    file_path_on_local = os.path.join(root, file)
                    upload_blob(file_path_on_local, file_path_on_azure)
