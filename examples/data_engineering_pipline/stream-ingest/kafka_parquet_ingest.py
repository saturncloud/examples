import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# --- 1. Configuration ---
KAFKA_BROKERS = "localhost:9092"
KAFKA_TOPIC = "quickstart-events"
PARQUET_OUTPUT_PATH = "file:///tmp/data_lake/raw_events" # Target Parquet location
CHECKPOINT_PATH = "file:///tmp/spark_checkpoints/kafka_events" # CRITICAL for fault tolerance

# 2. Define Schema for the expected Kafka JSON payload
# This defines the structure of the data we expect to read from the 'value' field of Kafka.
EVENT_SCHEMA = StructType([
    StructField("event_id", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("timestamp_str", StringType(), True), # Raw timestamp string
    StructField("data_value", StringType(), True)
])

# --- 3. Initialize Spark Session ---
def start_spark_session():
    """Initializes Spark Session and loads the Kafka connector."""
    # The Kafka package version MUST match Spark version (3.5.1)
    KAFKA_PACKAGE = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
    
    spark = (
        SparkSession.builder.appName("KafkaToParquetStreamingIngest")
        .config("spark.jars.packages", KAFKA_PACKAGE)
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    print(f"✅ Spark Session started with Kafka package: {KAFKA_PACKAGE}")
    return spark

# --- 4. Main Streaming Pipeline ---
def run_streaming_pipeline(spark):
    
    # --- A. Read Stream from Kafka ---
    print(f"🔗 Reading stream from Kafka topic: {KAFKA_TOPIC}")
    kafka_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BROKERS)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", "latest") # Start processing new events
        .load()
    )

    # --- B. Transformation and Cleaning ---
    processed_df = (
        kafka_df
        # 1. Select and cast Kafka binary 'value' to string
        .select(col("value").cast("string").alias("json_payload"), 
                col("timestamp").alias("kafka_ingest_ts"))
        
        # 2. Parse the JSON string payload into structured columns
        .withColumn("parsed_data", from_json(col("json_payload"), EVENT_SCHEMA))
        
        # 3. Flatten the DataFrame and convert raw timestamp string to proper TimestampType
        .select(
            col("parsed_data.event_id").alias("event_id"),
            col("parsed_data.user_id").alias("user_id"),
            to_timestamp(col("parsed_data.timestamp_str")).alias("event_ts"),
            col("parsed_data.data_value").alias("data_value"),
            col("kafka_ingest_ts")
        )
        # 4. Optional: Watermarking for stateful operations
        # .withWatermark("event_ts", "1 hour") 
    )

    # --- C. Write Stream to Parquet Sink ---
    print(f"💾 Writing stream to Parquet at: {PARQUET_OUTPUT_PATH}")
    print(f"🚧 Using Checkpoint location: {CHECKPOINT_PATH}")
    
    # Clean up previous runs' artifacts
    os.system(f"rm -rf {CHECKPOINT_PATH.replace('file://', '')} {PARQUET_OUTPUT_PATH.replace('file://', '')}")

    query = (
        processed_df.writeStream
        .format("parquet")
        .option("path", PARQUET_OUTPUT_PATH)
        .option("checkpointLocation", CHECKPOINT_PATH) # Guarantees fault tolerance
        .partitionBy("user_id", "event_ts") # Optimized for data lake queries
        .outputMode("append") 
        .trigger(processingTime="30 seconds") # Process micro-batches every 30s
        .start()
    )
    
    return query

if __name__ == "__main__":
    spark = start_spark_session()
    
    try:
        streaming_query = run_streaming_pipeline(spark)
        print("\nStreaming pipeline started. Open a new terminal to produce JSON events.")
        streaming_query.awaitTermination() # Blocks until query is stopped manually
        
    except KeyboardInterrupt:
        print("\nPipeline manually interrupted (Ctrl-C).")
    except Exception as e:
        print(f"\nPipeline failed: {e}")
    finally:
        if 'streaming_query' in locals() and streaming_query.isActive:
            streaming_query.stop()
        spark.stop()
        print("🛑 Spark session stopped.")