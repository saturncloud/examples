-- Run this script from inside a Snowflake worksheet

create database nyc_taxi;

create or replace stage taxi_stage url='s3://nyc-tlc/';

list @taxi_stage/  pattern = '.*trip.data/yellow.*';

create or replace table taxi_yellow (
    csv_filename varchar                   -- 2020   2016
  , vendorid int                           --    1      1
  , tpep_pickup_datetime timestamp_ntz     --    2      2
  , tpep_dropoff_datetime timestamp_ntz    --    3      3
  , passenger_count int                    --    4      4
  , pickup_longitude varchar               --           6
  , pickup_latitude varchar                --           7
  , trip_distance float                    --    5      5
  , ratecodeid int                         --    6      8
  , store_and_fwd_flag varchar             --    7      9
  , dropoff_longitude varchar              --          10
  , dropoff_latitude varchar               --          11
  , pulocationid int                       --    8
  , dolocationid int                       --    9
  , payment_type int                       --   10     12
  , fare_amount float                      --   11     13
  , extra float                            --   12     14
  , mta_tax float                          --   13     15
  , tip_amount float                       --   14     16
  , tolls_amount float                     --   15     17
  , improvement_surcharge float            --   16     18
  , total_amount float                     --   17     19
  , congestion_surcharge float             --   18     
);


create warehouse taxi_wh;

-- Load 2020 Yellow Cab data
copy into taxi_yellow from (
select metadata$filename, $1, $2, $3, $4, NULL, NULL, $5, $6, $7, NULL, NULL, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18
from @taxi_stage/) pattern='.*trip.data/yellow.*2020.*' file_format = (type = csv skip_header = 1);

-- Load 2019 Yellow Cab data
copy into taxi_yellow from (
select metadata$filename, $1, $2, $3, $4, NULL, NULL, $5, $6, $7, NULL, NULL, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18
from @taxi_stage/) pattern='.*trip.data/yellow.*2019.*' file_format = (type = csv skip_header = 1);

-- Load 2018 Yellow Cab data
copy into taxi_yellow from (
select metadata$filename, $1, $2, $3, $4, NULL, NULL, $5, $6, $7, NULL, NULL, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, 0
from @taxi_stage/) pattern='.*trip.data/yellow.*2018.*' file_format = (type = csv skip_header = 1);


-- Load 2017 Yellow Cab data
copy into taxi_yellow from (
select metadata$filename, $1, $2, $3, $4, NULL, NULL, $5, $6, $7, NULL, NULL, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, 0
from @taxi_stage/) pattern='.*trip.data/yellow.*2017.*' file_format = (type = csv skip_header = 1);

-- delete blank lines
delete from taxi_yellow where vendorid is null and tpep_pickup_datetime is null;

-- grant privileges
GRANT ALL PRIVILEGES ON DATABASE NYC_TAXI TO ROLE SYSADMIN;