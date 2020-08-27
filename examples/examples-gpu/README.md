![Saturn Cloud](saturn.png)

# Saturn Cloud Examples (GPU)

Each folder corresponds to an example project that utilizes the tools within [Saturn Cloud](https://www.saturncloud.io/s/). These examples run on a Jupyter Server and/or Dask cluster with a **GPU** instance type and image, and showcase workflows with tools that take advantage of GPU processing such as [RAPIDS](http://rapids.ai/) and deep learning.

Refer to the `README.md` file within each folder for detailed instructions on how to run them.

> **Pro tip**: Right-click on any `README.md` file and choose "Open With -> Markdown Preview" to view a rendered version

If you don't already use Saturn Cloud, [see how to get started here](https://www.saturncloud.io/docs/getting-started/)!

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
