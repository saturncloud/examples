library(recipes)
library(rsample)
library(keras)


download_data <- function() {
    if (!file.exists("births_data.rds")) {
        download.file(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/birth-data/births_2005.rds",
            "births_data.rds"
        )
    }
    births_raw_data <- readRDS("births_data.rds")

    return(births_raw_data)
}


filter_data <- function(births_raw_data) {
    births_data <- births_raw_data %>%
        select(weight_pounds, is_male, plurality, mother_age, gestation_weeks)

    return(births_data)
}


split_data <- function(births_data) {
    births_data_split <- births_data %>%
        initial_split(prop = 0.2)

    return(births_data_split)
}


prepare_recipe <- function(births_data_split) {
    recipe_object <- births_data_split %>%
        training() %>%
        recipe(weight_pounds ~ .) %>%
        step_naomit(all_outcomes(), all_predictors()) %>%
        step_discretize(
            mother_age,
            options = list(cuts = 5, min_unique = 2)
        ) %>%
        step_discretize(
            gestation_weeks,
            options = list(cuts = 5, min_unique = 2)
        ) %>%
        step_dummy(all_nominal(), -all_outcomes()) %>%
        step_mutate(is_male = ifelse(is_male, 1, 0)) %>%
        step_center(all_predictors(), -all_outcomes()) %>%
        step_scale(all_predictors(), -all_outcomes()) %>%
        prep()

    return(recipe_object)
}

define_model <- function(recipe_object,
                         layer1_units,
                         layer2_units,
                         layer1_activation,
                         layer2_activation) {
    input_shape <- ncol(
        juice(recipe_object, all_predictors(), composition = "matrix")
    )

    keras_model <- keras_model_sequential()

    keras_model %>%
        layer_dense(
            units = layer1_units,
            kernel_initializer = "uniform",
            activation = layer1_activation,
            input_shape = input_shape
        ) %>%
        layer_dropout(rate = 0.1) %>%
        layer_dense(
            units = layer2_units,
            kernel_initializer = "uniform",
            activation = layer2_activation
        ) %>%
        layer_dropout(rate = 0.1) %>%
        layer_dense(
            units = 1,
            kernel_initializer = "uniform",
            activation = "linear"
        ) %>%
        compile(
            optimizer = "adam",
            loss = "mse",
            metrics = list("mean_absolute_error")
        )

    return(keras_model)
}

train_model <- function(recipe_object,
                        layer1_units,
                        layer2_units,
                        layer1_activation,
                        layer2_activation) {
    model <- define_model(
        recipe_object,
        layer1_units,
        layer2_units,
        layer1_activation,
        layer2_activation
    )

    X_train <- juice(recipe_object, all_predictors(), composition = "matrix")
    y_train <- juice(recipe_object, all_outcomes()) %>%
        pull()

    fit(
        object = model,
        x = X_train,
        y = y_train,
        batch_size = 1024,
        epochs = 2,
        validation_split = 0.2,
        verbose = 0
    )

    return(model)
}


test_results <- function(births_data_split, recipe_object, keras_model) {
    testing_data <- bake(recipe_object, testing(births_data_split))
    X_test <- testing_data %>%
        select(-weight_pounds) %>%
        as.matrix()
    y_test <- testing_data %>%
        select(weight_pounds) %>%
        pull()
    results <- keras_model %>%
        evaluate(X_test, y_test)

    return(results)
}

test_model <- function(births_data_split,
                       recipe_object,
                       layer1_units,
                       layer2_units,
                       layer1_activation,
                       layer2_activation) {
    model <- train_model(
        recipe_object,
        layer1_units,
        layer2_units,
        layer1_activation,
        layer2_activation
    )
    results <- test_results(births_data_split, recipe_object, model)
    tibble(
        mean_absolute_error = results[2],
        layer1_units = layer1_units,
        layer2_units = layer2_units,
        layer1_activation = layer1_activation,
        layer2_activation = layer2_activation
    )
}