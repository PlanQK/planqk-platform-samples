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
algorithm_dto = AlgorithmDto(name="My Algorithm", computation_model="CLASSIC")
algorithm = algorithm_api.create_algorithm(algorithm_dto)

algorithm = algorithm_api.get_algorithm(algorithm.id)

"""
Updates several attributes of the algorithm
"""

name = "Updated algorithm name"
acronym = "ALG"
intent = "intent_example"
problem = "problem_example"
input_format = "input_format_example"
algo_parameter = "algo_parameter_example"
output_format = "output_format_example"
solution = "solution_example"
assumptions = "assumptions_example"
computation_model = "HYBRID"
speed_up = "unknown"
nisq_ready = True

# Create the update request payload
update_algorithm_request = UpdateAlgorithmRequest(
    id=algorithm.id,
    computation_model=computation_model,
    name=name,
    acronym=acronym,
    intent=intent,
    problem=problem,
    solution=solution,
    input_format=input_format,
    algo_parameter=algo_parameter,
    output_format=output_format,
    assumptions=assumptions,
    nisq_ready=nisq_ready,
    speed_up=speed_up
)
algorithm = algorithm_api.update_algorithm(algorithm_id=algorithm.id, update_algorithm_request=update_algorithm_request)
