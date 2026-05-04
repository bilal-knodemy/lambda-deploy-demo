from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working fine 🚀"}


@app.get("/user")
def get_user():
    data = {"name": "Ali"}

    if "age" not in data:
        raise Exception("Age not found in data")

    
handler = Mangum(app)