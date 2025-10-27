# Backend Documentation

Here's what we're using for the backend Python app and why.

## What We're Building

The backend is a Python API that handles data processing and talks to our database. We're keeping it simple but making sure it can handle what we need for the DLP project.

## Main Libraries

### FastAPI
**Why we picked it**: It's fast, popular, and makes building APIs really easy.

**What it does**:
- Creates REST API endpoints
- Automatically generates API docs
- Handles request validation
- Good for async operations

**Basic example**:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/data")
def get_data():
    return {"message": "hello world"}
```

### Pandas
**Why we picked it**: Best library for working with data in Python.

**What it does**:
- Reads CSV/Excel files
- Cleans and processes data
- Does basic data analysis
- Converts between different data formats

**Basic example**:
```python
import pandas as pd

# Read a CSV file
df = pd.read_csv("data.csv")

# Basic operations
clean_data = df.dropna()  # Remove empty rows
summary = df.describe()   # Get stats
```

### PyODBC
**Why we picked it**: Simple way to connect to databases.

**What it does**:
- Connects to PostgreSQL (or other databases)
- Runs SQL queries
- Handles database operations safely

**Basic example**:
```python
import pyodbc

# Connect to database
conn = pyodbc.connect("your_connection_string_here")

# Run a query
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()
```

## How It All Works Together

1. **FastAPI** handles incoming requests
2. **PyODBC** gets data from the database
3. **Pandas** processes that data if needed
4. **FastAPI** sends the response back

## Getting Started

### What you need to install:
```
pip install fastapi uvicorn pandas pyodbc
```

### Environment setup:
You'll need a `.env` file with your database connection string and other config.

## Docker

We'll run everything in Docker so it works the same everywhere. Basic Dockerfile will install Python, our dependencies, and run the app.

## Cloud Stuff

When we need to talk to AWS or other cloud services, we'll add their SDKs as needed. Most of them are just `pip install boto3` or similar.

## Testing

We'll use different endpoint testers in order to test requests and we can do different reviews on logs and such.

## References

- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Pandas docs](https://pandas.pydata.org/)
- [PyODBC docs](https://github.com/mkleehammer/pyodbc)

## Next Steps

Here's the plan for getting everything built:

1. **Design the JSON objects** that the frontend will need
2. **Create API endpoints** to send that data from backend to frontend first start with these and just a list of endpoints that are GOING to exist and then start to create them and find out dependencys.
3. **Set up database structure** - tables, indexes, and stored procedures to get the data
4. **Build the routes** and figure out what business logic we need and make sure that they are returning the expected json.
5. **Create the data access layer** and see what's missing
6. **Test everything** as we go and figure out how to test Python interactively in VS Code

This should help us make sure the database works right and everything connects properly.


File strucutre:

app/
├── __init__.py
├── main.py
├── config.py
│
├── api/
│   ├── __init__.py
│   ├── endpoints.py         # Endpoint CRUD routes
│   ├── security.py          # Policy & private data routes
│   ├── events.py            # Events summary routes
│   ├── storage.py           # Storage size routes
│   └── providers.py         # CSP coverage routes
│
├── models/
├── schemas/
├── services/
├── cloud/
├── utils/
└── database/

## Next steps THESE NEED TO BE MADE INTO CARDS

Foundation / project setup

Create repo layout, empty init.py files, config.py, main.py, requirements.txt, Dockerfile, .env.example
Deliverable: app starts and returns 200 on /health
Database & config

DB connection/session, sql, migrations, endpoint DB model
Deliverable: persist and read endpoint records
Endpoint CRUD (core)

Pydantic request/response models, endpoint service, routes: GET /endpoints, POST /endpoints, DELETE /endpoints/{id}
Deliverable: add/list/delete endpoints working
Cloud client base & AWS

Abstract provider interface + aws_client for policy, object list, storage metrics
Deliverable: fetch policy and size metrics from AWS
Policy analysis & policy endpoints

policy_analyzer service, GET /security/policies (summary), GET /security/policies/{endpointId} (raw)
Deliverable: mark endpoints secure/insecure and return raw policy
Storage metrics & providers

storage_analyzer, GET /storage/size, GET /providers aggregation
Deliverable: per-endpoint sizes and provider totals
Private-data scanning (first-pass)

Regex patterns, data_scanner to stream & scan objects, basic result storage
Deliverable: /security/private-data returns hasPrivateData + dataTypes
Events & scan orchestration

Event DB model, scanner_service to create events from scans, GET /events/summary
Deliverable: events summary (counts, recent)
Background jobs & long-running scans

Integrate background worker (like FastAPI background tasks), retry/rate-limit handling
Deliverable: async scans with status tracking
Add Azure & GCP clients

Implement azure_client and gcp_client mirroring AWS client, update services to be provider-agnostic
Deliverable: same functionality for Azure and GCP
Auth, secrets & security hardening

API auth (JWT/API keys), secure credential handling (roles/vault), no plain secrets in DB
Deliverable: secure credentials and API access
Tests, CI, docs, deployment

Unit/integration tests with mocks, CI pipeline, README, Docker image and compose
Deliverable: tests passing, CI, and runnable Docker image