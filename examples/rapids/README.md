# GPU data science with RAPIDS

<img src="https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/rapids.png" width="400">

This project provides the basics for using [RAPIDS](https://rapids.ai/) on Saturn Cloud. The project is set to have a workspace server with a GPU, and three workers in a Dask cluster, each with their own GPU. Here are some example notebooks that walk through using a GPU with RAPIDS, scaling to a cluster with Dask, then some runtime comparisons:

## [Use RAPIDS on a single GPU](01-rapids-gpu.ipynb)

This notebook gives an example of how to load data and train a random forest model on a GPU using RAPIDS.

## [Use RAPIDS on multiple GPUs in parallel with Dask](02-rapids-dask.ipynb)

By using RAPIDS with a Dask cluster, you can load data that does not fit into a single GPU's memory, as well as parallelize model training across multiple machines.

## [Compare RAPIDS with Dask to Scikit-learn](compare/README.md)

Once you're familiar with RAPIDS, check out the [compare](compare/README.md) folder for complete examples of a classification exercise with NYC Taxi data. Those notebooks compare the runtime of a CPU-based pipeline with a GPU-based one to illustrate the massive speedups you can get with RAPIDS and Dask together.
