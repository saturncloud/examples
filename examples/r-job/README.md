---
title: "Create a job using R"
weight: 2
description: "Setting and executing a job on Saturn Cloud using R"
---


A Saturn Cloud job is a computing environment set up to run recurring tasks. You can start a job in 3 ways:

1. on a schedule 
2. manually by pressing start button 
3. via an API 

## Example code
Saturn Cloud jobs and deployments need to load the code to run, and the easiest way to do so is with a git repository. So create a git repository on a service like [GitHub](github.com) and put the files your job will need into the repository.
This is an example R script which we will be running as a job. In this script, we are printing a message in logs. You can create one of your own as well (if you want to run a python script instead, see [this example](https://saturncloud.io/docs/examples/python/production/jobs/#example-code).

```R
library(logger)
log_info('Job is successfully running!')
```

Save this in your git repository as example.R

## Installations and Start Script

We will create an R script which installs logger package from CRAN. Let's name this file as install-packagesJ.R.
```R
install.packages('logger')
```
To run above R script we will create a bash file, let's name that startup-scriptJ.sh.
```bash
Rscript install-packagesJ.R
```

I have saved all the three files under same directory.

## Create a job

To create a job for example.R script or any of your own script, first press the **New Job** button on the upper right corner of the **Resources** page. 

![New job button](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/newjob.png "doc-image")

Specify the following settings below. Note that the git settings need to be set after the resource is created.

* **Command** - `Rscript path_to_your_repository/example.R`. Here 'path_to_your_repository' refers to the path of your repository where file example.R is stored.
* **Git Repositories** - Select **New Git Repository** and add your repository here.
* **Image** - Set to `saturn-rstudio` image.
* **Advanced Settings** -> Start Script - `sh /home/jovyan/git-repos/Dashboard/startup-scriptJ.sh`

You are now set. To run your job manually press the green start button on the resource page of the job.
You can skip this setup step by using the recipe file `.saturn/saturn.json` included in this example.

## Running a Saturn Cloud job as an API

In addition to running the job on a button press or on a schedule, you can also run it as an API. This is useful if you want a different program to cause the job to start. To run the job created programmatically, you need:

* **User Token** - You can get your user token from the **Settings** page of Saturn Cloud.
* **Job ID** - It is the hexadecimal value in the URL of the job's resource page: `https://app.community.saturnenterprise.io/dash/resources/job/{job_id}`.

Now using above parameters trigger the job via HTTP request sending system, like curl or Postman. The following is the code if you want to start the job using R.

```R
library(httr)
user_token = "youusertoken"  # (don't save this directly in a file!)
job_id="yourjob id"
url=paste("https://app.internal.saturnenterprise.io/api/jobs/",job_id,"/start",sep="")
POST(url, add_headers(Authorization=paste("Token ", user_token)))

```
## Running a Saturn Cloud job on a Schedule
You can also run this job or any other job you created, on schedule. This will automate running a job on a fixed time.  Check the box for field `Run this job on a schedule` and populate `Scheduled Settings` using [cron syntax](https://en.wikipedia.org/wiki/Cron) to meet the requirements of your task. 

![Schedule](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/schedule.png "doc-image")
