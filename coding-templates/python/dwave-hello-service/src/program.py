import time
from typing import Dict, Any, Optional, Union

import dimod
import numpy as np
from dwave.system import LeapHybridSampler
from loguru import logger

from .libs.return_objects import Response, ResultResponse, ErrorResponse


def run(data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) \
        -> Union[ResultResponse, ErrorResponse]:
    """
    DWave example

    Parameters:
        data (Optional[Dict[str, Any]]): The input data sent by the client
        params (Optional[Dict[str, Any]]): Contains parameters, which can be set by the client for parametrizing the execution

    Returns:
        response: (ResultResponse | ErrorResponse): Response as arbitrary json-serializable dict or an error to be passed back to the client
    """
    response: Response

    logger.info("D-Wave program started")
    start_time = time.time()

    sampler = LeapHybridSampler(solver={"category": "hybrid"})

    bqm = dimod.generators.ran_r(1, 300)
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
