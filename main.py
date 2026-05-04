import json
import logging
from datetime import datetime, timezone
from fastapi import FastAPI
from mangum import Mangum

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API is working fine 🚀"}


@app.get("/user")
def get_user():
    data = {"name": "Ali"}

    if "age" not in data:
        error_payload = {
            "event": "VALIDATION_ERROR",
            "service": "fastapi-user-service",
            "error_type": "KeyError",
            "message": "Age not found in data",
            "severity": "CRITICAL",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        logger.error(json.dumps(error_payload))

        raise Exception(json.dumps(error_payload))


handler = Mangum(app)