import json
import subprocess
import os


with open("RECIPE_SCHEMA_VERSION", "r") as f:
    RECIPE_SCHEMA_VERSION = f.read()


cmd = "git log -n 1 --pretty=format:'%H'"
with subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
    proc.wait()
    stdout, stderr = proc.communicate()
    code = proc.returncode
    COMMIT = stdout.decode("utf-8").strip("'")
    stderr_str = stderr.decode("utf-8")

if code != 0:
    print(f"ERROR executing {cmd}")
    if stderr_str:
        raise ValueError(stderr_str)

with open(".saturn/templates.json", "r") as f:
    templates = json.load(f)

for template in templates["templates"]:
    recipe_path = template.pop("recipe_path")

    with open(recipe_path, "r") as f:
        recipe = json.load(f)

    # Add the reference commit for saturncloud/examples
    for repo_dict in recipe["git_repositories"]:
        if "saturncloud/examples" in repo_dict["url"]:
            repo_dict["reference"] = COMMIT
            repo_dict["reference_type"] = "commit"

    template["resource"] = recipe

output = json.dumps(templates, indent=2) + "\n"
filename = f"{RECIPE_SCHEMA_VERSION}-templates.json"
with open(filename, "w") as f:
    f.write(output)

print(f"Created {filename}")

# If this is running in CI, write to S3
if os.getenv("CI"):
    import boto3

    s3 = boto3.client("s3")
    with open(filename, "rb") as f:
        s3.upload_fileobj(f, "saturn-example-templates", filename)

    print(f"Uploaded {filename} to https://example-templates.saturncloud.io/{filename}")
