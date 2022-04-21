library(ggplot2)
library(ggplot2)
library(shiny)

data <- read.csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/house_price_data_v2.csv") # nolint
model <- lm(sale_price ~ bedroom_abv_gr + year_built, data)

ui <- fluidPage(
  titlePanel("Housing Data"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("bedrooms", "Number of Bedrooms", min = 0, max = 8, value = 3, step = 1)
    ),
    mainPanel(
      plotOutput("price_by_year")
    )
  )
)

server <- function(input, output) {
  output$price_by_year <- renderPlot({
    data <- data.frame(year_built = 1970:2015)
    data$bedroom_abv_gr <- input$bedrooms
    data$prediction <- predict(model, newdata = data)

    ggplot(data, aes(x = year_built, y = prediction)) +
      geom_col(fill = "#FF6721") +
      theme_minimal() +
      scale_y_continuous(labels = scales::dollar) +
      labs(x = "Year home built", y = "Predicted value of house")
  })
}
shinyApp(ui = ui, server = server)
