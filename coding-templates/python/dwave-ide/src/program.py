"""
Template for implementing services running on the PlanQK platform
"""
import dimod
import numpy as np
import time
from loguru import logger
from typing import Dict, Any, Union

from .libs.return_objects import ResultResponse, ErrorResponse


def run(data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Union[ResultResponse, ErrorResponse]:
    """
    Default entry point of your code. Start coding here!

    Parameters:
        data (Dict[str, Any]): The input data sent by the client
        params (Dict[str, Any]): Contains parameters, which can be set by the client to configure the execution

    Returns:
        response: (ResultResponse | ErrorResponse): Response as arbitrary json-serializable dict or an error to be passed back to the client
    """

    logger.info("D-Wave program started")
    start_time = time.time()

    # through the PlanQKDwaveProvider you can access our supported D-Wave samplers
    provider = PlanqkDwaveProvider()

    # create a sampler by its class name, and set any additional parameters you desire
    sampler = provider.get_sampler("LeapHybridSampler", solver={"category": "hybrid"})

    # create a random BQM and sample it
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
