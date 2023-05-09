# PlanQK D-Wave Service: A Hello World Example

This example is prepare to run on the PlanQK Platform.
This means, the program code does not contain any authentication credentials such as D-Wave Leap access tokens.
So, if you try to run the program in your IDE or from command-line it will fail with the error `API token not defined`.
You could try it by yourself using the following code:

> **HINT:**
> As an alternative to Conda, you may use `requirements.txt` to create a virtual environment with the tooling of your choice.

```bash
conda env create -f environment.yml
conda activate dwave-hello-service
python3 -m src
```

However, by using the PlanQK Docker container you may replicate in your local environment what the PlanQK Platform does at runtime.
This is very useful for local testing before creating a PlanQK Service on the PlanQK Platform.

First, build the container:

```bash
docker pull ghcr.io/planqk/job-template:latest-base-1.0.0
docker build -t dwave-hello-service .
```

This simple example does not utilize any inputs.
Therefore, to start the container you may run the container as follows:

> **IMPORTANT:**
> Change the value of the `PLATFORM_TOKEN` environment variable to your personal D-Wave Leap access token.

```bash
docker run -it \
  -e FRAMEWORK=DWAVE \
  -e PLATFORM_TOKEN=<add your D-Wave Leap access token> \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  dwave-hello-service
```

Further, you can similarly execute your program utilizing PlanQK Platform capabilities.
For this, you have to set up a PlanQK personal access token with `api` and `quantum_tokens` scope and add your D-Wave Leap access token under the _Quantum Backend Token_ section in your user settings.
Afterwards, you can run the following command:

```bash
docker run -it \
  -e FRAMEWORK=DWAVE \
  -e DWAVE_ENDPOINT=https://platform.planqk.de/dwave/sapi/v2 \
  -e PLATFORM_TOKEN=<add your PlanQK personal access token> \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  dwave-hello-service
```

Finally, you are now prepared to create a PlanQK Service.
Execute the following command to package the program code and the required metadata files:

```bash
zip -r user_code.zip src environment.yml openapi-spec.yml requirements.txt
```

Navigate to <https://platform.planqk.de> and create a new PlanQK Service ([more info](https://docs.platform.planqk.de/en/latest/platform_instructions/service_platform.html#deploy-services-on-the-planqk-platform)) or, if you have the [PlanQK CLI](https://docs.platform.planqk.de/en/latest/platform_instructions/service_platform.html#using-the-planqk-cli) installed, execute the following command:

```bash
planqk up --file=user_code.zip
```

Afterwards, you may run a PlanQK Job against your new PlanQK Service.
Further, you may publish for internal use or into the PlanQK Marketplace to share it with other PlanQK users.
