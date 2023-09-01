import json
import os
import requests
import sys
import time

from azure.storage.blob import BlobServiceClient
from datetime import datetime
from glob import glob
from tools.trident_utils import (
    env_cred,
    env_endpoint,
    env_capacity_id,
    env_onelake,
    get_bearer_token,
    print_ntbk_output,
    print_test_ntbk_output,
)
from uuid import uuid4


def upload_whl_to_storage(conn_str, runner_type):
    os.system("python setup.py bdist_wheel")
    whls = glob("dist/*.whl")
    if len(whls) > 1:
        raise RuntimeError("There is more than 1 whl in your dist dir. Delete the dir and try again.")

    whl_path = whls[0]
    whl_name = whl_path.split('/')[-1]

    # impute runner_type into whl to prevent race condition between runner pipelines
    whl_name = whl_name.replace('-py3', f'.{runner_type}-py3')
    os.rename(whl_path, f'dist/{whl_name}')
    whl_path = f'dist/{whl_name}'

    client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = client.get_blob_client(container="dist", blob=whl_name)

    with open(file=whl_path, mode="rb") as whl:
        blob_client.upload_blob(whl, overwrite=True)

    os.system("rm -rf dist")

    print(f"Wheel Name: {whl_name}")

    return whl_name, blob_client


def authenticate(username, password, env):
    if username != env_cred[env]:
        raise ValueError(f"Only {env_cred[env]} is supported for {env} environment.")

    return get_bearer_token(env, username, password)


def create_workspace(endpointwl, bearer_token, username, capacity_id, user_id, workspace_name=None):
    user, tenant = username.split('@')
    url = f"https://{endpointwl}/metadata/folders"

    if workspace_name is None:
        workspace_name = f"Sempy_WS_{uuid4()}"
        print("Workspace name: ", workspace_name)

    payload = json.dumps({
        "displayName": workspace_name,
        "capacityObjectId": capacity_id,
        "isServiceApp": False,
        "contacts": [
            {
                "displayName": f"{user} (Owner)",
                "userPrincipalName": username,
                "objectId": user_id,
                "emailAddress": username,
                "objectType": 1,
                "isSecurityGroup": False
            }
        ],
        "datasetStorageMode": 1,
        "domainObjectId": ""
        })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        workspace_id = response.json()["objectId"]
        print(f"Workspace {workspace_id} is created.")
    else:
        raise ConnectionError(f"Workspace creation failed. Response {response.status_code}: {response.reason}, {response.text}")

    return workspace_id


def import_notebook(ntbk_path, whl_name, workspace_id, lakehouse_name, lakehouse_id, endpointwl, onelake, storage_token, commit_id):
    print(f"Start import of {ntbk_path}")
    ntbk_json = _impute_whl(ntbk_path, whl_name)

    # impute lakehouse metadata
    ntbk_json["metadata"]["trident"] = {
            "lakehouse": {
                "default_lakehouse": lakehouse_id,
                "known_lakehouses": [
                    {
                        "id": lakehouse_id
                    }
                ],
                "default_lakehouse_name": lakehouse_name,
                "default_lakehouse_workspace_id": workspace_id
            }
        }

    if ntbk_path == "tests/UnitTestRunner.ipynb":
        from sempy.fabric._client._utils import upload_to_lakehouse
        upload_to_lakehouse("tests", workspace_id, lakehouse_id, onelake, storage_token)
        upload_to_lakehouse("tools", workspace_id, lakehouse_id, onelake, storage_token)
        upload_to_lakehouse("pytest.ini", workspace_id, lakehouse_id, onelake, storage_token)

    url = f"https://{endpointwl}/metadata/workspaces/{workspace_id}/artifacts"

    ntbk = ntbk_path.split('/')[-1].split('.')[0]
    ntbk_name = f"{ntbk}_{commit_id}"

    payload = json.dumps({
        "artifactType": "SynapseNotebook",
        "description": "New notebook",
        "displayName": ntbk_name,
        "workloadPayload": json.dumps(ntbk_json),
        "payloadContentType": "InlinePlainText"
        })

    headers = {
        'Authorization': f'Bearer {pbi_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        pass
    if response.status_code == 409:
        print("Notebook already exists. Using existing one.")
    else:
        print(f"Bad response {response.status_code}: {response.text}")

    attempts = 0
    sleep_factor = 1.5
    while attempts < 10:
        response = requests.request("GET", url, headers=headers, data=payload).json()
        ntbk_prov = response[-1]
        prov_state = ntbk_prov["provisionState"]
        if prov_state == "Active":
            notebook_id = ntbk_prov["objectId"]
            break
        print(f"Notebook Provision State: {prov_state}")
        time.sleep(sleep_factor ** attempts)
        attempts += 1

    if attempts == 10:
        raise TimeoutError("Notebook upload to workspace timed out.")

    print(f"Finish import of {ntbk_path}")

    return notebook_id


def create_lakehouse(workspace_id, endpointwl, bearer_token, runner_type, commit_id):
    lh_name = f"Lakehouse_{runner_type}_{commit_id}"
    print(f"Start creation of lakehouse {lh_name}")

    url = f"https://{endpointwl}/metadata/workspaces/{workspace_id}/artifacts"

    payload = json.dumps({
        "artifactType": "Lakehouse",
        "displayName": lh_name
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        lakehouse_id = response.json()["objectId"]
        print(f"Lakehouse id: {lakehouse_id}")
    elif response.json()["error"]["code"] == "PowerBIMetadataArtifactDisplayNameInUseException":
        print("Lakehouse already created, rerun of ntbk_workflow tool. Continuing execution...")

        payload = json.dumps({"supportedTypes": ["Lakehouse"],
                              "tridentSupportedTypes": ["Lakehouse"],
                              "pageNumber": 1,
                              "pageSize": 10000,
                              "filters": [],
                              "orderDirection": ""})

        url = f"https://{endpointwl}/metadata/datahub/V2/artifacts"
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            for lakehouse in response.json():
                if lakehouse["displayName"] == lh_name:
                    lakehouse_id = lakehouse["artifactObjectId"]

                    return lh_name, lakehouse_id
        else:
            raise ConnectionError(f"Lakehouse lookup failed. Response {response.status_code}: {response.json()}")

    else:
        raise ConnectionError(f"Lakehouse creation failed. Response {response.status_code}: {response.json()}")

    print(f"Finish creation of lakehouse {lh_name}")

    return lh_name, lakehouse_id


def delete_artifact(artifact_id, endpointwl, bearer_token):
    print(f"Start delete of artifact {artifact_id}")

    url = f"https://{endpointwl}/metadata/artifacts/{artifact_id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Artifact {artifact_id} failed to delete. Response: {response.json()}")

    print(f"Artifact {artifact_id} is now deleted.")


def delete_workspace(workspace_id, endpointwl, bearer_token):
    url = f"https://{endpointwl}/metadata/folders/{workspace_id}"

    payload = json.dumps({})

    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    if response.status_code != 204:
        raise ConnectionError(f"Workspace {workspace_id} failed to delete. Response: {response.json()}")

    print(f"Workspace {workspace_id} is now deleted.")


def run_notebook(notebook_id, workspace_id, endpointwl, bearer_token, capacity_id):
    # Submit run notebook request
    url = f"https://{endpointwl}/metadata/artifacts/{notebook_id}/jobs/RunNotebook"
    payload = json.dumps({})
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=5)

    if response.status_code == 202:
        print("Run Notebook request accepted.")
    else:
        raise ConnectionError(f"Run notebook request was not accepted. Response: {response.json()}")

    run_id = response.json()["artifactJobInstanceId"]

    # Get MWC Token
    url = f"https://{endpointwl}/metadata/v201606/generatemwctoken"
    payload = json.dumps({
        "capacityObjectId": f"{capacity_id}",
        "workspaceObjectId": f"{workspace_id}",
        "workloadType": "Notebook",
        "artifactObjectIds": [
            f"{notebook_id}"
        ]
    })
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        print("MWC Token Found")
    else:
        raise ConnectionError(f"Error in getting MWC Token. Response: {response.json()}")

    mwc_token = response.json()["Token"]
    target_uri_host = response.json()["TargetUriHost"]

    # Query Status of Notebook
    url = f"https://{target_uri_host}/webapi/capacities/{capacity_id}/workloads/Notebook/Data/Direct/api/workspaces/{workspace_id}/artifacts/{notebook_id}/snapshot/{run_id}"
    payload = json.dumps({})
    headers = {
        'Authorization': f'mwctoken {mwc_token}'
    }

    start_time = time.time()
    print(f"Start Time: {start_time}")
    exec_secs_max = 3600
    timeout = start_time + exec_secs_max
    while True:
        if time.time() > timeout:
            raise TimeoutError(f"Notebook didn't complete within {exec_secs_max} seconds. Terminating run.")

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200 and response.status_code != 404:
            raise ConnectionError(f"Unable to query status of notebook. Response: {response.json()}")

        if "Notebook execution is completed." in response.text:
            print(f"Notebook completed in {time.time() - start_time} seconds.")
            break
        print(response.text)
        time.sleep(10)

    return response.json()


def _impute_whl(ntbk_path, whl_name):
    ntbk_json = json.load(open(ntbk_path))

    if whl_name is not None:
        pip_cell = {
            "cell_type": "code",
            "metadata": {},
            "outputs": [],
            "execution_count": None,
            "source": ["import pip\n", f"pip.main(['install', 'https://enyaprodstorage.blob.core.windows.net/dist/{whl_name}'])"]
        }

        ntbk_json["cells"].insert(2, pip_cell)

    return ntbk_json


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python tools/ntbk_workflow.py <env> <runner_type> <workspace> <username> <password> <storage account key>")
        sys.exit()

    env = sys.argv[1]

    runner_type = sys.argv[2]
    if runner_type != "notebooks" and runner_type != "unit_test":
        raise ValueError("<runner_type> must be 'notebooks' or 'unit_test'.")

    workspace_id = sys.argv[3]
    username = sys.argv[4]
    password = sys.argv[5]
    storage_key = sys.argv[6]

    conn_str = f"DefaultEndpointsProtocol=https;AccountName=enyaprodstorage;AccountKey={storage_key};EndpointSuffix=core.windows.net"
    whl, whl_blob_client = upload_whl_to_storage(conn_str, runner_type)

    if runner_type == 'notebooks':
        ntbks = [
            "docs/source/notebooks/synapse/powerbi_dependencies.ipynb",
            "docs/source/notebooks/synapse/powerbi_relationships.ipynb",
            "docs/source/notebooks/synapse/powerbi_measures.ipynb",
        ]
        storage_token = None
    else:
        ntbks = ["tests/UnitTestRunner.ipynb"]
        storage_token = get_bearer_token(env, username, password, audience="storage")

    pbi_token = authenticate(username, password, env)

    if workspace_id == "ci_workspace":
        # Default workspaces, which are named "(DONT DELETE) SemPy CI" in all envs
        workspace_map = {
            "edog": "d2f3f034-edd3-4040-a559-2bcc93f1bb68",
            "daily": "17453554-6060-47ce-9334-db34450ca211",
            "dxt": "56df6b2e-37fd-40de-86a8-9e1a97e27724",
            "msit": "180ef180-92c9-4a80-b270-ac80aa180553",
            "westus3": "e49568dc-d3c8-428f-8458-e6811dd63a5f",
        }
        workspace_id = workspace_map[env]

    run_id = datetime.now().strftime("%Y_%m_%dT%H_%M_%S")

    lakehouse_name, lakehouse_id = create_lakehouse(workspace_id, env_endpoint[env], pbi_token, runner_type, run_id)

    for nb in ntbks:
        print(f"Starting notebook run for {nb}")
        ntbk_id = import_notebook(nb, whl, workspace_id, lakehouse_name, lakehouse_id, env_endpoint[env], env_onelake[env], storage_token, run_id)
        response_json = run_notebook(ntbk_id, workspace_id, env_endpoint[env], pbi_token, env_capacity_id[env])
        if runner_type == "unit_test":
            print_test_ntbk_output(response_json)
        else:
            print_ntbk_output(response_json)
        delete_artifact(ntbk_id, env_endpoint[env], pbi_token)
        print(f"Finished notebook run for {nb}")

    delete_artifact(lakehouse_id, env_endpoint[env], pbi_token)

    whl_blob_client.delete_blob()
