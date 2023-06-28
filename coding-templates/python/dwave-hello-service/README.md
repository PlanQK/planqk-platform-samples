# PlanQK D-Wave Service: A Hello World Example

This example is prepared to be run on the PlanQK Platform.
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

Alternatively, you can execute the container using a PlanQK personal access token.
Set up a [PlanQK personal access token](https://platform.planqk.de/settings/access-tokens) with `api` and `quantum_tokens` scope.
Further, add your D-Wave Leap access token under the [Quantum Backend Token](https://platform.planqk.de/settings/backend-tokens) section in your user settings.
Next, you can run the following command:

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
zip -r dwave-hello-service.zip src environment.yml
```

Navigate to <https://platform.planqk.de> and create a new PlanQK Service or you may use the [PlanQK CLI](https://docs.platform.planqk.de/docs/getting-started/quickstart.html).

> **HINT:**
> To use the PlanQK CLI, you need to create a `planqk.json` file.
> See the [documentation](https://docs.platform.planqk.de/docs/getting-started/planqk-json-reference.html) for more details.

Next, you may run a PlanQK Job against your new PlanQK Service.
Further, you may publish for internal use or into the PlanQK Marketplace to share it with other PlanQK users.
