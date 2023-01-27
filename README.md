# Reddit /r/insurance ETLT Pipeline

An EtLT pipeline to do the following to extract and transform the initial post comments from the [r/insurance](https://www.reddit.com/r/insurance/) subreddit.

## Motivation

This project was designed to exercise pratical Data Engineering skills.  It was inspired by work done in relation to the datatalks.club Data Engineering Zoomcamp and is a follow up on projects completed during that course.

## Architecture

1) Spin up Google Cloud Resources via Terraform.
2) Run three scripts in Airflow running in a docker container.
3) The first script retrieves user posting data from Reddit's /r/Insurance subreddit using the Pushift API. It then reduces columns with Pandas and saves dataframe as a parquet file.
4) The second script performs simple transformations and data cleaning using PySpark.
5) The third script loads data into Google Cloud Storage and BigQuery for further analysis .
6) The data can then be imported into Google DataStudio to make a dashboard of relevant information.

Admittedly, some of the leveraged components, such as the use of Airflow, is kind of overkill for a simple pipeline like this but was utilized just to gain additional practice.

## Dashboard

The final dashboard can be configured as required but should look something like this:

This was created via Google Data Studio (Now called Google Looker Studio).

[insurance_subreddit_stats_dash.pdf](https://github.com/jluera/insurance_sub_pipeline/files/9134594/insurance_subreddit_stats_dash.pdf)
![insurance_sub_dashboard_image](https://user-images.githubusercontent.com/367461/179586842-8f60e9a3-0fa9-4c08-9705-528d58c1cf09.png)

-------------------
