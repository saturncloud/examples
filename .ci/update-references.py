from ensurepip import version
import json
import os
import sys

REF = sys.argv[1] if len(sys.argv) == 2 else None
VERSION = REF.replace("release-","") if REF else None


for file in os.listdir("examples"):
    recipe_path = os.path.join("examples", file, ".saturn/saturn.json")

    with open(recipe_path) as f:
        recipe = json.load(f)
        for repo_dict in recipe["git_repositories"]:
            if REF:
                repo_dict["reference"] = REF
            else:
                repo_dict.pop("reference", None)
        if VERSION:
            recipe["version"] = VERSION
        else:
            recipe.pop("version")

    with open(recipe_path, "w") as f:
        f.write(json.dumps(recipe, indent=2) + "\n")
