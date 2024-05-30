import json

from .program import run

input_file = 'input.json'
with open("./input/data.json", "r") as file:
    data = json.load(file)

with open("./input/params.json", "r") as file:
    params = json.load(file)

response = run(data, params)

with open("sample_result.json", "w") as file:
    json.dump(response.to_json(), file)

#print(response.to_json())
