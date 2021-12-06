# Use Weights & Biases on Saturn Cloud

This project provides examples showing how to use  <a href="https://wandb.ai/"  target='_blank' rel='noopener'>Weights & Biases</a> in Saturn Cloud to monitor 
the training and performance of your machine learning models. We have included single-node 
training of an image classifier, as well as a multi-node example that lets you see how nicely 
Weights & Biases can integrate with distributed training on Dask clusters. 

## [Train image classifier on single node (PyTorch)](train-pytorch-singlenode.ipynb)

In this notebook, you'll train an image classifier with PyTorch and use Weights & Biases to
 monitor model performance.

## [Train image classifier on cluster (PyTorch)](train-pytorch-cluster.ipynb)

This notebook expands upon the image classifier training task, using a Dask cluster to accelerate
 the same task. Weights & Biases is still able to easily and clearly provide model performance monitoring.

## How to Use Weights & Biases

To run these examples on Saturn Cloud, please follow these instructions you'll need your Weights & Biases account credentials in Saturn Cloud.
Open the Credentials tab in the left side of the Saturn Cloud menu, and [add your Weights & Biases user token as an Environment Variable](https://www.saturncloud.io/docs/getting-started/credentials/). Name it `WANDB_LOGIN`. (This is the [same token you would use if you logged in to Weights & Biases](https://docs.wandb.ai/ref/cli/wandb-login) at the command line.)
