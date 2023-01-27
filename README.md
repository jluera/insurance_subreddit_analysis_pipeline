# Reddit /r/insurance ETLT Pipeline

An EtLT pipeline to extract and transform the initial user post comments from the [r/insurance](https://www.reddit.com/r/insurance/) subreddit.

## Motivation

This project was designed to exercise practical Data Engineering skills.  It was inspired by work done in relation to the datatalks.club Data Engineering Zoomcamp and is a follow up on projects completed during that course.

## Project Architecture and Details
This project makes use of the following resources:
* Docker
* Apache Airflow (Running in Docker container)
* Terraform (Running in a Docker container)
* Google Cloud Storage (To ingest parquet files before they get loaded into Big Query)
* Google Big Query (To batch load parquet files from Cloud Storage tables and perform some simple analysis on them)

Data ingestion is handled by Airflow running in a Docker container.  Airflow initiates a single DAG which runs four scripts. The first script handles downloading the necessary data from the Reddit /r/insurance subreddit using the PushShift API. It then performs some simple data cleaning with Pandas and saves the dataset into a Parquet format. A second script loads this parquet file into Spark and performs some additional data cleansing. A third script handles loading the data into Google Cloud Storage. And the fourth script batch loads the data from Google Cloud Storage into a BigQuery table for further analysis.

## Workflow Summary
1) Spin up Google Cloud Resources via Terraform.
2) Run three scripts in Airflow running in a docker container.
3) The first script retrieves user posting data from Reddit's /r/Insurance subreddit using the Pushift API. It then reduces columns with Pandas and saves dataframe as a parquet file.
4) The second script performs simple transformations and data cleaning using PySpark.
5) The third script loads data into Google Cloud Storage and BigQuery for further analysis .
6) The data can then be imported into Google DataStudio to make a dashboard of relevant information.

Admittedly, some of the leveraged components, such as the use of Airflow, is kind of overkill for a simple pipeline like this but was utilized just to gain additional practice.

Prior to Data Ingestion, the Google Cloud services are spun up using Terraform, which is running in a Docker container. The terraform.tfvars file should be edited to add the necessary variables for your cloud environment. The other Terraform configs in this repo will pull those variables from the Terraform.tfvars file. You can then spin up your resources using terraform apply.

## Google credentials
You will need to create an environment variable called GOOGLE_APPLICATION_CREDENTIALS and assign it to the path of your json credentials file, which should be $HOME/.google/credentials/ . 
1. Edit .bashrc:
2. At the end of the file, add the following line:
```export GOOGLE_APPLICATION_CREDENTIALS="<path/to/authkeys>.json" ```
3. Log out of your current terminal session and log back in, or run source ~/.bashrc to activate the environment variable.
4. Refresh the token and verify the authentication with the GCP SDK:
```gcloud auth application-default login ```
5. Add the path to your terraform.tvars file.


## Terraform:
### Manual Terraform Install
```Run curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add - ```

```Run sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main" ```

```Run sudo apt-get update && sudo apt-get install terraform ```

## Terraform Configuration and Infrastructure Setup
Make sure that the credentials are updated and the environment variable is set up.
Clone the repo on your system and copy the files under the terraform directory to where you want to run it from.

Copy the terraform.tfvars.template file, rename it to drop the .template from the name, and edit it to add the correct resource names for your GCP environment.

Initialize Terraform:

```terraform init```

Plan the infrastructure and make sure that you're creating a bucket in Cloud Storage as well as a dataset in BigQuery

```terraform plan```

If the plan details are as expected, apply the changes.

```terraform apply```

This should spin up the GCP resources you will utilize later.

## Airflow Setup
* Copy the contents of the airflow folder over where needed
* Run the following command and write down the output:

```echo -e "AIRFLOW_UID=$(id -u)" ```
* Open the .env file and change the value of AIRFLOW_UID for the value of the previous command.
* Change the value of GCP_PROJECT_ID for the name of your project id in Google Cloud and also change the value of GCP_GCS_BUCKET for the name of your bucket.
* Build the custom Airflow Docker image:

```docker-compose build```
* Initialize the Airflow configs:

```docker-compose up airflow-init```
* Run Airflow

```docker-compose up```

You may now access the Airflow GUI by browsing to localhost:8080. Username and password are both airflow .

```IMPORTANT: this is NOT a production-ready setup! The username and password for Airflow have not been modified in any way; you can find them by searching for _AIRFLOW_WWW_USER_USERNAME and _AIRFLOW_WWW_USER_PASSWORD inside the docker-compose.yaml file.```

# Run the DAG with Airflow
If you performed all the steps of the previous section, you should now have a web browser with the Airflow dashboard.

To trigger the DAG, simply click on the switch icon next to the DAG name. 

After the data ingestion, you may shut down Airflow by pressing Ctrl+C on the terminal running Airflow and then running docker-compose down. 

## Dashboard
The dashboard used in this project was generated with Google Looker Studio (Formerly Google Data Studio).

The final dashboard can be configured as required but should look something like this:

[insurance_subreddit_stats_dash.pdf](https://github.com/jluera/insurance_sub_pipeline/files/9134594/insurance_subreddit_stats_dash.pdf)
![insurance_sub_dashboard_image](https://user-images.githubusercontent.com/367461/179586842-8f60e9a3-0fa9-4c08-9705-528d58c1cf09.png)



-------------------
