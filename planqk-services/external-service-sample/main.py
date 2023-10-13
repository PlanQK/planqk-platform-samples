import os
from random import *
from typing import Union

import requests
from fastapi import FastAPI, Request

app = FastAPI()

PLANQK_METERING_API = os.getenv("PLANQK_METERING_API",
                                "https://platform.planqk.de/qc-catalog/external-services/metering")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
PRODUCT_ID = os.getenv("PRODUCT_ID", None)


@app.get("/")
def health():
    return "UP"


@app.post("/")
def run(request: Request):
    """ This is the main entry point for the API. """

    # ... add your own code here ...

    meter_api_usage(request)

    # for the sake of this example, we'll just return a random number
    return randint(1, 100)


def meter_api_usage(request: Union[Request, None]):
    """ This function is used to meter the usage of the API. """

    correlation_id = request.headers.get("x-correlation-id")

    payload = {
        "correlationId": correlation_id,
        "productId": PRODUCT_ID,
        "count": 1
    }

    r = requests.post(PLANQK_METERING_API, json=payload, headers={"x-auth-token": ACCESS_TOKEN})
    if r.status_code != requests.codes.ok:
        print("Error while metering service usage")
        print("Check the ACCESS_TOKEN and PRODUCT_ID environment variables")
        print("Make sure you use the correlation id in the request header (x-correlation-id)")
