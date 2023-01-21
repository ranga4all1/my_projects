# Steps:

## 1. Bring `postgres` and `pgadmin` containers up
docker-compose up -d

## 2. ingest data

- wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
- wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

then use - `upload-data-green-taxi.ipynb`

## 3. Login to pgAdmin and run SQL queries

### 3.1 SQL queries

```
SELECT
	COUNT(*)
FROM
	green_taxi_data
WHERE
	lpep_pickup_datetime::date = '2019-01-15';
```


```
SELECT
	date_trunc('day', lpep_pickup_datetime) as pickup_day,
	max(trip_distance) as max_trip
FROM
	green_taxi_data
GROUP BY
	pickup_day
ORDER BY
	max_trip desc;
LIMIT
	1;
```

```
SELECT
	count(passenger_count)
FROM
	green_taxi_data
WHERE
	lpep_pickup_datetime::date = '2019-01-01' and 
	passenger_count = 2;
-- 	passenger_count = 3;
```
