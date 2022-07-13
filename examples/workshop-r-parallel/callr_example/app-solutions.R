# This is the RStudio default shiny app, except we want to add a button that does
# a big data processing in the background

library(shiny)

process_the_data <- function(url) {
  readr::read_csv(url) |>
    dplyr::group_by(region) |>
    dplyr::summarize(revenue = sum(revenue)) |>
    readr::write_csv("aggregate_data.csv")
}

ui <- fluidPage(
    titlePanel("Old Faithful Geyser Data"),
    sidebarLayout(
        sidebarPanel(
            sliderInput("bins",
                        "Number of bins:",
                        min = 1,
                        max = 50,
                        value = 30),
            actionButton("process_button", "Process the data")
        ),

        mainPanel(
           plotOutput("distPlot"),
           textOutput("processStart")
        )
    )
)

server <- function(input, output) {
    output$distPlot <- renderPlot({
        x    <- faithful[, 2]
        bins <- seq(min(x), max(x), length.out = input$bins + 1)
        hist(x, breaks = bins, col = "darkgray", border = "white")
    })

    output$processStart <- renderText({
      if (input$process_button > 0) {
        url <- "https://saturn-public-data.s3.us-east-2.amazonaws.com/r-parallel/example-data.csv"
        callr::r_bg(process_the_data, args = list(url = url))
        paste0("Data process started at ", Sys.time())
      } else {
        ""
      }
    })
}

shinyApp(ui = ui, server = server)
