from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
df = pd.read_csv(
    "https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv"
)
linear_regression = LinearRegression().fit(df[["BedroomAbvGr", "YearBuilt"]], df["SalePrice"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    bedrooms = int(request.form["bedrooms"])
    year_built = int(request.form["year_built"])

    if not ((1 <= bedrooms <= 8) and (1872 <= year_built <= 2100)):
        return render_template(
            "index.html",
            data="Invalid entry. Please enter a number of bedrooms between 1 and 8 and a year built between 1872 and 2100.",
        )

    input = pd.DataFrame([[bedrooms, year_built]], columns=["BedroomAbvGr", "YearBuilt"])
    prediction = linear_regression.predict(input)

    return render_template("index.html", data=f"The house price is: ${int(prediction)}.")
