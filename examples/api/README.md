---
title: "Create an API with FastAPI"
linkTitle: "Create an API for Deployment"
weight: 3
description: Use *FastAPI* to create RESTful APIs in Python and deploy them in Saturn Cloud
aliases:
  - /docs/examples/dashboards/api_deploy/
---
## What is an API?
A restful API is a way for programs to communicate with each other. They work similarly to websites, but instead of a human typing in a url and getting an HTML page back, a program can send a similar request to a URL and get different types of data back. For more information about APIs check out [this page](https://realpython.com/python-api/).

## What is FastAPI?
<a href="https://fastapi.tiangolo.com/" target='_blank' rel='noopener'>FastAPI</a> is a python based web framework for building Rest APIs . It does live up to its name--it is as fast as  NodeJS and Go. It has inbuild data validation and as automatic document generation feature so humans can understand your API design. 

## Objective
In the code below we are building an API as Python scripts (`.py` files). Its endpoint is "/predict",  which uses the data added as part of the url. The response containing result will be returned in a Python dictionary which gets converted to JSON. This implementation is utilizing FastAPI, but you can try other web frameworks like [Django](https://www.django-rest-framework.org/), [Flask](https://flask.palletsprojects.com/en/2.0.x/), [Falcon](https://falcon.readthedocs.io/en/stable/) as well.
## Building an API

First we will import necessary libraries and create a FastAPI instance and initialize it to variable app. You can start a Saturn Cloud Jupyter Server and work on the .py script yourself. Check [Create a Resource](https://saturncloud.io/docs/getting-started/start_resource/) to learn how to create a resource and use Jupyter on Saturn Cloud.

```python
from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.linear_model import LinearRegression

app = FastAPI()
```
In following code we are building a regression model. The data for same is taken from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data).
We will be accepting number of bedrooms and year build as inputs to predict house price. 

```python
df = pd.read_csv(
    "https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv"
)
lr = LinearRegression()
lr.fit(df[["BedroomAbvGr", "YearBuilt"]], df["SalePrice"])
```
Now we will define operation and path . Here we have used `GET` operation (read data) and path is `/predict`.
To get the inputs from the client, we are using query parameters. Here we are passing `BedroomAbvGr` for number of bedrooms and `YearBuilt` for year house was built.
We are returning HTTP response 400 if parameters passed are not in range of training data. If the parameters fall within valid range, API will return the response as a JSON object which gives us predicted house price. 

```python
@app.get("/predict")
async def predict(BedroomAbvGr: int = None, YearBuilt: int = None):
    a = pd.DataFrame([[BedroomAbvGr, YearBuilt]], columns=["BedroomAbvGr", "YearBuilt"])
    v = lr.predict(a)
    if not ((0 <= BedroomAbvGr <= 8) and (1872 <= YearBuilt <= 2100)):

        raise HTTPException(
            status_code=400,
            detail="Please enter BedroomAbvGr between 0 and 8. Enter YearBuilt between 1872 and 2100",
        )

    return {"prediction": v[0]}

```

## Deployment

Let's name the above file houseprice.py. Save this file in a Github repo that you can access. Now click **New Deployment**. It can be found on top right side of the resource page. 

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/plumber_deployment.png "doc-image")

To run, add following to command field. `Uvicorn` refers to the server that will use the API we have build to serve requests and `reload` makes the server restart after code changes. Since the host listens on 0.0.0.0, it will be reachable on an appropriate interface address to the connection. Port 8000 is a common HTTP port for web servers 

```bash
python3 -m uvicorn houseprice:app --reload --host 0.0.0.0 --port 8000
```
Add path to file in working directory field as shown below. In the screenshot below, my file houseprice.py is inside repository Dashboard. If you aren't familiar with how to set up SSH credentials and add git repositories to Saturn Cloud check [here](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/).
Go to `pip install` and add `uvicorn` and `fastapi`.  Now you are ready to deploy your API by pressing the green start button on the resource page of the deployment. 

![deploy command](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/api-deploy-command.png "doc-image")

Following is the setting for rest of the fields:
**Name** - this is set to default as 'your username'-dashboard
**Instance Count** - set to default as 1 
**Hardware and Size** - This example is small hence I have selected smallest available CPU resource.
**Image** - set to base saturncloud image

## Access Deployed API

Click the URL given in deployment detail page . Add '/docs' in the end of URL, you will see the automatic interactive API documentation. 

![fast-api](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/fastapi_docs.png "doc-image")

Enter the parameter values for `BedroomAbvGr` and `YearBuilt`. Click execute .

Another way to access deployed API is through browser. Submit the following query in your url. 

`https://houseprice-deploy.internal.saturnenterprise.io/predict?BedroomAbvGr=8&YearBuilt=2000`

In example above, the key value pairs that we see after `?` are known as query parameters (BedroomAbvGr=8 and YearBuilt=2000). 
To access this URL you need to either:

1. Be logged into Saturn Cloud and use your browser to go to the URL, which only works for GET requests.
2. (recommended) add an authorization token to your HTTP request. On the Saturn Cloud settings page you'll see your user token, which lets Saturn Cloud know that your request is authorized. Add a header to the HTTP request with the key of  `Authorization` and the value `token {USER_TOKEN}` where `{USER_TOKEN}` is your token from the settings page. In Python you could make the request like so

```python
import requests

user_token = "youusertoken" # (don't save this directly in a file!)
url = f'https://houseprice-deploy.internal.saturnenterprise.io/predict?BedroomAbvGr=8&YearBuilt=2000'
headers={"Authorization": f"token {user_token}"}
r = requests.get(url, headers=headers)
```

This documentation was an attempt to walk you through steps of creating your own API and deploy it. 
If you want to try this API yourself, just click on the **Deploy API** template resource and start the deployment. All the preinstallations have already been done for you.  
