import json
import logging
from datetime import datetime, timezone

import boto3
from fastapi import FastAPI
from mangum import Mangum

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI()

mangum_handler = Mangum(app)
cloudwatch = boto3.client("cloudwatch")


@app.get("/")
def home():
    return {"message": "API is working fine 🚀"}


@app.get("/user")
def get_user():
    data = {"name": "Ali", "age": None}  # Added default age key

    # Removed unnecessary check for 'age' in data


def lambda_handler(event, context):
    response = mangum_handler(event, context)

    if response.get("statusCode", 200) >= 500:
        error_payload = {
            "event": "LAMBDA_RUNTIME_ERROR",
            "service": "fastapi-user-service",
            "error_type": "HTTP500",
            "message": f"Handler returned HTTP {response['statusCode']}",
            "request_id": getattr(context, "aws_request_id", None),
            "severity": "CRITICAL",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        logger.error(json.dumps(error_payload))

        cloudwatch.put_metric_data(
            Namespace="FastAPIService",
            MetricData=[{
                "MetricName": "UserEndpointErrors",
                "Dimensions": [
                    {"Name": "Service", "Value": "fastapi-user-service"},
                    {"Name": "Endpoint", "Value": "/user"},
                ],
                "Value": 1,
                "Unit": "Count",
            }],
        )

    return response
