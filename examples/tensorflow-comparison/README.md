# Compare Training of Single GPU and Multi-GPU TensorFlow

These examples are the code that supports the Saturn Cloud [Multi-GPU TensorFlow blog post](https://saturncloud.io/blog/tensorflow_intro/).

**Included Notebooks:**

* Train a TensorFlow model with a [single GPU](comparison-training-singlenode.ipynb).
* Train a TensorFlow model with [multiple GPUs on a single machine](comparison-training-multigpu.ipynb).

## Notes

* TensorFlow GPU training runs do not release memory upon concluding. These will use all or nearly all GPU memory available. You can restart the Saturn Cloud resource if need to release the memory.
* Weights & Biases is used to monitor the examples. To use it, either set the environment variable `WANDB_LOGIN` as a Saturn Cloud credential, or set it manually within the notebooks.

