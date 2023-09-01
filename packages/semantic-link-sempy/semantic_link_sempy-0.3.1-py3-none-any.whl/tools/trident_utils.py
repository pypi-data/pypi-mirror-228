from urllib.parse import quote
from re import search
import requests


env_cred = {
    "edog": "AzTest@TridentCSTEdog.ccsctp.net",
    "daily": "AdminUser@TridentCSTDaily.onmicrosoft.com",
    "dxt": "AdminUser@TridentCSTDXT.onmicrosoft.com",
    "msit": "AdminUser@TridentCSTMSIT.onmicrosoft.com",
    "westus3": "AdminUser@TridentCSTProdWestUS3.onmicrosoft.com",
}

env_endpoint = {
    "edog": "biazure-int-edog-redirect.analysis-df.windows.net",
    "daily": "wabi-daily-us-east2-redirect.analysis.windows.net",
    "dxt": "wabi-staging-us-east-redirect.analysis.windows.net",
    "msit": "df-msit-scus-redirect.analysis.windows.net",
    "westus3": "wabi-west-us3-a-primary-redirect.analysis.windows.net",
}

env_capacity_id = {
    "edog": "B9040312-3894-400D-9051-D6107A1994D7",
    "daily": "CC03C367-FF3C-47BC-99C7-5356B14FAEA3",
    "dxt": "C367C00F-C102-4847-8A32-9663E07E03E6",
    "msit": "C488C5CC-681D-4453-A953-F967FA17A5D3",
    "westus3": "DD39D0B5-1583-4F1C-9C4B-A2A2B56E1432",
}

env_user_id = {
    "edog": "b9c26e50-6ae0-409f-b4b8-1a4dc41fdb74",
    "daily": "3cf83ccc-40b7-418a-b807-1c02bbbb0a9f",
    "dxt": "c5390f94-f4e3-452c-880d-54c4bf96e2f3",
    "msit": "dc5922b4-acb2-4bdb-9cf7-9a139035b04d"
}

env_onelake = {
    "edog": "onelakeedog.pbidedicated.windows-int.net",
    "daily": "daily-onelake.pbidedicated.windows.net",
    "dxt": "dxt-onelake.pbidedicated.windows.net",
    "msit": "msit-onelake.pbidedicated.windows.net",
    "westus3": "onelake.pbidedicated.windows.net",
}


class AADCredential:
    def __init__(self, token, **kwargs):
        self.token = token

    def get_token(self, *scopes, **kwargs):
        return self.token


def get_bearer_token(env, username, password, audience="pbi"):
    if audience != "pbi" and audience != "storage":
        raise ValueError("Only pbi and storage audiences are supported.")

    # XMLA client id
    client_id = "cf710c6e-dfcc-4fa8-a093-d47294e44c66"
    user, tenant = username.split('@')

    if env == 'edog':
        resource = "https://analysis.windows-int.net/powerbi/api"
        authority = "login.windows-ppe.net"
    else:
        resource = "https://analysis.windows.net/powerbi/api" if audience == "pbi" else "https://storage.azure.com"
        authority = "login.windows.net"

    login_url = f"https://{authority}/{tenant}/oauth2/token"
    payload = f'resource={quote(resource, safe="")}&client_id={client_id}&grant_type=password&username={username}&password={quote(password, safe="")}&scope=openid'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'fpc=AlqdPsBZ3IhEkuEX2q3BHxjyrCATAQAAAAFta9sOAAAALbyONgEAAAAZbWvbDgAAAA; stsservicecookie=estsppe'
    }
    response = requests.request("GET", login_url, headers=headers, data=payload).json()
    try:
        token_type = response["token_type"]
    except Exception as e:
        print(f"Bad response: {response}")
        raise e

    if token_type != "Bearer":
        raise ValueError("The token received is not a bearer.")

    return response["access_token"]


def print_test_ntbk_output(response):
    cells = _get_ntbk_cells(response)

    fail_count = 0
    for cell in cells:
        if cell['cell_type'] != 'code':
            continue
        outputs = cell["outputs"]
        for output in outputs:
            if output["output_type"] == "stream":
                print(output["text"])

                fail_match = search(r"\d+ failed", output["text"])
                if fail_match:
                    match_str = fail_match.group()
                    fail_count += int(search(r"\d+", match_str).group())

                error_match = search(r"\d+ error", output["text"])
                if error_match:
                    match_str = error_match.group()
                    fail_count += int(search(r"\d+", match_str).group())

    if fail_count > 0:
        raise RuntimeError(f"There were {fail_count} test failures.")


def print_ntbk_output(response):
    cells = _get_ntbk_cells(response)

    for cell in cells:
        if cell['cell_type'] != 'code':
            continue
        print(cell['source'])
        outputs = cell["outputs"]
        for output in outputs:
            if 'data' in output:
                data = output['data']
                if 'application/vnd.livy.statement-meta+json' not in data:
                    print(output['data']['text/plain'])
            if 'text' in output:
                print(output['text'])
        print()


def _get_ntbk_cells(response):
    result = response["result"]
    if result["runStatus"] != "Succeeded":
        print(result["error"])
        raise ValueError("Notebook run didn't succeed.")

    return result["snapshot"]["notebookContent"]["properties"]["cells"]
