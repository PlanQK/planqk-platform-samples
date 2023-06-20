# ${PROJECT_NAME}

This is a PlanQK Service template for customer Docker containers.



The application expects a `values` array with numbers (see [data.json](./input/data.json)) as input and returns the sum of the values as output.
Further, it provides an optional flag to round up the sum, configurable through parameters (see [params.json](./input/params.json)).

Please note that the application implements the PlanQK Platform interface for custom Docker containers.
The PlanQK Platform ensures that the input provided via the Service API in the form of `{ "data": <data>, "params": <params> }` is provided to your code at runtime.
At runtime the input data is mounted to file `/var/input/data.json` and the parameters to `/var/input/params.json` of the running container.
Both files contain valid JSON strings, the respective values of `{ "data": <data>, "params": <params> }`.
Additionally, the platform requires that any output produced by the service to be in a specific format.
Specifically, the output must be printed to the standard output (stdout) and prefixed with `PlanQK:Job:Result:` followed by a valid JSON string.
More options to output results are available, see the [PlanQK documentation](https://docs.platform.planqk.de/docs/service-platform/managed-services-custom-container.html#output).

> More information about the PlanQK Platform interface for custom Docker containers can be found in the [PlanQK documentation](https://docs.platform.planqk.de/docs/service-platform/managed-services-custom-container.html).

## Project structure

The template contains the following files and directories:

```
.
├── input
│   ├── data.json
│   └── params.json
├── Dockerfile
├── ...
├── openapi-spec.yml
└── README.md
```

The most important file is the `Dockerfile`.
Adapt this file to your needs.
You may also add additional files and directories to the project directory and add them to your container image.

The `input` directory contains some sample input to test your service, either locally using `docker run` or as a PlanQK Service using `planqk run`.

You may also want to specify your service's API using the `openapi-spec.yml` file.
You can leave most of the file as is, but you may adapt the schema of the HTTP POST method of the service API.
Specifically, you may want to adapt the `data` and `params` properties of the `requestBody` object, see line 30-51.

The template specifies the following schema for the `data` and `params` properties, expressing that the `data` property is an object with a `values` array of numbers and the `params` property is an object with a `round_up` boolean flag:

```yaml
schema:
  type: object
  properties:
    data:
      type: object
      properties:
        values:
          type: array
          items:
            type: number
    params:
      type: object
      properties:
        round_up:
          type: boolean
```

Adapt the schema to your needs.
Take a look to the [OpenAPI Specification](https://swagger.io/specification) for more information.

## Run the project

### ${PROJECT_LANG}

To run the application using ${PROJECT_LANG}, make sure you have ${PROJECT_LANG} installed on your system, navigate to the root directory of the project, and run the following command:

```bash
${PROJECT_RUN_COMMAND}
```

The application reads the input data from the file `/var/input/data.json` by default.
If the file is not found, it falls back to the `./input/data.json` file.
The application also reads parameters from the file `/var/input/params.json` by default.
If the file is not found, it falls back to the `./input/params.json` file, otherwise it assumes that `round_up` is `false`.

### Docker

To run the application using Docker, make sure you have Docker installed on your system, navigate to the root directory of the project, and run the following commands:

```bash
docker build -t ${PROJECT_NAME} .

PROJECT_ROOT=(`pwd`)
docker run -v $PROJECT_ROOT/input:/var/input ${PROJECT_NAME}
```

> **Info**:
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
> docker run -v %cd%/input:/var/input ${PROJECT_NAME}
> ```

This command uses the `data.json` and the `params.json` file from the `./input` directory as the input for your service.
The `-v` option is used to mount this directory as volume in the Docker container.
The Docker container runs the application and prints the result to stdout.

## Next steps

Use `planqk up` to deploy your service to the PlanQK Platform.
Next, you may use `planqk run` to execute your service.
For more information, see the [PlanQK documentation](https://docs.platform.planqk.de/docs/getting-started/quickstart.html).
