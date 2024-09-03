from fastapi import FastAPI

# creating an instance of FastAPI
app = FastAPI()

# defining a route
@app.get("/")
def home():
    return "Home for Fast API"