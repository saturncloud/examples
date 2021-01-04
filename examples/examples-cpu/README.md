<img src="./_img/saturn.png" width="600">

# Saturn Cloud Examples (CPU)

If you're new to Saturn Cloud, [see how to get started here](https://www.saturncloud.io/docs/getting-started/).

Once you've done that, click one of the links below to open a notebook and try an example.

**Data Exploration and Machine Learning**

1. Hyperparameter tuning
    - [single-machine (scikit-learn)](./nyc-taxi/hyperparameter-scikit.ipynb)
    - [multi-machine (Dask)](./nyc-taxi/hyperparameter-dask.ipynb)
1. Train an XGBoost Model
    - [single-machine (scikit-learn)](./nyc-taxi/xgboost.ipynb)
    - [multi-machine (Dask)](./nyc-taxi/xgboost-dask.ipynb)
1. [Deploy a Dashboard](./nyc-taxi/dashboard.ipynb)
1. [ETL with Dask](./nyc-taxi/data-aggregation.ipynb)

**Prefect**

[prefect](https://www.prefect.io/) is an open-source workflow orchestration tool, similar to [Apache Airflow](https://airflow.apache.org/). Prefect can take advantage of Dask to run tasks in a workflow in parallel.

1. [Run a prefect flow on Saturn](./prefect/prefect-scoring.ipynb)
1. [Run a Prefect Cloud flow on a Saturn Dask cluster](./prefect/prefect-cloud-scheduled-scoring.ipynb)

**Snowflake**

[Snowflake](https://www.snowflake.com/cloud-data-platform/) is a popular cloud-based data warehouse. If you have a Snowflake account, explore these examples to see how to use Saturn Cloud to process the data stored there.

1. [Reading Snowflake data into `pandas`](./snowflake/snowflake-pandas.ipynb)
1. [Reading Snowflake data into Dask DataFrame](./snowflake/snowflake-dask.ipynb)
1. Hyperparameter Tuning
    - [single-machine (scikit-learn)](./nyc-taxi-snowflake/hyperparameter-scikit.ipynb)
    - [multi-machine (Dask)](./nyc-taxi-snowflake/hyperparameter-dask.ipynb)
1. Train an XGBoost model
    - [single-machine (scikit-learn)](./nyc-taxi-snowflake/xgboost.ipynb)
    - [multi-machine (Dask)](./nyc-taxi-snowflake/xgboost-dask.ipynb)

<hr>

### Running in a new project

These examples are configured to run with small data sizes to quickly (and cost-effectively) illustrate the features of Saturn Cloud. If you prefer to run these examples in a new project, or would like to modify the code and run with larger data sizes and clusters, you can clone the repo by opening a new Terminal within the JupyterLab of your project, then copying the example you want into the `/home/jovyan/project` folder:

```bash
git clone https://github.com/saturncloud/examples.git /tmp/examples
cp -r /tmp/examples/examples/examples-cpu /home/jovyan/project/
```

## NYC Taxi

This example is in the [nyc-taxi](nyc-taxi) folder.

An end-to-end data science pipeline comprising data ingest, exploratory analysis, machine learning model training, and deploying models and a dashboard.

*You will learn:*
- How to get performance speedups for ML model training with Dask
- How to deploy a dashboard
- How to deploy an ML model with a REST API

There are examples for GPU-accelerated ML in the `examples-gpu` project.

## Prefect

This example is in the [prefect](prefect) folder.

*You will learn:*
- How to set up a Prefect flow for scheduled scoring of a statistical model
- How to use a Dask cluster to distribute work
- How to deploy the flow and run it on a schedule
- How to deploy a flow using Prefect Cloud

## Snowflake

This example is in the [snowflake](snowflake) folder.

*You will learn:*
- How to query Snowflake and load data into a Pandas dataframe
- How to query Snowflake and load data into a Dask dataframe
- How to write to Snowflake with Pandas and Dask

## NYC Taxi using Snowflake

This example is in the [nyc-taxi-snowflake](nyc-taxi-snowflake) folder.

The same end-to-end data science pipeline from the "NYC Taxi" example, except using [Snowflake](https://www.snowflake.com/) for data ingestion and exploratory analysis. The machine learning examples pull data from a Snowflake database rather than from S3.

*You will learn:*
- Everything from the "NYC Taxi" example _plus_:
- How to ingest data from S3 into a Snowflake database
- How to perform data aggregations in Snowflake and read the results into Pandas dataframes
- How to efficiently load large datasets from Snowflake into Dask, and train ML models with the data
