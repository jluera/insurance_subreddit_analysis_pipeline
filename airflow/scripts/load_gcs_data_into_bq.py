import os
from google.cloud import bigquery

credential_path = "/home/sysops/.google/credentials/google_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Loading data from Google Cloud Storage into Big Query
def gcs_to_bq():
    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_id = "de-zoom-proj.insurance_sub_dataset_test.insurance"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
    )
    # Replace the uri as needed
    uri = "gs://insurance_sub_bucket_de-zoom-proj/insurance.parquet"

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))

if __name__ == "__main__":
   gcs_to_bq()