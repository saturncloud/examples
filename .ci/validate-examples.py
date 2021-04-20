"""
Examples in the `examples/` directory must conform
to a rigid structure, so Jupyter servers to run them can
be created automatically in Saturn.

This script validates the content of those directories,
to try to prevent pushing broken code to customer's
Saturn installations.
"""
import argparse
import glob
import json
import os
import re
import requests
import sys

from marshmallow import fields, Schema, ValidationError
from typing import List

parser = argparse.ArgumentParser()
parser.add_argument("--examples-dir", type=str, help="Path to the 'examples' directory to check")
ADMIN_DIRS = ["_img"]
ARGS = parser.parse_args()
DIRECTORY_REGEX = r"^[0-9a-z\-]+$"
FILENAME_REGEX = r"^[0-9A-Za-z\-\.]+$"
SATURN_DIR_NAME = ".saturn"
SATURN_JSON_NAME = "saturn.json"
SATURN_JSON_KEYS = [
    "image",
    "jupyter",
    "environment_variables",
    "description",
    "title",
    "thumbnail_image_url",
    "weight",
    "auto_populate_in_saturn",
]
TOP_LEVEL_DIR = ARGS.examples_dir


class ErrorCollection:

    _errors: List[str] = []

    def add(self, error: str):
        self._errors.append(error)

    @property
    def num_errors(self) -> int:
        return len(self._errors)

    def report(self) -> None:
        print("\n------ check results ------\n")
        print(f"{self.num_errors} errors found checking examples\n")
        i = 1
        for error in self._errors:
            print(f"{i}. {error}")
            i += 1
        sys.exit(self.num_errors)


class JupyterSchema(Schema):
    size = fields.String(required=True)
    disk_space = fields.String(required=True)
    ssh_enabled = fields.Boolean(required=True)


class DaskClusterSchema(Schema):
    n_workers = fields.Integer(required=False)
    scheduler_size = fields.String(required=False)
    worker_size = fields.String(required=False)
    nthreads = fields.Integer(required=False)
    nprocs = fields.Integer(required=False)
    worker_is_spot = fields.Boolean(required=False)


class SaturnJsonSchema(Schema):
    image = fields.String(required=True)
    environment_variables = fields.Mapping(required=True)
    jupyter = fields.Nested(JupyterSchema, attribute="jupyter", required=True)
    dask_cluster = fields.Nested(DaskClusterSchema, required=False)
    required_secrets = fields.List(fields.String(), required=False)
    description = fields.String(required=True)
    title = fields.String(required=True)
    thumbnail_image_url = fields.Url(required=True)
    weight = fields.Integer(required=True)
    auto_populate_in_saturn = fields.Boolean(required=True)


def image_exists_on_dockerhub(image_name: str, image_tag: str) -> bool:
    """
    Given an image name and image_tag, check if it is
    publicly-accessible on DockerHub.

    Based on the code from this blog post:
    * htttps://ops.tips/blog/inspecting-docker-image-without-pull/

    :param image_name: Name of an image, such as ``continuumio/miniconda3``
    :param image_tag: Tag for the image, such as ``4.8.2``

    :Example:

    .. code-block:: python

        # should be True
        image_exists_on_dockerhub("continuumio/miniconda3", "4.8.2")

        # should be False
        import uuid
        image_exists_on_dockerhub(str(uuid.uuid4()), "0.0.1")
    """
    url = (
        "https://auth.docker.io/token?scope=repository:"
        f"{image_name}:pull&service=registry.docker.io"
    )
    res = requests.get(url=url)
    res.raise_for_status()
    token = res.json()["token"]
    res = requests.get(
        url=f"https://registry-1.docker.io/v2/{image_name}/manifests/{image_tag}",
        headers={
            "Accept": "application/vnd.docker.distribution.manifest.v2+json",
            "Authorization": f"Bearer {token}",
        },
    )
    return res.status_code == 200


def _lint_python_cell(file_name: str, code_lines: List[str]) -> List[str]:
    """
    Given the content of a Python code cell, check it for problems we
    want to avoid.

    :param file_name: Name of the notebook this code came from. This is used
        to make error messages more informative.
    :param code_lines: List of strings, where each item in the list is one
        line of Python code.

    :return: A list of strings, where each string represents an error
        found by this check
    """
    errors = []

    # Jupyter notebooks already store literal newlines
    code_str = "".join(code_lines)

    WARNING_FILTER_REGEX = r".*warnings\.filter.*"
    if bool(re.search(WARNING_FILTER_REGEX, code_str)):
        msg = (
            f"Found use of warnings.simplefilter() or warnings.filterwarnings() in {file_name}. "
            "Do not filter out warnings in example notebooks. Try to fix them or "
            "add text explaining why they can be safely ignored."
        )
        errors.append(msg)

    DELAYED_DECORATOR_REGEX = r"@delayed"
    if bool(re.search(DELAYED_DECORATOR_REGEX, code_str)):
        msg = (
            f"Found a use of '@delayed' in {file_name}. "
            "Instead, 'import dask' and then use '@dask.delayed'."
        )
        errors.append(msg)

    return errors


if __name__ == "__main__":

    ERRORS = ErrorCollection()

    example_dirs = os.listdir(TOP_LEVEL_DIR)
    if len(example_dirs) == 0:
        ERRORS.add(f"No directories found under '{TOP_LEVEL_DIR}'")

    weights = {}

    for example_dir in example_dirs:
        print(f"Working on directory '{example_dir}'")
        full_dir = os.path.join(TOP_LEVEL_DIR, example_dir)

        if not bool(re.search(DIRECTORY_REGEX, os.path.basename(example_dir))):
            msg = (
                f"All directories under '{TOP_LEVEL_DIR}' should be named with only "
                "lower alphanumeric characters and dashes. "
                f"'{full_dir}` violates this rule."
            )
            ERRORS.add(msg)
            continue

        all_files = glob.glob(f"{full_dir}/**", recursive=True)
        if len(all_files) == 0:
            msg = f"Directory '{full_dir}' is empty"
            ERRORS.add(msg)
            continue

        first_level_dirs = glob.glob(f"{full_dir}/**", recursive=False)
        for fname in first_level_dirs:
            if os.path.isdir(fname):
                readme_file = os.path.join(fname, "README.md")
                if not os.path.isfile(readme_file):
                    msg = (
                        f"Every directory two-levels below '{TOP_LEVEL_DIR}' "
                        f"must have a README.md. None found for '{fname}'."
                    )
                    ERRORS.add(msg)

        # every example must have at least one notebook. All cells in that
        # notebook should be cleared of output and execution counts
        notebook_files = [f for f in all_files if f.endswith(".ipynb")]
        if len(notebook_files) == 0:
            msg = f"No notebooks were found in '{full_dir}' or its subdirectories"
            ERRORS.add(msg)
        else:
            for notebook_file in notebook_files:
                with open(notebook_file, "r") as f:
                    notebook_dict = json.loads(f.read())
                non_empty_cells = 0
                for cell in notebook_dict["cells"]:
                    if cell.get("outputs", []) or cell.get("execution_count", None):
                        non_empty_cells += 1
                    if cell["cell_type"] == "code":
                        linting_errors = _lint_python_cell(notebook_file, cell["source"])
                        for err in linting_errors:
                            ERRORS.add(err)
                if non_empty_cells > 0:
                    msg = (
                        f"Found {non_empty_cells} non-empty cells in '{notebook_file}'. "
                        "Clear all outputs and re-commit this file."
                    )
                    ERRORS.add(msg)

        # all files and directories should have appropriate name
        for fname in all_files:
            if os.path.isdir(fname):
                base_name = os.path.basename(os.path.normpath(fname))
                is_valid = bool(re.search(DIRECTORY_REGEX, base_name))
                msg = (
                    f"[here] All directories should be named with only "
                    "lower alphanumeric characters and dashes. "
                    f"'{fname}` violates this rule."
                )
                if base_name in ADMIN_DIRS:
                    is_valid = True
            else:
                base_name = os.path.basename(fname)
                is_valid = bool(re.search(FILENAME_REGEX, base_name))
                msg = (
                    f"All files should be named with only "
                    "alphanumeric characters, dashes, and periods. "
                    f"'{fname}` violates this rule."
                )
            if not is_valid:
                ERRORS.add(msg)

        # each example must have a README.md
        readme_file = os.path.join(full_dir, "README.md")
        if not os.path.isfile(readme_file):
            msg = f"Every example must have a README.md. '{full_dir}' does not."
            ERRORS.add(msg)

        # each example must have a .saturn/ folder
        saturn_dir = os.path.join(full_dir, SATURN_DIR_NAME)
        if not os.path.isdir(saturn_dir):
            msg = f"'{full_dir}' does not include a '{SATURN_DIR_NAME}/' directory"
            ERRORS.add(msg)

        saturn_json = os.path.join(saturn_dir, SATURN_JSON_NAME)
        if not os.path.isfile(saturn_json):
            msg = f"Did not find saturn.json in '{saturn_dir}'. This file is required."
            ERRORS.add(msg)
            continue

        with open(saturn_json, "r") as f:
            try:
                saturn_config = SaturnJsonSchema().loads(f.read())
            except ValidationError as err:
                msg = f"'{saturn_json}' has the following schema issues: {str(err.messages)}"
                ERRORS.add(msg)
                continue

        for required_key in SATURN_JSON_KEYS:
            if required_key not in saturn_config.keys():
                msg = f"'{saturn_json}' missing required key: '{required_key}'"
                ERRORS.add(msg)

        weight = saturn_config["weight"]
        matches = [key for key, value in weights.items() if weight == value]
        if matches:
            msg = f"Weight ({weight}) for {example_dir} is non-unique. It matches {matches}."
            ERRORS.add(msg)
        weights[example_dir] = weight

        project_image = saturn_config["image"]
        image_name, image_tag = project_image.split(":")
        image_exists = image_exists_on_dockerhub(image_name=image_name, image_tag=image_tag)
        if not image_exists:
            msg = (
                f"image '{image_name}:{image_tag}' is not available on Docker Hub. "
                f"Found in '{saturn_json}'"
            )
            ERRORS.add(msg)

    ERRORS.report()
