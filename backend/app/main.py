from fastapi import FastAPI


# This is just a test endpoint to verify that the docker builds, runs, and returns something. 

# TODO:
# - Create the service logic that will call the dac and return the data as json and clean it
# - Create the endpoints that will point to the service logic
# - scanning logic for scanning the endpoints - this most likely will be a service the queries the dac for the last scan date and then schedules a message on a quie to be scanned.
# This is why we make the dac a library that can be imported so that we can use the service logic in both the endpoints and the scanning logic.

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}
