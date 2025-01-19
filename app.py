import os
from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google.cloud import bigquery
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

#init app
app = FastAPI(title="Reckless Roosters API",
    description="An API to query the BigQuery backend to get the source data for the Reckless Roosters project.",
    version="1.0.0",
    contact={
        "name": "Etashi",
        "url": "https://www.etashi.com",
        "email": "sj@etashi.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },)

# Set GOOGLE_APPLICATION_CREDENTIALS to a file in the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_dir, "58546-97026e5de806.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
# BigQuery client
client = bigquery.Client()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Define a homepage route
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Reckless Roosters"})


class QueryResult(BaseModel):
    rows: list
    total_rows: int


@app.get("/query", response_model=QueryResult, summary="Get raw location data", description="Execute a query against the BigQuery backend to get the source data for the Reckless Roosters project.")
async def query_bigquery(
    query: str = Query("SELECT * FROM `fatti-58546.animalcrime.gbif_distances_auto` LIMIT 10", description="The SQL query to execute on the BigQuery backend."),
    max_results: int = Query(10, description="Maximum number of rows to return.", gt=0, le=10)
):
    """
    Query BigQuery and return results.
    """

    # Use named parameters - avoid injection
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", max_results)
        ],
    
    )                                        

    #avoid injection
    def validate_sql(sql: str):
        parsed = sqlparse.parse(sql)
        for statement in parsed:
            if statement.get_type() != "SELECT":
                raise ValueError("Only SELECT statements are allowed.")
            for token in statement.tokens:
                if token.ttype is Keyword and token.value.upper() in {"DELETE", "DROP", "INSERT"}:
                    raise ValueError("DML statements are not allowed.")
        return True

    if validate_sql(query):
        job = client.query(query, job_config=job_config)
        rows = [dict(row) for row in job.result(max_results=max_results)]
        return {"rows": rows, "total_rows": len(rows)}
    else:
        return {"error": "Invalid SQL query."}

