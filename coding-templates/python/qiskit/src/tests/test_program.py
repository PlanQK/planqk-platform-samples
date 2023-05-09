from qiskit.result import Counts

from src.program import run


def test_should_return_result() -> None:
    data = dict()
    params = {"n_qubits": 2, "shots": 1024}
    response = run(data, params)
    assert type(response.result["counts_dict"]) is Counts
    assert type(response.result["counts_dict"]["00"]) is int
    assert type(response.result["counts_dict"]["11"]) is int
    assert response.metadata["n_qubits"] == 2
    assert response.metadata["backend"] == "qasm_simulator"
