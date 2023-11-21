"""
Template for implementing services running on the PlanQK platform
"""
import time
from loguru import logger
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from typing import Dict, Any, Union

from .libs.return_objects import ResultResponse, ErrorResponse


def run(data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Union[ResultResponse,
                                                                             ErrorResponse]:
    """
    Default entry point of your code. Start coding here!

    Parameters:
        data (Dict[str, Any]): The input data sent by the client
        params (Dict[str, Any]): Contains parameters, which can be set by the client to configure the execution

    Returns:
        response: (ResultResponse | ErrorResponse): Response as arbitrary json-serializable dict or an error to be passed back to the client
    """

    # defines the range of random numbers between 0 and 2^n_bits - 1
    n_bits = data.get("n_bits", 2)

    # Use AerSimulator
    simulator = AerSimulator()

    # create circuit
    circuit = QuantumCircuit(n_bits, n_bits)
    circuit.h(range(n_bits))

    # perform measurement
    circuit.measure(range(n_bits), range(n_bits))

    start_time = time.time()

    # execute the circuit
    logger.info("Starting execution...")
    job = simulator.run(circuit, shots=1)

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
