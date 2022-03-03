library(targets)
library(tarchetypes)
library(future)

source("functions.R")

options(tidyverse.quiet = TRUE)

tar_option_set(
    packages = c(
        "xgboost",
        "rmarkdown",
        "rsample",
        "tidyverse",
        "shiny",
        "Metrics"
    )
)

plan(multisession)

list(
    tar_target(
        data_download,
        download_data(),
        format = "qs",
        deployment = "main"
    ),
    tar_target(
        data,
        filter_data(data_download),
        format = "qs",
        deployment = "main"
    ),
    tar_target(
        preprocessed_data,
        preprocess_data(data),
        format = "qs",
        deployment = "main"
    ),
    tar_target(
        max_depth,
        seq(1, 8),
        deployment = "main"
    ),
    tar_target(
        run,
        create_model_table(
            preprocessed_data,
            max_depth
        ),
        pattern = cross(max_depth),
        format = "fst_tbl"
    ),
    tar_target(
        best_run,
        run %>%
            top_n(-1, mean_absolute_error) %>%
            head(1),
        format = "fst_tbl",
        deployment = "main"
    ),
    tar_render(report, "report.Rmd")
)