|<img src="img/snowflake.png" width="400" /> |$~~~~~~~~~~~~~~~~~~$| <img src="img/saturn.png" width="400" />|
| -- | -- | -- |


# Using Snowflake with Saturn Cloud

[Snowflake](https://www.snowflake.com/) is a data platform built for the cloud that allows for fast SQL queries. This example shows how to query data in Snowflake and pull into [Saturn Cloud](https://www.saturncloud.io/) for data science work. We will rely on the [Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html) to connect and issue queries from Python code.

# Credentials and connecting

To avoid setting and storing credentials directly in notebooks, we recommend sourcing credentials stored a in .yml file uploaded using the "Credentials" page in Saturn Cloud.

- Type: `File`
- Shared with: `<your username>`
- Path: /home/jovyan/snowflake_creds.yml
- Value: .yml file contents (below)

The .yml file can specify any arguments that can be passed to `snowflake.connector.connect`, such as:

```yaml
account: ...
user: ...
password: ...
role: ...
```

You will need to restart the Jupyter server if you add a file under "Credentials" while it is running. Then from any notebook where you want to connect to Snowflake, you can read in the credentials and then provide additional arguments (or override the ones set in the file):

```python
import yaml
import snowflake.connector

creds = yaml.full_load(open('/home/jovyan/snowflake_creds.yml'))
conn = snowflake.connector.connect(
    warehouse=...,
    database=...,
    schema=...,
    **creds,
)
```

# Load data into Snowflake

This example utilizes [public NYC Taxi data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page). To prepare Snowflake and load some taxi data into a table, run the commands in the [`load-data.sql`](load-data.sql) script from a Snowflake worksheet.

# Query data with Pandas

If your table or query result fits into the memory of your Jupyter client, you can load data into a pandas dataframe using methods `fetch_pandas_all()` or `fetch_pandas_batch()` available in the Snowflake Connector for Python a.k.a. the Python Connector.

See [`snowflake-pandas.ipynb`](snowflake-pandas.ipynb).

# Query data with Dask
If your table or query result _don't_ fit into the memory of the computer running your Jupyter client, you can use Dask! Then you can take advantage of using a Dask cluster with Saturn to speed up your computations.

See [`snowflake-dask.ipynb`](snowflake-dask.ipynb).
