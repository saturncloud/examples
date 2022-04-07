# Example R Script

# This R script uses some of the pre-installed packages in the RStudio Saturn Cloud image
# After running the code below, you should see a plot in the viewer pane.

library(tidyverse)

library(ggplot2)
library(tidyr)

n <- 25

data <- data.frame(
  text = sample(c("welcome", "to", "Saturn Cloud"), n, replace = TRUE),
  size = abs(rnorm(n)),
  x = runif(n),
  y = runif(n)
)

ggplot(data, aes(x = x, y = y, label = text, size = size)) +
  geom_text(color = "#ff6721") +
  theme_minimal() +
  theme(legend.position = "none")
