# RAPIDS Quickstart

![rapids](tbd)

This project provides the basics for using [RAPIDS](https://rapids.ai/) on Saturn Cloud. The project is set to have a workspace server with GPU, and three workers in a Dask cluster, each with their own GPU. Here are some examples notebooks that walk through using a GPU with RAPIDS, using Dask, then using Dask and RAPIDS together across multiple workers:

## [Use RAPIDS on a single GPU](01-rapids-gpu.ipynb)

This notebook gives an example of how to load data and train a random forest model on a GPU using RAPIDS.

## [Use RAPIDS on multiple GPUs in parallel with Dask](02-rapids-dask.ipynb)

By using RAPIDS with a Dask cluster, you can load data that does not fit into a single GPU's memory, as well as parallelize model training across multiple machines.
