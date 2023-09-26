from transformers import pipeline
import json


def read_json_file(filepath, default_value=None):
    try:
        with open(filepath) as f:
            return json.load(f)
    except:
        return default_value


# Read the input files
input_data = read_json_file('/var/input/data.json') or read_json_file('./input/data.json')

if not input_data:
    print('Error: data.json file not found')
    exit(1)


pipe = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
input = input_data.get('input', "This is a great place to eat.")
res = pipe(input)

result = {"input": input, "classification": res} 

# Return the result as a JSON object
print("PlanQK:Job:Result:", json.dumps(result))
