# Connecting to Snowflake with Saturn Cloud

This quickstart gives you what you need to get started connecting to Snowflake from Saturn Cloud. This includes:

* Creating a connection to a Snowflake database to pull data into a Pandas DataFrame
* Querying Snowflake data over a distributed cluster using Dask for when the data is too big to fit into memory on a single computer. _Once you have the data loaded in a distributed setting you can use tools like RAPIDS or PyTorch to train models on it, as can be seen in other Quickstarts._

Both of these tasks can be found in the [snowflake-dask.ipynb](snowflake-dask.ipynb) Jupyter notebook.