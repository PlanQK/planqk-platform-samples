package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.TaxonomyElement;
import de.stoneone.planqk.api.model.UpdateAlgorithmRequest;
import java.util.ArrayList;
import java.util.List;

public class AlgorithmAddAndDeleteProblemTypesSample {

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

        // Retrieve a list of available problem types
        List<TaxonomyElement> problemTypes = algorithmApi.getProblemTypes();

        // Retrieve Artificial Intelligence Problem from the list
        TaxonomyElement artificialIntelligenceProblem = problemTypes.stream()
            .filter(problemType -> "Artificial Intelligence Problem".equalsIgnoreCase(problemType.getLabel()))
            .findFirst()
            .orElseThrow();

        /*
         * Problem types have children or sub-categories e.g.
         * Natural language processing is a child of Artificial Intelligence Problem
         * Below we show how to retrieve Natural language processing from the list
         */
        TaxonomyElement naturalLanguageProcessing = problemTypes.stream()
            .flatMap(problemType -> problemType.getChildren().stream())
            .filter(c -> "Natural language processing".equalsIgnoreCase(c.getLabel()))
            .findFirst()
            .orElseThrow();

        List<String> problemTypeUuids = new ArrayList<>();
        problemTypeUuids.add(artificialIntelligenceProblem.getUuid());
        problemTypeUuids.add(naturalLanguageProcessing.getUuid());

        /*
         * Adds problem types to the algorithm
         */

        // Create the update request payload
        UpdateAlgorithmRequest updateAlgorithmRequest = new UpdateAlgorithmRequest()
            .name(name)
            .computationModel(UpdateAlgorithmRequest.ComputationModelEnum.CLASSIC)
            .problemTypeUuids(problemTypeUuids);
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

        //Remove all assigned problem types
        updateAlgorithmRequest.problemTypeUuids(new ArrayList<>());
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

    }
}
