from typing import List, Union, Optional


def add(numbers: Optional[List[Union[int, float]]]) -> int:
    result_sum = 0
    if numbers is not None:
        for s in numbers:
            result_sum += s
    return result_sum
