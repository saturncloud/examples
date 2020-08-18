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

parser = argparse.ArgumentParser()
parser.add_argument("--examples-dir", type=str, help="Path to the 'examples' directory to check")
ARGS = parser.parse_args()
DIRECTORY_REGEX = r"^[0-9a-z\-]+$"
FILENAME_REGEX = r"^[0-9A-Za-z\-\.]+$"
SATURN_DIR_NAME = ".saturn"
SATURN_JSON_NAME = "saturn.json"
SATURN_JSON_KEYS = ["image", "jupyter", "environment_variables"]
TOP_LEVEL_DIR = ARGS.examples_dir


class ErrorCollection:

    _errors = []

    def add(self, error):
        self._errors.append(error)

    @property
    def num_errors(self):
        return len(self._errors)

    def report(self):
        print("\n------ check results ------\n")
        print(f"{self.num_errors} errors found checking examples\n")
        i = 1
        for error in self._errors:
            print(f"{i}. {error}")
            i += 1
        sys.exit(self.num_errors)


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


if __name__ == "__main__":

    ERRORS = ErrorCollection()

    example_dirs = os.listdir(TOP_LEVEL_DIR)
    if len(example_dirs) == 0:
        ERRORS.add(f"No directories found under '{TOP_LEVEL_DIR}'")

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
                matches_name_pattern = bool(re.search(DIRECTORY_REGEX, base_name))
                msg = (
                    f"[here] All directories should be named with only "
                    "lower alphanumeric characters and dashes. "
                    f"'{fname}` violates this rule."
                )
            else:
                base_name = os.path.basename(fname)
                matches_name_pattern = bool(re.search(FILENAME_REGEX, base_name))
                msg = (
                    f"All files should be named with only "
                    "alphanumeric characters, dashes, and periods. "
                    f"'{fname}` violates this rule."
                )
            if not matches_name_pattern:
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
            saturn_config = json.loads(f.read())

        for required_key in SATURN_JSON_KEYS:
            if required_key not in saturn_config.keys():
                msg = f"'{saturn_json}' missing required key: '{required_key}'"
                ERRORS.add(msg)

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
