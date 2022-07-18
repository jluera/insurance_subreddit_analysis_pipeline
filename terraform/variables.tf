
variable "credentials" {
  description = "Path for GCP credential files"
  type = string
}
  
variable "project" {
  description = "The ID of the project in which to provision resources."
  type = string
}

variable "storage_bucket" {
  description = "The name of the bucket to create."
  type = string
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type = string
}

variable "location" {
  description = "Location for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type = string
}

variable "zone" {
    description = "Zone for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
    type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  type = string
  default = "standard"
}

variable "bq_dataset" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
}

variable "spark-cluster" {
  description = "Dataproc cluster to run spark jobs"
  type = string
}

variable "pushift_extract" {
  description = "script to extract subreddit data with pushift"
  type = string
}

variable "spark_data_clean" {
  description = "Script to clean subreddit data with Spark"
  type = string
}

variable "upload_gcs" {
  description = "Script to upload Spark ETL to Cloud Storage"
  type = string
}

variable "vm_image" {
  description = "Base image for your Virtual Machine."
  type = string
  default = "ubuntu-os-cloud/ubuntu-2204-lts"
}

