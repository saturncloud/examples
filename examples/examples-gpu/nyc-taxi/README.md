|<img src="../_img/taxi.png" width="200" /> | <img src="../_img/saturn.png" width="400" />|
| -- | -- |

# NYC Taxi analysis with Saturn Cloud

The notebooks in this example showcase a data science workflow with NYC taxi data, executed on [Saturn Cloud](https://www.saturncloud.io/). They are a subset of a [larger demo](https://youtu.be/SgXSIbB4Hik), reduced to quickly highlight key features of Saturn Cloud. The larger demo includes the following:

<img src="../_img/pipeline.png" width="800">

All code for the full demo is [available here](https://github.com/saturncloud/saturn-cloud-examples/tree/main/taxi_demo). You can follow the instructions there to create a new project and run the full examples. The example you are currently in is a reduced version to quickly (and cost-effectively) highlight key features of Saturn Cloud.

You are currently viewing the **GPU** project for the NYC taxi examples, which covers GPU-accelerated machine learning with RAPIDS. For all other examples, go to the `examples-cpu` project. 

The notebooks in _this_ example cover:

1. Train a random forest classifier using single-node Python (`scikit-learn`)
1. Accelerate random forest training on a GPU with RAPIDS (`cudf`, `cuml`)
1. Distribute the random forest training on a GPU cluster (`dask_cudf`, `cuml.dask`)

You are free to open each notebook in this example and start playing around! For a guided experience, follow the steps below.

## Train ML models

### Random forest classification

The random forest notebooks are an example of GPU-acceleration for model training with [RAPIDS](http://rapids.ai/). The [`cuml` package](https://github.com/rapidsai/cuml) features an API that closely resembles scikit-learn, but does all processing on GPUs. This leads to some crazy performance speedups! What if your data doesn't fit into a single GPU's memory? That's where Dask comes in! RAPIDS has native Dask integrations to be able to run on a cluster of machines with GPUs. Buckle up, this is going to be a fun ride!

Run these notebooks in order:

1. [`rf-scikit.ipynb`](rf-scikit.ipynb): single-node scikit version - takes a while 🙁
1. [`rf-rapids.ipynb`](rf-rapids.ipynb): single-GPU RAPIDS version - super fast! 🤯
1. [`rf-rapids-dask.ipynb`](rf-rapids-dask.ipynb): multi-GPU Dask+RAPIDS version - _extra_ super fast! 🤯🤯🤯

For the best experience, we recommend opening up two notebooks at a time side-by-side in JupyterLab. That way you can see which lines of code change between them (spoiler: not many!). There are a few different resources to monitor to see what's happening:

- **CPU utilization of Jupyter server** for scikit-learn example: open a new Terminal window and run `htop`. 
- **GPU utilization of Jupyter server** for RAPIDS example: open a new Terminal window and run:

    ```shell
    watch -n 1 nvidia-smi
    ```
    
- **GPU cluster utilization** for Dask+RAPIDS example: click the dashboard and GPU monitoring links provided in the notebook.

Here what this might look like in JupyterLab:

[![workspace](../_img/workspace.png)](../_img/workspace.png)

And then some browser windows for Dask cluster monitoring:

[![dask](../_img/dask.png)](../_img/dask.png)

# That's all folks

Thanks for following along! We encourage you to continue to play around with these examples and use the code for your own work. There is a much [larger version of NYC taxi analysis](https://github.com/saturncloud/saturn-cloud-examples/tree/main/taxi_demo) that you can clone into a new project and see more of the power of Dask+RAPIDS on Saturn Cloud.

If you have any issue with Saturn Cloud, please email us at support@saturncloud.io. If you notice any mistakes in these notebooks or documentation, [open an issue](https://github.com/saturncloud/examples/issues) or a [a pull request](https://github.com/saturncloud/examples/pulls).

## References

- NYC taxi image by [David Hurley on Unsplash](https://unsplash.com/photos/aPlUUmO4qr8).
