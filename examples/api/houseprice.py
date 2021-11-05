from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.linear_model import LinearRegression

app = FastAPI()
df = pd.read_csv(
    "https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv"
)
lr = LinearRegression()
lr.fit(df[["BedroomAbvGr", "YearBuilt"]], df["SalePrice"])


@app.get("/predict")
async def predict(BedroomAbvGr: int = None, YearBuilt: int = None):
    a = pd.DataFrame([[BedroomAbvGr, YearBuilt]], columns=["BedroomAbvGr", "YearBuilt"])
    v = lr.predict(a)
    if not ((0 <= BedroomAbvGr <= 8) and (1872 <= YearBuilt <= 2100)):

        raise HTTPException(
            status_code=400,
            detail="Please enter BedroomAbvGr between 0 and 8. Enter YearBuilt between 1872 and 2100",
        )

    return {"prediction": v[0]}
