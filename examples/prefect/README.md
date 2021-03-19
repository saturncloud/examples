# Scheduled jobs with Prefect and Prefect Cloud

Prefect is an open source workflow orchestration tool made for data-intensive workloads. This allows you to schedule and organize jobs to run any time, in your chosen order. It can accommodate dependencies between jobs, and is very useful for data pipelines and machine learning workflows.

Saturn Cloud supports two different tools in the Prefect ecosystem:
- Prefect Core, which is an open source library users can install, and
- Prefect Cloud, which is a fully hosted cloud service which you can purchase. The same team that maintains the `prefect` core library runs Prefect Cloud. Prefect Cloud is a hosted, high-availability, fault-tolerant service that handles all the orchestration responsibilities for running data pipelines.

If you would like an introduction to the concepts behind job scheduling with Prefect, you can start with our [Introduction to Prefect Concepts](https://www.saturncloud.io/docs/examples/prefect/prefect_concepts/) docs page then come back here and run these examples!

## [Develop a Scheduled Data Pipeline with Prefect](./01-prefect.ipynb)

Use the open-source `prefect` library to schedule a data pipeline.

## [Use Prefect Cloud with Saturn Cloud](./02-prefect-cloud.ipynb)

Connect to Prefect Cloud and orchestrate a flow running from Saturn Cloud.