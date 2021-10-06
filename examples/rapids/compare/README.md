# Comparing Scikit-learn, RAPIDS, and RAPIDS with Dask

The notebooks in this folder showcase a data science workflow with NYC taxi data, executed on Saturn Cloud. The notebooks in this example cover:

1. Train a random forest classifier using single-node Python (`scikit-learn`). This single-node version of a random forest takes a while to run.
1. Accelerate random forest training on a GPU with RAPIDS (`cudf`, `cuml`). This notebook greatly speeds up the random forest model using RAPIDS. The [`cuml` package](https://github.com/rapidsai/cuml) features an API that closely resembles scikit-learn, but does all processing on a GPU.
1. Distribute the random forest training on a GPU cluster (`dask_cudf`, `cuml.dask`). This notebook expands on the previous one by using a Dask cluster of machines with GPUs to train a model with RAPIDS. This means you can train a model on data that doesn't fit into memory of a single computer.

References:

- NYC taxi image by [David Hurley on Unsplash](https://unsplash.com/photos/aPlUUmO4qr8).
