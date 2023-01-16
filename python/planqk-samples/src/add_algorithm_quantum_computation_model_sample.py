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

# Retrieve a list of available quantum computation models
quantum_computation_models = taxonomies_api.get_quantum_computation_models()

# Retrieve Quantum Annealing from the list
quantum_computation_model_name = "Quantum Annealing"
quantum_annealing = [qa for qa in quantum_computation_models if qa.label == quantum_computation_model_name]

"""
Updates the algorithm and adds a quantum computation model to it
"""

# Create the update request payload
update_algorithm_request = UpdateAlgorithmRequest(
    id=algorithm.id,
    name="updated quantum algorithm's name",
    computation_model="QUANTUM",
    quantum_computation_model_uuids=[quantum_annealing[0].uuid]
)
algorithm = algorithm_api.update_algorithm(
    algorithm_id=algorithm.id,
    update_algorithm_request=update_algorithm_request
)

# Remove all assigned quantum computation models
# update_algorithm_request = UpdateAlgorithmRequest(
#     id=algorithm.id,
#     name=algorithm.name,
#     computation_model=algorithm.computation_model,
#     quantum_computation_model_uuids=[]
# )
# algorithm = algorithm_api.update_algorithm(
#     algorithm_id=algorithm.id,
#     update_algorithm_request=update_algorithm_request
# )
