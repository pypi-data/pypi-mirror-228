"""Module providingFunction utilities for the runner."""
import json
from io import StringIO
from typing import List

from google.protobuf.json_format import MessageToDict

from core.bp_metadata_utils.blueprint_meta_data import BlueprintMetaData
from models.shared.shared_pb2 import Finding
import logging


def verify_config_arguments(args_obj) -> dict:
    """
    Verifies if the obligatory attributes are available
    """
    caller_logs = {"org_id": [],
                   "project_id": [],
                   "api_key": [],
                   "blueprint_package_path": []}

    if "org_id" not in args_obj:
        caller_logs["org_id"].append(
            "Required argument missing from configuration file")
    elif args_obj["org_id"] == "":
        caller_logs["org_id"].append(
            "Required value missing or left blank in configuration file")

    if "project_id" not in args_obj:
        caller_logs["project_id"].append(
            "Required argument missing from configuration file")
    elif args_obj["project_id"] == "":
        caller_logs["project_id"].append(
            "Required value missing or left blank in configuration file")

    if "api_key" not in args_obj:
        caller_logs["api_key"].append(
            "Required argument missing from configuration file")
    elif args_obj["api_key"] == "":
        caller_logs["api_key"].append(
            "Required value missing or left blank in configuration file")

    if "blueprint_package_path" not in args_obj:
        caller_logs["blueprint_package_path"].append(
            "Required argument missing from configuration file")
    elif args_obj["blueprint_package_path"] == "":
        caller_logs["blueprint_package_path"].append(
            "Required value missing or left blank in configuration file")

    return caller_logs


def persist_runner_output(args_path: str, runner_stdout: StringIO, blueprint_problems: List[str], blueprint_metadata: List[BlueprintMetaData], findings: List[Finding]) -> None:
    """
    Consolidate and persists runners output data
    """

    if not args_path:
        return

    stdout_text = runner_stdout.getvalue()
    stdout_lines = stdout_text.splitlines()
    findings_json_list = []
    blueprint_metadata_json_list = []

    if findings:
        for finding in findings:
            if finding:
                findings_json_list.append(MessageToDict(finding))

    if blueprint_metadata:
        for metadata in blueprint_metadata:
            if metadata:
                blueprint_metadata_json_list.append(metadata.__json__())

    output = {
        "blueprint_metadata": blueprint_metadata_json_list,
        "blueprint_output": stdout_lines,
        "blueprint_problems": blueprint_problems,
        "findings": findings_json_list
    }

    file_path = args_path.replace("input", "output")

    with open(file_path, "w") as f:
        json.dump(output, f, indent=4)
