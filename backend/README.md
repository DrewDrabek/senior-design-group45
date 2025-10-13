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