"""
Template for implementing services running on the PlanQK platform
"""
import os
import time
from typing import Dict, Any, Optional, Union

from loguru import logger
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_provider import IBMProvider, least_busy

from .libs.return_objects import ResultResponse, ErrorResponse


def run(data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) \
        -> Union[ResultResponse, ErrorResponse]:
    """
    Default entry point of your code. Start coding here!

    Parameters:
        data (Optional[Dict[str, Any]]): The input data sent by the client
        params (Optional[Dict[str, Any]]): Contains parameters, which can be set by the client

    Returns:
        response: (ResultResponse | ErrorResponse): Response as arbitrary json-serializable dict or an error to be passed back to the client
    """
    n_bits = data.get('n_bits', 2)  # defines the range of random numbers between 0 and 2^n_bits - 1
    use_simulator = params.get('use_simulator', True)  # defines whether to use a simulator or a real quantum computer

    # initialize the IBM provider
    token = os.getenv('QISKIT_IBM_TOKEN', None)
    if token is not None:
        provider = IBMProvider(token=token)
    else:
        provider = IBMProvider()

    if use_simulator:
        backend = provider.get_backend("ibmq_qasm_simulator")
    else:
        devices = provider.backends(simulator=False, operational=True)
        backend = least_busy(devices)
    logger.info(f"Using backend: {backend.name()}")

    # create circuit
    circuit = QuantumCircuit(n_bits, n_bits)
    circuit.h(range(n_bits))

    # perform measurement
    circuit.measure(range(n_bits), range(n_bits))

    # transpile circuit
    circuit = transpile(circuit, backend)

    max_shots = backend.configuration().max_shots
    logger.info(f"Using max number of shots available for selected simulator: {max_shots}")

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
