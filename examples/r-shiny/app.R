library(ggplot2)
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