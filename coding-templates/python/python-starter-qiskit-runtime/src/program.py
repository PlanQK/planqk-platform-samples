"""
Template for implementing services running on the PlanQK platform
"""
import os
import time
from typing import Dict, Any, Union

from loguru import logger
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler

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

    logger.info("Program started")

    # defines the range of random numbers between 0 and 2^n_bits - 1
    n_bits = data.get('n_bits', 2)
    # defines whether to use a simulator or a real quantum computer
    use_simulator = params.get('use_simulator', True)

    # initialize qiskit runtime service
    token = os.getenv('QISKIT_IBM_TOKEN', None)
    service = QiskitRuntimeService(
        channel="ibm_quantum", token=token, instance="ibm-q/open/main"
    )

    # create circuit
    circuit = QuantumCircuit(n_bits, n_bits)
    circuit.h(range(n_bits))

    # perform measurement
    circuit.measure(range(n_bits), range(n_bits))

    start_time = time.time()
    logger.info("Acquiring session...")
    with Session(service, backend="ibmq_qasm_simulator", max_time=None) as session:
        sampler = Sampler(session=session)

        logger.info("Starting execution...")
        job = sampler.run(circuit, shots=10)
        logger.info(f"Job submitted: id={job.job_id()}")

        job_result = job.result()

        logger.info("Finished execution")
        execution_time = time.time() - start_time

        session.close()

    result = {
        "job_result": job_result,
    }
    metadata = {
        "execution_time": round(execution_time, 3),
    }

    logger.info("Calculation successfully executed")

    return ResultResponse(result=result, metadata=metadata)
