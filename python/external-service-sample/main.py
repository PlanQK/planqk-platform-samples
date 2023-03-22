from typing import Union
import os
import requests
import random
from enum import Enum

from fastapi import FastAPI, Request

app = FastAPI()


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

@app.get("/health")
def health():
    return "Up and running"


@app.post("/")
def run(request: Request):
    reportApiUsage(request)
    return random.random()


def reportApiUsage(request: Union[Request, None]):
    correlation_id = request.headers.get("x-correlation-id")
    METERING_API_URL = os.getenv("METERING_API_URL", None)
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
    API_PRODUCT_ID = os.getenv("API_PRODUCT_ID", None)

    payload = {
        "correlationId": correlation_id,
        "productId": API_PRODUCT_ID,
        "count": 1
    }
    r = requests.post(METERING_API_URL, json=payload,
                      headers={"X-Auth-Token": ACCESS_TOKEN})
    return
