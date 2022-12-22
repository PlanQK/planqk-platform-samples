from openapi_client.configuration import Configuration
from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformServicesApi

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
service_api = ServicePlatformServicesApi(api_client=api_client)

lifecycle = "ACCESSIBLE"
service_api.get_services(lifecycle=lifecycle)
