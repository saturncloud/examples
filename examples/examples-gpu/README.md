<img src="./_img/saturn.png" width="600">

# Saturn Cloud Examples (GPU)

If you're new to Saturn Cloud, [see how to get started here](https://www.saturncloud.io/docs/getting-started/).

Once you've done that, click one of the links below to open a notebook and try an example.

**Data Exploration and Machine Learning**

1. Train a Random Forest Model
    - [single-machine, CPU (scikit-learn)](./nyc-taxi/rf-scikit.ipynb)
    - [single-machine, GPU (RAPIDS)](./nyc-taxi/rf-rapids.ipynb)
    - [multi-machine, GPU (Dask + RAPIDS)](./nyc-taxi/rf-rapids-dask.ipynb)

<hr>

### Running in a new project

These examples are configured to run with small data sizes to quickly (and cost-effectively) illustrate the features of Saturn Cloud. If you prefer to run these examples in a new project, or would like to modify the code and run with larger data sizes and clusters, you can clone the repo by opening a new Terminal within the JupyterLab of your project, then copying the example you want into the `/home/jovyan/project` folder:

```bash
git clone https://github.com/saturncloud/examples.git /tmp/examples
cp -r /tmp/examples/examples/examples-gpu /home/jovyan/project/
```

## NYC Taxi

An end-to-end data science pipeline comprising data ingest, exploratory analysis, machine learning model training, and deploying models and a dashboard. The `examples-cpu` project contains most of the examples, but these are GPU examples for machine learning with RAPIDS.

*You will learn:*
- How to train a tree-based machine learning model on a GPU using RAPIDS
- How to train the same model on a cluster of GPU machines using RAPIDS with Dask
