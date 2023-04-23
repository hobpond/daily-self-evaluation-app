import json
import os
from google.cloud import bigquery

def load_config():
    with open("bigquery/config.json", "r") as f:
        config = json.load(f)
    return config

def create_bigquery_client():
    config = load_config()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config["google_application_credentials"]
    return bigquery.Client()
