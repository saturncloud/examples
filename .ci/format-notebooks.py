import json
import os


def _replace_whitespace(notebook_file: str) -> None:
    """
    Given a path to a notebook, read in its contents.
    Replace trailing whitespace in any code cells, then
    write the new notebook content back to the original file.

    :param notebook_file: An absolute path to a Jupyter notebook.
    """
    with open(notebook_file, "r") as f:
        notebook_dict = json.loads(f.read())

    cells = notebook_dict.copy()["cells"]
    for i, cell in enumerate(notebook_dict["cells"]):
        if cell["cell_type"] == "code":
            cleaned_code_lines = []
            for code_line in cell["source"]:
                if code_line == "\n":
                    cleaned_code_lines.append(code_line)
                elif code_line.endswith("\n") and not code_line.startswith("\n"):
                    cleaned_code_lines.append(code_line.rstrip() + "\n")
                else:
                    cleaned_code_lines.append(code_line.rstrip())
            cells[i]["source"] = cleaned_code_lines

    notebook_dict["cells"] = cells
    with open(notebook_file, "w") as f:
        f.write(json.dumps(notebook_dict, indent=1) + "\n")


def _format_all_notebooks(directory: str) -> None:
    """
    Given a directory, find all Jupyter notebook
    files in it and all it's subdirectories, and
    replace any trailing whitespace in code cells.

    :param directory: An absolute path to a directory.
    """
    for fname in os.listdir(directory):
        full_path = os.path.join(directory, fname)
        if os.path.isdir(full_path):
            _format_all_notebooks(full_path)
        else:
            if full_path.endswith(".ipynb") and "ipynb_checkpoints" not in full_path:
                print("  * " + full_path.replace(os.getcwd() + "/", ""))
                _replace_whitespace(full_path)


if __name__ == "__main__":
    print("fixing whitespace issues in notebooks")
    _format_all_notebooks(os.getcwd())
    print("done fixing whitespace")
