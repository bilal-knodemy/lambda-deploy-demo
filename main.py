from fastapi import FastAPI, HTTPException
from mangum import Mangum

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working fine 🚀"}

@app.get("/user")
def get_user():
    data = {"name": "Ali"}
    return {"name": data["age"]}

handler = Mangum(app)