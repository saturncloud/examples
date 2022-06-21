library(shiny)

source("helper_functions.R")

ui <- fluidPage(
  titlePanel("Pet Guesser"),
  sidebarLayout(
    sidebarPanel(
      textInput("name", "Pet name"),
      actionButton("guess_cat", "Guess Cats"),
      actionButton("guess_dog", "Guess Dogs")
    ),
    mainPanel(
      plotOutput("plot")
    )
  )
)

server <- function(input, output) {
  results <- reactive({
    input$guess_cat
    input$guess_dog
    isolate({
      selected_name <- fix_name(input$name)
      if (nchar(selected_name) == 0) {
        NULL
      } else {
        pet_type(pet_data, selected_name)
      }
    })
  })

  guess <- reactiveVal(label = "guess")

  observe({
    input$guess_cat
    isolate({
      guess("cats")
      })
  })

  observe({
    input$guess_dog
    isolate({
      guess("dogs")
      })
  })

  output$plot <- renderPlot({
    plot_value_basic(results())
  })
}

shinyApp(ui = ui, server = server)
