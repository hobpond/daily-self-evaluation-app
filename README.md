# Daily Self-Evaluation App

A web application built with FastAPI to help senior software development managers submit daily self-evaluations and track their growth. The application includes an HTML form for input and stores the submitted data in a Google BigQuery table.

## Prerequisites

- Python 3.7 or higher
- A Google Cloud account with access to BigQuery
- A BigQuery table with the appropriate schema

## Installation

1. Clone the repository:

```
git clone https://github.com/hobpond/daily-self-evaluation-app.git
cd daily-self-evaluation-app
```

2. Create a virtual environment and activate it:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```
pip install -r requirements.txt

```
4. Copy the `bigquery/config-template.json` file to `bigquery/config.jon` and update it with your Google Cloud JSON key file path, project ID, dataset ID, and table ID.

5. Create the BigQuery table by running the `bigquery/create_table.py` script:

## Usage

1. Run the FastAPI application:
```
uvicorn app.main:app --reload
```

2. Visit [http://localhost:8000/](http://localhost:8000/) to access the daily self-evaluation form.

3. Fill out the form and submit it. The data will be stored in the specified BigQuery table.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
