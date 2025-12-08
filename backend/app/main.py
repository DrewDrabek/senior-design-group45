import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import api
from app.services.services import Services
from app.database.sqlalc_dac import Sql_Alc_DAC


# This is just a test endpoint to verify that the docker builds, runs, and returns something. 

# TODO:
# - Create the service logic that will call the dac and return the data as json and clean it
# - Create the endpoints that will point to the service logic
# - scanning logic for scanning the endpoints - this most likely will be a service the queries the dac for the last scan date and then schedules a message on a quie to be scanned.
# This is why we make the dac a library that can be imported so that we can use the service logic in both the endpoints and the scanning logic.
# Documentation for the backend serivce on the main readme

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://drewdrabek@localhost:5432/postgres"
)

dac = Sql_Alc_DAC(DATABASE_URL, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to database
    await dac.connect()
    yield
    # Shutdown: disconnect from database
    await dac.disconnect()

app = FastAPI(lifespan=lifespan)

# Create service instance and attach to app state
app.state.dac = dac
app.state.service = Services(dac)
# This is probably what we should have at some point - came from this doc I used to help create the dac https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html

app.include_router(api.router)
    

@app.get("/")
async def read_root():
    return {"status": "running", "message": "application started okay"}

