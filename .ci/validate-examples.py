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
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--examples-dir", type=str, help="Path to the 'examples' directory to check")
ARGS = parser.parse_args()
DIRECTORY_REGEX = r"^[0-9a-z\-]+$"
FILENAME_REGEX = r"^[0-9a-z\-\.]+$"
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

        notebook_files = [f for f in all_files if f.endswith(".ipynb")]
        if len(notebook_files) == 0:
            msg = f"No notebooks were found in '{full_dir}' or its subdirectories"

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
                    "lower alphanumeric characters, dashes, and periods. "
                    f"'{fname}` violates this rule."
                )
            if not matches_name_pattern:
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
        else:
            with open(saturn_json, "r") as f:
                saturn_config = json.loads(f.read())

            for required_key in SATURN_JSON_KEYS:
                if required_key not in saturn_config.keys():
                    msg = f"'{saturn_json}' missing required key: '{required_key}'"
                    ERRORS.add(msg)

            project_image = saturn_config["image"]

    ERRORS.report()

# https://ops.tips/blog/inspecting-docker-image-without-pull/
# image=saturncloud/saturn:2020d.07.08.1

# curl \
#     --silent \
#     "https://auth.docker.io/token?scope=repository:$image:pull&service=registry.docker.io" \
#     | jq -r '.token'

# curl \
#     --silent \
#     --header "Accept: application/vnd.docker.distribution.manifest.v2+json" \
#     --header "Authorization: Bearer $token" \
#     "https://registry-1.docker.io/v2/$image/manifests/$tag" \
#     | jq -r '.config.digest'

# import requests

# image="saturncloud/saturn:2020.07.08.1"
# res = requests.get(
#     f"https://auth.docker.io/token?scope=repository:saturncloud/saturn:pull&service=registry.docker.io"
# )
# token = res.json()["token"]

# res = requests.get(
#     url=f"https://registry-1.docker.io/v2/saturncloud/saturn/manifests/2020.07.08.1",
#     headers={
#         "Accept": "application/vnd.docker.distribution.manifest.v2+json",
#         "Authorization": f"Bearer {token}"
#     }
# )
