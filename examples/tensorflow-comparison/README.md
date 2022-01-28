# Comparing training of singlenode and Multi-GPU Tensorflow.
These are the examples which were given in [this](https://saturncloud.io/blog/tensorflow_intro/) blogpost.

## Current Scripts

* Training the [single node](comparison-training-singlenode.ipynb)
* Training [multi-gpu single machine](comparison-training-multigpu.ipynb) 

## Things to Watch For

* Tensorflow GPU training runs (at least) do not release memory upon concluding. These will use all or nearly all GPU memory available.
* I've used Weights and Biases throughout this code to monitor GPU performance - if running this, user should set their own Saturn env credential for wandb.

