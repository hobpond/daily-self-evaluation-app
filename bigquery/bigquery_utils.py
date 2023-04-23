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

config = load_config()
client = create_bigquery_client()

def insert_bigquery_record(record: dict):
    table_id = f"{config['project_id']}.{config['dataset_id']}.{config['table_id']}"
    table = client.get_table(table_id)
    rows_to_insert = [record]
    errors = client.insert_rows(table, rows_to_insert)

    if errors == []:
        return True
    else:
        return False

def fetch_evaluations():
    table_id = f"{config['project_id']}.{config['dataset_id']}.{config['table_id']}"

    table_ref = client.dataset(config['dataset_id']).table(table_id)

    # Query to fetch all evaluations
    query = f"SELECT * FROM `{config['project_id']}.{config['dataset_id']}.{config['table_id']}` ORDER BY timestamp DESC"
    query_job = client.query(query)
    evaluations = query_job.result()

    return evaluations
