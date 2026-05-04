from fastapi import FastAPI, HTTPException
from mangum import Mangum

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working fine 🚀"}


@app.get("/user")
def get_user():
    data = {"name": "Ali"}

    if "age" not in data:
        # This forces a real server error (500)
        raise Exception("Age not found in data")

    return {
        "name": data["name"],
        "age": data["age"]
    }

handler = Mangum(app)