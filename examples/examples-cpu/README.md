![Saturn Cloud](https://pbs.twimg.com/media/EeBsCTPX0AAICkt.png)

# Saturn Cloud Examples (CPU)

Each folder corresponds to an example project that utilizes the tools within [Saturn Cloud](https://www.saturncloud.io/s/). These examples run on a Jupyter Server and/or Dask cluster with a CPU instance type and image (there is a separate set of example projects for GPU workloads).

Refer to the `README.md` file within each folder for detailed instructions on how to run them.

> **Pro tip**: Right-click on any `README.md` file and choose "Open With -> Markdown Preview" to view a rendered version

If you don't already use Saturn Cloud, [see how to get started here](https://www.saturncloud.io/docs/getting-started/)!

### Running in a new project

These examples are configured to run with small data sizes to quickly (and cost-effectively) illustrate the features of Saturn Cloud. If you prefer to run these examples in a new project, or would like to modify the code and run with larger data sizes and clusters, you can clone the repo by opening a new Terminal within the JupyterLab of your project, then copying the example you want into the `/home/jovyan/project` folder:

```bash
cd /home/jovyan
git clone https://github.com/saturncloud/examples.git examples
cp -r examples/examples/examples-cpu project/
```


## NYC Taxi

An end-to-end data science pipeline comprising data ingest, exploratory analysis, machine learning model training, and deploying models and a dashboard.

*You will learn:*
- How to get performance speedups for ML model training with Dask
- How to deploy a dashboard
- How to deploy an ML model with a REST API

## Prefect

*You will learn:*
- How to set up a Prefect flow for scheduled scoring of a statistical model
- How to use a Dask cluster to distribute work
- How to deploy the flow
