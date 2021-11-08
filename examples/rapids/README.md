# GPU data science with RAPIDS

<img src="https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/rapids.png" width="400">

This resource provides the basics for using [RAPIDS](https://rapids.ai/) on Saturn Cloud. The resource is set to have a workspace server with a GPU, and three workers in a Dask cluster, each with their own GPU. Here are some example notebooks that walk through using a GPU with RAPIDS, scaling to a cluster with Dask, then some runtime comparisons:

## [Use RAPIDS on a single GPU](01-rapids-single-gpu.ipynb)

This notebook gives an example of how to load data and train a random forest model on a GPU using RAPIDS.

## [Use RAPIDS on multiple GPUs in parallel with Dask](02-rapids-gpu-cluster.ipynb)

By using RAPIDS with a Dask cluster, you can parallelize model training across multiple machines or load data that does not fit into a single GPU's memory.

## Next steps

Thanks for trying out this resource! To learn more about how Saturn Cloud works, check out our [Documentation](https://saturncloud.io/docs/), [blog](https://saturncloud.io/s/blog/), or join an [upcoming event](https://saturncloud.io/s/events/).

If you have any questions or suggestions reach out to us at support@saturncloud.io or open an issue on the [examples Github repo](https://github.com/saturncloud/examples).