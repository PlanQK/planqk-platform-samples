import dimod
import numpy as np
import os
import time
from dwave.system import LeapHybridSampler
from loguru import logger
from typing import Dict, Any

from .libs.return_objects import ResultResponse

PLANQK_PERSONAL_ACCESS_TOKEN = os.getenv("PLANQK_PERSONAL_ACCESS_TOKEN", "change me for local usage")
PLANQK_ENDPOINT = os.getenv("PLANQK_ENDPOINT", "https://platform.planqk.de/dwave/sapi/v2")


def run(data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> ResultResponse:
    logger.info("D-Wave program started")
    start_time = time.time()

    sampler = LeapHybridSampler(solver={"category": "hybrid"},
                                endpoint=PLANQK_ENDPOINT,
                                token=PLANQK_PERSONAL_ACCESS_TOKEN)

    bqm = dimod.generators.ran_r(1, 5)
    sample_set = sampler.sample(bqm)

    # filter for solution with the lowest energy
    sample = sample_set.lowest()
    sample_result = next(sample.data(fields={"sample", "energy"}))

    eval_time = time.time() - start_time

    result = {
        "solution": {str(key): int(val) for key, val in sample_result.sample.items()}
    }
    metadata = {
        "message": "Hello PlanQK Service",
        "eval_time": np.round(eval_time, 2),
        "energy": sample_result.energy,
    }

    logger.info("D-Wave program successfully executed")

    return ResultResponse(metadata=metadata, result=result)
