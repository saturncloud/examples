# Examples
Public facing examples for populating Saturn Cloud installations

## Structure

Each project that will be included in Saturn Cloud installations will be in its own directory under the examples directory.

These projects should include all the information needed to run them from within Saturn including:

 - resource requirements (jupyter server instance size, memory)
 - project settings (image name, start script, env vars)
 - project files (python scripts, notebooks, markdown...)

This will look something like this:

```text
examples/
├── examples-cpu
│   ├── nyc-taxi
│   │   ├── dashboard
│   │   │   └── dashboard.ipynb
│   │   ├── machine-learning
│   │   │   ├── hyperparameter-dask.ipynb
│   │   │   ├── hyperparameter-scikit.ipynb
│   │   │   ├── .ipynb_checkpoints
│   │   │   │   └── xgboost-dask-checkpoint.ipynb
│   │   │   ├── random-forest-scikit.ipynb
│   │   │   ├── xgboost-dask.ipynb
│   │   │   └── xgboost.ipynb
│   │   └── README.md
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
    │   ├── machine-learning
    │   │   ├── random-forest-rapids.ipynb
    │   │   └── xgboost-rapids.ipynb
    │   └── README.md
    ├── README.md
    └── .saturn
        ├── saturn.json
        └── start
```

NOTE: this was generated with `tree -a examples/`.
