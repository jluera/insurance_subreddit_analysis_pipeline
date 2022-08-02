'''
For the queries below you will need to replace @project.@dataset_id.@table_id
with the actual project id, dataset id and table id you are using.
'''

-- Post Count By Day
CREATE VIEW insurance_sub_dataset.post_by_day_view AS (
SELECT 
  extract(DATE from created_utc) as posts_by_day,
  COUNT(id)
FROM `@project.@dataset_id.@table_id` 
GROUP BY posts_by_day 
ORDER BY posts_by_day
);

-- Subscribers Over Time
CREATE VIEW insurance_sub_dataset.subscribers_over_time_view AS (
SELECT 
  extract(DATE from created_utc) as post_date,
  ROUND(AVG(subreddit_subscribers),0) AS amount_subscribers
FROM `@project.@dataset_id.@table_id` 
GROUP BY post_date 
ORDER BY post_date
);

-- Top 10 Users Post Count
CREATE VIEW insurance_sub_dataset.top_ten_users_post_count_view AS (
SELECT author, count(id) as posts
FROM `@project.@dataset_id.@table_id` 
GROUP BY author
ORDER BY posts DESC LIMIT 10
);

-- Optional Materialized View Of Key Columns (Optional)
CREATE MATERIALIZED VIEW insurance_sub_dataset.key_columns_view AS (
SELECT 
  id,
  created_utc,
  extract(DATE from created_utc) as date,
  link_flair_text as category,
  title,
  subreddit_subscribers
FROM `@project.@dataset_id.@table_id` 
ORDER BY created_utc
);
