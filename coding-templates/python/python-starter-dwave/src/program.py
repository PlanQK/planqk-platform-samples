"""
Template for implementing services running on the PlanQK platform
"""
import time
from typing import Dict, Any, Union

import dimod
import numpy as np
from loguru import logger
from planqk.dwave.provider import PlanqkDwaveProvider

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

    # defines whether to use a simulator or a real quantum computer
    use_simulator = params.get('use_simulator', True)

    # through the PlanqkDwaveProvider you can access our supported D-Wave samplers
    provider = PlanqkDwaveProvider()

    # create a sampler by its class name, and set any additional parameters you desire
    if use_simulator:
        sampler = provider.get_sampler("SimulatedAnnealingSampler")
    else:
        sampler = provider.get_sampler("LeapHybridSampler", solver={"category": "hybrid"})
    logger.debug(f"Using sampler: {sampler}")

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
