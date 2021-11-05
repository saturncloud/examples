import json
import os
import sys

REF = sys.argv[1]


for file in os.listdir("examples"):
    recipe_path = os.path.join("examples", file, ".saturn/saturn.json")

    with open(recipe_path) as f:
        recipe = json.load(f)
        for repo_dict in recipe["git_repositories"]:
            repo_dict["reference"] = REF

    with open(recipe_path, "w") as f:
        f.write(json.dumps(recipe, indent=2))
