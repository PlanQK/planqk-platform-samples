"""
Template for implementing services running on the PlanQK platform
"""

import time
from typing import Any, Dict, Union

from loguru import logger
from planqk.qiskit import PlanqkQuantumProvider
from qiskit import QuantumCircuit, transpile

from .libs.return_objects import ErrorResponse, ResultResponse


def run(
    data: Dict[str, Any] = None, params: Dict[str, Any] = None
) -> Union[ResultResponse, ErrorResponse]:
    """
    Default entry point of your code. Start coding here!

    Parameters:
        data (Dict[str, Any]): The input data sent by the client
        params (Dict[str, Any]): Contains parameters, which can be set by the client to configure the execution

    Returns:
        response: (ResultResponse | ErrorResponse): Response as arbitrary json-serializable dict or an error to be passed back to the client
    """

    # defines the range of random numbers between 0 and 2^n_bits - 1
    n_bits: int = data.get("n_bits", 2)
    # defines whether to use a simulator or a real quantum computer
    use_simulator: bool = params.get("use_simulator", True)
    # defines whether to use the maximum number of shots available for a selected backend
    use_max_shots: bool = params.get("use_max_shots", False)

    # initialize PlanQK provider
    # use next line if you are using the PlanQK CLI and have logged-in with "planqk login"
    provider = PlanqkQuantumProvider()
    # otherwise, use the following line and replace "your personal access token" with your personal access token
    # provider = PlanqkQuantumProvider(access_token="your personal access token")

    # you may choose one of the following backends, depending whether you
    # want to use a specific simulator or specific AWS Braket backend
    if use_simulator:
        # simulation backends from AWS Braket
        backend_name = "aws.sim.sv1"
        # backend_name = "aws.sim.dm1"

    else:
        # AWS Braket backends
        backend_name = "aws.ionq.aria"
        # backend_name = "aws.ionq.aria-2"
        # backend_name = "aws.ionq.harmony"
        # backend_name = "aws.oqc.lucy"
        # backend_name = "aws.rigetti.aspen"

    logger.info(f"Using backend: {backend_name}")
    backend = provider.get_backend(backend_name)

    # create circuit
    circuit = QuantumCircuit(n_bits, n_bits)
    circuit.h(range(n_bits))

    # perform measurement
    circuit.measure(range(n_bits), range(n_bits))

    # transpile circuit
    circuit = transpile(circuit, backend)

    max_shots = 100
    if use_max_shots:
        max_shots = backend.configuration().max_shots
        logger.info(f"Using max number of shots available: {max_shots}")

    start_time = time.time()

    # execute the circuit
    logger.info("Starting execution...")
    job = backend.run(circuit, shots=max_shots)

    # extract random number and convert from binary to decimal
    random_number = int(list(job.result().get_counts().keys())[0], 2)

    logger.info("Finished execution")
    execution_time = time.time() - start_time

    result = {
        "random_number": random_number,
    }
    metadata = {
        "execution_time": round(execution_time, 3),
    }

    logger.info("Calculation successfully executed")

    return ResultResponse(result=result, metadata=metadata)
