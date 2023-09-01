import json
import webbrowser
from datetime import datetime
from pathlib import Path
from shutil import copy

from .config import load_config
from .pbi import PowerBIClient
from .scraping import driver, filename, filepath

dirname = datetime.now().strftime("%Y%m%d-%H%M%S")
project_dir = Path(dirname)
project_dir.mkdir()

pbi_client = PowerBIClient()

pbi_client.dump_token(path=project_dir)

config = load_config()

workspace_name = config["workspace"]
print(workspace_name)
report_name = config["report"]
print(report_name)
page_name = config.get("pageName", "")
print(page_name)
think_time_seconds = config.get("thinkTimeSeconds", 5)

# Get Workspace
workspace_id = pbi_client.get_workspace_id(workspace_name)

if not workspace_id:
    raise Exception

print(f"Workspace ID: {workspace_id}")

# Get Report
report = pbi_client.get_report(workspace_id, report_name)
report_url = report["embedUrl"]
report_id = report["id"]

print(f"Report ID: {report_id}")

# Get Page
page = pbi_client.get_page(workspace_id, report_id, page_name)
page_id = page["name"]

print(f"Page ID: {page_id}")


# Fitlers
filters = config["filters"]

report_path = Path(project_dir) / "PBIReport.json"

report_dict = {
    "reportUrl": report_url,
    "pageName": page_id,
    # "bookmarkList": bookmarks,
    "sessionRestart": 100,
    "filters": filters,
    "thinkTimeSeconds": think_time_seconds,
}

report_parameter_str = json.dumps(report_dict)

report_str = "reportParameters={0};".format(report_parameter_str)

with open(report_path, "w", encoding="utf8") as report_file:
    report_file.write(report_str)

project_filepath = (Path(dirname) / filename).absolute()

copy(filepath, str(project_filepath))

fileurl = f"file:///{project_filepath}"

# webbrowser.open(fileurl)

# driver.get(fileurl)
