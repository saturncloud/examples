library(readr)
library(dplyr)
library(stringr)
library(tidyr)
library(glue)
library(ggplot2)

# load the pet data and format it to have clean cat and dog names
pet_data <-
  read_csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/pet-names/seattle_pet_licenses.csv",
           col_types = cols(.default=col_character())
  ) %>%
  select(
    name = `Animal's Name`,
    species = `Species`,
  ) %>%
  mutate_all(tolower) %>%
  filter(
    !is.na(name),
    !is.na(species),
    name != "",
    !str_detect(name, "[^ \\.-[a-zA-Z]]"),
    species %in% c("cat","dog")
  )

# function to fix the input to remove special characters and extra white space
fix_name <- function(example_name){
  example_name %>%
    tolower() %>%
    str_remove_all("[^ \\.-[a-zA-Z]]") %>%
    trimws()
}

# given the pet data, will find just the info about the select name
pet_type <- function(pet_data, selected_name){
  results <- pet_data %>% filter(name == selected_name) 
  
  cats <- sum(results$species == "cat")
  dogs <- sum(results$species == "dog")
  p <- cats/(cats + dogs)
  type <- 
    if(cats > dogs){
      "cats" 
    } else if(dogs > cats){
      "dogs"
    } else {
      "tie"
    }
  
  # number of cats, dogs, percent of cats, and the correct type
  list(cats = cats, dogs = dogs, p = p, type = type)
}

# a simple plot of the data
plot_value_basic <- function(results){
  if(is.null(results)){
    ggplot()
  } else {
    ggplot(data.frame(count = c(results$cats, results$dogs), 
                              type = c("cats","dogs")), 
                   aes(x=type,y=count)) + 
      geom_col()  
  }
}

# a _fancy_ plot of the data
plot_value <- function(results){
  if(is.null(results)){
    p <- NA_real_
  } else {
    p <- results$p
  }
  
  plot <- ggplot(data = data.frame(x = p), aes(xmin = x-0.025, xmax = x+0.025, ymin = -0.1, ymax=0.1)) + 
    geom_line(data = rbind(data.frame(x = seq(0,1,0.1), y = -0.05, group = 1:11),
                           data.frame(x = seq(0,1,0.1), y = 0.05, group = 1:11)),
              aes(x = x, y = y, group = group),
              color = "#c0c0c0") + 
    geom_line(data = rbind(data.frame(x = seq(0,1,0.05), y = -0.025, group = 1:21),
                           data.frame(x = seq(0,1,0.05), y = 0.025, group = 1:21)),
              aes(x = x, y = y, group = group),
              color = "#c0c0c0") + 
    geom_line(data = data.frame(x = c(0, 1),y = c(0, 0)), aes(x = x, y = y), color = "#c0c0c0") + 
    coord_cartesian(xlim = c(0, 1), ylim = c(-0.105, 0.105))+
    theme_void() +
    theme(axis.title.y.left = element_text(angle = 90, size = 24),
          axis.title.y.right = element_text(angle = -90, size = 24),
          plot.margin = margin(12, 12, 12, 12)) +
    scale_y_continuous(name = "DOG", sec.axis = dup_axis(name = "CAT"))
  if(is.finite(p)){
    plot <- plot + geom_rect(fill = "#FF6622", alpha=0.8)
  }
  plot
}