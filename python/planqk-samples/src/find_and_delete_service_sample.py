from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformServicesApi
from openapi_client.configuration import Configuration
from openapi_client.model.service_dto import ServiceDto

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
services_api = ServicePlatformServicesApi(api_client=api_client)

# Either use "get_service(...)" to look-up by id, or search for it by name, which is what we show next
lifecycle = 'CREATED'
services = services_api.get_services(lifecycle=lifecycle)
name = "Your service name"

service = None
# Filter the list by name
for x in services:
    if x['My Service Name'] == name:
        service = x

# You can delete the service after you finish
services_api.delete_service(service.id)
