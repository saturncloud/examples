# production_pipeline.py
import os
os.environ['NUMBA_CUDA_ENABLE_PYNVJITLINK'] = '1'

import findspark
findspark.init('/workspace/sparkRapid/spark-4.0.1-bin-hadoop3')

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import cudf
import cuml
import cupy as cp

print("🏭 Production RAPIDS + Spark Pipeline")
print("=" * 50)

class ProductionPipeline:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Production-RAPIDS-Pipeline") \
            .config("spark.sql.adaptive.enabled", "true") \
            .getOrCreate()
    
    def process_large_dataset(self):
        """Simulate processing large dataset"""
        print("📊 Processing large dataset...")
        
        # Simulate large dataset (in production, this would be from HDFS/S3)
        data = [(i, f"user_{i}", i % 100, 50000 + (i % 1000) * 100, 25 + (i % 40)) 
                for i in range(50000)]
        
        columns = ["id", "name", "department", "salary", "age"]
        spark_df = self.spark.createDataFrame(data, columns)
        
        # Spark ETL
        aggregated = spark_df \
            .groupBy("department") \
            .agg(
                count("*").alias("user_count"),
                avg("salary").alias("avg_salary"),
                avg("age").alias("avg_age"),
                stddev("salary").alias("salary_stddev")
            )
        
        print(f"✅ Spark processed {spark_df.count():,} records")
        return aggregated
    
    def gpu_acceleration(self, spark_df):
        """GPU-accelerated processing"""
        print("⚡ GPU acceleration with RAPIDS...")
        
        # Convert to cuDF
        pandas_df = spark_df.toPandas()
        gpu_df = cudf.from_pandas(pandas_df)
        
        # Advanced GPU operations
        gpu_df['log_salary'] = cp.log(gpu_df['avg_salary'])
        gpu_df['salary_efficiency'] = gpu_df['avg_salary'] / gpu_df['user_count']
        
        # cuML clustering
        from cuml.cluster import KMeans
        features = gpu_df[['avg_salary', 'avg_age', 'user_count']].fillna(0)
        
        kmeans = KMeans(n_clusters=4, random_state=42)
        gpu_df['cluster'] = kmeans.fit_predict(features)
        
        print(f"✅ GPU processing completed: {gpu_df.shape}")
        return gpu_df
    
    def run(self):
        try:
            # Stage 1: Spark distributed processing
            spark_result = self.process_large_dataset()
            
            # Stage 2: GPU acceleration
            final_result = self.gpu_acceleration(spark_result)
            
            print("\n🎯 FINAL RESULTS:")
            print("=" * 30)
            print(f"Total departments: {len(final_result)}")
            print(f"Features created: {len(final_result.columns)}")
            print(f"Clusters identified: {final_result['cluster'].nunique()}")
            print("\nSample output:")
            print(final_result[['department', 'avg_salary', 'cluster']].head(10))
            
            return final_result
            
        finally:
            self.spark.stop()

if __name__ == "__main__":
    pipeline = ProductionPipeline()
    result = pipeline.run()
    print("\n🎉 Production pipeline completed successfully!")

