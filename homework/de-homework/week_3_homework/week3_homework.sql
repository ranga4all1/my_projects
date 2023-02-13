-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-375303.fhv.external_fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://fhv-ranga/tripdata-2019/fhv_tripdata_2019-*.csv.gz']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE dtc-de-375303.fhv.fhv_tripdata_non_partitioned AS
SELECT * FROM dtc-de-375303.fhv.external_fhv_tripdata;

-- Question 1:
-- What is the count for fhv vehicle records for year 2019?
SELECT COUNT(1) FROM dtc-de-375303.fhv.external_fhv_tripdata;
SELECT COUNT(*) FROM dtc-de-375303.fhv.fhv_tripdata_non_partitioned;
-- anwser: 43244696

-- Question 2:
-- Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.
-- What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
SELECT COUNT(DISTINCT Affiliated_base_number)
FROM dtc-de-375303.fhv.external_fhv_tripdata;

SELECT COUNT(DISTINCT Affiliated_base_number)
FROM dtc-de-375303.fhv.fhv_tripdata_non_partitioned;
-- answer: 0 MB for the External Table and 317.94MB for the BQ Table

-- Question 3:
-- How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
SELECT COUNT(*)
FROM dtc-de-375303.fhv.external_fhv_tripdata
WHERE PUlocationID IS NULL;

SELECT COUNT(*)
FROM dtc-de-375303.fhv.external_fhv_tripdata
WHERE DOlocationID IS NULL;

SELECT COUNT(*)
FROM dtc-de-375303.fhv.fhv_tripdata_non_partitioned
WHERE PUlocationID IS NULL;

SELECT COUNT(*)
FROM dtc-de-375303.fhv.fhv_tripdata_non_partitioned
WHERE DOlocationID IS NULL;

-- 2024066
-- 723689
-- 2024066
-- 723689
-- Total: (2024066 + 723689) * 2 = 5495510

-- alternate way to count NULL in column
SELECT
     SUM(CASE WHEN DOlocationID IS NULL THEN 1 ELSE 0 END) AS null_value_count      
    ,COUNT(DOlocationID) AS non_null_value_count
FROM dtc-de-375303.fhv.fhv_tripdata_non_partitioned;

-- answer: 0 MB for the External Table and 317.94MB for the Materialized Table


-- Question 4
-- What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?
-- answer: Partition by pickup_datetime Cluster on affiliated_base_number

-- Question 5
-- Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).
-- Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE dtc-de-375303.fhv.tripdata_partitoned_clustered
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
SELECT * FROM dtc-de-375303.fhv.fhv_tripdata_non_partitioned;

-- Query scans 647.87 MB
SELECT COUNT(DISTINCT Affiliated_base_number)
FROM dtc-de-375303.fhv.fhv_tripdata_non_partitioned
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

-- Query scans  23.05 MB
SELECT COUNT(DISTINCT Affiliated_base_number)
FROM dtc-de-375303.fhv.tripdata_partitoned_clustered
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

-- answer: 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table


-- Question 6
-- Where is the data stored in the External Table you created?
-- answer: GCP Bucket

-- Question 7
-- It is best practice in Big Query to always cluster your data?
-- True    -> ideal preference - 1. partition, 2. cluster
