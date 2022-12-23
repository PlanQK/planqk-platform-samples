import time

import requests
from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformApplicationsApi
from openapi_client.apis import ServicePlatformServicesApi
from openapi_client.configuration import Configuration
from openapi_client.model.create_application_request import CreateApplicationRequest
from openapi_client.model.create_internal_subscription_request import CreateInternalSubscriptionRequest


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


# Waits up to 5 minutes for a PlanQK Service execution to finish.
def wait_for_execution_to_be_finished():
    status_timer = 0
    execution_status = requests.get(url=status_url, headers=default_headers).json()['status']
    while execution_status == 'PENDING':
        time.sleep(15)
        status_timer += 15
        if status_timer > 300:
            print("Timeout exceeded waiting for PlanQK Service execution to be finished")
            break
        execution_status = requests.get(url=status_url, headers=default_headers).json()['status']
        if execution_status == 'SUCCEEDED' or execution_status == 'FAILED':
            return execution_status
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

# Publish the service for internal use (only you can subscribe to it and, for example, execute PlanQK Jobs with it)
version = services_api.publish_service_internal(service_id=service.id, version_id=version.id)

# Internally published services are in lifecycle state "ACCESSIBLE"
if version.lifecycle == "ACCESSIBLE":
    print("service successfully published")

# Create a PlanQK Application
create_app_request = CreateApplicationRequest(name="My Application")
application = applications_api.create_application(create_application_request=create_app_request)

# Subscribe your application with the internally published service
subscription_request = CreateInternalSubscriptionRequest(
    application_id=application.id,
    service_id=service.id,
)

applications_api.create_internal_subscription(
    id=application.id,
    create_internal_subscription_request=subscription_request
)

"""
You require an access token to execute a PlanQK Service.
This access token must be sent as "Authorization" header in any request of the PlanQK
Service API. The header must follow the following template: "Authorization: Bearer <your access token>"
"""
access_token = applications_api.get_access_token(id=application.id)['token']

"""Each managed PlanQK Service provides three HTTP endpoints as its API (this may differ for "external" PlanQK 
Services, therefore, check in "Marketplace > Services > Service Details > Technical Specifications" the published API 
description): 

(1) "POST /": Executes the service in an asynchronous fashion; returns an execution id
(2) "GET /<execution id>": Used to check the status of your execution
(3) "GET /<execution id>/result": Used to retrieve the final result for your execution

"""

# Prepare input file containing the "data" and "params" JSON structure:
input_data = open("Absolute path to your input file, e.g., 'input.json'", 'rb')

# Prepare the HTTP payload to trigger an execution
service_endpoint = version.gateway_endpoint
default_headers = {
    "Authorization": f"Bearer {access_token}",
    'Content-Type': 'application/json'
}

# Execute the service
execution = requests.post(url=service_endpoint, data=input_data, headers=default_headers)

execution_id = ""  # id for the current execution
if execution.status_code in (200, 201):
    execution_id = execution.json()['id']
else:
    print(f"The service execution failed with status code:{execution.status_code}")

# Url for checking the status of the execution
status_url = service_endpoint + '/' + execution_id

# check if execution has finished
current_status = wait_for_execution_to_be_finished()
print(f"The service execution is: {current_status}")

if current_status == 'SUCCEEDED':
    result = requests.get(url=status_url + '/result', headers=default_headers).json()
    print(f"The service execution result: {result}")
