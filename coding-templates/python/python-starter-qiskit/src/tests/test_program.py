import os

from src.program import run

os.environ["DEBUG"] = "true"


def test_should_return_random_number() -> None:

    data = {"n_bits": 8}
    params = {}

    response = run(data, params)
    assert response.result["random_number"] < 256
    assert response.result["random_number"] >= 0
    assert "execution_time" in response.metadata.keys()
