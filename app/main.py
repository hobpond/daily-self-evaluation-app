from bigquery import bigquery_utils
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google.cloud import bigquery
from uuid import uuid4
import datetime

config = bigquery_utils.load_config()
client = bigquery_utils.create_bigquery_client()
table_id = f"{config['project_id']}.{config['dataset_id']}.{config['table_id']}"

app = FastAPI()

class EvaluationData(BaseModel):
    expectations: str
    smart_criteria: str
    communication_effectiveness: str
    team_performance: str
    feedback: str
    growth_plan: str

# Initialize the BigQuery client
client = bigquery.Client()

def insert_bigquery_record(record: dict):
    table = client.get_table(table_id)
    rows_to_insert = [record]
    errors = client.insert_rows(table, rows_to_insert)

    if errors == []:
        return True
    else:
        return False

@app.post("/submit_evaluation/")
async def submit_evaluation(evaluation_data: EvaluationData):
    # Prepare the data to be inserted into BigQuery
    record = {
        "id": str(uuid4()),
        "timestamp": datetime.datetime.utcnow(),
        "expectations": evaluation_data.expectations,
        "smart_criteria": evaluation_data.smart_criteria,
        "communication_effectiveness": evaluation_data.communication_effectiveness,
        "team_performance": evaluation_data.team_performance,
        "feedback": evaluation_data.feedback,
        "growth_plan": evaluation_data.growth_plan
    }

    # Insert the data into BigQuery
    if insert_bigquery_record(record):
        return {"message": "Evaluation submitted successfully", "data": evaluation_data}
    else:
        return {"message": "Error inserting data into BigQuery", "data": evaluation_data}

# Mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Serve the HTML form
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("evaluation_form.html", {"request": request})
