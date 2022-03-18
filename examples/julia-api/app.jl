using Genie
using CSV
using AWSS3
using AWS
using GLM
using DataFrames

using Genie.Router


df = DataFrame(CSV.File(AWSS3.read(S3Path("s3://saturn-public-data/examples/dashboard/housePriceData.csv", config=global_aws_config(; region="us-east-2")))))

formula = @formula(SalePrice ~ BedroomAbvGr + YearBuilt)
linear_regressor = lm(formula, df)

Genie.config.run_as_server = true

route("/predict") do
    bedrooms = parse(Int64, params(:bedrooms, 1))
    yearBuilt = YearBuilt = parse(Int64, params(:yearBuilt, 1872))

    if !((1 <= bedrooms <= 8) && (1872 <= yearBuilt <= 2100))
        return ("Please enter a number of bedrooms between 1 and 8 and a year built between 1872 and 2100.")
    end

    prediction = predict(linear_regressor, DataFrame(BedroomAbvGr=bedrooms, YearBuilt=yearBuilt))
    prediction = round(prediction[1])
    return ("The prediction for a house with $bedrooms bedrooms built in $yearBuilt is \$$prediction.")
end

route("/") do
    return ("This API returns a linear regression for the price of a house based on the number of bedrooms and the year it was built. For example, append /predict?bedrooms=2&yearBuilt=1900 to the url to predict the sale price for a house built in 1900 with 2 bedrooms.")
end

Genie.startup(8000, "0.0.0.0")