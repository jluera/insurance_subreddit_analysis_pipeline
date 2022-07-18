# finance_sub_pipeline

An EtLT pipeline to do the following to extract and transform the initial post comments from the /r/Insurance subreddit.

1) Pull post data from the /r/Insurance subreddit using the Pushift, reduce columns with Pandas and save dataframe as a parquet file
2) Perform some simple transformations and data cleaning using PySparkand 
3) Load data into Google Cloud Storage and BigQuery for further analsysis which would be spun up via Terraform
4) The data can then be imported into Google DataStudio to make a simple dashboard like this:


[insurance_subreddit_stats_dash.pdf](https://github.com/jluera/finance_sub_pipeline/files/9134594/insurance_subreddit_stats_dash.pdf)
