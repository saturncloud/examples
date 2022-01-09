---
title: "Create a Dashboard with Shiny"
linkTitle: "Create a Dashboard with Shiny"
weight: 3
description: Use Shiny to create simple Dashboard and deploy it in Saturn Cloud
---

## What is Shiny?

<a href="https://shiny.rstudio.com/" target='_blank' rel='noopener'>Shiny</a> is a widely used package for building interactive web applications in R. Shiny is easy to use and flexible. It integrates nicely with CSS themes, htmlwidgets and JavaScript actions.
You can create dashboards or run machine learning models through interactive applications without any prior knowledge of web development tools, using the R Shiny package. Saturn Cloud deployment resources allow you to deploy any code, including R shiny apps. A Shiny app is built with three components

**User Interface:** Responsible for creating the layout of your web app, like panels, textbox, dropdown etc. This is basically what users sees at their end.
**Server:** Constitutes logic which will display content in the webapp as per the inputs given by user from UI. 
**ShinyApp function:*: This function call launches the shiny app as per UI/server pair.

## Objective

In the example below we are building a dashboard as R script (`.R` file) using Shiny, then deploying it in Saturn Cloud using a Saturn Cloud deployment resource. For this example we are creating a bar plot which predicts sale prices for each year as per selected number of bedrooms. The data for same is taken from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data), and the plot is rendered with ggplot2.

## Building a Dashboard

Let us create another R script called `app.R`. This script will contain Shiny Dashboard. We have created a simple dashboard which has a slider and a plot.
User will select a number as single input from slider This number represents number of bedrooms. In the following code in first line we have loaded the ggplot2 and shiny packages.
Now we will read house price data in variable data. We then create a regression model where sale price of house is target variable.

In UI function we will create appearance of our dashboard. In slider input we are setting number of bedrooms ranging from 0 to 8.
Since we want our output to show a ggplot2 plot, we will use function plotOutput inside mainPanel. 
plotOutput displays outputs returned from render functions (renderPlot in our case). 

In server function we have logic to create the bar chart as per selected number of bedrooms from slider.
In our case renderPlot fetches ggplot object and stores it in variable `price_by_year`. Then the housed prices per year are generated (based on number of selected bedrooms) using the `ggplot` function. 

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

## Deployment

Save the `app.R` in inside a GitHub repo. You'll need to connect [git on Saturn Cloud](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/) to your git repo host. Now click **New Deployment**. It can be found on top right side of the resource page.

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/plumber_deployment.png "doc-image")

You'll want to set the following:

* **Name** - the name of the resource, which also is used as the URL for the Dashboard
* **Run Command:** - set to `shiny::runApp(host="0.0.0.0", port=8000)`, which starts the shiny app on port 8000 (required for all Saturn Cloud deployments), and open to outside traffic
* **Instance Count** - How many concurrent machines to host the API on. Set to default as 1.
* **Hardware and Size** - This example is small hence I have selected smallest available CPU resource.
* **Image** - set to `saturn-rstudio` image, which is preconfigured to have R and some common R libraries (including ggplot2).
* **Extra Packages (CRAN):** - add `shiny` so that it is installed at startup.
* **Working Directory:** - set to `/home/jovyan/{your-git-repository-name}`, and add any subfolders if your `app.R` file isn't in the base directory of your repo

After creating the resource, add your git repository with the `app.R` to the resource.

With this you are ready to deploy your dashboard by pressing the green button on the resource page of the deployment.

## Access Deployed Dashboard

In the **Deployment** on the Saturn Cloud resource page you'll see a **URL**. This is the URL for your shiny app. By default, this app will be available to anyone who is logged into Saturn Cloud. But if you want this app to be accessible to people who do not have Saturn Cloud accounts you'll need to select **Make it public and allow unauthenticated access** in the deployment settings.
