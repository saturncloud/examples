# Example projects

These are the quickstart projects available in Saturn cloud. Each project has a set of files to include on workspace machine when the project is started, as well as parameters for how the workspace should be set up. The parameters include the number of machines for a Dask cluster, if any, the size of the machines, and a start script to run when they are first turn on. If you would like to use code from one of these projects, select the quickstart options from within Saturn Cloud.

In addition to be used as quickstarts, many of the [Saturn Cloud docs](http://saturncloud.io/docs) pull directly from these notebooks. The docs pull in the notebooks using a manually run script [`make_md.py`](https://github.com/saturncloud/docs/blob/main/make_md.py) from the [docs repo](https://github.com/saturncloud/docs).

**Note: this repo includes the existing legacy `examples-cpu` and `examples-gpu`. This is for compatibility with existing enterprise customers, and will be deprecated in the future**

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
    "thumbnail_image_url": "https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-thumbnails/dashboard.png",
    "weight": 10
}
```

It's possible that other files might existing in the .saturn folder, such as `script` which contains the initialization script for the project. However, no file besides `saturn.json` is required.

Notes about the project structure:
* The disk_space must be one of the preset choices from the Saturn Cloud UI, it can't be an arbitrary amount of disk space.
* The startup script must be name `start` without a file extension for Atlas to know it.
* Options like "environmental_variables" may be required even if they are empty, be aware there is a risk in removing them entirely.

## Flat files

If your quickstart involves flat files they should be saved in the saturn cloud public S3 (ask @hhuuggoo for permission to access this). Each quickstart's file should be saved in the `examples` folder in the bucket in a subfolder with the same name as the quickstart folder in this repo. In your code, use the HTTP path to download the file rather than a Python S3 package, since not all of the readers will have an understanding of S3. For example in Pandas you can run:

```python
pd.read_csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/pickup_grouped_by_zone.csv")
```


## Example thumbnail

Each example needs a thumbnail to show in the ui. The thumbnails should be 500px*250px images. They should be saved in the s3 bucket `saturn-public-assets` in the `example-thumbnails` folder with a name that matches the name of the example. So for the `dashboard` example the url would be: `https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-thumbnails/dashboard.png`