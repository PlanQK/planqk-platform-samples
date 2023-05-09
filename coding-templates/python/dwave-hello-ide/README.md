# PlanQK D-Wave: A Hello World Example

This example is prepare to run locally in your IDE or from command-line.
The program code in this example only contains PlanQK authentication credentials, i.e., a PlanQK personal access token.
However, you are able to run the program code as is as PlanQK Service on the PlanQK Platform.

First, open [`src > program.py`](src/program.py) and add your PlanQK personal access token (requires `api` and `quantum_tokens` scope) in line 11:

```python
PLANQK_PERSONAL_ACCESS_TOKEN = "change me for local usage"
```

Furthermore, it is required to add your personal D-Wave Leap access token under the _Quantum Backend Token_ section in your user settings.
Afterwards, you may run the program code from the command-line:

> **HINT:**
> As an alternative to Conda, you may use `requirements.txt` to create a virtual environment with the tooling of your choice.

```bash
conda env create -f environment.yml
conda activate dwave-hello-ide
python3 -m src
```

In turn, the exact same code can be run as PlanQK Service.
In this case, your personal access token will be packaged with the program code but will not be used at runtime because your code is already running on the PlanQK Platform and the runtime will directly use your configured D-Wave Leap access token.
Therefore, you may want to change the value of the `PLANQK_PERSONAL_ACCESS_TOKEN` to `noop` for example.

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
