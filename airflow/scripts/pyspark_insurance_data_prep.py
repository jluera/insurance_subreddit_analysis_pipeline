import os
import pyspark
from pyspark.sql import SparkSession, types, functions as F
from pyspark.sql.functions import from_unixtime
from pyspark.sql.functions import to_utc_timestamp

# Create spark session
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('type_conversion') \
    .getOrCreate()

# Read parquet file and create dataframe
df1 = spark.read \
    .option("header", "true") \
    .parquet('/tmp/reduced_insurance_comments.parquet') 

# created_utc and retrieved_on unixtime columns require a cast and then to_utc_timetamp conversion
df1 = df1.withColumn('created_utc', df1.created_utc.cast('timestamp'))
df1 = df1.withColumn('created_utc', to_utc_timestamp(F.col("created_utc"), 'UTC'))

df1 = df1.withColumn('retrieved_on', df1.retrieved_on.cast('timestamp'))
df1 = df1.withColumn('retrieved_on', to_utc_timestamp(F.col("retrieved_on"), 'UTC'))

# Cast specific numeric columns datatypes as needed
df1 = df1.withColumn('num_comments', df1.num_comments.cast('integer'))
df1 = df1.withColumn('subreddit_type', df1.subreddit_type.cast('integer'))
df1 = df1.withColumn('total_awards_received', df1.total_awards_received.cast('integer'))
df1 = df1.withColumn('upvote_ratio', df1.upvote_ratio.cast('float'))

# Converting specific text columns to lowercase
df1 = df1.withColumn('title', F.lower(df1.title))
df1 = df1.withColumn('domain', F.lower(df1.domain))
df1 = df1.withColumn('full_link', F.lower(df1.full_link))
df1 = df1.withColumn('selftext', F.lower(df1.selftext))

# Remove any unicode characters that may exist in title or selftext columns
df1 = df1.withColumn("title", F.regexp_replace(F.regexp_replace("title", "[^\x00-\x7F]+", ""), '""', ''))
df1 = df1.withColumn("selftext", F.regexp_replace(F.regexp_replace("selftext", "[^\x00-\x7F]+", ""), '""', ''))

# Remove certain punctuation and special characters from title and selftext columns
df1 = df1.withColumn("title", F.regexp_replace(F.regexp_replace("title", "[\$#,!.?|#;]", ""), '""', ''))
df1 = df1.withColumn("title", F.regexp_replace("title", "\\(", ""))
df1 = df1.withColumn("title", F.regexp_replace("title", "\\)", ""))

df1 = df1.withColumn("selftext", F.regexp_replace(F.regexp_replace("selftext", "[\$#,!.?|#;]", ""), '""', ''))
df1 = df1.withColumn("selftext", F.regexp_replace("selftext", "\\(", ""))
df1 = df1.withColumn("selftext", F.regexp_replace("selftext", "\\)", ""))

# Write out cleaned parquet file
df1.write.parquet("/tmp/insurance.parquet")

# Delete the original parquet file
if os.path.exists("/tmp/reduced_insurance_comments.parquet"):
  os.remove("/tmp/reduced_insurance_comments.parquet")
  print("The file /tmp/reduced_insurance_comments.parquet has been deleted")
else:
  print("The file does not exist")
