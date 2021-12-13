# Saturn Cloud Default Resources

[![link checks](https://github.com/saturncloud/examples/workflows/link%20checks/badge.svg?branch=main)](https://github.com/saturncloud/examples/actions/workflows/check-links.yml)

These are the Saturn Cloud Examples most of which are used to create default template resources on every Saturn Cloud installation (this behavior can be turned on or off by Saturn Cloud admins).

Each example has a [recipe](https://github.com/saturncloud/recipes) that describes how the resource should be setup as well as files (notebooks, markdown, python scripts) that contain the actual example content.
If you would like to explore these examples, select one of the template resources from the resources page of Saturn Cloud or view the examples in the [Saturn Cloud docs](https://saturncloud.io/docs/examples).

The [Saturn Cloud docs](https://saturncloud.io/docs/examples) pull directly from these notebooks. The docs pull in the notebooks using a manually run script [`make_md.py`](https://github.com/saturncloud/website/blob/main/make_md.py) from the [website repo](https://github.com/saturncloud/website/).

## Templates structure

In the section above we say _most_ of the examples become default templates. This is because there is a special doc that specifies which examples are templates and how those get configured. That doc is `.saturn/templates.json`

Notes about templates:

* CI will check that the thumbnail_image_url exists, so you need to upload the thumbnail for it to pass.
* Every template needs to have a unique weight

## Resource structure

Each resource is a separate dir within the `examples` folder. For each resource there is one subdir called `.saturn` which contains the information specific to the Saturn Cloud resource.

The most important file within the `.saturn` folder is the `saturn.json` file which is a resource recipe. Here is an example of a `saturn.json` file:

```json
{
  "name": "pytorch",
  "image_uri": "saturncloud/saturn-pytorch:2021.11.10",
  "description": "Use PyTorch with a single GPU or across multiple GPUs with Dask",
  "working_directory": "/home/jovyan/git-repos/examples/examples/pytorch",
  "extra_packages": {
    "pip": "torch dask-pytorch-ddp seaborn"
  },
  "git_repositories": [
    {
      "url": "https://github.com/saturncloud/examples"
    }
  ],
  "jupyter_server": {
    "disk_space": "10Gi",
    "instance_type": "g4dnxlarge",
  },
  "dask_cluster": {
    "num_workers": 3,
    "worker": {
      "instance_type": "g4dnxlarge",
    },
    "scheduler": {
      "instance_type": "large"
    }
  }
}
```

It's possible that other files might existing in the .saturn folder, such as `start` which might be referenced from the recipe and contain the start_script for the resource. However, no file besides `saturn.json` is required.

Notes about recipes:

* The disk_space must be one of the preset choices from the Saturn Cloud UI, it can't be an arbitrary amount of disk space.
* You can reference a start script in a separate file by including a start script like `bash .saturn/start`. Note that the path is relative to the `working_directory`.

## Data files

If your example involves data files they should be saved in the Saturn Cloud public S3 (ask @hhuuggoo for permission to access this). Each data file should be saved in the `examples` folder in the bucket in a subfolder with the same name as the example folder in this repo. In your code, use the HTTP path to download the file rather than a Python S3 package, since not all of the readers will have an understanding of S3. For example in Pandas you can run:

```python
pd.read_csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/pickup_grouped_by_zone.csv")
```

## Dask cluster

If your example needs a Dask cluster, make sure you specify both the number of workers in the `saturn.json` file and also within the notebooks themselves to correctly use wait for workers. If you have to change the number of workers in the example make sure you change it in both places.

Example chunk in a notebook, where n_workers is the same value as the `saturn.json` one:

```python
n_workers = 3
cluster = SaturnCluster(n_workers=n_workers)
client = Client(cluster)
client.wait_for_workers(n_workers)
```

## Example thumbnail

Each example needs a thumbnail to show in the ui. The thumbnails should be 500px*250px images. They should be saved in the s3 bucket `saturn-public-assets` in the `example-thumbnails` folder with a name that matches the name of the example. So for the `dashboard` example the url would be: `https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-thumbnails/dashboard.png`
