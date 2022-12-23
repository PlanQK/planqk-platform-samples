from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformServicesApi
from openapi_client.configuration import Configuration

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access toke'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
service_api = ServicePlatformServicesApi(api_client=api_client)

"""
Uncomment one of the following lines if your self-hosted service communicates with of the quantum cloud providers,
e.g., with IBM Quantum Cloud or D-Wave Leap.
"""
quantumBackend = "NONE"  # Default value
# quantumBackend = "IBM";
# quantumBackend = "DWAVE";

name = "Your service name"
production_endpoint = "Your public endpoint URL"
description = "Your service description"
api_definition = open("Absolute path to your OpenAPI definition", 'rb')
service = service_api.create_external_service(
    name=name,
    url=production_endpoint,
    quantum_backend=quantumBackend,
    description=description,
    api_definition=api_definition
)

"""
A PlanQK Service consists of a list of ServiceDefinitionDto objects. A service definition represents a certain version of a
PlanQK Service. At the moment, there will always be one service definition object in the list. In the future, you will be
able to maintain multiple versions of your service.
"""
version = service.service_definitions[0]

service = service_api.get_service(service.id)

# You can delete the service after you finish
# service_api.delete_service(service.id)
