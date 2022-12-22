from openapi_client.api_client import ApiClient
from openapi_client.apis import ServicePlatformApplicationsApi
from openapi_client.apis import ServicePlatformMarketplaceApi
from openapi_client.apis import ServicePlatformServicesApi
from openapi_client.configuration import Configuration
from openapi_client.model.create_application_request import CreateApplicationRequest
from openapi_client.model.create_subscription_request import CreateSubscriptionRequest

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
services_api = ServicePlatformServicesApi(api_client=api_client)
applications_api = ServicePlatformApplicationsApi(api_client=api_client)
marketplace_api = ServicePlatformMarketplaceApi(api_client=api_client)

# Create a PlanQK Application
create_app_request = CreateApplicationRequest(
    name="My Application",
)
application = applications_api.create_application(create_application_request=create_app_request)
application = applications_api.get_application(id=application.id)

"""
Find a PlanQK Service in the PlanQK Marketplace
Either use "findService(...)" to look-up by id (the id of a service can be found in
Marketplace > Services > Service Details > Technical Specifications),
or search for it by name, which is what we show next
"""

# Get all available PlanQK Services
apis = marketplace_api.find_services()
service_name = "Published Service"

# Filter the list by name
for x in apis:
    if x['name'] == service_name:
        api = x

"""
Each PlanQK Service has at least one pricing plan.
You must select a suitable one, either a "free" plan if available of a "paid" plan.
"""

# We assume here your selected PlanQK Service provides a "free" plan
free_plan = api['pricing_plans'][0]

# Subscribe your application with the published service
create_subscription_request = CreateSubscriptionRequest(application_id=application.id, pricing_plan_id=free_plan.id)
marketplace_api.create_subscription(id=api.id, create_subscription_request=create_subscription_request)

# Retrieve a list of all active subscriptions of an application
subscriptions = applications_api.get_application_subscriptions(id=application.id)
