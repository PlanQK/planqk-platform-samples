from openapi_client.configuration import Configuration
from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformApplicationsApi
from openapi_client.model.create_application_request import CreateApplicationRequest

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
application_api = ServicePlatformApplicationsApi(api_client=api_client)

application_name = "My Application"
create_app_request = CreateApplicationRequest(name=application_name)
application = application_api.create_application(create_app_request)
application = application_api.get_application(application.id)
