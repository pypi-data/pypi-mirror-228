"""
 Take Ownership: https://learn.microsoft.com/en-us/rest/api/power-bi/reports/take-over-in-group
"""
import typing as t
from pathlib import Path
from urllib.parse import urljoin

import requests
from azure.identity import (  # ClientSecretCredential,; InteractiveBrowserCredential,
    DefaultAzureCredential,
)

SCOPE = "https://analysis.windows.net/powerbi/api/.default"


class PowerBIClient:
    base_url = "https://api.powerbi.com/v1.0/myorg/ "

    def __init__(self):
        # TODO: if client_id, tenant_id, client_secret provided, use ClientSecretCredential
        # By default: AAD
        self.token = self.get_token()

    @staticmethod
    def get_token():
        # TODO: check "authentification" method in config: oauth / browser / service principal
        # TODO: check ig azure-cli is available, if not use InteractiveBrowser
        # azure-cli installed (brew install ...)
        # `az login --allow-no-subscriptions` -- or see the option with scope in parameters
        credentials = DefaultAzureCredential()
        access_token = credentials.get_token(SCOPE)
        token = access_token.token
        return token

    def dump_token(self, path: t.Union[str, Path] = "."):
        token_path = Path(path) / "PBIToken.json"

        token_sub_string = '{{"PBIToken":"{0}"}}'.format(self.token)
        token_str = "accessToken='{0}';".format(token_sub_string)

        with open(token_path, "w", encoding="utf8") as token_file:
            token_file.write(token_str)

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def get(self, endpoint, params: t.Optional[dict] = None):
        url = urljoin(self.base_url, endpoint)
        return requests.get(url, params=params, headers=self.headers)

    def get_workspaces(self):
        # TODO: create dataclass to load json
        endpoint = "groups"
        res = self.get(endpoint)
        return res.json()["value"]

    def get_workspace_id(self, workspace_name: str):
        workspaces = self.get_workspaces()
        try:
            return next(
                workspace["id"]
                for workspace in workspaces
                if workspace["name"] == workspace_name
            )
        except StopIteration:
            return None

    def get_reports(self, workspace_id: str) -> dict:
        # TODO: create dataclass to load json
        endpoint = f"groups/{workspace_id}/reports"
        res = self.get(endpoint)
        return res.json()["value"]

    def get_report(self, workspace_id: str, report_name: str) -> dict:
        reports = self.get_reports(workspace_id)
        return next(report for report in reports if report["name"] == report_name)

    def get_report_id(self, workspace_id: str, report_name: str) -> str:
        report = self.get_report(workspace_id, report_name)
        return report["id"]

    def get_pages(self, workspace_id: str, report_id: str) -> list:
        endpoint = f"/groups/{workspace_id}/reports/{report_id}/pages"
        print(endpoint)
        res = self.get(endpoint)
        print(res)
        return res.json()["value"]

    def get_page(self, workspace_id: str, report_id: str, page_page: str) -> dict:
        pages = self.get_pages(workspace_id, report_id)
        return next(page for page in pages if page["displayName"] == page_page)

    # https://learn.microsoft.com/en-us/rest/api/power-bi/reports/get-pages-in-group
