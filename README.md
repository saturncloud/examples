# Quickstart projects

These are the quickstart projects available in Saturn cloud. Each project has a set of files to include on workspace machine when the project is started, as well as parameters for how the workspace should be set up. The parameters include the number of machines for a Dask cluster, if any, the size of the machines, and a start script to run when they are first turn on. If you would like to use code from one of these projects, select the quickstart options from within Saturn Cloud.

## Project structure

Each project is a separate folder within the `examples` folder. For each project there is one subfolder called `.saturn` which contains the information specific to the Saturn Cloud project. Everything not within a `.saturn` folder will be available within the workspace machine of the project in Saturn Cloud.

The most important file within the `.saturn` folder is the `saturn.json` file which includes setup parameters. Here is an example of a `saturn.json` file:

```json
{
    "image": "saturncloud/saturn-pytorch:2021.02.09-3",
    "jupyter": {
        "size": "g4dnxlarge",
        "disk_space": "10Gi",
        "ssh_enabled": false
    },
    "dask_cluster": {
        "n_workers": 3,
        "scheduler_size": "medium",
        "worker_size": "g4dnxlarge"
    },
    "environment_variables": {
        "DASK_DISTRIBUTED__WORKER__DAEMON": "False"
    },
    "description": "Use Pytorch on one GPU or across multiple GPUs with Dask",
    "title": "Pytorch",
    "thumbnail_image_url": "url"
}
```

It's possible that other files might existing in the .saturn folder, such as `start_script` which contains the initialization script for the project. However, no file besides `saturn.json` is required.