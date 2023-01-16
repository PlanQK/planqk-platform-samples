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

# Required attributes to create an algorithm
algorithm_dto = AlgorithmDto(id="", name="My Algorithm", computation_model="CLASSIC")
algorithm = algorithm_api.create_algorithm(algorithm_dto)

algorithm = algorithm_api.get_algorithm(algorithm.id)

# Uploads a sketch
description = "Sketch description"
base_url = "https://platform.planqk.de/qc-catalog"
file = open("Absolute path to the file", 'rb')
sketch = algorithm_api.upload_sketch(
    algorithm_id=algorithm.id,
    description=description,
    base_url=base_url,
    file=file
)

sketch = algorithm_api.get_sketch(algorithm_id=algorithm.id, sketch_id=sketch.id)
sketch_image = algorithm_api.get_sketch_image(algorithm_id=algorithm.id, sketch_id=sketch.id)

# Deletes sketch
algorithm_api.delete_sketch(algorithm_id=algorithm.id, sketch_id=sketch.id)
