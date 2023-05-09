"""
Template for implementing services running on the PlanQK platform
"""
from typing import Dict, Any, Optional, Union

from loguru import logger
from planqk.qiskit import PlanqkQuantumProvider
from qiskit import QuantumCircuit, transpile

from .libs.return_objects import ResultResponse, ErrorResponse


def run(data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) \
        -> Union[ResultResponse, ErrorResponse]:
    """
    Default entry point of your code. Start coding here!

    Parameters:
        data (Optional[Dict[str, Any]]): The input data sent by the client
        params (Optional[Dict[str, Any]]): Contains parameters, which can be set by the client for parametrizing the execution

    Returns:
        response: (ResultResponse | ErrorResponse): Response as arbitrary json-serializable dict or an error to be passed back to the client
    """
    access_token = params.get("access_token", None)

    provider = PlanqkQuantumProvider(access_token)
    backend_name = params.get("backend", "ionq.simulator")
    backend = provider.get_backend(backend_name)

    circuit = QuantumCircuit(3, 3)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.measure([0, 1, 2], [0, 1, 2])

    circuit = transpile(circuit, backend)

    shots = params.get("shots", 1)
    job = backend.run(circuit, shots=shots)

    counts_dict = job.result().get_counts()

    result = {
        'counts_dict': counts_dict
    }
    metadata = {
        'shots': shots,
        'backend': backend_name,
    }

    logger.info("Qiskit circuit successfully executed")

    return ResultResponse(result=result, metadata=metadata)
