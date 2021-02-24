# PyTorch Quickstart

This project provides the basics for using PyTorch on Saturn Cloud. The project is set to have a workspace server with GPU, and three workers in a Dask cluster, each with their own GPU. Here are some examples notebooks that walk through using a GPU with PyTorch, using Dask, then using Dask and PyTorch together across multiple workers:



## [Use Pytorch on a single GPU](01-start-with-pytorch.ipynb)

This workbook gives an example of how to train a PyTorch neural network with a GPU by training a LSTM to generate pet names.

## [Start running code in parallel with Dask](02-start-with-dask.ipynb)

This workbook shows a basic example of how you can parallelize abitrary code with a Dask cluster. The example takes a list of inputs and a function to use on each item in the list, then sends each of the operations to the Dask cluster.

## [Use Pytorch to train across multiple GPUs in parallel with Dask](03-start-with-pytorch+dask.ipynb)

By combining Pytorch with Dask you can train a neural network over many different GPUs at once. This example uses the same pet names example as the single-GPU notebook, but instead uses the three GPUs of the dask workers to train the model.