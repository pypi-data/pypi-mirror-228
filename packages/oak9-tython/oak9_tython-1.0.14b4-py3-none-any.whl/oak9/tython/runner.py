import argparse
import json
import os
import sys
from io import StringIO
from typing import Protocol, runtime_checkable, Set, Optional, List
from core.services.tython_api_service import TythonApiService
from core.bp_metadata_utils.customer_blueprint_repo import CustomerBlueprintRepo
from core.bp_metadata_utils.python_source_file_utils import get_blueprint_classes
from core.types import Finding, Configuration
import core.utilities as Utilities


@runtime_checkable
class SupportsValidation(Protocol):
    def validate(self) -> Set[Finding]:
        """
        Entry point into component's validation logic
        """


class Runner:

    @staticmethod
    def run(validation_target: SupportsValidation):
        return validation_target.validate()


def main(argv):
    parser = argparse.ArgumentParser(description="Runner Script")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debugging mode")
    parser.add_argument("config_file", help="Path to configuration JSON file")
    args = parser.parse_args()

    # Enable debugging
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    stdout = sys.stdout
    sys.stdout = runner_stdout = StringIO()

    args_path = args.config_file
    if not os.path.exists(args_path):
        raise Exception(f"Configuration file {args_path} not found.")

    findings = list()
    blueprint_metadata_list = []
    blueprint_problems = []

    try:
        config = None

        args_file = open(args_path)
        args_obj = json.load(args_file)
        args_file.close()
        verify_config_logs = Utilities.verify_config_arguments(args_obj)

        if any(verify_config_logs.values()):
            error_messages = "\n".join([f"{key}: {', '.join(values)}" for key, values in verify_config_logs.items() if values])
            raise Exception(f"Invalid config arguments. Please verify your configuration file:\n{error_messages}")

        config = Configuration(**args_obj)
        runner = Runner()
        blueprint_repo = CustomerBlueprintRepo(config.blueprint_package_path)

        try:
            blueprint_metadata_list = blueprint_repo.blueprints
        except:
            blueprint_problems.append(
                "Docstring formatting does not meet specification. Update your blueprint docstrings for a more helpful summary of your blueprint")
            blueprint_metadata_list = []

        # Failing here if the config details are botched
        tython_api_service = TythonApiService(config)
        env_id = args_obj.get('env_id', None)
        if env_id is None or env_id == '':
            tython_api_service.config.env_id = tython_api_service.get_default_environment()

        request_id = tython_api_service.build_app()
        runner_inputs = tython_api_service.fetch_graph_data(request_id)

        if not runner_inputs:
            logging.info("No graph data to validate. Ensure the project you are attempting to "
                         "validate contains resources")

        # get all blueprint classes
        blueprint_classes = []
        for blueprint_file_path in blueprint_repo.blueprint_file_paths:
            blueprint_classes.extend(
                get_blueprint_classes(blueprint_file_path))

        # Run each blueprint
        for blueprint in blueprint_classes:
            customer_blueprint = blueprint[1](graph=runner_inputs)
            # TODO: check usage guidelines to see if findings should be reported
            try:
                blueprint_findings = runner.run(customer_blueprint)
                findings.extend(blueprint_findings)
            except Exception as e:
                blueprint_problems.append(str(e))

        if config.mode == "apply" and findings:
            tython_api_service.apply_findings(findings, request_id)
        elif config.mode == "apply" and not findings:
            logging.debug("No findings found for this validation.")

        sys.exit(0)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        sys.exit(1)

    finally:
        try:
            Utilities.persist_runner_output(
                args_path, runner_stdout, blueprint_problems, blueprint_metadata_list, list(findings))
            logging.info("Runner output saved successfully.")
        except Exception as e:
            logging.error(
                f"An error occurred while saving runner output: {str(e)}")
        finally:
            sys.stdout = stdout


if __package__ == "":
    # Resulting path is the name of the wheel itself
    path = os.path.dirname(__file__)
    sys.path.insert(0, path)

if __name__ == "__main__":
    main(sys.argv[1:])
