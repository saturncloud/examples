library(future)
library(furrr)
library(tidyverse)
library(glue)

plan(future::multisession())

data <- read.csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/r-parallel/example-data.csv")

get_nth_transaction <- function(x, n){
  if(length(x) < n){
    NA
  } else {
    sort(x)[n]
  }
}

aggregate_function <- function(data){
  data %>%
    group_by(customer_id, region) %>%
    summarize(median_revenue = median(revenue),
              num_transactions = n(),
              first_transaction = get_nth_transaction(transaction_date, 1),
              second_transaction = get_nth_transaction(transaction_date, 2),
              .groups = "drop") %>%
    mutate(time_between = as.numeric(difftime(second_transaction, first_transaction, units = "days")))
}


# Example 1: no parallelization ------------------------------------------------

# expected to take 60 seconds
system.time({
  aggregate_data <- 
    data %>%
    aggregate_function()
  
})

# Method 2: no parallelization, but split it by region first -------------------

region_data <- data %>%
  group_by(region) %>%
  group_split()

system.time({
  aggregate_region_data <- list()
  for(i in 1:length(region_data)){
    message(glue("Processing {i}"))
    aggregate_region_data[[i]] <- aggregate_function(region_data[[i]])
  }
  aggregate_data <- bind_rows(aggregate_region_data)
})

# Method 3: split by region and parallelize with future ------------------------

region_data <- data %>%
  group_by(region) %>%
  group_split()

system.time({
  aggregate_region_data <- list()
  for(i in 1:length(region_data)){
    message(glue("Creating {i} future"))
    aggregate_region_data[[i]] <- future({aggregate_function(region_data[[i]])})
  }
  aggregate_data <- bind_rows(value(aggregate_region_data))
})

# Method 4: split by region and use future -------------------------------------

system.time({
  region_data <- data %>%
    group_by(region) %>%
    group_split() %>%
    future_map_dfr(aggregate_function)
})

