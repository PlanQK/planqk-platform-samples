package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.TaxonomyElement;
import de.stoneone.planqk.api.model.UpdateAlgorithmRequest;
import java.util.ArrayList;
import java.util.List;

public class AlgorithmAddAndDeleteLearningMethodsSample {

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

        // Retrieve a list of available learning methods
        List<TaxonomyElement> learningMethods = algorithmApi.getLearningMethods();

        // Retrieve Supervised Learning from the list
        TaxonomyElement supervisedLearning = learningMethods.stream()
            .filter(taxonomyElement -> "Supervised Learning".equalsIgnoreCase(taxonomyElement.getLabel()))
            .findFirst()
            .orElseThrow();

        List<String> learningMethodUuids = new ArrayList<>();
        learningMethodUuids.add(supervisedLearning.getUuid());

        /*
         * Updates the algorithm and adds a learning method to it
         */

        // Create the update request payload
        UpdateAlgorithmRequest updateAlgorithmRequest = new UpdateAlgorithmRequest()
            .name(name)
            .computationModel(UpdateAlgorithmRequest.ComputationModelEnum.CLASSIC)
            .learningMethodUuids(learningMethodUuids);
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

        //Remove all assigned learning methods
        updateAlgorithmRequest.learningMethodUuids(new ArrayList<>());
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

    }
}
