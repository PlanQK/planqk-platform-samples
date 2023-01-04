package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.SketchDto;
import java.io.File;
import java.io.IOException;

public class AlgorithmUploadAndDeleteSketchSample {

    public static void main(String[] args) throws IOException {
        String token = "Your personal access token";
        ApiClient apiClient = new ApiClient("apiKey", token);

        CommunityAlgorithmsApi algorithmApi = apiClient.buildClient(CommunityAlgorithmsApi.class);

        // Required attributes to create an algorithm
        String name = "My Algorithm";
        AlgorithmDto.ComputationModelEnum computationModel = AlgorithmDto.ComputationModelEnum.CLASSIC;

        AlgorithmDto payload = new AlgorithmDto()
            .name(name)
            .computationModel(computationModel);
        AlgorithmDto algorithm = algorithmApi.createAlgorithm(payload);

        algorithm = algorithmApi.getAlgorithm(algorithm.getId());

        //Uploads a sketch
        String description = "Sketch description";
        String baseUrl = "https://platform.planqk.de/qc-catalog";
        File file = new File("Absolute path to the file");
        SketchDto sketch = algorithmApi.uploadSketch(algorithm.getId(), description, baseUrl, file);

        sketch = algorithmApi.getSketch(algorithm.getId(), sketch.getId());

        byte[] sketchImage = algorithmApi.getSketchImage(algorithm.getId(), sketch.getId());

        //Deletes sketch
        algorithmApi.deleteSketch(algorithm.getId(), sketch.getId());
    }
}
