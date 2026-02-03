# Backend Documentation

## Overview
This backend provides REST APIs for managing cloud storage endpoints, security policies, private data detection, and event tracking.

---

## File Structure

### Core Application Files

**`app/main.py`**
- FastAPI application entry point
- Sets up database connection on startup
- Initializes services and routers
- Health check endpoint at `/`

**`app/api/api.py`**
- Defines all REST API endpoints
- Includes endpoints for:
  - Endpoints management (list, create, delete)
  - Security policies (summary, detail)
  - Private data detection
  - Events (recent events, summary)
  - Storage analysis
  - Provider breakdown

**`app/services/services.py`**
- Business logic layer that formats database responses
- Transforms raw data into JSON structures
- Handles org name lookups and aggregations
- Provides consistent response formatting

**`app/database/sqlalc_dac.py`**
- Data Access Layer using SQLAlchemy
- Manages database connections
- Executes all SQL queries
- Methods for CRUD operations on endpoints, policies, events, etc.

### Queue Service

**`queue_adder/main.py`**
- Background service that monitors endpoints
- Runs every 2 minutes
- Queries for endpoints not scanned in 24 hours
- Posts scan jobs to AWS SQS queue
- Tests database connection on startup

### Docker Files

**`Dockerfile`**
- Builds the FastAPI backend application
- Exposes port 8000
- Runs: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

**`Dockerfile.queue_adder`**
- Builds the queue adder background service
- Runs: `python -m queue_adder.main`
- Continuously monitors and queues endpoints for scanning

---

## Requirements

### System Requirements
- Python 3.10+
- PostgreSQL database
- AWS account (for SQS queue)

### Python Packages
See `requirements.txt`:
- `fastapi` - Web framework
- `sqlalchemy` - Database ORM
- `asyncpg` - Async PostgreSQL driver
- `uvicorn` - ASGI server
- `boto3` - AWS SDK for SQS
- `python-dotenv` - Environment variable management

---

## Setup & Configuration

### Prerequisites
- Docker and Docker Compose installed
- PostgreSQL database running (local or remote)
- AWS SQS queue created
- AWS credentials configured

### Environment Variables
Create a `.env` file in the backend directory:
```
DATABASE_URL=postgresql+asyncpg://username:password@host:5432/database_name
AWS_REGION=us-east-2
QUEUE_URL=https://sqs.us-east-2.amazonaws.com/YOUR_ACCOUNT_ID/YOUR_QUEUE_NAME
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### Database Setup
- PostgreSQL must be running and accessible
- Tables must be created (see `../sql/README.md`)
- Ensure `DATABASE_URL` environment variable is set correctly

---

## Running the Application

### Run FastAPI Backend
```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- API will be available at `http://localhost:8000`
- Swagger docs at `http://localhost:8000/docs`

### Run Queue Adder Service
```bash
# From backend directory
python -m queue_adder.main
```
- Monitors endpoints every 2 minutes
- Sends scan jobs to SQS

---

## Docker Build & Run

### Build FastAPI Backend
```bash
docker build -t backend:latest -f Dockerfile .
```

### Run FastAPI Backend
```bash
docker run -e DATABASE_URL="postgresql+asyncpg://..." \
           -e AWS_REGION=us-east-2 \
           -p 8000:8000 \
           backend:latest
```

### Build Queue Adder Service
```bash
docker build -t queue-adder:latest -f Dockerfile.queue_adder .
```

### Run Queue Adder Service
```bash
docker run -e DATABASE_URL="postgresql+asyncpg://..." \
           -e QUEUE_URL="https://sqs.us-east-2.amazonaws.com/..." \
           -e AWS_REGION=us-east-2 \
           -e AWS_ACCESS_KEY_ID="..." \
           -e AWS_SECRET_ACCESS_KEY="..." \
           queue-adder:latest
```

---

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/endpoints?org_id=xxx` | List all endpoints for org |
| POST | `/api/endpoints` | Create new endpoint |
| DELETE | `/api/endpoints/{id}?org_id=xxx` | Delete endpoint |
| GET | `/api/security/policies?org_id=xxx` | Security status for all endpoints |
| GET | `/api/security/policies/{id}?org_id=xxx` | Security details for specific endpoint |
| GET | `/api/security/private-data?org_id=xxx` | Private data detection summary |
| GET | `/api/events?org_id=xxx&limit=50` | Recent security events |
| GET | `/api/events/summary?org_id=xxx` | Total event count |
| GET | `/api/storage/size?org_id=xxx` | Storage sizes per endpoint |
| GET | `/api/providers?org_id=xxx` | Cloud provider breakdown |

---

## Notes

- All responses include `orgName` from the database
- Timestamps are in ISO 8601 format
- UUIDs are auto-generated (uuidv7)
- Database connection is reused via connection pool
- Queue adder automatically updates `last_scanned_at` when jobs are queued