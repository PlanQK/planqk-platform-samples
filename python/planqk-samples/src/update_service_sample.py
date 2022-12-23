import time

from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformApplicationsApi
from openapi_client.apis import ServicePlatformServicesApi
from openapi_client.configuration import Configuration
from openapi_client.model.industry_dto import IndustryDto
from openapi_client.model.update_version_request import UpdateVersionRequest


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


# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
services_api = ServicePlatformServicesApi(api_client=api_client)
applications_api = ServicePlatformApplicationsApi(api_client=api_client)

name = "Your service name"
quantumBackend = "NONE"  # Default value
description = "Your service description"
use_platform_token = "FALSE"  # FALSE to use own backend tokens in case 'quantumBackend' is 'DWAVE', 'IBM' etc.
cpu = 500  # minimum
memory = 2048  # default memory configuration: 2048 = 2GB

with open('Absolute path to the user_code.zip file', 'rb') \
        as user_code, open('Absolute path to the OpenAPI definition', 'rb') \
        as api_definition:
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

service = services_api.get_service(id=service.id)

# Retrieve a list of available industries
industries = services_api.get_industries()
# Retrieve 'information_technology' industry from the list
information_technology = None
industry_name = 'information_technology'

for industry in industries:
    if industry['name'] == industry_name:
        information_technology = IndustryDto(id=industry['id'], name=industry['name'])

# Create the update request payload
update_version_request = UpdateVersionRequest(
    description="Updated description",
    industries=[information_technology]
)
version = services_api.update_service_version(
    service_id=service.id,
    version_id=version.id,
    update_version_request=update_version_request
)

# Remove all assigned industries
update_version_request = UpdateVersionRequest(industries=[])
version = services_api.update_service_version(
    service_id=service.id,
    version_id=version.id,
    update_version_request=update_version_request
)

# Updates the source code of the service
with open('Path to the updated user_code.zip file', 'rb') as updated_user_code:
    services_api.update_source_code(
        service_id=service.id,
        version_id=version.id,
        source_code=updated_user_code
    )

wait_for_service_to_be_created()

# Updates the API Definition
with open('Path to the updated API definition', 'rb') as updated_api_definition:
    services_api.update_api_definition(
        service_id=service.id,
        version_id=version.id,
        file=updated_api_definition
    )
