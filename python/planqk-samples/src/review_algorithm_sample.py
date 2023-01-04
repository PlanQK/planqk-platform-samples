from openapi_client.api_client import ApiClient
from openapi_client.apis import CommunityAlgorithmsApi
from openapi_client.configuration import Configuration
from openapi_client.model.algorithm_dto import AlgorithmDto

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
algorithm_api = CommunityAlgorithmsApi(api_client=api_client)

algorithm_dto = AlgorithmDto(id="", name="My Algorithm", computation_model="CLASSIC")  # required
algorithm = algorithm_api.create_algorithm(algorithm_dto)

algorithm = algorithm_api.get_algorithm(algorithm.id)

# Starts the review of an algorithm by The PlanQK Expert Community
algorithm_api.start_review(algorithm.id)

# Reviewed by PlanQK Expert Community
algorithm_api.approve_review(algorithm.id)

# The review was withdrawn
algorithm_api.withdraw_review(algorithm.id)
