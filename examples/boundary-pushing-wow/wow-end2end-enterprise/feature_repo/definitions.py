from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

# Define the 'Entity' (The object we are tracking)
user = Entity(name="user_id", join_keys=["user_id"])

# Define the 'Source' (The Spark output)
user_source = FileSource(
    path="/workspace/data/user_features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# Define the 'Feature View'
user_stats_view = FeatureView(
    name="user_stats",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total_spend", dtype=Float32),
    ],
    online=True,
    source=user_source,
)