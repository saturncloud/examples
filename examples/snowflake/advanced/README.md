|<img src="../_img/taxi.png" width="200" /> | <img src="../_img/saturn.png" width="400" />| <img src="../_img/snowflake.png" width="400" />|
| -- | -- | -- |

# NYC Taxi analysis with Saturn Cloud

The notebooks in this example showcase a data science workflow with NYC taxi data, executed on [Saturn Cloud](https://www.saturncloud.io/) with data hosted in [Snowflake](https://www.snowflake.com/). 

![snowflake-saturn](../_img/snowflake-saturn.png)

The notebooks in this example cover:

1. Train a random forest classifier using single-node Python (`scikit-learn`)
1. Accelerate random forest training on a GPU with RAPIDS (`cudf`, `cuml`)
1. Distribute the random forest training on a GPU cluster (`dask_cudf`, `cuml.dask`)

You are free to open each notebook in this example and start playing around! For a guided experience, follow the steps below.

## Connect to Snowflake

This example uses data stored in a Snowflake data warehouse that is managed by the team at Saturn Cloud. We've set up a read-only user for use in these examples. If you would like to access data stored in your own Snowflake account, you should set up [Credentials](https://www.saturncloud.io/docs/concepts/credentials/) for your account, user, and password then set the other connection information accordingly. For more details on Snowflake connection information, see ["Connecting to Snowflake"](https://docs.snowflake.com/en/user-guide/python-connector-example.html#connecting-to-snowflake) in the `snowflake-connector-python` docs.

Note that in order to update environment variables your Jupyter server will need to be stopped.

## Train ML models

### Random forest classification

The random forest notebooks are an example of GPU-acceleration for model training with [RAPIDS](http://rapids.ai/). The [`cuml` package](https://github.com/rapidsai/cuml) features an API that closely resembles scikit-learn, but does all processing on GPUs. This leads to some crazy performance speedups! What if your data doesn't fit into a single GPU's memory? That's where Dask comes in! RAPIDS has native Dask integrations to be able to run on a cluster of machines with GPUs. Buckle up, this is going to be a fun ride!

Run these notebooks in order:

1. [`rf-scikit.ipynb`](./rf-scikit.ipynb): single-node scikit version - takes a while 🙁
1. [`rf-rapids.ipynb`](./rf-rapids.ipynb): single-GPU RAPIDS version - super fast! 🤯
1. [`rf-rapids-dask.ipynb`](./rf-rapids-dask.ipynb): multi-GPU Dask+RAPIDS version - _extra_ super fast! 🤯🤯🤯

For the best experience, we recommend opening up two notebooks at a time side-by-side in JupyterLab. That way you can see which lines of code change between them (spoiler: not many!). There are a few different resources to monitor to see what's happening:

- **CPU utilization of Jupyter client** for scikit-learn example: open a new Terminal window and run `htop`. 
- **GPU utilization of Jupyter client** for RAPIDS example: open a new Terminal window and run:

    ```shell
    watch -n 1 nvidia-smi
    ```
    
- **GPU cluster utilization** for Dask+RAPIDS example: click the dashboard and GPU monitoring links provided in the notebook.

Here what this might look like in JupyterLab:

[![workspace](../_img/workspace.png)](_img/workspace.png)

And then some browser windows for Dask cluster monitoring:

[![dask](../_img/dask.png)](_img/dask.png)

# That's all folks

If you have any issue with Saturn Cloud, please email us at support@saturncloud.io. If you notice any mistakes in these notebooks or documentation, [open an issue](https://github.com/saturncloud/examples/issues) or a [a pull request](https://github.com/saturncloud/examples/pulls).

## References

- NYC taxi image by [David Hurley on Unsplash](https://unsplash.com/photos/aPlUUmO4qr8).
