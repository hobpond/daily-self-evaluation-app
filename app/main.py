from app.model.evaluation_data import EvaluationData
from bigquery import bigquery_utils
from fastapi import FastAPI, Request
from fastapi_pagination import Page, Params, add_pagination, paginate
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.datastructures import URL
from google.cloud import bigquery
from uuid import uuid4
import datetime

app = FastAPI()

# Mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2Templates
templates = Jinja2Templates(directory="templates")
templates.env.globals['URL'] = URL

@app.get("/review", response_model=Page[EvaluationData], name="review")
async def get_evaluations_paginated(request: Request, page: int = 1, size: int = 1):
    evaluations = paginate(bigquery_utils.fetch_evaluations(), Params(size=size, page=page))
    return templates.TemplateResponse("review.html", {"request": request, "evaluations": evaluations})    

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
    if bigquery_utils.insert_bigquery_record(record):
        return {"message": "Evaluation submitted successfully", "data": evaluation_data}
    else:
        return {"message": "Error inserting data into BigQuery", "data": evaluation_data}

# Serve the HTML form
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("evaluation_form.html", {"request": request})

add_pagination(app)
