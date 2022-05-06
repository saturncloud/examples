data <- read.csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/house_price_data_v2.csv") # nolint
model <- lm(sale_price ~ bedroom_abv_gr + year_built, data)

#* Predict price of a house
#* @get /predict
function(bedrooms, year, res) {
  bedrooms <- as.numeric(bedrooms)
  year <- as.numeric(year)
  if (bedrooms >= 0 && bedrooms <= 8 && year >= 1872 && year <= 2100) {
    new_data <- data.frame(bedroom_abv_gr = bedrooms, year_built = year)
    predict(model, newdata = new_data)
  } else {
    res$status <- 400
    list(error = "Must have 0-8 bedrooms and been built between 1872-2100")
  }
}
#* Redirect to Docs
#* @get /
function(res) {
  res$status <- 302 # redirect
  res$setHeader("Location", "./__docs__/")
}