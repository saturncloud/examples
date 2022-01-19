library(targets)
library(tarchetypes)
library(future)

source("functions.R")

options(tidyverse.quiet = TRUE)

tar_option_set(
    packages = c(
        "keras",
        "recipes",
        "rmarkdown",
        "rsample",
        "tidyverse",
        "shiny"
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
        data_split,
        split_data(data),
        format = "qs",
        deployment = "main"
    ),
    tar_target(
        recipe,
        prepare_recipe(data_split),
        format = "qs",
        deployment = "main"
    ),
    tar_target(
        layer1_units,
        c(8, 16, 32),
        deployment = "main"
    ),
    tar_target(
        layer2_units,
        c(16),
        deployment = "main"
    ),
    tar_target(
        layer1_activation,
        c("relu", "sigmoid"),
        deployment = "main"
    ),
    tar_target(
        layer2_activation,
        c("relu"),
        deployment = "main"
    ),
    tar_target(
        run,
        test_model(
            data_split,
            recipe, layer1_units,
            layer2_units,
            layer1_activation,
            layer2_activation
        ),
        pattern = cross(layer1_units, layer1_activation),
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
