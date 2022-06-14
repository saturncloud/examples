# This is the final version of the app with all the styling changes

library(shiny)

source("helper_functions.R")
  
# STEP 3 swap to a bootstrap page
ui <- bootstrapPage(
  # STEP 2 - add a bslib theme
  theme  = bslib::bs_theme(version = 5, primary = "#ff6622"),
  tags$head(
    tags$title("The ultimate pet guesser!"),
    tags$meta(name="description", content="Guess if the name is for a cat or dog"),
    HTML('<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">')),
    tags$link(rel = "stylesheet",
              type = "text/css",
              href = "site.css"),
  tags$section(class="py-5",
               div(class="container",
                   div(class="row",
                       div(class="col-10 offset-1 col-md-6 offset-md-3 text-center",
                           img(height="48",
                               class="py-2 img-fluid",
                               src="https://saturncloud.io/icons/saturncloud-logo-1.svg"
                           ),
                           div(class="row",
                               div(class="col-6 offset-3",
                                   div(class="overlapping-images",
                                       img(src="dog.jpg", class="img-circle img-left"),
                                       img(src="cat.jpg", class="img-circle img-right")
                                       )
                                   ),
                               ),
                           h1("Pet name species guesser"),
                           p(glue("Try and guess if a pet name is more popular with cats or dogs in the Seattle pet license data."))
                       )
                   )
               )
  ),
  # step 4 - redesign this
  tags$section(class="bg-light py-3",
               div(class="container",
                   div(class="row",
                       div(class="col-lg-6",
                           div(class="bg-white rounded border shadow m-1 p-2 h-100",
                           HTML('<div class="form-group shiny-input-container w-100">
                                    <label class="control-label" id="name-label" for="name">Pet Name</label>
                                    <input id="name" type="text" class="form-control shiny-bound-input" value="">
                                </div>'),
                           div(class="d-grid gap-2",
                               actionButton("guess_cat","Guess Cats", class="text-white btn-primary"),
                               actionButton("guess_dog","Guess Dogs", class="text-white btn-primary")
                               )
                           )
                       ),
                       div(class="col-lg-6 text-center",
                           plotOutput("plot",height="200px"),
                           uiOutput("text")
                       )
                   )
               )
  )
)

server <- function(input, output) {
  results <- reactive({
    input$guess_cat
    input$guess_dog
    isolate({
      selected_name <- fix_name(input$name)
      if(nchar(selected_name) == 0){
        NULL
      } else {
        pet_type(pet_data, selected_name)
      }  
    })
  })
  
  
  guess <- reactiveVal(label = "guess")
  
  observe({
    input$guess_cat
    isolate({guess("cats")})
  })
  
  observe({
    input$guess_dog
    isolate({guess("dogs")})
  })
  
  
  output$plot <- renderPlot(bg="transparent", {
    # STEP 1 - swap this for a prettier graph
    plot_value(results())
  })
  
  output$text <- renderUI({
    if(is.null(results())){
      h3("Please select a valid name")
    } else if(!is.finite(results()$p)){
      h3("No pets in the data with that name")
    } else {
      if(results()$type == guess()){
        value <- "correct!"
        value_class <- "correct-value"
      } else {
        value <- "incorrect."
        value_class <- "incorrect-value"
      }
      
      HTML(glue("<h3><strong class={value_class}>{guess()} is {value}</strong> ({results()$cats} cats, {results()$dogs} dogs).</h3>"))
    }
  })
}

shinyApp(ui = ui, server = server)
