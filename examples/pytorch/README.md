# PyTorch Examples

These examples provide the basics for using PyTorch on Saturn Cloud. The resource is set to have a workspace server with GPU, and three workers in a Dask cluster, each with their own GPU. Here are some examples notebooks that walk through using a GPU with PyTorch then using Dask and PyTorch together across multiple workers:

## [Use Pytorch on a single GPU](01-pytorch-gpu.ipynb)

This workbook gives an example of how to train a PyTorch neural network with a GPU by training a LSTM to generate pet names.

## [Use Pytorch to train many different models across multiple GPUs in parallel](02-pytorch-gpu-multiple-models.ipynb)

By combining Pytorch with Dask you can run experiments on how a model performs with different parameters by quickly testing them across multiple machines. This example takes the same pet names code from the single GPU and sets up an experiment to try adjusting the parameters and running on different GPUs concurrently.

## [Use Pytorch to train a single model across multiple GPUs in parallel with Dask](03-pytorch-gpu-single-model.ipynb)

By combining Pytorch with Dask you can train a single neural network over many different GPUs at once. This example uses the same pet names example as the single-GPU notebook, but instead uses the three GPUs of the Dask workers to train the model.