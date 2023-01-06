package de.stoneone.planqk.samples;

import de.stoneone.planqk.api.CommunityAlgorithmsApi;
import de.stoneone.planqk.api.invoker.ApiClient;
import de.stoneone.planqk.api.model.AlgorithmDto;
import de.stoneone.planqk.api.model.TaxonomyElement;
import de.stoneone.planqk.api.model.UpdateAlgorithmRequest;
import java.util.ArrayList;
import java.util.List;

public class AlgorithmAddQuantumComputationModelSample {

    public static void main(String[] args) {
        String token = "Your personal access token";
        ApiClient apiClient = new ApiClient("apiKey", token);

        CommunityAlgorithmsApi algorithmApi = apiClient.buildClient(CommunityAlgorithmsApi.class);

        // Required attributes to create an algorithm
        String name = "My Algorithm";
        AlgorithmDto.ComputationModelEnum computationModel = AlgorithmDto.ComputationModelEnum.QUANTUM;

        AlgorithmDto payload = new AlgorithmDto()
            .name(name)
            .computationModel(computationModel);
        AlgorithmDto algorithm = algorithmApi.createAlgorithm(payload);

        algorithm = algorithmApi.getAlgorithm(algorithm.getId());

        // Retrieve a list of available quantum computation models
        List<TaxonomyElement> quantumComputationModels = algorithmApi.getQuantumComputationModels();

        // Retrieve Quantum Annealing from the list
        TaxonomyElement quantumAnnealing = quantumComputationModels.stream()
            .filter(taxonomyElement -> "Quantum Annealing".equalsIgnoreCase(taxonomyElement.getLabel()))
            .findFirst()
            .orElseThrow();

        List<String> quantumComputationModelsUuids = new ArrayList<>();
        quantumComputationModelsUuids.add(quantumAnnealing.getUuid());

        /*
         * Updates the algorithm and adds quantum computation models to it
         */

        // Create the update request payload
        UpdateAlgorithmRequest updateAlgorithmRequest = new UpdateAlgorithmRequest()
            .name(name)
            .computationModel(UpdateAlgorithmRequest.ComputationModelEnum.QUANTUM)
            .quantumComputationModelUuids(quantumComputationModelsUuids);
        algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);

        /*
        Remove all assigned quantum computation models
         updateAlgorithmRequest.quantumComputationModelUuids(new ArrayList<>());
         algorithm = algorithmApi.updateAlgorithm(algorithm.getId(), updateAlgorithmRequest);
        */

    }
}
