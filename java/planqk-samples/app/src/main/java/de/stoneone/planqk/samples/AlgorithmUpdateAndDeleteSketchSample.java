package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.SketchDto;
import java.io.File;
import java.io.IOException;

public class AlgorithmUpdateAndDeleteSketchSample {

    public static void main(String[] args) throws IOException {
        String token = "Your personal access token";
        ApiClient apiClient = new ApiClient("apiKey", token);

        CommunityAlgorithmsApi algorithmApi = apiClient.buildClient(CommunityAlgorithmsApi.class);

        AlgorithmDto payload = new AlgorithmDto()
            .name("My Algorithm")  // required
            .computationModel(AlgorithmDto.ComputationModelEnum.CLASSIC);  // required
        AlgorithmDto algorithm = algorithmApi.createAlgorithm(payload);

        algorithm = algorithmApi.getAlgorithm(algorithm.getId());

        //Uploads a sketch
        String description = "Sketch description";
        String baseUrl = "https://platform.planqk.de/qc-catalog";
        File file = new File("Absolute path to the file");
        SketchDto sketch = algorithmApi.uploadSketch(algorithm.getId(), description, baseUrl, file);

        sketch = algorithmApi.getSketch(algorithm.getId(), sketch.getId());

        //Updates sketch
        sketch.description("updated description");
        algorithmApi.updateSketch(algorithm.getId(), sketch.getId(), sketch);

        //Deletes sketch
        algorithmApi.deleteSketch(algorithm.getId(), sketch.getId());
    }
}
