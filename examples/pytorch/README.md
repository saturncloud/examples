# PyTorch Quickstart

This resource provides the basics for using PyTorch on Saturn Cloud. The resource is set to have a workspace server with GPU, and three workers in a Dask cluster, each with their own GPU. Here are some examples notebooks that walk through using a GPU with PyTorch, using Dask, then using Dask and PyTorch together across multiple workers:

## [Use Pytorch on a single GPU](01-start-with-pytorch.ipynb)

This workbook gives an example of how to train a PyTorch neural network with a GPU by training a LSTM to generate pet names.

## [Start running code in parallel with Dask](02-start-with-dask.ipynb)

This workbook shows a basic example of how you can parallelize abitrary code with a Dask cluster. The example takes a list of inputs and a function to use on each item in the list, then sends each of the operations to the Dask cluster.

## [Use Pytorch to train many different models across multiple GPUs in parallel](03-start-with-pytorch+dask-multiple-models.ipynb)

By combining Pytorch with Dask you can run experiments on how a model performs with different parameters by quickly testing them across multiple machines. This example takes the same pet names code from the single GPU and sets up an experiment to try adjusting the parameters and running on different GPUs concurrently.

## [Use Pytorch to train a single model across multiple GPUs in parallel with Dask](04-start-with-pytorch+dask-single-model.ipynb)

By combining Pytorch with Dask you can train a single neural network over many different GPUs at once. This example uses the same pet names example as the single-GPU notebook, but instead uses the three GPUs of the Dask workers to train the model.