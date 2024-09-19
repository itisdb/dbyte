from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the root of the dbyteAPI"}

@app.get("/health_check")
async def health_check():
    return {"message": "dbyteAPI is up and running!"}

