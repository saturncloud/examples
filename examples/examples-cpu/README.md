![Saturn Cloud](saturn.png)

# Saturn Cloud Examples (CPU)

Each folder corresponds to an example project that utilizes the tools within [Saturn Cloud](https://www.saturncloud.io/s/). These examples run on a Jupyter Server and/or Dask cluster with a **CPU** instance type and image.

Refer to the `README.md` file within each folder for detailed instructions on how to run them.

> **Pro tip**: Right-click on any `README.md` file and choose "Open With -> Markdown Preview" to view a rendered version

If you don't already use Saturn Cloud, [see how to get started here](https://www.saturncloud.io/docs/getting-started/)!

### Running in a new project

These examples are configured to run with small data sizes to quickly (and cost-effectively) illustrate the features of Saturn Cloud. If you prefer to run these examples in a new project, or would like to modify the code and run with larger data sizes and clusters, you can clone the repo by opening a new Terminal within the JupyterLab of your project, then copying the example you want into the `/home/jovyan/project` folder:

```bash
git clone https://github.com/saturncloud/examples.git /tmp/examples
cp -r /tmp/examples/examples/examples-cpu /home/jovyan/project/
```

## NYC Taxi

This example is in the [`nyc-taxi`](nyc-taxi) folder.

An end-to-end data science pipeline comprising data ingest, exploratory analysis, machine learning model training, and deploying models and a dashboard.

*You will learn:*
- How to get performance speedups for ML model training with Dask
- How to deploy a dashboard
- How to deploy an ML model with a REST API

There are examples for GPU-accelerated ML in the `examples-gpu` project.

## Prefect

This example is in the [`prefect`](prefect) folder.

*You will learn:*
- How to set up a Prefect flow for scheduled scoring of a statistical model
- How to use a Dask cluster to distribute work
- How to deploy the flow and run it on a schedule

## Snowflake

This example is in the [`snowflake`](snowflake) folder.

*You will learn:*
- How to query Snowflake and load data into a Pandas dataframe
- How to query Snowflake and load data into a Dask dataframe
- How to write to Snowflake with Pandas and Dask

## NYC Taxi using Snowflake

This example is in the [`nyc-taxi-snowflake`](nyc-taxi-snowflake) folder.

The same end-to-end data science pipeline in the "NYC Taxi" example, except using [Snowflake](https://www.snowflake.com/) for data ingest and exploratory analysis. The ML examples then pull data from a Snowflake database rather than from S3.

*You will learn:*
- Everything from the "NYC Taxi" example _plus_:
- How to ingest data from S3 into a Snowflake database
- How to perform data aggregations in Snowflake and read the results into Pandas dataframes
- How to efficiently load large datasets from Snowflake into Dask, and train ML models with the data


