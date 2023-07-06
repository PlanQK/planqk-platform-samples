# qiskit-ibmq

```bash
conda env create -f environment.yml
conda activate qiskit-ibmq
python3 -m src
```

## Build the container

```bash
docker pull ghcr.io/planqk/job-template:latest-base-1.0.0
docker build -t planqk-qiskit-service .
```

## Start the container

You have to mount the `data.json` and `params.json` files from the `input` directory into the container.
You may run the container as follows - however, you could mount any other JSON-encoded file:

```bash
PROJECT_ROOT=(`pwd`) 
docker run -it \
  -e FRAMEWORK=QISKIT \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  -v $PROJECT_ROOT/input/data.json:/var/input/data/data.json \
  -v $PROJECT_ROOT/input/params.json:/var/input/params/params.json \
  planqk-qiskit-service
```

> **NOTE**:
> If you want to run your program against the IBMQ cloud, you have to modify the `params.json` and change the `"backend"` property to `"ibmq_qasm_simulator"` for example.
> Alternatively, you may use the `params-ibmq.json` file.
>
> In addition, you need to pass your IBMQ cloud token via the `PLATFORM_TOKEN` variable to the container:
>
> ```bash
> PROJECT_ROOT=(`pwd`) 
> docker run -it \
>   -e FRAMEWORK=QISKIT \
>   -e PLATFORM_TOKEN=<add your IBMQ access token> \
>   -e BASE64_ENCODED=false \
>   -e LOG_LEVEL=DEBUG \
>   -v $PROJECT_ROOT/input/data.json:/var/input/data/data.json \
>   -v $PROJECT_ROOT/input/params-ibmq.json:/var/input/params/params.json \
>   planqk-qiskit-service
> ```
