|<img src="img/taxi.png" width="200" /> | <img src="img/saturn.png" width="400" />|
| -- | -- |

# NYC Taxi analysis with Saturn Cloud

The notebooks in this example showcase a data science workflow with NYC taxi data, executed on [Saturn Cloud](https://www.saturncloud.io/). They are a subset of a [larger demo](https://youtu.be/SgXSIbB4Hik), reduced to quickly highlight key features of Saturn Cloud. The larger demo includes the following:

<img src="img/pipeline.png" width="800">

All code for the full demo is [available here](https://github.com/saturncloud/saturn-cloud-examples/tree/main/taxi_demo). You can follow the instructions there to create a new project and run the full examples. The example you are currently in is a reduced version to quickly (and cost-effectively) highlight key features of Saturn Cloud.

The notebooks in _this_ example cover:

1. Create and deploy a dashboard with exploratory analysis (`holoviz`, `bokeh`, `panel`)
1. Load records from CSV files and produce aggregate data files (`dask.dataframe`, `pandas`)*
1. Train a number of machine learning models using single-node Python tools (`scikit-learn` and `xgboost`)
1. Use Dask to distribute and speed up model training (`dask-ml` and `dask-xgboost`)*
1. Deploy models via REST API (`flask`)

_\* These examples illustrate how to launch and utilize a Dask cluster with Saturn._

You are free to open each notebook in this example and start playing around! For a guided experience, follow the steps below.

## Dashboard

The dashboard presents summary statistics about NYC taxi rides from the years 2017 through 2019. Plots are built with [HoloViz](https://holoviz.org/) and [Bokeh](https://bokeh.org/), and the dashboard is served using [Panel](https://panel.holoviz.org/). Any other Python visualization or dashboard library is supported by Saturn; this is just one example.

![dashboard](img/dashboard.png)

Saturn Cloud hosts pre-aggregated data files on a public S3 bucket, so you can immediately run and view the dashboard. See [`dashboard.ipynb`](dashboard.ipynb) for the dashboard code. 

### Running dashboard

If you run all the cells in the notebook, the final cell will display the dashboard inline.

To run it as a separate process from JupyterLab: open a terminal, then cd into the dashboard directory and run `panel serve`:

```bash
cd /home/jovyan/examples-cpu/nyc-taxi/
panel serve dashboard.ipynb
```

The dashboard will be live behind the Jupyter proxy. You can copy the URL of this Jupyter window and replace `/lab/*` with `/proxy/5006/dashboard`. For example, your Jupyter URL might be:

```
https://main.demo.saturnenterprise.io/user/aaron/examples-cpu/lab/workspaces/examples-cpu
```

Then your dashboard URL would be: 

```
https://main.demo.saturnenterprise.io/user/aaron/examples-cpu/proxy/5006/dashboard
```

It will take a few seconds to load when first viewing the page, as all the cells in this notebook must be executed first.

#### Deployment 

To run as part of a persistent Deployment, go to the "Deployments" page in Saturn Cloud and create a new deployment. This will host the dashboard so users can view it without having to launch a Jupyter project.

- Name: `examples-taxi-dashboard`
- Project: `examples-cpu`
- Command: (see below)
- Instance Count: 1
- Instance Size: Medium - 2 cores - 4 GB RAM

The command is:

```bash
python -m panel serve /home/jovyan/project/examples/nyc-taxi/dashboard.ipynb --port=8000 --address="0.0.0.0" --allow-websocket-origin="*"
```

After you create the Deployment, click the play button to start it up. It will take a few minutes to launch the deployment, then when its up you can view the dashboard at the URL listed on the Deployment card. You can view logs by clicking on the Status link.

Note that the "Predict my Tip" widget on the "ML" tab will return `-1.00%` until we specify a model deployment for it to point to. We will get there later in the example.

## Aggregate data files

**NOTE**: This section requires that you have AWS credentials with write access to an S3 bucket. It is not required to proceed with the later examples so you can skip this section.

Saturn Cloud hosts pre-aggregated NYC taxi data from 2017-2019 for the dashboard in the previous step. The [`data-aggregation.ipynb`](data-aggregation.ipynb) notebook contains all the code to perform these aggregations. It is set up to run on a small sample (first few months of 2017) to be able to be executed in this example project. 

To tell the notebook where to write data, the `DASHBOARD_DATA` environment variable must be set with an S3 location, and you will need [AWS credentials](https://www.saturncloud.io/docs/connecting/data/iam/) set up to write to that location. You will need to stop this Jupyter project to make the necessary modifications, so don't close this JupyterLab window (or read the instructions carefully)!

Go to the "Jupyter" page, stop and then edit this project (`examples-cpu`). Set the environment variable in the "Environment Variables" section or using the "Start Script". This ensures that the environment variable is set for all notebooks and deployments created from the project. The dashboard ([`dashboard.ipynb`](dashboard.ipynb)) will then pull from the location specified in `DASHBOARD_DATA` rather than the public S3 bucket hosted by Saturn.

If you don't have AWS credentials set, go to the "Credentials" page in Saturn Cloud and add Environment Variable entries for:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

You will only need to set these credentials once - all of your Jupyter projects will then utilize these credentials. 

It is possible to manually add environment variables from the JupyterLab terminal or a notebook, but these will not be persisted when you stop the Jupyter project or when you deploy it.

## Train ML models

TBD

## Deploy ML model

TBD


## References

- NYC taxi image by [David Hurley on Unsplash](https://unsplash.com/photos/aPlUUmO4qr8).