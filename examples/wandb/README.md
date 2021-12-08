# Use Weights & Biases on Saturn Cloud

This project provides examples showing how to use  <a href="https://wandb.ai/"  target='_blank' rel='noopener'>Weights & Biases</a> in Saturn Cloud to monitor 
the training and performance of your machine learning models. This resource contains two examples:

* [Weights & Biases on a single machine](wandb.ipynb) -- This notebook uses Weights & Biases monitoring training of an PyTorch image classifier
* [Weights & Biases on a Dask cluster](wandb-dask.ipynb) -- This notebook shows the same PyTorch image classifier, but now monitoring it across a Dask cluster.

## Set up Weights & Biases

**This step is required to run these examples.**

Open the Credentials tab in the left side of the Saturn Cloud menu, and create a new environment variable named `WANDB_LOGIN` for your [Weights & Biases user token](https://www.saturncloud.io/docs/getting-started/credentials/).
