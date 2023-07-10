"""
Template for implementing services running on the PlanQK platform
"""
import math
from loguru import logger
from typing import Dict, Any, Union

# Import response wrappers:
# - use ResultResponse to return computation results
# - use ErrorResponse to return meaningful error messages to the caller
from .libs.return_objects import ResultResponse, ErrorResponse
# Import your own libs
from .libs.utilities import add


def run(data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Union[ResultResponse, ErrorResponse]:
    """
    Default entry point of your code. Start coding here!

    Parameters:
        data (Dict[str, Any]): The input data sent by the client
        params (Dict[str, Any]): Contains parameters, which can be set by the client to configure the execution

    Returns:
        response: (ResultResponse | ErrorResponse): Response as arbitrary json-serializable dict or an error to be passed back to the client
    """

    try:
        values = data["values"]
        result = add(values)
        round_down = params.get("round_off", False)
        if round_down:
            result = math.floor(result)
        logger.debug("Calculation successfully executed")
        return ResultResponse(result={"sum": result})
    except Exception as e:
        return ErrorResponse(code="500", detail=f"{type(e).__name__}: {e}")
