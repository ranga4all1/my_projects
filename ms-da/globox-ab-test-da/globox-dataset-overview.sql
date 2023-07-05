-- Understanding the GloBox Database

-- 1. Can a user show up more than once in the activity table? Yes or no, and why?
SELECT * 
FROM "activity"
LIMIT 10;

-- check null values
SELECT * 
FROM "activity"
WHERE device IS NULL;

SELECT COUNT(uid) 
FROM "activity";

-- 2223

SELECT COUNT(DISTINCT uid) 
FROM "activity";

-- 2094

SELECT COUNT(uid) AS total_count, COUNT(DISTINCT uid) AS distinct_count
FROM "activity";
-- | total_count | distinct_count |
-- | ----------- | -------------- |
-- | 2233        | 2094           |


-- Final query
-- Get list of uid that repeated 
SELECT uid, COUNT(uid) AS repeat_count
FROM "activity"
GROUP BY uid
HAVING COUNT(uid) > 1;

-- Yes - a user can make purchases on multiple days
-- Above list shows uid's that repeated

-- Diff between COUNT(uid) and COUNT(DISTINCT uid) is (2223 - 2094) = 129. 
-- This means a few user id repeated more than once.
-- Also, per ERD: activity: user purchase activity, containing 1 row per day that a user made a purchase

-------------

-- Collect basic db info

-- What columns are in your database?
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name;

-- A VIEW of all your columns
-- 1) Create a new view called table_columns
DROP VIEW IF EXISTS table_columns;

CREATE VIEW table_columns AS
  (SELECT table_name, 
       STRING_AGG(column_name, ', ') AS columns
  FROM information_schema.columns
  WHERE table_schema = 'public'
  GROUP BY table_name);
-- 2) Query the newly created view table_columns
SELECT *
FROM table_columns;

/*
| table_name    | columns                     |
| ------------- | --------------------------- |
| groups        | uid, group, join_dt, device |        |
| users         | id, country, gender         |
| activity      | uid, dt, device, spent      |
*/
-------------

-- 2. What type of join should we use to join the users table to the activity table?

-- Need to include all users even if they did not make purchase
-- LEFT join
-- users(id) --> groups(uid) --> activity(uid) 

-- using LEFT join
SELECT u.id, u.country, u.gender,
		g.device, g.group, SUM(COALESCE(a.spent::numeric, 0)) AS total_spent,
		CASE
			WHEN SUM(COALESCE(a.spent::numeric, 0)) > 0 THEN 'Yes'
			ELSE 'No'
		END 
		AS is_converted
		
FROM "groups" AS g
LEFT JOIN "users" AS u 
ON g.uid = u.id
LEFT JOIN "activity" AS a
ON g.uid = a.uid
GROUP BY u.id, u.country, u.gender,
	g.device, g.group
ORDER BY u.id;

-- using FULL join
SELECT u.id, u.country, u.gender,
		g.device, g.group, SUM(COALESCE(a.spent::numeric, 0)) AS total_spent,
		CASE
			WHEN SUM(COALESCE(a.spent::numeric, 0)) > 0 THEN 'Yes'
			ELSE 'No'
		END 
		AS is_converted
		
FROM "groups" AS g
FULL JOIN "users" AS u 
ON g.uid = u.id
FULL JOIN "activity" AS a
ON g.uid = a.uid
GROUP BY u.id, u.country, u.gender,
	g.device, g.group
ORDER BY u.id;


-------------

-- 3. What SQL function can we use to fill in NULL values?

-- ISNULL() function	# not available in Postgres
-- CASE statement
-- COALESCE() function # For Postgres

-- check null values
SELECT * 
FROM "activity"
WHERE device IS NULL;

-- way to replace with ISNULL()
SELECT *, ISNULL(device, 'no_device_info') AS device 
FROM "activity"
WHERE device IS NULL;

-- way to replace with COALESCE()
SELECT *, COALESCE(device, 'no_device_info') AS device_updated
FROM "activity"
WHERE device IS NULL;

-------------

-- 4. What are the start and end dates of the experiment?

-- get start date
SELECT *
FROM "groups"
ORDER BY join_dt;
-- 2023-01-25

-- get end date
SELECT * 
FROM "groups"
ORDER BY join_dt DESC;
-- 2023-02-06

-- Final query 
-- to get start and end dates
SELECT MIN(join_dt) AS start_date, MAX(join_dt) AS end_date 
FROM "groups";

/*
| start_date | end_date   |
| ---------- | ---------- |
| 2023-01-25 | 2023-02-06 |
*/

-------------

-- 5. How many total users were in the experiment?

-- Users in experiment with purchase activity
SELECT COUNT(DISTINCT uid) 
FROM "activity";
-- 2094

-- Final query
-- All users:
SELECT COUNT(*) 
FROM "users";
-- or
SELECT COUNT(DISTINCT id) 
FROM "users";
-- or
SELECT COUNT(DISTINCT uid) 
FROM "groups";
-- 48943

-------------

-- 6. How many users were in the control and treatment groups?
-- A : Control group
-- B : Experiment group

SELECT "group", COUNT(DISTINCT uid) AS count_per_group
FROM "groups"
GROUP BY "group";

/*
| group | count_per_group |
| ----- | --------------- |
| A     | 24343           |
| B     | 24600           |
*/
-------------

-- 7. What was the conversion rate of all users?

-- conversion rate of all users
WITH all_users
	AS (SELECT COUNT(DISTINCT id) AS all_count
		FROM "users"),

	converted_users
	AS (SELECT COUNT(DISTINCT uid) AS converted_count
	FROM "activity"),

	conversion_rate 
	AS (SELECT (converted_users.converted_count::numeric / all_users.all_count::numeric)
		AS conversion_rate
		FROM all_users, converted_users)

SELECT ROUND((conversion_rate*100),2) AS conversion_rate_percent
FROM   conversion_rate;
-- 4.28

-- another way
WITH globox
AS (
SELECT u.id, u.country, u.gender,
			g.device, g.group, SUM(COALESCE(a.spent::numeric, 0)) AS total_spent,
			CASE
				WHEN SUM(COALESCE(a.spent::numeric, 0)) > 0 THEN '1'
				ELSE '0'
			END 
			AS is_converted

	FROM "groups" AS g
	LEFT JOIN "users" AS u 
	ON g.uid = u.id
	LEFT JOIN "activity" AS a
	ON g.uid = a.uid
	GROUP BY u.id, u.country, u.gender,
		g.device, g.group
	ORDER BY u.id)

SELECT ROUND(SUM(is_converted::numeric) / COUNT(is_converted::numeric)*100, 2) AS conversion_rate_percent
FROM globox;

/*
| conversion_rate_percent |
| ----------------------- |
| 4.28                    |
*/

-------------

-- 8. What is the user conversion rate for the control and treatment groups?

SELECT COUNT(DISTINCT a.uid) AS count_cg
	FROM "groups" AS g
	INNER JOIN "activity" as a
	ON g.uid = a.uid
	WHERE "group" = 'A'
-- -955

SELECT COUNT(DISTINCT a.uid) AS count_cg
	FROM "groups" AS g
	INNER JOIN "activity" as a
	ON g.uid = a.uid
	WHERE "group" = 'B'
-- 1139

SELECT COUNT(DISTINCT id) AS all_count
		FROM "users"
-- 48943

SELECT "group", COUNT(DISTINCT uid) AS count_control
FROM "groups"
WHERE "group" = 'A'
GROUP BY "group"
-- 24343

SELECT "group", COUNT(DISTINCT uid) AS count_experiment
FROM "groups"
WHERE "group" = 'B'
GROUP BY "group"
-- 24600

-- conversion rate for the control and treatment groups
WITH cg_users
	AS (SELECT COUNT(DISTINCT a.uid) AS count_cg
	FROM "groups" AS g
	INNER JOIN "activity" as a
	ON g.uid = a.uid
	WHERE "group" = 'A'),
	
	tg_users
	AS (SELECT COUNT(DISTINCT a.uid) AS count_tg
	FROM "groups" AS g
	INNER JOIN "activity" as a
	ON g.uid = a.uid
	WHERE "group" = 'B'),

	control_users
	AS (SELECT "group", COUNT(DISTINCT uid) AS count_control
	FROM "groups"
	WHERE "group" = 'A'
	GROUP BY "group"),

	experiment_users
	AS (SELECT "group", COUNT(DISTINCT uid) AS count_experiment
	FROM "groups"
	WHERE "group" = 'B'
	GROUP BY "group"),

	cg_conversion_rate 
	AS (SELECT (cg_users.count_cg::numeric / control_users.count_control::numeric )
		AS cg_conversion_rate
		FROM cg_users, control_users),
	
	tg_conversion_rate 
	AS (SELECT (tg_users.count_tg::numeric / experiment_users.count_experiment::numeric )
		AS tg_conversion_rate
		FROM tg_users, experiment_users)

SELECT ROUND((cg_conversion_rate*100),2) AS cg_conversion_rate_percent,
	   ROUND((tg_conversion_rate*100),2) AS tg_conversion_rate_percent
FROM   cg_conversion_rate, tg_conversion_rate;

/*
| cg_conversion_rate_percent | tg_conversion_rate_percent |
| -------------------------- | -------------------------- |
| 3.92                       | 4.63                       |
*/

-- another way
WITH globox
AS (
SELECT u.id, u.country, u.gender,
			g.device, g.group, SUM(COALESCE(a.spent::numeric, 0)) AS total_spent,
			CASE
				WHEN SUM(COALESCE(a.spent::numeric, 0)) > 0 THEN '1'
				ELSE '0'
			END 
			AS is_converted

	FROM "groups" AS g
	LEFT JOIN "users" AS u 
	ON g.uid = u.id
	LEFT JOIN "activity" AS a
	ON g.uid = a.uid
	GROUP BY u.id, u.country, u.gender,
		g.device, g.group
	ORDER BY u.id)

SELECT "group", ROUND(SUM(is_converted::numeric) / COUNT(is_converted::numeric)*100, 2) AS conversion_rate_percent
FROM globox
GROUP BY "group"
ORDER BY "group";

/*
| group | conversion_rate_percent |
| ----- | ----------------------- |
| A     | 3.92                    |
| B     | 4.63                    |
*/

-------------

-- 9. What is the average amount spent per user for the control and treatment groups, 
-- 		including users who did not convert?

WITH globox
AS (
SELECT u.id, u.country, u.gender,
			g.device, g.group, SUM(COALESCE(a.spent::numeric, 0)) AS total_spent,
			CASE
				WHEN SUM(COALESCE(a.spent::numeric, 0)) > 0 THEN 'Yes'
				ELSE 'No'
			END 
			AS is_converted

	FROM "groups" AS g
	LEFT JOIN "users" AS u 
	ON g.uid = u.id
	LEFT JOIN "activity" AS a
	ON g.uid = a.uid
	GROUP BY u.id, u.country, u.gender,
		g.device, g.group
	ORDER BY u.id)

SELECT "group", AVG(COALESCE(total_spent::numeric, 0)) AS avg_spent
FROM globox
GROUP BY "group"
ORDER BY "group";

/*
| group | avg_spent          |
| ----- | ------------------ |
| A     | 3.3745184679288412 |
| B     | 3.3908669458857832 |
*/

-------------

-- 10. Why does it matter to include users who did not convert 
-- 		when calculating the average amount spent per user?
/*
In order to measure the impact on total revenue(amount spent),
we cannot only average the users who converted because there
could have been fewer users who converted in the treatment.

More info: When we think about how much revenue a company is making, two things matter:
	1) How many users/customers are making purchases
	2) How much money users/customers are spending, when they do
	The experiment could result in more users converting, but spending less when they do. Or, it could result in fewer users converting, but spending more when they do.
*/

-------------


-- Write a SQL query that returns: the user ID, the user’s country, the user’s gender, the user’s device type, the user’s test group, whether or not they converted (spent > $0), and how much they spent in total ($0+). 

DROP VIEW IF EXISTS globox;

CREATE VIEW globox
AS
	(SELECT u.id, u.country, u.gender,
			g.device, g.group, SUM(COALESCE(a.spent::numeric, 0)) AS total_spent,
			CASE
				WHEN SUM(COALESCE(a.spent::numeric, 0)) > 0 THEN 'Yes'
				ELSE 'No'
			END 
			AS is_converted

	FROM "groups" AS g
	LEFT JOIN "users" AS u 
	ON g.uid = u.id
	LEFT JOIN "activity" AS a
	ON g.uid = a.uid
	GROUP BY u.id, u.country, u.gender,
		g.device, g.group
	ORDER BY u.id);

SELECT * 
FROM globox;


-- alternate way
select u.id as user_id,
    g.group as test_group,
    u.country, u.gender, g.device,
    sum(coalesce(a.spent,0)) as amount_spent,
    case when sum(a.spent) > 0 then 1 else 0 end 
        as converted
from users as u
inner join groups as g
    on u.id = g.uid
left join activity as a
    on u.id = a.uid
group by 1,2,3,4,5;
-------------

--alternate way with dates included (only first date per user)
SELECT g.uid, g.join_dt AS date_joined, u.country, u.gender, a.dt AS date_converted,
			g.device, g.group, SUM(COALESCE(a.spent::numeric, 0)) AS total_spent,
			CASE
				WHEN SUM(COALESCE(a.spent::numeric, 0)) > 0 THEN 1
				ELSE 0
			END 
			AS is_converted

	FROM "groups" AS g
	INNER JOIN "users" AS u 
	ON g.uid = u.id
	LEFT JOIN "activity" AS a
	ON g.uid = a.uid
	GROUP BY g.uid, g.join_dt, a.dt, u.country, u.gender,
		g.device, g.group
	ORDER BY g.uid;

-------------

-- Query for checking novelty effect

with join_dt_agg as (
  select g.join_dt as dt, g.group as test_group,
    count(distinct u.id) as user_count
  from users as u
  inner join groups as g
      on u.id = g.uid
  group by 1,2
),

convert_dt_agg as (
  select a.dt, g.group as test_group,
    count(distinct a.uid) as converted_user_count
  from groups as g
  left join activity as a
      on g.uid = a.uid
  group by 1,2
),

cumulative_users as (
  select j.test_group, j.dt, 
    j.user_count, c.converted_user_count,
    sum(j.user_count) over (partition by j.test_group order by j.dt) as cum_users,
    sum(c.converted_user_count) over (partition by j.test_group order by j.dt) as cum_converted_users
  from join_dt_agg as j
  inner join convert_dt_agg as c
    on j.dt = c.dt and j.test_group = c.test_group
  order by 1,2
),

cumulative_conversion as (
  select *, cum_converted_users/cum_users as cum_conversion_rate
  from cumulative_users
)

select a.dt,
	a.cum_conversion_rate as a_cum_convert,
  b.cum_conversion_rate as b_cum_convert,
  b.cum_conversion_rate - a.cum_conversion_rate as cum_diff
from cumulative_conversion as a
inner join cumulative_conversion as b
	on a.dt = b.dt
  and a.test_group = 'A' and b.test_group = 'B';
