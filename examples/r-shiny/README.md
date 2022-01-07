---
title: "Create a Dashboard with Shiny"
linkTitle: "Create a Dashboard with Shiny"
weight: 3
description: Use Shiny to create simple Dashboard and deploy it in Saturn Cloud
---

## What is Shiny?
<a href="https://shiny.rstudio.com/" target='_blank' rel='noopener'>Shiny</a> is a widely used package for building interactive web applications in R.  Shiny is easy to use and flexible. It integrates nicely with CSS themes, htmlwidgets and JavaScript actions.
You can create dashboards or run machine learning models through interactive applications without any prior knowledge of web development tools, using the R Shiny package. 
Shiny app structure constitutes : 

**User Interface**: Responsible for creating the layout of your web app, like panels, textbox, dropdown etc. This is basically what users sees at their end.
**Server**: Constitutes logic which will display content in the webapp as per the inputs given by user from UI. 
**ShinyApp**: This function launches the shiny app as per UI/server pair.

## Objective
In the example below we are building a dashboard as R script (`.R` file) using Shiny. For this example we are creating a histogram which predicts sale prices for each year as per selected number of bedrooms. The data for same is taken from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data).

## Building a Dashboard
First we will create an R script which installs shiny and ggplot2 packages from CRAN. Let's name this file as `setup.R`.

```R
install.packages("shiny")
install.packages("ggplot2")
```

Now let us create another R script called `app.R`. This script will contain Shiny Dashboard. We have created a simple dashboard which has a slider and a plot.
User will select a number as single input from slider This number represents number of bedrooms.  In the following code in first line we have loaded the ggplot2 and shiny packages. 
Now we will read house price data in variable data. We then create a regression model where Sale price of house is target variable.

In UI function we will create appearance of our dashboard. Title of our dashboard "Housing Data" is added to title panel.
We then give structure to our app using sidebarLayout function. sidebarLayout contains sidebarPanel and mainPanel. In slider input we are setting number of bedrooms ranging from 0 to 8.
Since we want our output to show histogram plot, we will use function plotOutput inside mainPanel. 
plotOutput displays outputs returned from render functions (renderPlot in our case). 

In server function we have logic to create histogram as per selected number of bedrooms from slider. Function renderPlot will return output to function plotOutput. 
In our case renderPlot fetches ggplot object and stores it in variable `price_by_year`. First we create a dataset with year ranging from 1970 to 2015. Then generate house prices by year, based on number of selected bedrooms, using ggplot function. 

In the last line we are call shinyApp and pass in UI and server variables.

```R
library(ggplot2)
library(shiny)

data <- read.csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv")
model <- lm(SalePrice~BedroomAbvGr+YearBuilt, data)

ui <- fluidPage(
    titlePanel("Housing Data"),
    sidebarLayout(
        sidebarPanel(
          sliderInput("bedrooms", "Number of Bedrooms", min=0,max=8, value=3,step=1)
        ),
        mainPanel(
           plotOutput("price_by_year")
        )
    )
)
    
server <- function(input, output) {
    
    output$price_by_year <- renderPlot({
      data <- data.frame(YearBuilt = 1970:2015)
      data$BedroomAbvGr <- input$bedrooms
      data$prediction <- predict(model, newdata = data)
      
      ggplot(data, aes(x = YearBuilt, y = prediction))+
        geom_col(fill = "#FF6721") +
                   theme_minimal() +
        scale_y_continuous(labels = scales::dollar) +
        labs(x = "Year home built", y = "Predicted value of house")
    })
}
shinyApp(ui = ui, server = server)
```
Now create another R script which will run above piece of code. Let's name this as `run-app.R`. Start the server using shiny object. Since the host listens on 0.0.0.0, it will be reachable on an appropriate interface address to the connection. The API must use port 8000 for Saturn Cloud to be able to direct traffic to it.
```R
shiny::runApp(host="0.0.0.0", port=8000, launch.browser=FALSE)
```

## Deployment

Save all three files (`setup.R`, `app.R`, `run-app.R`) in a directory inside GitHub repo. You'll need to connect [git on Saturn Cloud](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/) to your git repo host. Now click **New Deployment**. It can be found on top right side of the resource page. 

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/plumber_deployment.png "doc-image")


To run, add following to the **command** field of the deployment.
```bash
Rscript run-app.R
```
Add path to file in working directory field as shown below--this should be the location off the `app.R` file.

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/Shiny-deploy.png "doc-image")


Go to Advanced Settings -> Start Script.  Add following :

`Rscript setup.R`


Now `setup.R` will be executed when the deployment is started, which installs shiny and ggplot2. 

![script](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/shiny-sh.png "doc-image")

These are the rest of the fields you'll need to fill out


**Name** - the name of the resource, which also is used as the URL for the Dashboard\
**Instance Count** - How many concurrent machines to host the API on. Set to default as 1.
**Hardware and Size** - This example is small hence I have selected smallest available CPU resource.
**Image** - set to `saturn-rstudio` image, which is preconfigured to have R and some common R libraries.

With this you are ready to deploy your dashboard by pressing the green button on the resource page of the deployment. 

## Access Deployed Dashboard

Click the URL given in deployment detail page . You will be redirected to Dashboard page. 

![doc plumber](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/shiny-dashboard.png "doc-image")


If you are logged into Saturn Cloud you can directly click the url and access the app. But if you want this app to be accessible to everone, you would need to add authorization token. 

On the Saturn Cloud settings page you'll see your user token, which lets Saturn Cloud know that your request is authorized. Add a header to the HTTP request with the key of  `Authorization` and the value `token {USER_TOKEN}` where `{USER_TOKEN}` is your token from the settings page. In R you could make the request like:

```R
library(httr)
user_token = "youusertoken"  # (don't save this directly in a file!)
job_id="yourjob id"
url=paste("https://app.internal.saturnenterprise.io/api/jobs/",job_id,"/start",sep="")
POST(url, add_headers(Authorization=paste("Token ", user_token)))
```

