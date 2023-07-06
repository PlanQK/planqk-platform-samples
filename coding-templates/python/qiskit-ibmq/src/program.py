import time
from typing import Dict, Any, Optional, Union

import qiskit as q
from loguru import logger

from .libs.return_objects import Response, ResultResponse, ErrorResponse


def run(data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) \
        -> Union[ResultResponse, ErrorResponse]:
    """
    Qiskit example

    Parameters:
        data (Optional[Dict[str, Any]]): The input data sent by the client
        params (Optional[Dict[str, Any]]): Contains parameters, which can be set by the client for parametrizing the execution

    Returns:
        response: (ResultResponse | ErrorResponse): Response as arbitrary json-serializable dict or an error to be passed back to the client
    """
    response: Response
    try:
        # parameter handling
        num_qubits = params.get('num_qubits', 2)
        shots = params.get('shots', 1024)
        backend_name = params.get('backend', 'qasm_simulator')
        token = params.get('token', None)

        start_time = time.time()

        backend = get_backend(backend_name, token)

        # building the GHZ state
        circuit = q.QuantumCircuit(num_qubits, num_qubits)
        circuit.h(0)
        circuit.cnot(range(num_qubits - 1), range(1, num_qubits))
        circuit.measure(range(num_qubits), range(num_qubits))

        job = q.execute(circuit, backend=backend, shots=shots)
        counts_dict = job.result().get_counts()

        eval_time = time.time() - start_time

        result = {
            'counts_dict': counts_dict
        }
        metadata = {
            'n_qubits': num_qubits,
            'backend': backend_name,
            'eval_time': round(eval_time, 2)
        }

        logger.info("Qiskit circuit successfully executed")

        return ResultResponse(result=result, metadata=metadata)
    except Exception as e:
        return ErrorResponse(code="500", detail=f"{type(e).__name__}: {e}")


def get_backend(backend_name, token):
    """
    Helper function to determine a Qiskit backend
    """
    backend = None
    local_simulator_list = [backend.name() for backend in q.Aer.backends()]
    if backend_name in local_simulator_list:
        backend = q.Aer.get_backend(backend_name)
    elif backend_name is None:
        logger.info('No backend was provided, using local qasm_simulator.')
        backend = q.Aer.get_backend('qasm_simulator')
    else:
        logger.info(f'{backend_name} is a no local backend, trying to communicat with IBMQ backends.')
        if token is None:
            logger.info(f'No valid IBMQ token. Setting backend to qasm_simulator')
            backend = q.Aer.get_backend('qasm_simulator')
        else:
            if not q.IBMQ.active_account():
                provider = q.IBMQ.enable_account(token=token)
                backend = provider.get_backend(backend_name)
                logger.info(f'Backend set to {backend.name()}')
    return backend
