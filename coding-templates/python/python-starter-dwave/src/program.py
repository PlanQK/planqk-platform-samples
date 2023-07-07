import dimod
import numpy as np
import time
from dwave.system import LeapHybridSampler
from loguru import logger
from typing import Dict, Any

from .libs.return_objects import ResultResponse


def run(data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> ResultResponse:
    logger.info("D-Wave program started")
    start_time = time.time()

    sampler = LeapHybridSampler(solver={"category": "hybrid"})

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
