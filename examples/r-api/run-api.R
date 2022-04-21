library(dplyr)
library(plumber)
plumber::pr_run(plumber::plumb("endpoints.R"), port = 8000, host = "0.0.0.0")
