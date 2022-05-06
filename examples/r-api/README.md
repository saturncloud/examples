---
title: "Create an API with Plumber"
linkTitle: "Create an API with Plumber"
weight: 3
description: Use Plumber to create simple R API and deploy it in Saturn Cloud
---
## What is an API?
An API is a way for programs to communicate with each other. They work similarly to websites, but instead of a human typing in a url and getting an HTML page back, a program can send a similar request to a URL and get different types of data back. For more information about APIs check out [this page](https://www.howtogeek.com/343877/what-is-an-api/).

## What is Plumber?
<a href="https://www.rplumber.io/index.html" target='_blank' rel='noopener'>Plumber</a> is a widely used package for writing APIs in R.  Plumber is easy to use and flexible. It provides a convenient and reliable way for R to communicate with other software and services.
You can convert a simple R functions to a responsive API by adding few comments. Decorate your existing code with ‘#*’ . By adding these special comments as a prefix you communicate to Plumber that 'these R functions have to be transformed to API endpoints'. 
## Objective
In the example below we are building an API as R script (`.R` file) using Plumber. For this example we are creating a regression model. The data for same is taken from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data).
We will be accepting number of bedrooms and year build as inputs. We have defined an endpoint, "/predict", which will return the predicted price of a house.
. 
## Building an API
First we will create an R script which installs plumber package from CRAN. Let's name this file as `setup.R`.

```R
install.packages("plumber")
install.packages("dplyr")
```

Now let us create another R script called `endpoints.R`. This script will contain the endpoints for our plumber API, which in this case will be `/` and `/predict`. Endpoint `/` redirects to interactive API documentation. Endpoint `/predict` calls a regression model and predics house price. 

In the following code in first line we have placed oxygen2-like comments for describing what this API will do. Now we will define the operation and path. Here we have used `GET` operation (to read data) and path is `/predict`. This endpoint will return the predicted price of a house.

This function is taking 3 arguments: `response`, `bedrooms` which represents number of bedrooms and `year` which represents year build. `bedrooms` and `year` are inputs from the client.

Inside function we read houseprice data and perform linear regression to build a model. We then predict price of house for given inputs. We are returning HTTP response 400 if parameters passed are not in range of training data. If the parameters fall within valid range, API will return predicted house price.

The path for second endpoint is `/`. We are redirecting this endpoint to `/__docs__/`, which is interactive API documentation. In this documentation UI you can enter the required values and trigger response.

```R
data <- read.csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv")
model <- lm(SalePrice~BedroomAbvGr+YearBuilt, data)

#* Predict price of a house
#* @get /predict
function(bedrooms,year,res){
  bedrooms<-as.numeric(bedrooms)
  year<-as.numeric(year)
  if(between(bedrooms,0, 8) && between(year, 1871,2100)){
    X <- data.frame(BedroomAbvGr=bedrooms, YearBuilt=year)
    return(predict(model, newdata = X))
  } else {
    res$status <- 400  
    return(list(error = "Please enter BedroomAbvGr between 0 and 8. Enter YearBuilt between 1872 and 2100."))
  }  
}
#* Redirect to Docs
#* @get /
function(res) {
  res$status <- 303 # redirect
  res$setHeader("Location", "./__docs__/")
}
```
Now create another R script which will run above piece of code. Let's name this as `run-api.R`.  Load the plumber package. Start the server using plumber object. Since the host listens on 0.0.0.0, it will be reachable on an appropriate interface address to the connection. The API must use port 8000 for Saturn Cloud to be able to direct traffic to it.
```R
library(dplyr)
library(plumber)
plumber::pr_run(plumber::plumb("endpoints.R"), port=8000, host="0.0.0.0")
```

## Deployment

Save both these files (`setup.R`, `endpoints.R`, `run-api.R`) in a GitHub repo, in our case we'll use [saturncloud/examples](github.com/saturncloud/examples). Now click **New Deployment**. It can be found on top right side of the resource page. 

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/plumber_deployment.png "doc-image")


To run, add following to command field.
```bash
Rscript run-api.R
```
Add path to file in working directory field as shown below. In the screenshot below, my file `run-api.R` is inside repository Dashboard. If you aren't familiar with how to set up SSH credentials and add git repositories to Saturn Cloud check [here](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/).

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/working-directory.png "doc-image")


Go to Advanced Settings -> Start Script.  Add following :

`Rscript setup.R`


Now `setup.R` will be executed when the deployment is started, which installs plumber and dplyr. 

![script](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/script.png "doc-image")

These are the rest of the fields you'll need to fill out


**Name** - the name of the resource, which also is used as the URL for the API
**Instance Count** - How many concurrent machines to host the API on. Set to default as 1.
**Hardware and Size** - This example is small hence I have selected smallest available CPU resource.
**Image** - set to `saturn-rstudio` image, which is preconfigured to have R and some common R libraries.

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/deploy_settings.png "doc-image")

With this you are ready to deploy your API by pressing the green button on the resource page of the deployment. 

## Access Deployed API

Click the URL given in deployment detail page you will be directed to the automatic interactive API documentation. 

![doc plumber](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/docsplumber.png "doc-image")

Enter the parameter values for `bedrooms` and `year`. Click execute .

Another way to access deployed API is through browser. Submit the following query in your url. 

`https://houseprice-deploy.internal.saturnenterprise.io/predict?bedrooms=3&year=2000`

In example above, the key value pairs that we see after `?` are known as query parameters (bedrooms=8 and year=2000). 
To access this URL you need to either:

1. Be logged into Saturn Cloud and use your browser to go to the URL, which only works for GET requests.
2. (recommended) add an authorization token to your HTTP request. On the Saturn Cloud settings page you'll see your user token, which lets Saturn Cloud know that your request is authorized. Add a header to the HTTP request with the key of  `Authorization` and the value `token {USER_TOKEN}` where `{USER_TOKEN}` is your token from the settings page. In R you could make the request like so:

```R
library(httr)
user_token = "youusertoken"  # (don't save this directly in a file!)
job_id="yourjob id"
url=paste("https://app.internal.saturnenterprise.io/api/jobs/",job_id,"/start",sep="")
POST(url, add_headers(Authorization=paste("Token ", user_token)))
```

