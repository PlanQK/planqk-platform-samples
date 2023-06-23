# python-starter

You have your quantum code ready in a Python file and want to provide it to others via the PlanQK platform?
Great, only a few more steps until your service is ready and can be deployed!

## 1. Adapt your code for the user code template

Your code must be structured in a (not too) specific way.
This template is available via the [help page](https://docs.platform.planqk.de/en/latest/platform_instructions/service_platform.html).
Follow either the instructions in order to generate it or download the zip file.
After generating/extracting it, you should find the following structure:

```
.
├── Dockerfile
├── openapi-spec.yml
├── environment.yml
├── requirements.txt
├── input
│   └── ...
└── src
    ├── __init__.py
    ├── __main__.py
    ├── libs
    │   ├── __init__.py
    │   ├── return_objects.py
    │   └── ...
    └── program.py
``` 

The most important method, which takes the user input and generates the output of interest is the `run` method inside `program.py`.

> **IMPORTANT:**
> Do not rename either the `src` folder, the `program.py` package, as well as the `run` method inside it.
> These are fixed entry points for the service.
> Changing their names will result in a malfunctioning service.

The fist goal is to be able to run the `src` directory as a Python module with your own code inside `program.py`.
Execute the following when inside the root folder:

> **HINT:**
> As an alternative to Conda, you may use `requirements.txt` to create a virtual environment with the tooling of your choice.

```bash
conda env create -f environment.yml
conda activate python-starter
python3 -m src
```

This will execute the `__main__`-method inside the `src` folder.
Locally, you can test your code with a JSON-conform input format that gets imported within the `__main__`-method.
The input must have the properties `"data"` and `"params"`.

Any required python package (like `numpy`, `pandas`, ...) must be mentioned within, you guessed it, the `environment.yml` with their version number in the pip-installation format (e.g. `numpy==1.19.0`).
It is important to define your dependencies in the `environment.yml` file as this file is used later by the PlanQK Platform at runtime.
For development, you may use the `requirements.txt` file and a virtual environment tooling of your choice.
Once you've installed your dependencies, you can import these packages within any Python file needed.

If you have written packages yourself, which are required for your service, you can simply put them into the `libs` folder and import them via relative imports into your program.

> **NOTE:**
> If you plan to run your program on real quantum hardware or cloud simulators, your program should expect some valid `"backend"`-string within the `"params"` object (e.g. `"backend": "ibmq_qasm_simulator"` or `"backend": "ibmq_manila"`).

> **RECOMMENDED:**
> After being able to run your code as a module and if you're interested in offering your service via an API to others, you should also take the time to adapt the `openapi-spec.yml` file, in order to describe your API.

At last, you must zip (at minimum) the `src` folder and the `environment.yml` file, which will be the file you upload in order to create a PlanQK Service.
**You must not zip the project folder itself but its content.**
Execute the following from within the project folder:

```bash
zip -r user_code.zip src environment.yml
```

## 2. Service Creation

Now that you have your service in a zip-file, creating a PlanQK Service via the platform is easy:
From the landing page, go to "[Service Platform > My Services](https://platform.planqk.de/services)".
Here you need to click on `Create Service` in the top right corner.

> **NOTE:**
> You need to create a valid credit card before as described in this [video tutorial](https://www.loom.com/share/1ddf3b919bbc4219883f576931a14a12).
> A detailed step-by-step guide is also available in the [PlanQK documentation](https://docs.platform.planqk.de/en/latest/platform_instructions/service_platform.html).

**Service Properties**

| Property          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name              | Choose a meaningful name for your service. If you publish your service later on, this name will be displayed to other users.                                                                                                                                                                                                                                                                                                                                                                                                             |
| Service Import    | Click on "Import from file" and upload your zipped service. The option "Import from URL" can be used if your service is running somewhere (e.g., on your own infrastructure) and you just want the PlanQK platform to manage the access to it.                                                                                                                                                                                                                                                                                           |
| API Specification | Click on "Import from OpenAPI File" if you have prepared an OpenAPI specification for your service describing your service interface and input data. You can leave this empty to use the default OpenAPI specification supplied with this template.                                                                                                                                                                                                                                                                                      | 
| Description       | Other users will see this description of the service, if its name sparked some interest, and they clicked on it in the marketplace. So any additional information you want to provide goes in here.                                                                                                                                                                                                                                                                                                                                      |
| Quantum Backend   | Currently, only IBM and D-Wave are supported quantum backends and only one can be picked. Afterwards, you have to decide to use your own Quantum Backend Token (see [Add tokens to your account](#add-tokens-to-your-account)) or if you let PlanQK manage it for you. If you are working with local simulators only (e.g., when using the `AerBackend` from Qiskit or the `SimulatedAnnealingSampler` from the D-Wave anneal package) you may choose the option "None", since locally running code does not get affected by the choice. |
| Pricing Plans     | Will be important for when you want to offer your service via the marketplace and charge your customers for using them. If you just want to test your service, you should select "Free".                                                                                                                                                                                                                                                                                                                                                 |

And there you go.
As soon as you click on "Create Service", the containerization of your program code starts and will be deployed on the PlanQK Platform.
As soon as it's finished (as indicated in the "My services" section) you will be able to publish and test your service thoroughly.
For example, you may run a PlanQK Job against it.
Further, you may publish it for internal use or into the PlanQK Marketplace to share it with other PlanQK users.

# Additional Infos

## Add Tokens to Your Account

When you want to execute services via real quantum backends, you must provide valid tokens, in order to communicate with IBM's or D-Wave's devices.
To add a token, go to the user-menu in the top right corner and click on "Settings".
Under "Quantum Backend Tokens" you can add one to your account.

> **IMPORTANT:**
> These tokens will be used when you select the _Use your own Quantum Backend Token_ option during service creation.

## Test Your Implementation Using Docker

You may utilize Docker to test your current implementation.
In general, by following the next steps you replicate the steps done by the PlanQK platform, which is a way to verify your service in an early stage.

### Build the Docker Image

```bash
docker pull ghcr.io/planqk/job-template:latest-base-1.0.0
docker build -t python-starter .

# or (for Apple M1 chips)
docker buildx build -o type=docker --platform "linux/amd64" --tag python-starter .
```

### Start the Docker Container

In case, you do not use any input data or parameters that need to be passed into the container, you may run the container with the following command:

```bash
docker run -it \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  python-starter
```

However, to pass the `"data"` and `"params"` attributes as JSON-serialized files into the container, you either mount it in the form of separate files (recommended) or pass it as environment variables (base64 encoded).

To use the [`data.json`](input/data.json) and [`params.json`](input/params.json) from the [`input`](input) directory, you could execute the following command:

```bash
PROJECT_ROOT=(`pwd`) 
docker run -it \
  -e BASE64_ENCODED=false \
  -e LOG_LEVEL=DEBUG \
  -v $PROJECT_ROOT/input/data.json:/var/input/data/data.json \
  -v $PROJECT_ROOT/input/params.json:/var/input/params/params.json \
  python-starter
```

> **HINT**
> For GitBash users on Windows, replace
> ```bash
> PROJECT_ROOT=(`pwd`)
> ```
> with
> ```bash
> PROJECT_ROOT=(/`pwd`)
> ```
>
> For Windows command-prompt users, you can use the following command:
> ```bash
> docker run -it \
>   -e BASE64_ENCODED=false \
>   -e LOG_LEVEL=DEBUG \
>   -v %cd%/input/data.json:/var/input/data/data.json \
>   -v %cd%/input/params.json:/var/input/params/params.json \
>   python-starter
> ```

> **NOTE:**
> In general, you may mount any JSON-serialized input data file to `/var/input/data/data.json` and any file containing params to `/var/input/params/params.json` of the `python-starter` container.

If the service executed successfully, you should see something like `Job:ResulsResponse:` followed by the output you defined for your service.
Otherwise, if you see `Job:ErrorResponse`: Bad news, something went wrong.
However, the details of the response hopefully give you a clue as to what the problem was.

Alternatively, you could also pass any input by environment variables.
You can either use command line tools like `base64` or [Base64 Encoder](https://www.base64encode.org) to encode the input.
For example, to create a base64 encoded string of the `"data"` part of the `input.json` file, execute the following:

```bash
base64 -w 0 <<EOF
{"values": [100, 50, 200, 70, 0.69]}
EOF

>> eyJ2YWx1ZXMiOiBbMTAwLCA1MCwgMjAwLCA3MCwgMC42OV19
```

> **NOTE:**
> In general, the maximum default length of environment variables in Linux-based systems is at 128KiB.
> On Windows, the maximum default length is at 32KiB.

To create a base64 encoded string of the `"params"` part, execute the following:

```bash
base64 -w 0 <<EOF
{"round_off": false}
EOF

>> eyJyb3VuZF9vZmYiOiBmYWxzZX0=
```

Afterwards, start the container with the environment variables `DATA_VALUE` and `PARAMS_VALUE` as follows:

```bash
docker run -it \
  -e DATA_VALUE=eyJ2YWx1ZXMiOiBbMTAwLCA1MCwgMjAwLCA3MCwgMC42OV19 \
  -e PARAMS_VALUE=eyJyb3VuZF9vZmYiOiBmYWxzZX0= \
  python-starter
```
