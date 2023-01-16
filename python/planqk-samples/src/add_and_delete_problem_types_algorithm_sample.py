from openapi_client.api_client import ApiClient
from openapi_client.apis import CommunityAlgorithmsApi
from openapi_client.configuration import Configuration
from openapi_client.model.algorithm_dto import AlgorithmDto
from openapi_client.model.update_algorithm_request import UpdateAlgorithmRequest
from openapi_client.apis import TaxonomiesApi

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
algorithm_api = CommunityAlgorithmsApi(api_client=api_client)
taxonomies_api = TaxonomiesApi(api_client=api_client)

# Required attributes to create an algorithm
algorithm_dto = AlgorithmDto(name="My Algorithm", computation_model="CLASSIC")
algorithm = algorithm_api.create_algorithm(algorithm_dto)

algorithm = algorithm_api.get_algorithm(algorithm.id)

# Retrieve a list of available problem types
problem_types = taxonomies_api.get_problem_types()

# Retrieve Artificial Intelligence Problem from the list
problem_type_name = "Artificial Intelligence Problem"
artificial_intelligence_problem = [pt for pt in problem_types if pt.label == problem_type_name]

"""
Problem types have children or sub-categories e.g.
Natural language processing is a child of Artificial Intelligence Problem.
Below we show how to retrieve Natural language processing from the list
"""
problem_type_children_name = "Natural language processing"
natural_language_processing = [pt for pt in problem_types[0].children if pt.label == problem_type_children_name]

"""
Updates the algorithm and adds problem types to it
"""

# Create the update request payload
update_algorithm_request = UpdateAlgorithmRequest(
    id=algorithm.id,
    name="updated algorithm name",
    computation_model="HYBRID",
    problem_type_uuids=[artificial_intelligence_problem[0].uuid, natural_language_processing[0].uuid]
)
algorithm = algorithm_api.update_algorithm(algorithm_id=algorithm.id, update_algorithm_request=update_algorithm_request)

# Remove all assigned problem types
update_algorithm_request = UpdateAlgorithmRequest(
    id=algorithm.id,
    name=algorithm.name,
    computation_model=algorithm.computation_model,
    problem_type_uuids=[]
)
algorithm = algorithm_api.update_algorithm(algorithm_id=algorithm.id, update_algorithm_request=update_algorithm_request)
