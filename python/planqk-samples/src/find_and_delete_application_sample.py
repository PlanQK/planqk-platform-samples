from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformApplicationsApi
from openapi_client.configuration import Configuration

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
applications_api = ServicePlatformApplicationsApi(api_client=api_client)

name = 'My Application'

# Either use "get_application(...)" to look-up by id, or search for it by name, which is what we show next
applications = applications_api.get_applications()

found_application = None

# Filter the list by name
for application in applications:
    if application['name'] == name:
        found_application = application

# Deletes application, if found
applications_api.delete_application(found_application.id)
