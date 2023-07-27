"""
Template for implementing services running on the PlanQK platform
"""
import time
from loguru import logger

import pennylane as qml
from pennylane import numpy as np
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

    init_params = data.get("init_params", [0, 1])
    if init_params is None or not isinstance(init_params, list):
        return ErrorResponse(code="501", detail="No valid initial parameters provided")
    logger.info(f"Starting parameters: {init_params}")

    iter_steps = params.get("iter_steps", 100)
    if not isinstance(iter_steps, int) or iter_steps < 1:
        return ErrorResponse(code="501", detail="Number of iterations must be of type int and >= 1")

    step_size = params.get("step_size", 0.3)
    if not isinstance(step_size, float) or step_size <= 0:
        return ErrorResponse(code="501", detail="Step size must be of float and > 0")

    print_iter = params.get("print_iter", 5)
    if not isinstance(print_iter, int):
        logger.info("Logging interim results every 5 iterations")
        print_iter = 5

    dev = qml.device(name="default.qubit", wires=1)
    @qml.qnode(dev)
    def circuit(params):
        qml.RX(params[0], wires = 0)
        qml.RY(params[1], wires = 0)
        return qml.expval(qml.PauliZ(0))

    opt = qml.GradientDescentOptimizer(stepsize=step_size)    
    angles = np.array(init_params, requires_grad=True)

    start_time = time.time()
    for iter_idx in range(iter_steps):
        angles = opt.step(circuit, angles)
        if (iter_idx+1) % 5 == 0:
            logger.info(f"Cost after iteration step {iter_idx+1:5d}: {circuit(angles):5f}")
            print(f"Cost after step {iter_idx+1:5d}: {circuit(angles):5f}")
    exec_time = time.time() - start_time

    result = {
        "optimal_params": angles.tolist(),
        "objective_value": round(circuit(angles).tolist(), 5)
    }

    metadata = {
        "execution_time": exec_time,
        "optimizer": "GradientDescentOptimizer",
    }

    return ResultResponse(result=result, metadata=metadata)
