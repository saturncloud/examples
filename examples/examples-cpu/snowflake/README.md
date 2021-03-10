|<img src="../_img/snowflake.png" width="400" /> |$~~~~~~~~~~~~~~~~~~$| <img src="../_img/saturn.png" width="400" />|
| -- | -- | -- |

# Using Snowflake with Saturn Cloud

[Snowflake](https://www.snowflake.com/) is a data platform built for the cloud that allows for fast SQL queries. This example shows how to query data in Snowflake and pull into [Saturn Cloud](https://www.saturncloud.io/) for data science work. We will rely on the [Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html) to connect and issue queries from Python code.

# Connecting to Snowflake

This example uses data stored in a Snowflake data warehouse that is managed by the team at Saturn Cloud. We've set up a read-only user for use in these examples. If you would like to access data stored in your own Snowflake account, you should set up [Credentials](https://www.saturncloud.io/docs/concepts/credentials/) for your account, user, and password then set the other connection information accordingly. For more details on Snowflake connection information, see ["Connecting to Snowflake"](https://docs.snowflake.com/en/user-guide/python-connector-example.html#connecting-to-snowflake) in the `snowflake-connector-python` docs.

If you would like more details about how to use your own Snowflake account, scroll down to the "Using your own Snowflake" section in this document.

# Query data with Pandas

If your table or query result fits into the memory of your Jupyter client, you can load data into a pandas dataframe using `pd.read_sql()`.

See [snowflake-pandas.ipynb](./snowflake-pandas.ipynb).

# Query data with Dask
If your table or query result _don't_ fit into the memory of the computer running your Jupyter client, you can use Dask! Then you can take advantage of using a Dask cluster with Saturn to speed up your computations.

See [snowflake-dask.ipynb](./snowflake-dask.ipynb).


# Using your own Snowflake

To avoid setting and storing credentials directly in notebooks, we recommend sourcing credentials from environment variables using the "Credentials" page in Saturn Cloud.

```sh
Type: Environment Variable
Shared with: <your username>
Name: <variable name>
Value: <variable value>
```

Create a credential for each of these variables:
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`

You will need to restart the Jupyter server if you add "Credentials" while it is running. Then from any notebook where you want to connect to Snowflake, you can read in the credentials and then provide additional arguments:

```python
import os
import snowflake.connector

conn = snowflake.connector.connect(
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ['SNOWFLAKE_PASSWORD'],
    warehouse=...,
    database=...,
    schema=...,
)
```

## Load data

This example utilizes [public NYC Taxi data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page). To prepare Snowflake and load some taxi data into a table, run the commands in the [load-data.sql](./load-data.sql) script from a Snowflake worksheet.
