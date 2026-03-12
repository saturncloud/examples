library(shiny)
library(tidyverse)
library(bslib)
library(bsicons)

# --- 1. REAL DATA PREPARATION ---
# Using the real 'diamonds' dataset from ggplot2
data <- diamonds %>% 
  mutate(SaleID = row_number()) %>%
  rename(Sales = price) 

# --- 2. UI DEFINITION ---
ui <- page_sidebar(
  title = "Real-World KPI Dashboard (Diamonds)",
  
  sidebar = sidebar(
    title = "Data Filters",
    # Filter by diamond cut (Quality)
    selectInput("cut", "Select Diamond Cut", 
                choices = unique(data$cut), 
                selected = "Ideal", 
                multiple = TRUE),
    helpText("The KPIs will update based on the quality of diamonds selected.")
  ),
  
  # 3-Tile KPI Layout
  layout_column_wrap(
    width = 1/3,
    value_box(
      title = "Total Revenue",
      value = uiOutput("total_sales"),
      showcase = bs_icon("gem"),
      theme = "primary"
    ),
    value_box(
      title = "Avg Diamond Price",
      value = uiOutput("avg_sale"),
      showcase = bs_icon("cash-stack"),
      theme = "success"
    ),
    value_box(
      title = "Inventory Count",
      value = uiOutput("total_cust"),
      showcase = bs_icon("box-seam"),
      theme = "info"
    )
  ),
  
  card(
    card_header("Price Distribution (by Carat)"),
    plotOutput("sales_plot")
  )
)

# --- 3. SERVER LOGIC ---
server <- function(input, output) {
  
  # Reactive filtering based on user input
  filtered_data <- reactive({
    data %>%
      filter(cut %in% input$cut)
  })
  
  output$total_sales <- renderText({
    paste0("$", format(round(sum(filtered_data()$Sales), 0), big.mark=","))
  })
  
  output$avg_sale <- renderText({
    paste0("$", round(mean(filtered_data()$Sales), 2))
  })
  
  output$total_cust <- renderText({
    format(nrow(filtered_data()), big.mark=",")
  })
  
  output$sales_plot <- renderPlot({
    ggplot(filtered_data(), aes(x = carat, y = Sales)) +
      geom_point(alpha = 0.2, color = "#3498db") +
      geom_smooth(color = "red") +
      theme_minimal() +
      labs(x = "Carat Weight", y = "Price ($)")
  })
}

shinyApp(ui = ui, server = server)