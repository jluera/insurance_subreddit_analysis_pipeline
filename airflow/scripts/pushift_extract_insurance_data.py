from os.path import exists
import pandas as pd
from pmaw import PushshiftAPI
import datetime as dt
import gc

# Specify the subreddit you want to extract data from here
subreddit="insurance" 

# Set the name of the .csv file we will write to 
parquet_file = "/tmp/reduced_" + subreddit + "_comments.parquet" # Set the name of the .parquet file we will write

# Create variables used to set desired time window of extracted data
before = int(dt.datetime(2022,7,15,0,0).timestamp())
after = int(dt.datetime(2022,1,1,0,0).timestamp())

# api.search_submissions ( https://github.com/pushshift/api )
api = PushshiftAPI()
limit=100000
submissions = api.search_submissions(subreddit=subreddit, limit=limit, before=before, after=after)
print(f'Retrieved {len(submissions)} submissions from Pushshift')

# Load the extracted data from subreddit into a pandas dataframe
extracted_submissions_pd_df = pd.DataFrame(submissions)

# Create a new pandas dataframe reducing the number of columns down to 20 from the original 77 columns
reduced_columns_pd_df = extracted_submissions_pd_df[['author', 'author_fullname', 'created_utc', 'domain', 
                    'full_link', 'id', 'num_comments',  'permalink', 'pinned', 'retrieved_on', 
                    'selftext', 'subreddit', 'subreddit_id', 'subreddit_subscribers', 
                    'subreddit_type', 'title', 'total_awards_received', 'upvote_ratio', 'url', 
                    'link_flair_text', ]]

# Convert dataframe of subreddit data into a parquet file
reduced_columns_pd_df.to_parquet(parquet_file)

# Release pandas dataframe memory
del [[extracted_submissions_pd_df, reduced_columns_pd_df]]
gc.collect()
extracted_submissions_pd_df=pd.DataFrame
reduced_columns_pd_df=pd.DataFrame

# Check if the df.parquent file was created
file_exists = exists(parquet_file)
if file_exists:
    print(f'The file {parquet_file} has been created')
else:
    print(f"The file {parquet_file} was not created")