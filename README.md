# Examples
Public facing examples for populating Saturn Cloud installations

## Structure

Each project that will be included in Saturn Cloud installations will be in its own directory under the examples directory.

These projects should include all the information needed to run them from within Saturn including:

 - resource requirements (jupyter server instance size, memory)
 - project settings (image name, start script, env vars)
 - project files (python scripts, notebooks, markdown...)

This will look something like:

```
.
├── examples
│   ├── taxi-cpu
│   │   ├── dashboard
│   │   │   └── dashboard.ipynb
│   │   ├── eda
│   │   ├── etl
│   │   │   └── data-loading.ipynb
│   │   └── saturn
│   │       ├── image
│   │       │   ├── environment.yaml
│   │       │   └── postBuild
│   │       └── start
│   └── taxi-gpu
│       ├── dashboard
│       │   └── dashboard.ipynb
│       ├── eda
│       ├── etl
│       │   └── data-loading.ipynb
│       └── saturn
│           ├── image
│           │   ├── environment.yaml
│           │   └── postBuild
│           └── start
└── README.md
