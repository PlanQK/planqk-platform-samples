from openapi_client.api_client import ApiClient
from openapi_client.apis import CommunityAlgorithmsApi
from openapi_client.configuration import Configuration

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
algorithm_api = CommunityAlgorithmsApi(api_client=api_client)

# Query params that can be used to fetch the page of algorithms
search = ""  # parameter to filter the algorithms by name or acronym
page = 0  # Zero-based page index, allows to fetch a specific page
size = 20  # The size of the page to be returned
sort = [""]  # Sorting criteria in the format: (asc|desc). Default sort order is ascending.

# Either use "get_algorithm(...)" to look-up by id, or search for it by name, which is what we show next
# Get page of algorithms
algorithms = algorithm_api.get_algorithms(search=search, page=page, size=size, sort=sort)

found_algorithm = None
name = "My Algorithm"

# Filter the list by name
for algorithm in algorithms['content']:
    if algorithm['name'] == name:
        found_algorithm = algorithm

# Deletes algorithm, if found
algorithm_api.delete_algorithm(algorithm_id=algorithm.id)
