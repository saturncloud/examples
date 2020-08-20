# contributing

This document describes how to contribute to `saturncloud/examples`.

When you add a new example, add an entry to [`CODEOWNERS`](./.github/CODEOWNERS) to be sure you'll be added as a reviewer on future updates to it.

## `examples/` Directory Structure

Examples in this the `examples/` directory follow a specific directory structure that allows Saturn to automatically seed them in a new user's environment with these.

Each directory below `examples/` corresponds to one new Saturn Project + Jupyter that will be created in users' environments. Those projects will be named using the directory name, so the names of these directories should have names which only contain lowercase alphanumeric characters and dashes.

```text
examples/
├── examples-cpu
│   ├── nyc-taxi
│   │   ├── dashboard.ipynb
│   │   ├── hyperparameter-dask.ipynb
│   │   ├── hyperparameter-scikit.ipynb
│   │   ├── random-forest-scikit.ipynb
│   │   ├── README.md
│   │   ├── xgboost-dask.ipynb
│   │   └── xgboost.ipynb
│   ├── prefect
│   │   ├── flow.png
│   │   ├── prefect-scheduled-scoring.ipynb
│   │   └── README.md
│   ├── README.md
│   └── .saturn
│       ├── saturn.json
│       └── start
└── examples-gpu
    ├── nyc-taxi
    │   ├── random-forest-rapids.ipynb
    │   ├── README.md
    │   └── xgboost-rapids.ipynb
    ├── README.md
    └── .saturn
        ├── saturn.json
        └── start
```

NOTE: this was generated with `tree -a examples/`.

### The `README.md`

Each folder exactly one and two levels below `examples/` should have a `README.md`. This should contain relevant information for understanding the example, such as:

* description of any manual steps needed to use the code (like configuring credentials)
* links to reference material like blogs posts or data dictionaries

So, for example, in the directory structure above, `examples-cpu/README.md` is required, `examples-cpu/prefect/README.md` is required, but `examples-cpu/prefect/some-other-directory/README.md` would not be required.

### The `.saturn` Directory

Each example must contain a special directory called `.saturn`. This contains the details needed for Saturn to create the necessary resources for the example. This can contain the following files, and any other files will be ignored.

* [`.saturn/saturn.json`](#saturn-json)
* [`.saturn/start`](#start-script)

#### `.saturn/saturn.json` <a name="saturn-json"></a>

A JSON with the following structure:

```json
{
    "image": "saturncloud/saturn:2020.07.08.1",
    "jupyter": {
        "size": "8xlarge",
        "disk_space": "256Gi",
        "ssh_enabled": false
    },
    "environment_variables": {
        "TAXI_S3": "s3://saturn-titan/nyc-taxi"
    }
}
```

* `image`: the name of an image to use for the Jupyter server and all Dask clusters
* `jupyter`: customization specific to the jupyter server, including:
    - `size`: A valid size for a Saturn instance
    - `disk_space`: An amount of disk space, in units `Gi`. See the "Disk Space" dropdown on the "Jupyter" page in the Saturn UI for valid values.
    - `ssh_enabled`: A boolean indicating whether to set up [SSH access from outside Saturn into the Server](https://www.saturncloud.io/docs/connecting/tools/ssh/)
* `environment_variables`:
    - A dictionary whose keys are the names of environment variables, and whose values are the values for the environment variables.

Any customization of Dask clusters should be done in notebook code, using [`dask-saturn`](https://github.com/saturncloud/dask-saturn).

#### `.saturn/start` <a name="start-script"></a>

A shell script that will be run on startup of the Jupyter server and all Dask resources. This should contain code that runs quickly, like `pip install`-ing libraries.

## Adding or Updating Examples

All changes to this repository are required to go through pull requests. Create a new branch, commit your changes, and [submit a pull request](https://github.com/saturncloud/examples/compare).

When your pull request is opened, a set of automated checks will run to check that your code conforms with the structure described in ["Example Directory Structure"](#example-directory-structure).

## Frequently Asked Questions

#### Can I include other code or add more sub-directories under and example in the `examples/` directory?

All other directories included under the example directory will be included in the example, and an arbitrary amount of nesting is permitted.

#### What do I do if my example needs a customer image?

All images referenced in an example's `.saturn/saturn.json` should be publicly available on Docker Hub. This project does not handle building new images.

If you need a new image, you can make a pull request in https://github.com/saturncloud/images to add it.
