create database nyc_taxi;

create or replace stage taxi_stage url='s3://nyc-tlc/';

list @taxi_stage/  pattern = '.*trip.data/yellow.*';

create or replace table taxi_yellow (
    csv_filename varchar
  , vendorid int
  , pickup_datetime timestamp_ntz
  , dropoff_datetime timestamp_ntz
  , passenger_count int
  , pickup_longitude varchar
  , pickup_latitude varchar
  , trip_distance float
  , ratecodeid int
  , store_and_fwd_flag varchar
  , dropoff_longitude varchar
  , dropoff_latitude varchar
  , pickup_taxizone_id int
  , dropoff_taxizone_id int
  , payment_type int
  , fare_amount float
  , extra float
  , mta_tax float
  , tip_amount float
  , tolls_amount float
  , improvement_surcharge float
  , total_amount float
  , congestion_surcharge float
);

-- Load 2019 Yellow Cab data
copy into taxi_yellow from (
    select
        metadata$filename, 
        $1, 
        $2, 
        $3, 
        $4,
        NULL,
        NULL, 
        $5, 
        $6, 
        $7, 
        NULL,
        NULL, 
        $8, 
        $9, 
        $10, 
        $11, 
        $12, 
        $13, 
        $14,
        $15,
        $16, 
        $17, 
        $18
        from 
            @taxi_stage/
)
pattern='.*trip.data/yellow.*2019.*'
file_format = (type = csv skip_header = 1);

-- Load 2018 Yellow Cab data
copy into taxi_yellow from (
    select
        metadata$filename, 
        $1, 
        $2, 
        $3,
        $4, 
        NULL,
        NULL, 
        $5, 
        $6,
        $7, 
        NULL,
        NULL, 
        $8, 
        $9, 
        $10,
        $11, 
        $12, 
        $13, 
        $14, 
        $15, 
        $16, 
        $17, 
        0
    from 
        @taxi_stage/
) 
pattern='.*trip.data/yellow.*2018.*'
file_format = (type = csv skip_header = 1);


-- Load 2017 Yellow Cab data
copy into taxi_yellow from (
    select 
        metadata$filename,
        $1, 
        $2, 
        $3,
        $4, 
        NULL, 
        NULL, 
        $5, 
        $6, 
        $7, 
        NULL, 
        NULL, 
        $8,
        $9, 
        $10, 
        $11, 
        $12, 
        $13, 
        $14, 
        $15, 
        $16, 
        $17,
        0
    from 
        @taxi_stage/
) 
pattern='.*trip.data/yellow.*2017.*' 
file_format = (type = csv skip_header = 1);

-- delete blank lines
delete from taxi_yellow where vendorid is null and pickup_datetime is null;

-- grant privileges
GRANT ALL PRIVILEGES ON DATABASE NYC_TAXI TO ROLE SYSADMIN;
