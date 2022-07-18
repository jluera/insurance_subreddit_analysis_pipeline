terraform {
  required_version = ">= 1.2.2"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws) depending on where you want to save your tf-state 
  required_providers {
    google-beta = {
      source  = "hashicorp/google"
    }
  }
}


####################################################################################
# Data Lake
####################################################################################
// Create Cloud Storage Bucket
resource "google_storage_bucket" "data_lake_bucket" {
  name          = "${var.storage_bucket}_${var.project}"
  location      = var.region

  # Optional settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  force_destroy = true
}

resource "google_storage_bucket" "dataproc_staging_bucket" {
  name          = "dataproc-staging-bucket_${var.project}"
  location      = var.region

  # Optional settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true
  force_destroy = true
}

####################################################################################
# Data Warehouse
####################################################################################
// Create Big Query Dataset
resource "google_bigquery_dataset" "bigquery_dataset" {
  dataset_id  = var.bq_dataset
  project     = var.project
  location      = var.region
  delete_contents_on_destroy = true
}

####################################################################################
# Compute Instance VM
####################################################################################
resource "google_compute_instance" "vm_instance" {
  name          = "airflow-instance"
  project       = var.project
  machine_type  = "e2-standard-4"
  zone          = var.zone

  boot_disk {
    initialize_params {
      image = var.vm_image
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }
}