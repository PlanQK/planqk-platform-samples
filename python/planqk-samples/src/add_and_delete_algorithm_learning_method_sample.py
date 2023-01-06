from openapi_client.api_client import ApiClient
from openapi_client.apis import CommunityAlgorithmsApi
from openapi_client.configuration import Configuration
from openapi_client.model.algorithm_dto import AlgorithmDto
from openapi_client.model.update_algorithm_request import UpdateAlgorithmRequest

# Pass dict with token as value to Configuration
api_key = {'apiKey': 'Your personal access token'}
configuration = Configuration(api_key=api_key)

# Pass config to ApiClient
api_client = ApiClient(configuration=configuration)
algorithm_api = CommunityAlgorithmsApi(api_client=api_client)

# Required attributes to create an algorithm
algorithm_dto = AlgorithmDto(id="", name="My Algorithm", computation_model="CLASSIC")
algorithm = algorithm_api.create_algorithm(algorithm_dto)
algorithm = algorithm_api.get_algorithm(algorithm.id)

# Retrieve a list of available learning methods
learning_methods = algorithm_api.get_learning_methods()

# Retrieve Supervised Learning from the list
learning_method_name = "Supervised Learning"
supervised_learning = [lm for lm in learning_methods if lm.label == learning_method_name]

"""
Updates the algorithm and adds a learning method to it
"""

# Create the update request payload
update_algorithm_request = UpdateAlgorithmRequest(
    id=algorithm.id,
    name="updated algorithm's name",
    computation_model="HYBRID",
    learning_method_uuids=[supervised_learning[0].uuid]
)
algorithm = algorithm_api.update_algorithm(
    algorithm_id=algorithm.id,
    update_algorithm_request=update_algorithm_request
)

# Remove all assigned learning methods
update_algorithm_request = UpdateAlgorithmRequest(
    id=algorithm.id,
    name=algorithm.name,
    computation_model=algorithm.computation_model,
    learning_method_uuids=[]
)
algorithm = algorithm_api.update_algorithm(
    algorithm_id=algorithm.id,
    update_algorithm_request=update_algorithm_request
)
