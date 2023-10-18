import gradio as gr
from planqk.service.client import PlanqkServiceClient

consumer_key = "noop"
consumer_secret = "noop"
service_endpoint = "noop"

title = "python-starter: sum of values"
description = "This service sums up all values in the input array."


def run_service(values_array: list[list[float]], round_off: bool):
    client = PlanqkServiceClient(service_endpoint, consumer_key, consumer_secret)

    values: list[float] = []
    for v in values_array:
        values.append(v[0])

    data = {
        "values": values,
    }
    params = {
        "round_off": round_off,
    }
    print(f"data={data}", f"params={params}")

    job = client.start_execution(data=data, params=params)
    result = client.get_result(job.id)

    print(f"result={result}")
    return float(result["result"]["sum"])


demo = gr.Interface(
    run_service,
    [
        gr.Dataframe(
            label="The values to sum up",
            headers=["Values"],
            value=[[1], [2], [3], [4], [5]],
            col_count=(1, "fixed"),
            type="array"
        ),
        gr.Checkbox(label="Round off the result"),
    ],
    gr.Number(label="The sum of the values"),
    examples=[
        [
            [[1], [2], [3], [4], [5]],
            False
        ],
        [
            [[100], [50], [200], [70], [0.69]],
            True
        ],
    ],
    title=title,
    description=description,
    allow_flagging="never"
)

demo.launch()
