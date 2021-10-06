from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.linear_model import LinearRegression

app = FastAPI()


@app.get('/predict')
async def predict(BedroomAbvGr: int = 3, YearBuilt: int = 2000):
    df = pd.read_csv("https://saturn-public-data.s3.us-east-2.amazonaws.com/examples/dashboard/housePriceData.csv")
    lr = LinearRegression()
    lr.fit(df[['BedroomAbvGr', 'YearBuilt']], df['SalePrice'])
    a = pd.DataFrame([[BedroomAbvGr, YearBuilt]], columns=['BedroomAbvGr', 'YearBuilt'])
    v = lr.predict(a)
    if v <= 0:
        raise HTTPException(status_code=400,
                            detail="Please enter BedroomAbvGr between 0 and 8. Enter YearBuilt greater than 1872")

    return {'prediction': v[0]}