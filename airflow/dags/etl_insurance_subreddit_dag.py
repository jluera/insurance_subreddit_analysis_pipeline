from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime

"""
DAG to extract /r/Insurance subreddit data, clean with pyspark, and copy to Google Cloud Storage
"""

# Output name of extracted file. This be passed to each 
# DAG task so they know which file to process
output_name = datetime.now().strftime("%Y%m%d")

# Run our DAG daily and ensures DAG run will kick off 
# once Airflow is started, as it will try to "catch up"
schedule_interval = '@once' 
start_date = days_ago(1)

default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}

with DAG(
    dag_id='insurance_subreddit_etlt_pipeline',
    description ='Insurance Subreddit ETLT',
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
    tags=['InsuranceETLT'],
) as dag:

    extract_insurance_sub_data = BashOperator(
        task_id = 'extract_insurance_sub_data',
        bash_command = f"python /opt/airflow/extraction/pushift_extract_subreddit_data.py {output_name}",
        dag = dag,
    )
    extract_insurance_sub_data.doc_md = 'Extract Insurance subreddit data with pushift api, use pandas to select columns and convert into parquet file'

    pyspark_data_prep = BashOperator(
        task_id = 'data_cleaning',
        bash_command = f'python /opt/airflow/extraction/pyspark_subreddit_data_prep.py {output_name}',
        dag = dag,
    )
    pyspark_data_prep.doc_md = 'Use pyspark to set datatypes and clean data'
    
    copy_to_gcs = BashOperator(
        task_id = 'copy_to_gcs',
        bash_command = f"python /opt/airflow/extraction/upload_data_to_gcs_dag.py {output_name}",
        dag = dag,
    )
    copy_to_gcs.doc_md = 'Copy cleaned parquet file to gcs'

    load_into_bq = BashOperator(
        task_id = 'load_into_bq',
        bash_command = f"python /opt/airflow/extraction/load_gcs_data_into_bq.py {output_name}",
        dag = dag,
    )
    load_into_bq.doc_md = 'Copy GCS parquet data into a Big Query table'

extract_reddit_data >> pyspark_data_prep >> copy_to_gcs >> load_into_bq