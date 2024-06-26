<p align="center">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/mqt_light.png" width="60%">
   <img src="https://raw.githubusercontent.com/cda-tum/mqt/main/docs/_static/mqt_dark.png" width="60%">
 </picture>
</p>

# MQT Coding Template @ PlanQK

This coding template provides a starting point for developing a service that uses software tools from the [Munich Quantum Toolkit (MQT)](https://mqt.readthedocs.io/),
which is a collection of software tools and libraries for quantum computing developed by the [Chair for Design Automation](https://www.cda.cit.tum.de/) at the [Technical University of Munich](https://www.tum.de/).
Currently, the following tools from the MQT are available as part of this coding template:

- [MQT DDSIM](https://github.com/cda-tum/mqt-ddsim): A Tool for Classical Quantum Circuit Simulation based on Decision Diagrams.
- [MQT QMAP](https://github.com/cda-tum/mqt-qmap): A Tool for Quantum Circuit Mapping.
- [MQT QCEC](https://github.com/cda-tum/mqt-qcec): A Tool for Quantum Circuit Equivalence Checking.
- [MQT Bench](https://github.com/cda-tum/mqt-bench): A tool for Benchmarking Software and Design Automation Tools for Quantum Computing.

For a full list of tools and libraries available as part of the MQT, please visit the [MQT website](https://mqt.readthedocs.io/).

<p align="center">
  <a href="https://mqt.readthedocs.io/">
  <img width=30% src="https://img.shields.io/badge/MQT@ReadTheDocs-blue?style=for-the-badge&logo=read%20the%20docs" alt="Documentation" />
  </a>
</p>

## Usage

The fist goal is to be able to run the `src` directory as a Python module with the code inside `program.py`.

We recommend building your service from within a dedicated and fresh Conda environment to install and track all required packages from the start.
For this reason, the template already contains an `environment.yml` file from which a fresh environment can be created:

> **HINT:**
> As an alternative to Conda, you may use the `requirements.txt` file to create a virtual environment with the tooling of your choice.

```bash
conda env create -f environment.yml
conda activate python-starter-mqt
python3 -m src
```

## Run the project using Docker

You may utilize Docker to run your code locally and test your current implementation.
In general, by following the next steps you replicate the steps done by the PlanQK platform, which is a way to verify your service in an early stage.

### Build the Docker image

```bash
docker pull ghcr.io/planqk/job-template:latest-base-1.0.0
docker build -t python-starter-mqt .

# or (for Apple M1 chips)
docker buildx build -o type=docker --platform "linux/amd64" --tag python-starter-mqt .
```

### Start the Docker container

In case, you do not use any input data or parameters that need to be passed into the container, you may run the container with the following command:

```bash
docker run -it \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  python-starter-mqt
```

However, to pass the `"data"` and `"params"` attributes as JSON-serialized files into the container, you either mount it in the form of separate files (recommended) or pass it as environment variables (base64 encoded).

To use the [`data.json`](input/data.json) and [`params.json`](input/params.json) from the [`input`](input) directory, you could execute the following command:

```bash
PROJECT_ROOT=(`pwd`)
docker run -it \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  -v $PROJECT_ROOT/input:/var/input \
  python-starter-mqt
```

If the service executed successfully, you should see something like `Job:ResulsResponse:` followed by the output you defined for your service.
Otherwise, if you see `Job:ErrorResponse`: Bad news, something went wrong.
However, the details of the response hopefully give you a clue what the problem was.
