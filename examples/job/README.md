---
title: "Create a job"
weight: 2
description: "Setting and executing a job on Saturn Cloud"
aliases:
  - /docs/examples/dashboards/api_deploy/jobs
  - /docs/examples/dashboards/jobs/
---


A Saturn Cloud job is a computing environment set up to run recurring tasks. You can start a job in 3 ways:

1. on a schedule 
2. manually by pressing start button 
3. via an API 

## Example code
Saturn Cloud jobs and deployments need to load the code to run, and the easiest way to do so is with a git repository. So create a git repository on a service like [GitHub](github.com) and put the files your job will need into the repository.
This is an example script which we will be running as a job. You can create one of your own as well (if you want to run a notebook instead of a job, see [this blog post]({{< ref "notebook-apis.md" >}})).

```python
import logging
logging.getLogger().setLevel(logging.INFO)
logging.info('Job is successfully running!')
```

Save this in your git repository as example.py

## Create a job

To create a job for above script or any of your own script or notebook, first press the **New Job** button on the upper right corner of the **Resources** page. 

![New job button](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/newjob.png "doc-image")

Specify the following settings below. Note that the git settings need to be set after the resource is created.

* **Command** - `python path_to_your_repository/example.py`. Here 'path_to_your_repository' refers to the path of your repository where file example.py is stored
* **Git Repositories** - Select **New Git Repository** and add your repository here.

You are now set. To run your job manually press the green start button on the resource page of the job.
If you want to check this example, go to our **Create a Job** template and press start. You do not need to perform any of the above steps, we have already set it up for you!

## Running a Saturn Cloud job as an API

In addition to running the job on a button press or on a schedule, you can also run it as an API. This is useful if you want a different program to cause the job to start. To run the job created programmatically, you need:

* **User Token** - You can get your user token from the **Settings** page of Saturn Cloud.
* **Job ID** - It is the hexadecimal value in the URL of the job's resource page: `https://app.community.saturnenterprise.io/dash/resources/job/{job_id}`.

Now using above parameters trigger the job via HTTP request sending system, like curl or Postman. The following is the code if you want to start the job using Python.

```python
import requests

user_token = "youusertoken" # (don't save this directly in a file!)
job_id = "yourjobid"

url = f'https://app.community.saturnenterprise.io/api/jobs/{job_id}/start'
headers={"Authorization": f"token {user_token}"}
r = requests.post(url, headers=headers)
```
## Running a Saturn Cloud job on a Schedule
You can also run this job or any other job you created, on schedule. This will automate running a job on a fixed time.  Check the box for field `Run this job on a schedule` and populate `Scheduled Settings` using [cron syntax](https://en.wikipedia.org/wiki/Cron) to meet the requirements of your task. 

![Schedule button](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/schedule.png "doc-image")


