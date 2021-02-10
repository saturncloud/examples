<img src="./_img/saturn.png" width="600">

# Saturn Cloud Examples (GPU)

## Welcome to Saturn Cloud! 

These example notebooks highlight ways Saturn Cloud can help accelerate your data science work. Click on one of the links below to get started!

**Data Exploration and Machine Learning**

1. Train a Random Forest Model
    - [single-machine, CPU (scikit-learn)](./nyc-taxi/rf-scikit.ipynb)
    - [single-machine, GPU (RAPIDS)](./nyc-taxi/rf-rapids.ipynb)
    - [multi-machine, GPU (Dask + RAPIDS)](./nyc-taxi/rf-rapids-dask.ipynb)

**Snowflake**

Snowflake is a popular data warehouse technology. Explore these examples to see how to use Saturn Cloud to process the data stored there. [Click here to learn more](https://www.snowflake.com/cloud-data-platform/).

1. Train a Random Forest Model
    - [single-machine, CPU (scikit-learn)](./nyc-taxi-snowflake/rf-scikit.ipynb)
    - [single-machine, GPU (RAPIDS)](./nyc-taxi-snowflake/rf-rapids.ipynb)
    - [multi-machine, GPU (Dask + RAPIDS)](./nyc-taxi-snowflake/rf-rapids-dask.ipynb)

<hr>

## NYC Taxi

An end-to-end data science pipeline comprising data ingest, exploratory analysis, machine learning model training, and deploying models and a dashboard. The `examples-cpu` project contains most of the examples, but these are GPU examples for machine learning with RAPIDS.

*You will learn:*
- How to train a tree-based machine learning model on a GPU using RAPIDS
- How to train the same model on a cluster of GPU machines using RAPIDS with Dask

## Next steps

Thanks for trying out these examples! To learn more about how Saturn Cloud works, check out our [Documentation](https://www.saturncloud.io/docs/), [blog](https://www.saturncloud.io/s/blog/), or join an [upcoming event](https://www.saturncloud.io/s/events/).

If you have any questions or suggestions for example projects, reach out to us at support@saturncloud.io or open an issue on the [examples Github repo](https://github.com/saturncloud/examples).
