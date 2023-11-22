import json
import logging
import os
import sys

from loguru import logger

from .libs.logging import LogHandler
from .program import run

logging_level = os.environ.get("LOG_LEVEL", "DEBUG")
logging.getLogger().handlers = [LogHandler()]
logging.getLogger().setLevel(logging_level)
logger.configure(handlers=[{"sink": sys.stdout, "level": logging_level}])

with open("./input/data.json") as file:
    data = json.load(file)

with open("./input/params.json") as file:
    params = json.load(file)

response = run(data, params)

print()
print(response.to_json())
