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

# Retrieve a list of available application areas
application_areas = algorithm_api.get_application_areas()

# Retrieve Engineering Science from the list
application_area_name = "Engineering Science"
engineering_science = [area for area in application_areas if area.label == application_area_name]

"""
Application areas have children or sub-categories e.g.
Civil Engineering is a child of Engineering Science.
Below we show how to Civil Engineering from the list
"""
application_area_children_name = "Civil Engineering"
civil_engineering = [a for a in application_areas[0].children if a.label == application_area_children_name]

"""
Adds application areas to the algorithm
"""
# Create the update request payload
update_algorithm_request = UpdateAlgorithmRequest(
    id=algorithm.id,
    name="updated algorithm's name",
    computation_model="HYBRID",
    application_area_uuids=[engineering_science[0].uuid, civil_engineering[0].uuid]
)
algorithm = algorithm_api.update_algorithm(
    algorithm_id=algorithm.id,
    update_algorithm_request=update_algorithm_request
)

# Remove all assigned application areas
update_algorithm_request = UpdateAlgorithmRequest(
    id=algorithm.id,
    name=algorithm.name,
    computation_model=algorithm.computation_model,
    problem_type_uuids=[]
)
algorithm = algorithm_api.update_algorithm(
    algorithm_id=algorithm.id,
    update_algorithm_request=update_algorithm_request
)
