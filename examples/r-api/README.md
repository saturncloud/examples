---
title: "Create an API with Plumber"
linkTitle: "Create an API for Deployment"
weight: 3
description: Use *Plumber* to create simple R API and deploy it in Saturn Cloud
aliases:
  - /docs/examples/dashboards/api_deploy/
---
## What is an API?
An API is a way for programs to communicate with each other. They work similarly to websites, but instead of a human typing in a url and getting an HTML page back, a program can send a similar request to a URL and get different types of data back. For more information about APIs check out [this page](https://www.howtogeek.com/343877/what-is-an-api/).

## What is Plumber?
<a href="https://www.rplumber.io/index.html" target='_blank' rel='noopener'>Plumber</a> is a widely used package for writing APIs in R.  Plumber is easy to use and flexible. It provides a convenient and reliable way for R to communicate with other software and services.
You can convert a simple R functions to a responsive API by adding few comments. Decorate your existing code with ‘#*’ . By adding these special comments as a prefix you communicate to Plumber that 'these R functions have to be transformed to API endpoints'. 
## Objective
In the example below we are building an API as R script (`.R` files) using Plumber. For this example we are creating a regression model. The data for same is taken from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data).
We will be accepting number of bedrooms and year build as inputs. We have defined an endpoint, "/predict", which will return the predicted price of a house.
. 
## Building an API
First we will create an R script which installs plumber package from CRAN. Let's name this file as install-packages.R.

```R
install.packages('plumber')
install.packages("dplyr")
```

Now let us create another R script room.R, this script will contain our regression model, which we will wrap with plumber. In the following code in first line we have placed oxigen2-like comments for describing what this API will do. Now we will define operation and path . Here we have used `GET` operation (read data) and path is `/predict`. This endpoint will return the predicted price of a house.

This function is taking 3 arguments: `response`, `bedrooms` which represents number of bedrooms and `year` which represents year build. `bedrooms` and `year` are inputs from the client.

Inside function we read houseprice data and perform linear regression to build a model. We then predict price of house for given inputs. We are returning HTTP response 400 if parameters passed are not in range of training data. If the parameters fall within valid range, API will return predicted house price.

```R
#* Predict price of a house
#* @get /predict
function(bedrooms,year,res){
  data <- read.csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv")
  l = lm(SalePrice~BedroomAbvGr+YearBuilt, data)
  bedrooms<-as.numeric(bedrooms)
  year<-as.numeric(year)
  if(between(bedrooms,0, 8) & between(year, 1871,2100)){
    X <- data.frame(BedroomAbvGr=bedrooms,YearBuilt=year)
    return(predict(l, newdata = X))
    
  } else {
    res$status <- 400  
    return(list(error = "Please enter BedroomAbvGr between 0 and 8. Enter YearBuilt between 1872 and 2100."))
  }  
}
```
Now create another R script which will run above piece of code. Let's name this as runapi.R.  Load the plumber package. Start the server using plumber object. Since the host listens on 0.0.0.0, it will be reachable on an appropriate interface address to the connection. Port 8000 is a common HTTP port for web servers.
```R
library(dplyr)
library(plumber)
plumber::pr_run(plumber::plumb("room.R"), port=8000, host="0.0.0.0")
```

## Deployment

 Save all these files (room.R, install-packages.R,runapi.R and startup-script.sh) in a Github repo. Now click **New Deployment**. It can be found on top right side of the resource page. 

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/plumber_deployment.png "doc-image")


To run, add following to command field.
```bash
Rscript runapi.R
```
Add path to file in working directory field as shown below. In the screenshot below, my file runapi.R is inside repository Dashboard. If you aren't familiar with how to set up SSH credentials and add git repositories to Saturn Cloud check [here](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/).

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/working-directory.png "doc-image")


Go to Advanced Settings -> Start Script.  Add following :

sh /home/jovyan/git-repos/Dashboard/startup-script.sh

startup-script.sh will be executed whenever a resource is started . This script will run install-packages.R to install Plumber. Now you are ready to deploy your API by pressing the green start button on the resource page of the deployment. 

![script](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/script.png "doc-image")

Following is the setting for rest of the fields:


**Name** - this is set to default as 'your username'-api\
**Instance Count** - set to default as 1 \
**Hardware and Size** - This example is small hence I have selected smallest available CPU resource.\
**Image** - set to saturn-rstudio image

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/deploy_settings.png "doc-image")

You can skip this setup step by using the recipe file `.saturn/saturn.json` included in this example.
## Access Deployed API

Click the URL given in deployment detail page . Add `/__docs__/` in the end of URL, you will see the automatic interactive API documentation. 

![doc plumber](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/docsplumber.png "doc-image")

Enter the parameter values for `bedrooms` and `year`. Click execute .

Another way to access deployed API is through browser. Submit the following query in your url. 

`https://houseprice-deploy.internal.saturnenterprise.io/predict?bedrooms=3&year=2000`

In example above, the key value pairs that we see after `?` are known as query parameters (bedrooms=8 and year=2000). 
To access this URL you need to either:

1. Be logged into Saturn Cloud and use your browser to go to the URL, which only works for GET requests.
2. (recommended) add an authorization token to your HTTP request. On the Saturn Cloud settings page you'll see your user token, which lets Saturn Cloud know that your request is authorized. Add a header to the HTTP request with the key of  `Authorization` and the value `token {USER_TOKEN}` where `{USER_TOKEN}` is your token from the settings page. In R you could make the request like so

```R
library(httr)
user_token = "youusertoken"  # (don't save this directly in a file!)
job_id="yourjob id"
url=paste("https://app.internal.saturnenterprise.io/api/jobs/",job_id,"/start",sep="")
POST(url, add_headers(Authorization=paste("Token ", user_token)))
```

