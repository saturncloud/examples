# This is the RStudio default shiny app, except we want to add a button that does a big data processing in the background

library(shiny)

process_the_data <- function(url){
  readr::read_csv(url) |>
    dplyr::group_by(region) |>
    dplyr::summarize(revenue = sum(revenue)) |>
    readr::write_csv("aggregate_data.csv")
}

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Old Faithful Geyser Data"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            sliderInput("bins",
                        "Number of bins:",
                        min = 1,
                        max = 50,
                        value = 30),
            actionButton("process_button","Process the data")
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot"),
           textOutput("processStart")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$distPlot <- renderPlot({
        # generate bins based on input$bins from ui.R
        x    <- faithful[, 2]
        bins <- seq(min(x), max(x), length.out = input$bins + 1)

        # draw the histogram with the specified number of bins
        hist(x, breaks = bins, col = 'darkgray', border = 'white')
    })
    
    output$processStart <- renderText({
      if(input$process_button > 0){
        paste0("Data process started at ", Sys.time())
      } else {
        callr::r_bg(process_the_data, args = list(url = "https://saturn-public-data.s3.us-east-2.amazonaws.com/r-parallel/example-data.csv"))
      }
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
