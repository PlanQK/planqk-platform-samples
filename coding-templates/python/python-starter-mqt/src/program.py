"""Coding Template for the Munich Quantum Toolkit (MQT)"""

from __future__ import annotations

import time
from typing import Any

from loguru import logger
from mqt.ddsim import DDSIMProvider
from mqt.qcec import verify
from mqt.qmap import compile
from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import Fake5QV1

from .libs.return_objects import ErrorResponse, ResultResponse


def run(data: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> ResultResponse | ErrorResponse:  # noqa: ARG001
    """Default entry point of your code. Start coding here!

    Parameters:
        data: The input data sent by the client
        params: Contains parameters, which can be set by the client to configure the execution

    Returns:
        response: Response as arbitrary json-serializable dict or an error to be passed back to the client
    """
    # Create a circuit using Qiskit, for example the following circuit:
    qc = QuantumCircuit(4, name="ghz")
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(0, 3)
    qc.measure_all()

    # Simulate the circuit using one of the simulators offered by DDSIM
    provider = DDSIMProvider()
    logger.info(f"Available simulators: {[backend.name for backend in provider.backends()]}")

    backend = provider.get_backend("qasm_simulator")
    n_shots = 8192
    logger.info(f"Sampling {n_shots} shots from the output distribution using the {backend.name} backend")
    start_time = time.time()
    results_ddsim = backend.run(qc, shots=n_shots).result()
    execution_time_sim = round(time.time() - start_time, 4)
    logger.info(f"Finished simulation. Execution time: {execution_time_sim} seconds")
    logger.info(f"Measurement results: {results_ddsim.get_counts()}")

    # Map the circuit to a real architecture using QMAP
    architecture = Fake5QV1()

    logger.info(
        f"Mapping to an architecture with {architecture.configuration().n_qubits} qubits and the following coupling map: {architecture.configuration().coupling_map}"
    )
    start_time = time.time()
    qc_map, results_qmap = compile(
        qc, architecture, method="exact"
    )  # "exact" only for demonstration purposes, use "heuristic" for larger circuits
    execution_time_map = round(time.time() - start_time, 4)
    logger.info(f"Finished mapping. Execution time: {execution_time_map} seconds")
    logger.info(f"Mapped circuit:\n{qc_map}")
    logger.debug(f"Statistics and metadata:\n {results_qmap.json()}")

    # Verify that the compiled circuit is still equivalent to the original circuit using QCEC
    logger.info("Verifying the equivalence of the original and mapped circuits using QCEC")
    start_time = time.time()
    results_qcec = verify(
        qc,
        qc_map,
    )
    execution_time_ver = round(time.time() - start_time, 4)
    logger.info(f"Finished verification. Execution time: {execution_time_ver} seconds")
    logger.info(f"Circuit are {results_qcec.equivalence}")
    logger.debug(f"Statistics and metadata:\n {results_qcec.json()}")

    # Perform the same simulation on the mapped circuit
    logger.info(
        f"Sampling {n_shots} shots from the output distribution of the mapped circuit using the {backend.name} backend"
    )
    start_time = time.time()
    results_ddsim_map = backend.run(qc_map, shots=n_shots).result()
    execution_time_sim_map = round(time.time() - start_time, 4)
    logger.info(f"Finished simulation. Execution time: {execution_time_sim_map} seconds")
    logger.info(f"Measurement results: {results_ddsim_map.get_counts()}")

    result = {
        "counts": results_ddsim.get_counts(),
        "equivalence": results_qcec.equivalence,
        "counts_mapped": results_ddsim_map.get_counts(),
    }
    metadata = {
        "qcec_results": results_qcec.json(),
        "qmap_results": results_qmap.json(),
        "execution_time_sim": execution_time_sim,
        "execution_time_map": execution_time_map,
        "execution_time_ver": execution_time_ver,
        "execution_time_sim_map": execution_time_sim_map,
    }
    logger.info("Calculation successfully executed")

    return ResultResponse(result=result, metadata=metadata)
