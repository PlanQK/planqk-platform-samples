# dwave-ide

This example is prepared to be run locally in your IDE or from command-line.
The program code in this example only contains PlanQK authentication credentials, i.e., a PlanQK personal access token.
However, you are able to run the program code as is as PlanQK Service on the PlanQK Platform.

First, open [`src > program.py`](src/program.py) and add your PlanQK personal access token (requires `api` and `quantum_tokens` scope) in line 11:

```python
PLANQK_PERSONAL_ACCESS_TOKEN = "change me for local usage"
```

Furthermore, it is required to add your personal D-Wave Leap access token under the
_Quantum Backend Token_ section in your [user settings](https://platform.planqk.de/settings/backend-tokens).
Next, you may run the program code from the command-line:

> **HINT:**
> As an alternative to Conda, you may use `requirements.txt` to create a virtual environment with the tooling of your choice.

```bash
conda env create -f environment.yml
conda activate python-starter-dwave-ide
python3 -m src
```

In turn, the exact same code can be run as PlanQK Service.
To avoid that your personal access token is packaged with the program code, you may use the `noop` value for the `PLANQK_PERSONAL_ACCESS_TOKEN` environment variable.
The PlanQK Platform will automatically inject the appropriate access tokens at runtime to run your program code.

Execute the following command to package the program code and the required metadata files:

```bash
zip -r python-starter-dwave-ide.zip src environment.yml
```

Navigate to <https://platform.planqk.de> and create a new PlanQK Service or you may use the [PlanQK CLI](https://docs.platform.planqk.de/quickstart.html).

> **HINT:**
> To use the PlanQK CLI, you need to create a `planqk.json` file.
> See the [documentation](https://docs.platform.planqk.de/planqk-json-reference.html) for more details.

Next, you may run a PlanQK Job against your new PlanQK Service.
Further, you may publish for internal use or into the PlanQK Marketplace to share it with other PlanQK users.
