---
title: "Create a Dashboard with Shiny"
linkTitle: "Create a Dashboard with Shiny"
weight: 3
description: Use Shiny to create simple Dashboard and deploy it in Saturn Cloud
---
## What is a Dashboard?
Dashboards is a tool where you can view you raw data in form of meaningful visualisations. It transforms data to charts, graphs and tables that help in analysis of information, defining KPIs  and eventually taking data centric decisions. 
## What is Shiny?
<a href="https://shiny.rstudio.com/" target='_blank' rel='noopener'>Shiny</a> is a widely used package for building interactive web applications in R.  Shiny is easy to use and flexible. It integrates nicely with CSS themes, htmlwidgets and JavaScript actions.
You can create dashboards or run machine learning models through web apps etc without any prior knowledge of web development tools, using Shiny package. 
Shiny app structure constitutes : 

**User Interface**: Responsible for creating the layout of your web app, like panels, textbox, dropdown etc. This is basically what users sees at their end.\
**Server**: Constitutes logic which will display content in the webapp as per the inputs given by user from UI.  \
**ShinyApp**: This function launches the shiny app as per UI/server pair.

## Objective
In the example below we are building a dashboard as R script (`.R` file) using Shiny. For this example we are creating a histogram for sale prices as per selected number of bins. The data for same is taken from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data).

## Building a Dashboard
First we will create an R script which installs shiny and ggplot2 packages from CRAN. Let's name this file as `setup.R`.

```R
install.packages("shiny")
install.packages("ggplot2")
```

Now let us create another R script called `app.R`. This script will contain Shiny Dashboard. We have created a simple dashboard which has a slider and a plot.
User will select a number as single input from slider This number represents value of bins for histogram plot  In the following code in first line we have loaded the ggplot2 and shiny packages. 
Now we will read house price data in variable data.

In UI function we will create appearance of our dashboard. Title of our dashboard "Housing Data" is added to title panel.
We then give structure to our app using sidebarLayout function. sidebarLayout contains sidebarPanel and mainPanel. In slider input we are setting number of bins ranging from 1 to 30.
Since we want our output to show histogram plot, we will use function plotOutput inside mainPanel. 
plotOutput displays outputs returned from render functions (renderPlot in our case). 

In server function we have logic to create histogram as per selected number of bins from slider. Function renderPlot will return output to function plotOutput. 
In our case renderPlot fetches qplot object and stores it in variable `distPlot`. From housing dataset we first extract sale prices of houses. Then generate bins as per the user input and then draw histogram based on bin number using qplot function. 

In the last line we are call shinyApp and pass in UI and server variables.

```R
library(ggplot2)
library(shiny)

data<-read.csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv")
ui <- fluidPage(
    titlePanel("Housing Data"),
    sidebarLayout(
        sidebarPanel(
            sliderInput("bins",
                        "Number of bins:",
                        min = 1,
                        max = 30,
                        value = 15)
        ),
        mainPanel(
           plotOutput("distPlot")
        )
    )
)
server <- function(input, output) {
      output$distPlot <- renderPlot({
        x<- data$SalePrice
        bins <- seq(min(x), max(x), length.out = input$bins + 1)
        qplot(x, geom="histogram",breaks =bins,   
              main = "Histogram for Sale Prices for houses", 
              xlab = "Sale Price",  
              fill=I("Orange"), 
              col=I("darkgray"))        
    })
}
shinyApp(ui = ui, server = server)

```
Now create another R script which will run above piece of code. Let's name this as `run-app.R`. Start the server using shiny object. Since the host listens on 0.0.0.0, it will be reachable on an appropriate interface address to the connection. The API must use port 8000 for Saturn Cloud to be able to direct traffic to it.
```R
shiny::runApp(host="0.0.0.0", port=8000, launch.browser=FALSE)
```

## Deployment

Save all three files (`setup.R`, `app.R`, `run-app.R`) in a directory inside GitHub repo. Now click **New Deployment**. It can be found on top right side of the resource page. 

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/plumber_deployment.png "doc-image")


To run, add following to command field.
```bash
Rscript run-app.R
```
Add path to file in working directory field as shown below. In the screenshot below, my file `run-app.R` is inside repository Dashboard, directory shiny. If you aren't familiar with how to set up SSH credentials and add git repositories to Saturn Cloud check [here](https://saturncloud.io/docs/using-saturn-cloud/gitrepo/).

![deploy](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/Shiny-deploy.png "doc-image")


Go to Advanced Settings -> Start Script.  Add following :

`Rscript setup.R`


Now `setup.R` will be executed when the deployment is started, which installs shiny and ggplot2. 

![script](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/shiny-sh.png "doc-image")

These are the rest of the fields you'll need to fill out


**Name** - the name of the resource, which also is used as the URL for the Dashboard\
**Instance Count** - How many concurrent machines to host the API on. Set to default as 1.\
**Hardware and Size** - This example is small hence I have selected smallest available CPU resource.\
**Image** - set to `saturn-rstudio` image, which is preconfigured to have R and some common R libraries.\

With this you are ready to deploy your dashboard by pressing the green button on the resource page of the deployment. 

## Access Deployed Dashboard

Click the URL given in deployment detail page . You will be redirected to Dashboard page. 

![doc plumber](https://saturn-public-assets.s3.us-east-2.amazonaws.com/example-resources/shiny-dashboard.png "doc-image")

Set the slider to the value you want for number of bins for histogram. By default number of bins in this example is set to 15. Histogram for housing sale prices is generated as per the selected value. 


