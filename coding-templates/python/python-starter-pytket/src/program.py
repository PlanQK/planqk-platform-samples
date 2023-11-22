"""
Template for implementing services running on the PlanQK platform
"""
import time
from loguru import logger

import qiskit as q
from qiskit_aer import AerSimulator

from pytket import Circuit
from pytket.qasm import circuit_to_qasm_str

from planqk.qiskit.provider import PlanqkQuantumProvider as PlanqkProvider
from planqk.exceptions import InvalidAccessTokenError
from typing import Dict, Any, Union

from .libs.return_objects import ResultResponse, ErrorResponse

DEFAULT_CLOUD_BACKEND = "azure.ionq.simulator"


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

    # Instantiate PlanQK provider, if PlanQK execution is requested
    planqk_execution = params.get("planqk_execution", False)
    if planqk_execution:
        planqk_access_token = params.get("planqk_access_token", None)
        if planqk_access_token is None:
            provider = PlanqkProvider()
        else:
            provider = PlanqkProvider(access_token=planqk_access_token)

    # Set backend for execution via PlanQK
    backend = params.get("backend", None)
    if planqk_execution:
        if backend is None:
            logger.info(f"No backend specified, using {DEFAULT_CLOUD_BACKEND}")
            backend = DEFAULT_CLOUD_BACKEND
            try:
                backend = provider.get_backend(backend)
            except InvalidAccessTokenError as e:
                logger.error(
                    "No valid PlanQK access token provided, executing with local simulator")
                backend = AerSimulator()
            except Exception:
                logger.error(
                    f"Could not load backend {backend}, executing with local simulator")
                backend = AerSimulator()

    else:
        logger.info("Executing locally with AerSimulator")
        backend = AerSimulator()

    # create circuit
    circuit = Circuit(n_bits, n_bits)
    for idx in range(n_bits):
        circuit.H(idx)

    # perform measurement
    circuit.measure_all()

    # transform to qiskit Quantum Circuit
    qasm_circuit = circuit_to_qasm_str(circuit)
    qiskit_circuit = q.QuantumCircuit.from_qasm_str(qasm_circuit)

    start_time = time.time()

    # execute the circuit
    logger.info("Starting execution...")
    job = q.execute(qiskit_circuit, backend, shots=1)

    # extract random number and convert from binary to decimal
    random_bitstring = list(job.result().get_counts().keys())[0]
    random_number = int(random_bitstring, 2)

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
