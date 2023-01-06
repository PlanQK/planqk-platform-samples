package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.TaxonomyElement;
import de.stoneone.planqk.api.model.UpdateAlgorithmRequest;
import java.util.ArrayList;
import java.util.List;

public class AlgorithmAddAndDeleteApplicationAreasSample {

    public static void main(String[] args) {
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

        // Retrieve a list of available application areas
        List<TaxonomyElement> applicationAreas = algorithmApi.getApplicationAreas();

        // Retrieve Engineering Science from the list
        TaxonomyElement engineeringScience = applicationAreas.stream()
            .filter(taxonomyElement -> "Engineering Science".equalsIgnoreCase(taxonomyElement.getLabel()))
            .findFirst()
            .orElseThrow();

        /*
         * Application areas have children or sub-categories e.g.
         * Civil Engineering is a child of Engineering Science.
         * Below we show how to Civil Engineering from the list
         */
        TaxonomyElement civilEngineering = applicationAreas.stream()
            .flatMap(taxonomyElement -> taxonomyElement.getChildren().stream())
            .filter(c -> "Civil Engineering".equalsIgnoreCase(c.getLabel()))
            .findFirst()
            .orElseThrow();

        List<String> applicationAreasUuids = new ArrayList<>();
        applicationAreasUuids.add(engineeringScience.getUuid());
        applicationAreasUuids.add(civilEngineering.getUuid());

        /*
         * Updates the algorithm and adds application areas to it
         */

        // Create the update request payload
        UpdateAlgorithmRequest updateAlgorithmRequest = new UpdateAlgorithmRequest()
            .name(name)
            .computationModel(UpdateAlgorithmRequest.ComputationModelEnum.CLASSIC)
            .applicationAreaUuids(applicationAreasUuids);
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

        //Remove all assigned application areas
        updateAlgorithmRequest.applicationAreaUuids(new ArrayList<>());
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

    }
}
