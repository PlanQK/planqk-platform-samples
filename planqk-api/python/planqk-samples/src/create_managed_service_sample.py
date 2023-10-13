import time

from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformServicesApi
from openapi_client.configuration import Configuration

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)


# Waits up to 5 minutes till the PlanQK Service has been created
def wait_for_service_to_be_created():
    timer = 0
    # Check build status
    build_status = services_api.get_build_status(service_id=service.id, version_id=version.id)
    while build_status['status'] == 'WORKING' or build_status['status'] == 'QUEUED':
        time.sleep(15)
        timer += 15
        if timer > 300:
            break
        # Check build status again to see if job failed or succeeded
        build_status = services_api.get_build_status(service_id=service.id, version_id=version.id)
        if build_status['status'] == 'SUCCESS':
            print("Service successfully created".upper())
            break
        elif build_status['status'] == 'FAILURE':
            print("Error creating PlanQK Service".upper())
            break


# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
services_api = ServicePlatformServicesApi(api_client=api_client)

"""
Uncomment one of the following lines if your self-hosted service communicates with of the quantum cloud providers,
e.g., with IBM Quantum Cloud or D-Wave Leap.
"""
quantumBackend = "NONE"  # Default value
# quantumBackend = "IBM";
# quantumBackend = "DWAVE";

name = "Your service name"
description = "Your service description"
use_platform_token = "FALSE"  # FALSE to use own backend tokens in case 'quantumBackend' is 'DWAVE', 'IBM' etc.
cpu = 500  # minimum
memory = 2048  # default memory configuration: 2048 = 2GB
user_code = open('Absolute path to the user_code.zip file', 'rb')
api_definition = open('Absolute path to the OpenAPI definition', 'rb')

service = services_api.create_managed_service(
    name=name,
    quantum_backend=quantumBackend,
    description=description,
    use_platform_token=use_platform_token,
    cpu=cpu,
    memory=memory,
    user_code=user_code,
    api_definition=api_definition
)

"""
A PlanQK Service consists of a list of ServiceDefinitionDto objects. A service definition represents a certain version of a
PlanQK Service. At the moment, there will always be one service definition object in the list. In the future, you will be
able to maintain multiple versions of your service.
"""
version = service.service_definitions[0]

wait_for_service_to_be_created()

service = services_api.get_service(service.id)

# You can delete the service after you finish
# service_api.delete_service(service.id)
