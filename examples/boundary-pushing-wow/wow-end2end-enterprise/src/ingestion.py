import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from datetime import datetime, timedelta

def run_ingestion():
    spark = SparkSession.builder.appName("EnterpriseIngestion").getOrCreate()
    
    # 1. Generate Synthetic Data
    data = [
        (101, 50.5, datetime.now() - timedelta(days=1)),
        (101, 150.0, datetime.now() - timedelta(hours=2)),
        (102, 20.0, datetime.now() - timedelta(days=2)),
    ]
    columns = ["user_id", "amount", "event_timestamp"]
    df = spark.createDataFrame(data, columns)

    # 2. Feature Engineering: Calculate total spend per user
    # Feast requires an 'event_timestamp' for time-travel
    features_df = df.groupBy("user_id").agg(
        F.sum("amount").alias("total_spend"),
        F.max("event_timestamp").alias("event_timestamp")
    ).withColumn("created_timestamp", F.current_timestamp())

    # 3. Save to Offline Store (Parquet)
    output_path = "/workspace/data/user_features.parquet"
    features_df.write.mode("overwrite").parquet(output_path)
    print(f"✅ Features ingested to {output_path}")

if __name__ == "__main__":
    run_ingestion()