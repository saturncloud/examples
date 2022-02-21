library(rsample)
library(xgboost)
library(Metrics)


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
preprocess_data <- function(df) {
    df_preprocessed <- df %>%
        drop_na()
    return(df_preprocessed)
}

create_split <- function(data) {
    data_split <- initial_split(data, prop = 0.8)
    return(data_split)
}

create_matrices <- function(data) {
    train_test_split <- create_split(data)

    train_df <- training(train_test_split)
    test_df <- testing(train_test_split)

    train_data <- subset(train_df, select = -c(weight_pounds))
    test_data <- subset(test_df, select = -c(weight_pounds))

    dtrain <- xgb.DMatrix(
        data = as.matrix(train_data),
        label = train_df$weight_pounds
    )
    dtest <- xgb.DMatrix(
        data = as.matrix(test_data),
        label = test_df$weight_pounds
    )

    return(list("train" = dtrain, "test" = dtest))
}
train_model <- function(params, dtrain) {
    model <- xgb.train(
        params = params,
        data = dtrain,
        nrounds = 100,
        nthread = 1,
        objective = "reg:squarederror",
    )
    return(model)
}

test_results <- function(model, dtest) {
    results <- predict(model, dtest)
    return(results)
}

create_model_table <- function(data, max_depth) {
    dmatrices <- create_matrices(data)

    dtrain <- dmatrices$train
    dtest <- dmatrices$test

    params <- list("max_depth" = max_depth)

    model <- train_model(params, dtrain)
    results <- test_results(model, dtest)
    return(
        tibble(
            mean_absolute_error = mae(getinfo(dtest, "label"), results),
            params = unlist(params)
        )
    )
}