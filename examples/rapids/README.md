# GPU data science with RAPIDS

<img src="https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/rapids.png" width="400">

[RAPIDS](https://rapids.ai/) is a collection of libraries that enable you to take advantage of NVIDIA GPUs to accelerate machine learning workflows. Minimal changes are required to transition from familiar pandas and scikit-learn to GPU accelerated code! For more information on RAPIDS, see ["Getting Started"](https://rapids.ai/start.html) in the RAPIDS docs.

## About This Resource
This resource provides the basics for using RAPIDS on Saturn Cloud. The resource is set to have a workspace server with a GPU, and three workers in a Dask cluster, each with their own GPU. Here are some example notebooks that walk through using a GPU with RAPIDS and scaling to a cluster with Dask:

## [Use RAPIDS on a single GPU](01-rapids-single-gpu.ipynb)

This notebook gives an example of how to load data and train a random forest model on a GPU using RAPIDS.

## [Use RAPIDS on multiple GPUs in parallel with Dask](02-rapids-gpu-cluster.ipynb)

By using RAPIDS with a Dask cluster, you can parallelize model training across multiple machines or load data that does not fit into a single GPU's memory.
