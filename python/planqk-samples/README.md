# PlanQK Platform Sample for Python

This repository contains several examples showing how to use Python and PlanQK's API client to interact with the platform.

## Prepare the project

Set up a new Python virtual environment, e.g., you may use Conda and the following commands:

```bash
conda env create -f environment.yml
conda activate planqk-samples
```

Afterwards, install the required third-party dependencies into your virtual environment:

```bash
pip install -r requirements.txt
```

## Generate and prepare the API client

Install the OpenAPI Generator:

```bash
npm install -g @openapitools/openapi-generator-cli
```

Generate the API client project in a new directory:

```bash
mkdir generator-output && cd generator-output

openapi-generator-cli version-manager set 5.4.0
openapi-generator-cli generate -g python -i https://platform.planqk.de/qc-catalog/v3/api-docs
cp -R openapi_client ../src
```

## Run the examples

> Make sure you are inside the `src` directory, then for example run the following command:

```bash
python3 authentication_sample.py
```
