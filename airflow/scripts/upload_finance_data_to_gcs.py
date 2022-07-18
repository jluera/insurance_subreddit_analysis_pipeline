import os
import glob
from google.cloud import storage

credential_path = "/home/sysops/.google/credentials/google_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
PROJECT_ID = "de-zoom-proj"
BUCKET = "insurance_sub_bucket_de-zoom-proj"
GCS_OBJECT = "insurance.parquet"
LOCAL_FILE_PATH = "/tmp/insurance/"




# Copy cleaned finance subreddit parquet file to Google Cloud Storage
def upload_object():
    """Uploads a file to gcs bucket."""
    # The ID of your GCS bucket 
    # bucket_name = "your-bucket-name" 
    
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    # Collecting the name of the actual paritioned parquet file
    os.chdir("/tmp/insurance")
    for parquet_file in glob.glob("*.parquet"):
        LOCAL_FILE = LOCAL_FILE_PATH + parquet_file

    # Upload of file to Google Cloud Storage using Google Client Libraries
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET)
    blob = bucket.blob(GCS_OBJECT)
    blob.upload_from_filename(LOCAL_FILE)

    # Print message after the upload
    print(
        f"File {LOCAL_FILE} uploaded to {BUCKET}/{GCS_OBJECT}."
    )


if __name__ == "__main__":
   upload_object()
