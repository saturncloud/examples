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
