# Comparing training of singlenode and Multi-GPU Tensorflow.
These are the examples which were given in [this](https://saturncloud.io/blog/tensorflow_intro/) blogpost.

## Current Scripts

* Training single node (slowish): `training_singlenode.ipynb`
* Training multi-gpu single machine (fast): `training_multigpu.ipynb`

## Things to Watch For

* Tensorflow GPU training runs (at least) do not release memory upon concluding. These will use all or nearly all GPU memory available.
* I've used Weights and Biases throughout this code to monitor GPU performance - if running this, user should set their own Saturn env credential for wandb.

