# Create an API on Saturn Cloud Using Julia and Genie

![Genie logo](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/genie_logo.png "doc-image")

## Overview

[Genie](https://genieframework.com/) is a full-stack web framework for Julia. Genie allows you to create complex web apps, but here we are using it to make a simple API. Check out the [Genie documentation](https://genieframework.com/docs/tutorials/Overview.html) for more information.

An API is a way for programs to communicate with each other. They work similarly to websites, but instead of a human typing in a url and getting an HTML page back, a program can send a similar request to a URL and get different types of data back.

This API runs a linear regression on historical house prices and outputs the predicted house price based on this model when you hit a specific endpoint. 

## Creating the API
All the API code is contained in a file called "app.py." To deploy this dashboard on Saturn Cloud, call **`julia app.jl`** as the command in a Saturn Cloud deployment. See [Saturn Cloud docs](https://saturncloud.io/docs/examples/dashboards/dashboard/) for more detailed instructions on deploying this and other dashboards.

### Import the Libraries

This exercise uses GLM and Genie to create a API:
* [GLM](https://juliastats.org/GLM.jl/v0.11/): generalized linear models
* [Genie](https://github.com/GenieFramework/Genie.jl): full-stack web apps

``` julia
using AWS
using AWSS3
using CSV
using DataFrames
using GLM
using Genie
using Genie.Router
```

### Load the Data and Create the Model
First, we load the housing price data from S3 into a DataFrame. This data is then passed into a GLM model that uses the number of bedrooms and the year the house was built to predict the sale price of the home. This model is relatively simple, so we create it when we start the API server, but you could also load a more complex pre-trained model.

``` julia
df = DataFrame(CSV.File(AWSS3.read(S3Path("s3://saturn-public-data/examples/dashboard/housePriceData.csv", config=global_aws_config(; region="us-east-2")))))

formula = @formula(SalePrice ~ BedroomAbvGr + YearBuilt)
linear_regressor = lm(formula, df)
```

### Define the Endpoints

After creating the model, define the endpoints of the API. Here we are defining two endpoints: `/predict`  and `/`. The `/` endpoint function runs when you hit the base url of the API. This endpoint simple provides instructions for how to access the model.

The `/predict` endpoint runs the model prediction function. It takes two arguments: the number of bedrooms of the house and the year the house was built. To call this function, construct a url in the form `/predict?bedrooms=2&yearBuilt=1900`, for example. This will pass the value "2" as the number of bedrooms and "1900" as the year built. The API will then respond with a string showing the predicted sales price. 

Genie handles errors and other endpoints automatically, so if you encounter either, you will be presented with a helpful webpage explaining the error or lack of endpoint.

``` julia
route("/predict") do
    bedrooms = parse(Int64, params(:bedrooms, 1))
    yearBuilt = YearBuilt = parse(Int64, params(:yearBuilt, 1872))

    if !((1 <= bedrooms <= 8) && (1872 <= yearBuilt <= 2100))
        return ("Please enter a number of bedrooms between 1 and 8 and a year built between 1872 and 2100.")
    end

    prediction = predict(linear_regressor, DataFrame(BedroomAbvGr=bedrooms, YearBuilt=yearBuilt))
    prediction = round(prediction[1])
    return ("The prediction for a house with $bedrooms bedrooms built in $yearBuilt is \$$prediction.")
end

route("/") do
    return ("This API returns a linear regression for the price of a house based on the number of bedrooms and the year it was built. For example, append /predict?bedrooms=2&yearBuilt=1900 to the url to predict the sale price for a house built in 1900 with 2 bedrooms.")
end
```

### Start the Server

Lastly, specify the Genie configuration and server specifications. It is important that you set the port to "8000" and the host to "0.0.0.0" for the API to run properly on Saturn Cloud.

``` julia
Genie.config.run_as_server = true
Genie.startup(8000, "0.0.0.0")
```

### Run the API

You then need to only load the app code to git and link the code appropriately to a Saturn Cloud deployment. 

Check out our other [Julia resources](https://saturncloud.io/docs/examples/julia/) for other examples using Julia.