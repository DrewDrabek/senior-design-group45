from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

    # The goal here is to get a just the docker file running and then seeing the response that I should be getting from it