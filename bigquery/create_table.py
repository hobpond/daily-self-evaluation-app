from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from . import bigquery_utils
import json
import os

def main():
    config = bigquery_utils.load_config()
    client = bigquery_utils.create_bigquery_client()

    project_id = config["project_id"]
    dataset_id = config["dataset_id"]
    table_id = config["table_id"]

    client = bigquery_utils.create_bigquery_client()

    project_id = config["project_id"]
    dataset_id = config["dataset_id"]
    table_id = config["table_id"]

    # Initialize the BigQuery client
    client = bigquery.Client()

    # Read the schema from the schema.json file
    with open("bigquery/schema.json", "r") as f:
        schema_json = json.load(f)

    # Convert the JSON schema to BigQuery schema
    schema = [bigquery.SchemaField.from_api_repr(field) for field in schema_json]

    # Create the dataset if it does not exist
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        client.create_dataset(dataset)

    # Create the table with the specified schema
    table_ref = dataset_ref.table(table_id)
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)

    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

if __name__ == "__main__":
    main()